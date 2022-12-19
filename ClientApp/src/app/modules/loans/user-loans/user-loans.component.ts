import { Component, HostListener, Input, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { LoanModel } from 'src/app/models/loan-model';
import { LoansService } from '../loans.service';

@Component({
  selector: 'app-user-loans',
  templateUrl: './user-loans.component.html',
  styleUrls: ['./user-loans.component.scss']
})
export class UserLoansComponent implements OnInit, OnDestroy {

  loans?: LoanModel[];

  switchHeader: HTMLElement | null = null;
  greyMode = false;  

  @Input() staticHeaders = false;
  constructor(private router: Router, private loansService: LoansService) { }

  ngOnInit(): void {
    this.switchHeader = document.getElementById('complete-loans-separator');
    this.loansService.getUserLoans().subscribe(res => {
      this.loans = res;
    })

  }

  onLoanClicked(): void {
    this.router.navigate(['/loan'], { queryParams: { id: 1 } });
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
