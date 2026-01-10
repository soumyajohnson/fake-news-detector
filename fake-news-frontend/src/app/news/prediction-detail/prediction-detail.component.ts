import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { NewsService } from '../../core/services/news.service';
import { Prediction } from '../../shared/models/prediction.model';
import { NavbarComponent } from '../../shared/components/navbar/navbar.component';


@Component({
  selector: 'app-prediction-detail',
  standalone: true,
  imports: [
    CommonModule, 
    RouterModule, 
    MatCardModule, 
    MatChipsModule, 
    MatButtonModule, 
    MatIconModule,
    MatProgressBarModule,
    NavbarComponent
  ],
  templateUrl: './prediction-detail.component.html',
  styleUrls: ['./prediction-detail.component.scss']
})
export class PredictionDetailComponent implements OnInit {
  prediction: Prediction | null = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private newsService: NewsService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.newsService.getPrediction(id).subscribe({
        next: (res) => {
          this.prediction = res;
          this.cdr.detectChanges();
        },
        error: (err) => {
          console.error(err);
          this.cdr.detectChanges();
        }
      });
    }
  }

  delete() {
    if (this.prediction && this.prediction.id && confirm('Are you sure you want to delete this record? This action cannot be undone.')) {
      this.newsService.deleteHistory(this.prediction.id).subscribe(() => {
        this.router.navigate(['/history']);
      });
    }
  }

  get isFake(): boolean {
    return this.prediction?.output?.label?.toLowerCase() === 'fake';
  }

  get confidencePercentage(): number {
    return (this.prediction?.output?.confidence || 0) * 100;
  }
}
