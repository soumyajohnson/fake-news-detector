package com.example.fakenews.dto;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ExplanationHighlight {
    private String span;
    private double score;
}
