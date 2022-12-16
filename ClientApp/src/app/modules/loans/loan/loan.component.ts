import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { LoanModel } from 'src/app/models/loan-model';
import { LoansService } from '../loans.service';

@Component({
  selector: 'app-loan',
  templateUrl: './loan.component.html',
  styleUrls: ['./loan.component.scss']
})
export class LoanComponent implements OnInit {

  loanId?: number;
  loan?: LoanModel;
  constructor(private loansService: LoansService, private route: ActivatedRoute) { }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.loanId = params['id'];
      if (this.loanId) {
        this.loansService.getUserLoanById(this.loanId).subscribe({
          next: (loan) => {
            this.loan = loan;
            console.log(loan);
          }
        })
      }
    })
  }

}
