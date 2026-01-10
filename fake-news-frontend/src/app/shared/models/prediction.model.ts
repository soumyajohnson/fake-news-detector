import { Explanation } from './explanation.model';
import { SocialPost } from './social-post.model';

export interface Prediction {
  id?: string;
  createdAt?: string;
  request: {
    inputText: string;
    url?: string;
    sourcePlatform?: string;
  };
  output: {
    label: string;
    confidence: number;
  };
  explanation: Explanation;
  socialContext: SocialPost[];
}
