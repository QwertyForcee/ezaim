import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApplicationCommonModule } from '../common/common.module';
import { RouterModule } from '@angular/router';
import { UserLoansComponent } from './user-loans/user-loans.component';



@NgModule({
  declarations: [
    UserLoansComponent
  ],
  imports: [
    CommonModule,
    ApplicationCommonModule,
    RouterModule,
  ]
})
export class LoansModule { }
