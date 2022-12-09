import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApplicationCommonModule } from '../common/common.module';
import { RouterModule } from '@angular/router';
import { UserLoansComponent } from './user-loans/user-loans.component';
import { LoanComponent } from './loan/loan.component';
import { ReactiveFormsModule } from '@angular/forms';
import { LoanCalendarComponent } from './loan-calendar/loan-calendar.component';
import { LoansPageComponent } from './loans-page/loans-page.component';
import { MatTooltipModule } from '@angular/material/tooltip';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';



@NgModule({
  declarations: [
    UserLoansComponent,
    LoanComponent,
    LoanCalendarComponent,
    LoansPageComponent
  ],
  imports: [
    ApplicationCommonModule,
    CommonModule,
    RouterModule,
    ReactiveFormsModule,
    MatTooltipModule,
    BrowserAnimationsModule
  ]
})
export class LoansModule { }
