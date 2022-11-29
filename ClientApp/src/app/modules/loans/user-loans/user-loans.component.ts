import { Component, HostListener, OnDestroy, OnInit } from '@angular/core';

@Component({
  selector: 'app-user-loans',
  templateUrl: './user-loans.component.html',
  styleUrls: ['./user-loans.component.scss']
})
export class UserLoansComponent implements OnInit, OnDestroy {

  switchHeader: HTMLElement | null = null;
  greyMode = false;
  constructor() { }

  ngOnInit(): void {
    this.switchHeader = document.getElementById('complete-loans-separator');
    const header = this.switchHeader?.getBoundingClientRect();
    if (header) {
      //console.log(header.top, header.right, header.bottom, header.left);
    }

  }

  onLoanClicked(): void {

  }

  @HostListener('window:scroll', ['$event'])
  onPageScroll(event: any): void {
    const header = document.getElementById('complete-loans-separator')?.getBoundingClientRect();
    if (header && header.y < screen.height / 2) {
      this.greyMode = true;

      document.body.classList.add('body-grey');
      const completeHeader = document.body.getElementsByClassName('complete-loans-header')[0] as HTMLElement;
      if (completeHeader){
        completeHeader?.classList.remove('complete-loans-header-hidden');
      }

      document.body.getElementsByClassName('profile-menu')[0]?.classList.add('centered');

    } else {
      this.greyMode = false;

      // document.body.getElementsByClassName('complete-loans-header')[0]?.classList.add('complete-loans-header-hidden');
      document.body.classList.remove('body-grey');
      document.body.getElementsByClassName('profile-menu')[0]?.classList.remove('centered');
      
      const completeHeader = document.body.getElementsByClassName('complete-loans-header')[0] as HTMLElement;
      if (completeHeader){
        completeHeader?.classList.add('complete-loans-header-hidden');
      }
    }
  }

  ngOnDestroy(): void {
    document.body.classList.remove('body-grey');
  }
}
