package com.smartfinance.expensetracker.dto;


import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class FraudRequest {
    private double amount;
    private String category;


    @JsonProperty("hour_of_day")
    private int hourOfDay;

    @JsonProperty("day_of_week")
    private int dayOfWeek;
}
