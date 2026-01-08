package com.example.fakenews.dto;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class SocialPost {
    private String text;
    private String url;
    private String source;
    private String published;
}
