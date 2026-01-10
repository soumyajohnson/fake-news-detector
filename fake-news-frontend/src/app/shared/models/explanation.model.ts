export interface ExplanationHighlight {
  span: string;
  score: number;
}

export interface Explanation {
  summary: string;
  method: string;
  highlights: ExplanationHighlight[];
}