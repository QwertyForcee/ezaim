import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApplicationCommonModule } from '../common/common.module';
import { RouterModule } from '@angular/router';
import { UserLoansComponent } from './user-loans/user-loans.component';
import { LoanComponent } from './loan/loan.component';
import { ReactiveFormsModule } from '@angular/forms';
import { LoanCalendarComponent } from './loan-calendar/loan-calendar.component';



@NgModule({
  declarations: [
    UserLoansComponent,
    LoanComponent,
    LoanCalendarComponent
  ],
  imports: [
    ApplicationCommonModule,
    CommonModule,
    RouterModule,
    ReactiveFormsModule
  ]
})
export class LoansModule { }
