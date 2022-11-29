import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './modules/auth/login/login.component';
import { UserLoansComponent } from './modules/loans/user-loans/user-loans.component';
import { ProfileDataComponent } from './modules/profile/profile-data/profile-data.component';
import { ProfileComponent } from './modules/profile/profile/profile.component';
import { HomeComponent } from './shared/home/home.component';


const profile_routes: Routes = [
  { path: '', component: ProfileDataComponent },
  { path: 'loans', component: UserLoansComponent }
];

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'auth', component: LoginComponent },
  { path: 'profile', component: ProfileComponent, children: profile_routes }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
