package com.example.fakenews.controller;

import com.example.fakenews.model.Prediction;
import com.example.fakenews.service.HistoryService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/history")
@RequiredArgsConstructor
public class HistoryController {

    private final HistoryService historyService;

    @GetMapping
    public List<Prediction> getHistory() {
        return historyService.getUserHistory();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Prediction> getPrediction(@PathVariable String id) {
        return ResponseEntity.ok(historyService.getPredictionById(id));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deletePrediction(@PathVariable String id) {
        historyService.deletePrediction(id);
        return ResponseEntity.noContent().build();
    }
}
