package com.smartfinance.expensetracker.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class VaultSecretPrinter implements CommandLineRunner {

    @Value("${spring.datasource.url}")
    private String dbUrl;

    @Value("${spring.datasource.username}")
    private String dbUser;

    @Value("${spring.datasource.password}")
    private String dbPassword;

    @Override
    public void run(String... args) throws Exception {
        System.out.println("=== Vault Secrets Fetched ===");
        System.out.println("DB URL: " + dbUrl);
        System.out.println("DB User: " + dbUser);
        System.out.println("DB Password: " + dbPassword);
        System.out.println("=============================");
    }
}