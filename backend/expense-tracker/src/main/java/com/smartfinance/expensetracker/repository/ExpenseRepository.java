package com.smartfinance.expensetracker.repository;

import com.smartfinance.expensetracker.model.Expense;
import com.smartfinance.expensetracker.model.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface ExpenseRepository extends JpaRepository<Expense, Long> {
    List<Expense> findByUser(User user);
}
