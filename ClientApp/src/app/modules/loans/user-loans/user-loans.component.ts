import { Component, HostListener, Input, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import * as moment from 'moment';
import { LoanStatus } from 'src/app/enums/loan-status-enum';
import { Currency } from 'src/app/models/currency';
import { LoanModel } from 'src/app/models/loan-model';
import { UserSettings } from 'src/app/models/user-settings';
import { ProfileDataService } from '../../profile/services/profile-data.service';
import { LoansService } from '../loans.service';

@Component({
  selector: 'app-user-loans',
  templateUrl: './user-loans.component.html',
  styleUrls: ['./user-loans.component.scss']
})
export class UserLoansComponent implements OnInit, OnDestroy {

  loans?: LoanModel[];
  currencies?: Currency[];
  userSettings?: UserSettings;

  switchHeader: HTMLElement | null = null;
  greyMode = false;

  get activeLoans() {
    return this.loans?.filter(l => l.is_active) ?? [];
  }

  get notActiveLoans() {
    return this.loans?.filter(l => !l.is_active) ?? [];
  }

  get hasAnyLoan() {
    return this.loans && this.loans.length > 0;
  }

  getformattedDate(date: string) {
    return moment(date).format(this.userSettings?.date_format);
  }

  // getFormattedDate(loan) {
  //   return loan.created_at
  // }

  @Input() staticHeaders = false;
  constructor(private router: Router, private loansService: LoansService, private profileDataService: ProfileDataService) { }

  ngOnInit(): void {
    this.switchHeader = document.getElementById('complete-loans-separator');
    this.loansService.getUserLoans().subscribe(res => {
      this.loans = res;
    })

    this.profileDataService.getCurrencies().subscribe(res => {
      this.currencies = res;
    })

    this.profileDataService.getUserSettings().subscribe(res => {
      this.userSettings = res[0];
    })
  }

  onLoanClicked(id: number): void {
    this.router.navigate(['/loan'], { queryParams: { id } });
  }

  @HostListener('window:scroll', ['$event'])
  onPageScroll(event: any): void {
    const header = document.getElementById('complete-loans-separator')?.getBoundingClientRect();
    if (header && header.y < screen.height / 2) {
      this.greyMode = true;

      document.body.classList.add('body-grey');
      const completeHeader = document.body.getElementsByClassName('complete-loans-header')[0] as HTMLElement;
      if (completeHeader) {
        completeHeader?.classList.remove('complete-loans-header-hidden');
      }

      document.body.getElementsByClassName('profile-menu')[0]?.classList.add('centered');

    } else {
      this.greyMode = false;

      // document.body.getElementsByClassName('complete-loans-header')[0]?.classList.add('complete-loans-header-hidden');
      document.body.classList.remove('body-grey');
      document.body.getElementsByClassName('profile-menu')[0]?.classList.remove('centered');

      const completeHeader = document.body.getElementsByClassName('complete-loans-header')[0] as HTMLElement;
      if (completeHeader) {
        completeHeader?.classList.add('complete-loans-header-hidden');
      }
    }
  }

  ngOnDestroy(): void {
    document.body.classList.remove('body-grey');
  }
}
