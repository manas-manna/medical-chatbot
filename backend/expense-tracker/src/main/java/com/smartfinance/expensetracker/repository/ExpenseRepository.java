package com.smartfinance.expensetracker.repository;

import com.smartfinance.expensetracker.model.Expense;
import com.smartfinance.expensetracker.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDateTime;
import java.util.List;

public interface ExpenseRepository extends JpaRepository<Expense, Long> {
    List<Expense> findByUser(User user);

    @Query("SELECT e FROM Expense e WHERE e.user.email = :email AND e.timestamp  >= :startDate")
    List<Expense> findByUserEmailAndDateAfter(@Param("email") String email, @Param("startDate") LocalDateTime startDate);

}
