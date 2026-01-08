package com.example.fakenews.model;

import com.example.fakenews.dto.Explanation;
import com.example.fakenews.dto.SocialPost;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.Instant;
import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Document(collection = "predictions")
public class Prediction {

    @Id
    private String id;

    private String userId;

    @Builder.Default
    private Instant createdAt = Instant.now();

    private PredictionRequest request;

    @Builder.Default
    private PredictionModel model = new PredictionModel("distilbert-fakenews", "v1");

    private PredictionOutput output;

    private Explanation explanation;

    private List<SocialPost> socialContext;

    // --- Nested Inner Classes ---

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class PredictionRequest {
        private String inputText;
        private String url;
        private String sourcePlatform;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class PredictionModel {
        private String name;
        private String version;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class PredictionOutput {
        private String label;
        private double confidence;
        private List<Double> probs;
    }
}
