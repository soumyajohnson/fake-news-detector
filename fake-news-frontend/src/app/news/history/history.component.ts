import { Component, OnInit, ViewChild, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatPaginatorModule, MatPaginator } from '@angular/material/paginator';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatChipsModule } from '@angular/material/chips';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatMenuModule } from '@angular/material/menu';
import { ReactiveFormsModule, FormControl } from '@angular/forms';
import { NewsService } from '../../core/services/news.service';
import { Prediction } from '../../shared/models/prediction.model';
import { NavbarComponent } from '../../shared/components/navbar/navbar.component';
import { Observable, BehaviorSubject, combineLatest, map, switchMap, startWith, tap } from 'rxjs';
import { N } from '@angular/cdk/keycodes';

@Component({
  selector: 'app-history',
  standalone: true,
  imports: [
    CommonModule, 
    RouterModule, 
    MatTableModule, 
    MatPaginatorModule,
    MatButtonModule, 
    MatIconModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatChipsModule,
    MatProgressBarModule,
    MatMenuModule,
    ReactiveFormsModule,
    NavbarComponent
  ],
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.scss']
})
export class HistoryComponent implements OnInit, AfterViewInit {
  @ViewChild(MatPaginator) paginator!: MatPaginator;

  refresh$ = new BehaviorSubject<void>(undefined);
  
  // Filter Controls
  searchControl = new FormControl('');
  statusFilterControl = new FormControl('All');
  sortControl = new FormControl('newest');

  // DataSource for Table
  dataSource = new MatTableDataSource<Prediction>([]);

  // We keep the observable for the async pipe in template for mobile view/loading state
  history$: Observable<Prediction[]> = combineLatest([
    this.refresh$.pipe(switchMap(() => this.newsService.getHistory())),
    this.searchControl.valueChanges.pipe(startWith('')),
    this.statusFilterControl.valueChanges.pipe(startWith('All')),
    this.sortControl.valueChanges.pipe(startWith('newest'))
  ]).pipe(
    map(([data, search, status, sort]) => {
      console.log('History data received:', data);
      let filtered = data || [];
      
      // 1. Search Filter
      if (search) {
        const query = search.toLowerCase();
        filtered = filtered.filter(p => 
          p.request.inputText.toLowerCase().includes(query) ||
          (p.request.url && p.request.url.toLowerCase().includes(query))
        );
      }

      // 2. Status Filter
      if (status && status !== 'All') {
        filtered = filtered.filter(p => 
          p.output?.label?.toUpperCase() === status.toUpperCase()
        );
      }

      // 3. Sorting
      filtered.sort((a, b) => {
        const dateA = new Date(a.createdAt || 0).getTime();
        const dateB = new Date(b.createdAt || 0).getTime();
        return sort === 'newest' ? dateB - dateA : dateA - dateB;
      });

      return filtered;
    }),
    tap(filteredData => {
      // Update MatTableDataSource for pagination
      this.dataSource.data = filteredData;
      if (this.paginator) {
        this.dataSource.paginator = this.paginator;
      }
    })
  );

  displayedColumns: string[] = ['date', 'text', 'label', 'confidence', 'actions'];

  constructor(private newsService: NewsService) {
    this.searchControl.setValue('');
    this.statusFilterControl.setValue('All');
    this.sortControl.setValue('newest');
  }

  ngOnInit(): void {}

  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator;
  }

  delete(id: string | undefined, event: Event) {
    event.stopPropagation();
    if (!id) return;
    
    if (confirm('Are you sure you want to delete this record?')) {
      this.newsService.deleteHistory(id).subscribe(() => {
        this.refresh$.next();
      });
    }
  }

  getConfidenceColor(label: string | undefined): string {
    return label?.toLowerCase() === 'fake' ? 'warn' : 'primary';
  }
}
