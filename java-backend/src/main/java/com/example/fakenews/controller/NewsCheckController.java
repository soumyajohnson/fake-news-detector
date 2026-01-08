package com.example.fakenews.controller;

import com.example.fakenews.dto.NewsCheckRequest;
import com.example.fakenews.model.Prediction;
import com.example.fakenews.service.MlClientService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
public class NewsCheckController {

    private final MlClientService mlClientService;

    @Autowired
    public NewsCheckController(MlClientService mlClientService) {
        this.mlClientService = mlClientService;
    }

    @PostMapping("/api/check")
    public Prediction checkNews(@Valid @RequestBody NewsCheckRequest request) {
        return mlClientService.checkAndSave(request);
    }

    @GetMapping("/health")
    public String health() {
        return "OK";
    }
}
