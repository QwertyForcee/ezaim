import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './modules/auth/guards/auth.guard';
import { LoginComponent } from './modules/auth/login/login.component';
import { LoanComponent } from './modules/loans/loan/loan.component';
import { LoansPageComponent } from './modules/loans/loans-page/loans-page.component';
import { NewLoanFormComponent } from './modules/loans/new-loan-form/new-loan-form.component';
import { UserLoansComponent } from './modules/loans/user-loans/user-loans.component';
import { PaymentsHistoryComponent } from './modules/profile/payments-history/payments-history.component';
import { ProfileDataComponent } from './modules/profile/profile-data/profile-data.component';
import { ProfileComponent } from './modules/profile/profile/profile.component';
import { TelegramAccountsComponent } from './modules/profile/telegram-accounts/telegram-accounts.component';
import { UserSettingsComponent } from './modules/profile/user-settings/user-settings.component';
import { HomeComponent } from './shared/home/home.component';


const profile_routes: Routes = [
  { path: '', component: ProfileDataComponent, canActivate: [AuthGuard] },
  { path: 'loans', component: UserLoansComponent, canActivate: [AuthGuard] },
  { path: 'tg-accounts', component: TelegramAccountsComponent, canActivate: [AuthGuard] },
  { path: 'settings', component: UserSettingsComponent, canActivate: [AuthGuard] },
  { path: 'history', component: PaymentsHistoryComponent, canActivate: [AuthGuard] },
];

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'auth', component: LoginComponent },
  { path: 'profile', component: ProfileComponent, children: profile_routes, canActivate: [AuthGuard] },
  { path: 'loan', component: LoanComponent, canActivate: [AuthGuard] },
  { path: 'loans', component: LoansPageComponent, canActivate: [AuthGuard] },
  { path: 'new-loan', component: NewLoanFormComponent, canActivate: [AuthGuard] },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
