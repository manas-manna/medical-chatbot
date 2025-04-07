package com.smartfinance.expensetracker.service;

import com.smartfinance.expensetracker.model.Expense;
import com.smartfinance.expensetracker.model.User;
import com.smartfinance.expensetracker.repository.ExpenseRepository;
import com.smartfinance.expensetracker.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class ExpenseService {

    @Autowired
    private ExpenseRepository expenseRepository;

    @Autowired
    private UserRepository userRepository;

    public Expense addExpense(Expense expense, String userEmail) {
        User user = userRepository.findByEmail(userEmail)
                .orElseThrow(() -> new RuntimeException("User not found"));

        expense.setUser(user);
        expense.setTimestamp(LocalDateTime.now());

        return expenseRepository.save(expense);
    }

    public List<Expense> getUserExpenses(String userEmail) {
        User user = userRepository.findByEmail(userEmail)
                .orElseThrow(() -> new RuntimeException("User not found"));
        return expenseRepository.findByUser(user);
    }
}