package com.smartfinance.expensetracker.service;

import com.smartfinance.expensetracker.dto.FraudRequest;
import com.smartfinance.expensetracker.dto.FraudResponse;
import com.smartfinance.expensetracker.model.Expense;
import com.smartfinance.expensetracker.model.User;
import com.smartfinance.expensetracker.repository.ExpenseRepository;
import com.smartfinance.expensetracker.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class ExpenseService {

    @Autowired
    private ExpenseRepository expenseRepository;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private RestTemplate restTemplate;

    public Expense addExpense(Expense expense, String userEmail) {
        User user = userRepository.findByEmail(userEmail)
                .orElseThrow(() -> new RuntimeException("User not found"));

        expense.setUser(user);
        expense.setTimestamp(LocalDateTime.now());

        //  Prepare data for fraud detection
        FraudRequest request = new FraudRequest();
        request.setAmount(expense.getAmount());
        request.setCategory(expense.getCategory());

        LocalDateTime now = expense.getTimestamp();
        request.setHourOfDay(now.getHour());
        request.setDayOfWeek(now.getDayOfWeek().getValue()); // 1 = Monday

        //  Call FastAPI microservice
        try {
            String url = "http://localhost:8000/predict-fraud";
            ResponseEntity<FraudResponse> response = restTemplate.postForEntity(url, request, FraudResponse.class);

            if (response.getStatusCode().is2xxSuccessful()) {
                expense.setFraud(response.getBody().isFraud());
            } else {
                expense.setFraud(false); // Fallback
            }
        } catch (Exception e) {
            System.out.println("Error calling fraud detection service: " + e.getMessage());
            expense.setFraud(false); // Fallback in case of error
        }


        return expenseRepository.save(expense);
    }

    public List<Expense> getUserExpenses(String userEmail) {
        User user = userRepository.findByEmail(userEmail)
                .orElseThrow(() -> new RuntimeException("User not found"));
        return expenseRepository.findByUser(user);
    }



    public Map<String, Double> getExpenseSummary(String email, String range) {
        LocalDateTime now = LocalDateTime.now();
        LocalDateTime startDate;

        switch (range) {
            case "7d":
                startDate = now.minusDays(7);
                break;
            case "30d":
                startDate = now.minusDays(30);
                break;
            default:
                throw new IllegalArgumentException("Invalid range: " + range);
        }

        List<Expense> expenses = expenseRepository.findByUserEmailAndDateAfter(email, startDate);

        Map<String, Double> summary = new HashMap<>();
        for (Expense e : expenses) {
            String category = e.getCategory();
            double amount = e.getAmount().doubleValue(); // Convert BigDecimal to double
            summary.put(category,
                    summary.getOrDefault(category, 0.0) + amount);
        }

        return summary;
    }

}