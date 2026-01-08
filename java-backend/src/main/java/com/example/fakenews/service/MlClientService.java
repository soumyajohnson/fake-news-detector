package com.example.fakenews.service;

import com.example.fakenews.dto.NewsCheckRequest;
import com.example.fakenews.dto.NewsCheckResponse;
import com.example.fakenews.model.Prediction;
import com.example.fakenews.repository.PredictionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

import java.time.Instant;

@Service
public class MlClientService {

    private final RestTemplate restTemplate;
    private final PredictionRepository predictionRepository;
    
    @Value("${ml.service.url:http://localhost:8000/predict_explain}")
    private String mlServiceUrl;

    @Autowired
    public MlClientService(RestTemplate restTemplate, PredictionRepository predictionRepository) {
        this.restTemplate = restTemplate;
        this.predictionRepository = predictionRepository;
    }

    public Prediction checkAndSave(NewsCheckRequest request) {
        // 1. Call ML Service
        NewsCheckResponse mlResponse;
        try {
            // We only send 'text' to ML service as per its contract
            NewsCheckRequest mlRequest = new NewsCheckRequest(request.getText(), null, null);
            mlResponse = restTemplate.postForObject(mlServiceUrl, mlRequest, NewsCheckResponse.class);
        } catch (RestClientException e) {
            throw new RuntimeException("ML service not reachable", e);
        }

        if (mlResponse == null) {
            throw new RuntimeException("ML service returned null response");
        }

        // 2. Extract User ID
        String userId = SecurityContextHolder.getContext().getAuthentication().getName();

        // 3. Build Prediction Entity
        Prediction prediction = Prediction.builder()
                .userId(userId)
                .createdAt(Instant.now())
                .request(Prediction.PredictionRequest.builder()
                        .inputText(request.getText())
                        .url(request.getUrl())
                        .sourcePlatform(request.getSourcePlatform())
                        .build())
                .model(Prediction.PredictionModel.builder()
                        .name("distilbert-fakenews") // Could also come from ML response if supported
                        .version("v1")
                        .build())
                .output(Prediction.PredictionOutput.builder()
                        .label(mlResponse.getLabel())
                        .confidence(mlResponse.getConfidence())
                        .probs(mlResponse.getProbs())
                        .build())
                .explanation(mlResponse.getExplanation())
                .socialContext(mlResponse.getSocialContext())
                .build();

        // 4. Save and Return
        return predictionRepository.save(prediction);
    }
}
