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
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class ExpenseService {

    private static final Logger log = LoggerFactory.getLogger(ExpenseService.class);

    @Autowired
    private ExpenseRepository expenseRepository;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private RestTemplate restTemplate;


    public Expense addExpense(Expense expense, String userEmail) {
        User user = userRepository.findByEmail(userEmail)
                .orElseThrow(() -> {
                    log.error("User not found with email {}", userEmail);
                    return new RuntimeException("User not found");
                });

        expense.setUser(user);
        expense.setTimestamp(LocalDateTime.now());

        log.info("Creating new expense: amount={}, category={}, user={}",
                expense.getAmount(), expense.getCategory(), userEmail);

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
                boolean isFraud = response.getBody().isFraud();
                expense.setFraud(isFraud);

                if (isFraud) {
                    log.warn("Fraudulent expense detected: user={}, amount={}, category={}",
                            userEmail, expense.getAmount(), expense.getCategory());
                } else {
                    log.info("Expense passed fraud check: user={}, amount={}, category={}",
                            userEmail, expense.getAmount(), expense.getCategory());
                }
            } else {
                log.error("Fraud service failed for user {}. Response: {}", userEmail, response.getStatusCode());
                expense.setFraud(false); // fallback
            }
        } catch (Exception e) {
            log.error("Error calling fraud detection service for user {}: {}", userEmail, e.getMessage(), e);
            expense.setFraud(false); // fallback in case of error
        }

        Expense savedExpense = expenseRepository.save(expense);
        log.info("Expense saved successfully: id={}, user={}", savedExpense.getId(), userEmail);
        return expenseRepository.save(expense);
    }

    public List<Expense> getUserExpenses(String userEmail) {
        User user = userRepository.findByEmail(userEmail)
                .orElseThrow(() -> {
                    log.error("User not found with email {}", userEmail);
                    return new RuntimeException("User not found");
                });

        log.info("Fetching expenses for user {}", userEmail);
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
                log.warn("Invalid range provided: {}", range);
                throw new IllegalArgumentException("Invalid range: " + range);
        }

        log.info("Generating summary for user {} with range {}", email, range);

        List<Expense> expenses = expenseRepository.findByUserEmailAndDateAfter(email, startDate);

        Map<String, Double> summary = new HashMap<>();
        for (Expense e : expenses) {
            String category = e.getCategory();
            double amount = e.getAmount().doubleValue(); // Convert BigDecimal to double
            summary.put(category,
                    summary.getOrDefault(category, 0.0) + amount);
        }

        log.info("Expense summary generated for user {}: {}", email, summary);
        return summary;
    }

}