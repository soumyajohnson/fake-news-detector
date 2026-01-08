package com.example.fakenews.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class NewsCheckRequest {
    @NotBlank(message = "Text cannot be blank")
    private String text;
    
    private String url;
    private String sourcePlatform;
}
