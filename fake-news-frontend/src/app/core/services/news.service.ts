import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Prediction } from '../../shared/models/prediction.model';

@Injectable({
  providedIn: 'root'
})
export class NewsService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  checkNews(text: string, sourcePlatform?: string, url?: string): Observable<Prediction> {
    const payload = { text, sourcePlatform, url };
    return this.http.post<Prediction>(`${this.apiUrl}/check`, payload);
  }

  getHistory(): Observable<Prediction[]> {
    return this.http.get<Prediction[]>(`${this.apiUrl}/history`);
  }

  getPrediction(id: string): Observable<Prediction> {
    return this.http.get<Prediction>(`${this.apiUrl}/history/${id}`);
  }

  deleteHistory(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/history/${id}`);
  }
}
