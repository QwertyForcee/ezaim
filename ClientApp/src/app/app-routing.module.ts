import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './modules/auth/login/login.component';
import { LoanComponent } from './modules/loans/loan/loan.component';
import { LoansPageComponent } from './modules/loans/loans-page/loans-page.component';
import { NewLoanFormComponent } from './modules/loans/new-loan-form/new-loan-form.component';
import { UserLoansComponent } from './modules/loans/user-loans/user-loans.component';
import { ProfileDataComponent } from './modules/profile/profile-data/profile-data.component';
import { ProfileComponent } from './modules/profile/profile/profile.component';
import { TelegramAccountsComponent } from './modules/profile/telegram-accounts/telegram-accounts.component';
import { HomeComponent } from './shared/home/home.component';


const profile_routes: Routes = [
  { path: '', component: ProfileDataComponent },
  { path: 'loans', component: UserLoansComponent },
  { path: 'tg-accounts', component: TelegramAccountsComponent },
];

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'auth', component: LoginComponent },
  { path: 'profile', component: ProfileComponent, children: profile_routes },
  { path: 'loan', component: LoanComponent },
  { path: 'loans', component: LoansPageComponent },
  { path: 'new-loan', component: NewLoanFormComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
