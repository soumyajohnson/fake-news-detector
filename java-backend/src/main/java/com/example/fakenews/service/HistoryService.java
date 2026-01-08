package com.example.fakenews.service;

import com.example.fakenews.exception.ResourceNotFoundException;
import com.example.fakenews.model.Prediction;
import com.example.fakenews.repository.PredictionRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class HistoryService {

    private final PredictionRepository predictionRepository;

    private String getCurrentUserId() {
        return SecurityContextHolder.getContext().getAuthentication().getName();
    }

    public List<Prediction> getUserHistory() {
        return predictionRepository.findTop20ByUserIdOrderByCreatedAtDesc(getCurrentUserId());
    }

    public Prediction getPredictionById(String id) {
        return predictionRepository.findByIdAndUserId(id, getCurrentUserId())
                .orElseThrow(() -> new ResourceNotFoundException("Prediction not found with id: " + id));
    }

    public void deletePrediction(String id) {
        long deletedCount = predictionRepository.deleteByIdAndUserId(id, getCurrentUserId());
        if (deletedCount == 0) {
            throw new ResourceNotFoundException("Prediction not found with id: " + id);
        }
    }
}
