import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';
import { LoginComponent } from './auth/login/login.component';
import { RegisterComponent } from './auth/register/register.component';
import { CheckNewsComponent } from './news/check-news/check-news.component';
import { HistoryComponent } from './news/history/history.component';
import { PredictionDetailComponent } from './news/prediction-detail/prediction-detail.component';

export const routes: Routes = [
  { path: 'auth/login', component: LoginComponent },
  { path: 'auth/register', component: RegisterComponent },
  { path: 'check', component: CheckNewsComponent, canActivate: [authGuard] },
  { path: 'history', component: HistoryComponent, canActivate: [authGuard] },
  { path: 'history/:id', component: PredictionDetailComponent, canActivate: [authGuard] },
  { path: '', redirectTo: '/auth/login', pathMatch: 'full' }
];