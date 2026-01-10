import { Component, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatChipsModule } from '@angular/material/chips';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatTabsModule } from '@angular/material/tabs';
import { MatIconModule } from '@angular/material/icon';
import { NewsService } from '../../core/services/news.service';
import { Prediction } from '../../shared/models/prediction.model';

import { NavbarComponent } from '../../shared/components/navbar/navbar.component';

@Component({
  selector: 'app-check-news',
  standalone: true,
  imports: [
    CommonModule, 
    ReactiveFormsModule, 
    MatCardModule, 
    MatFormFieldModule, 
    MatInputModule, 
    MatButtonModule, 
    MatChipsModule, 
    MatProgressSpinnerModule,
    MatProgressBarModule,
    MatTabsModule,
    MatIconModule,
    NavbarComponent
  ],
  templateUrl: './check-news.component.html',
  styleUrls: ['./check-news.component.scss']
})
export class CheckNewsComponent {
  checkForm: FormGroup;
  prediction: Prediction | null = null;
  loading: boolean = false;
  error: string = '';

  constructor(
    private fb: FormBuilder, 
    private newsService: NewsService,
    private cdr: ChangeDetectorRef
  ) {
    this.checkForm = this.fb.group({
      text: ['', Validators.required],
      sourcePlatform: [''],
      url: ['']
    });
  }

  onSubmit() {
    if (this.checkForm.valid) {
      this.loading = true;
      this.prediction = null;
      this.error = '';
      const { text, sourcePlatform, url } = this.checkForm.value;
      
      this.newsService.checkNews(text, sourcePlatform, url).subscribe({
        next: (res) => {
          console.log('Check response:', res);
          // console.log('prediction:', this.prediction);
          // console.log('loading:', this.loading);
          this.prediction = res;
          this.loading = false;
          this.cdr.detectChanges();
        },
        error: (err) => {
          console.error('Check error:', err);
          this.error = 'Failed to check news. Please try again.';
          this.loading = false;
          this.cdr.detectChanges();
        }
      });
    }
  }

  clearForm() {
    this.checkForm.reset();
    this.prediction = null;
    this.error = '';
  }

  get isFake(): boolean {
    return this.prediction?.output?.label?.toLowerCase() === 'fake';
  }

  get confidencePercentage(): number {
    return (this.prediction?.output?.confidence || 0) * 100;
  }
}
