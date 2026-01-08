package com.example.fakenews.dto;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Explanation {
    private String summary;
    private String method;
    private List<ExplanationHighlight> highlights;
}
