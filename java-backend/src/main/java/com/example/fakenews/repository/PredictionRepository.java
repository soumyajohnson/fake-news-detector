package com.example.fakenews.repository;

import com.example.fakenews.model.Prediction;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface PredictionRepository extends MongoRepository<Prediction, String> {
    
    List<Prediction> findTop20ByUserIdOrderByCreatedAtDesc(String userId);

    Optional<Prediction> findByIdAndUserId(String id, String userId);

    long deleteByIdAndUserId(String id, String userId);
}
