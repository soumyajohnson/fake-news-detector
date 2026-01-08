package com.example.fakenews.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class NewsCheckResponse {
    private String label;
    private double confidence;
    private List<Double> probs;
    private Explanation explanation;

    @JsonProperty("social_context")
    private List<SocialPost> socialContext;
}
