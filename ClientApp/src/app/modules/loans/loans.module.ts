import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApplicationCommonModule } from '../common/common.module';
import { RouterModule } from '@angular/router';
import { UserLoansComponent } from './user-loans/user-loans.component';
import { LoanComponent } from './loan/loan.component';
import { ReactiveFormsModule } from '@angular/forms';



@NgModule({
  declarations: [
    UserLoansComponent,
    LoanComponent
  ],
  imports: [
    ApplicationCommonModule,
    CommonModule,
    RouterModule,
    ReactiveFormsModule
  ]
})
export class LoansModule { }
