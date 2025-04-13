package com.smartfinance.expensetracker.seeder;

import com.smartfinance.expensetracker.model.User;
import com.smartfinance.expensetracker.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class DataSeeder implements CommandLineRunner {

    @Autowired
    private UserRepository userRepository;

    @Override
    public void run(String... args) {
        String email = "manas@gmail.com";
        if (!userRepository.existsByEmail(email)) {
            User user = new User();
            user.setEmail(email);
            user.setName("Manas");
            user.setPassword("0000"); // Or hash if needed
            user.setRole("USER");
            user.setActive(true);

            userRepository.save(user);
        }
    }
}