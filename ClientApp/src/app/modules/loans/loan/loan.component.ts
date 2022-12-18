import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import * as moment from 'moment';
import { LoanModel } from 'src/app/models/loan-model';
import { ProfileDataService } from '../../profile/services/profile-data.service';
import { LoansService } from '../loans.service';

@Component({
  selector: 'app-loan',
  templateUrl: './loan.component.html',
  styleUrls: ['./loan.component.scss']
})
export class LoanComponent implements OnInit {

  loanId?: number;
  loan?: LoanModel;
  dateFormat: string = 'mm/dd/yyyy';

  constructor(private profileDataService: ProfileDataService, private loansService: LoansService, private route: ActivatedRoute) { }

  get getFormattedDate() {
    return moment(this.loan?.created_at).format(this.dateFormat); 
  }
  
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

    this.profileDataService.getUserSettings().subscribe(result => {
      if (result && result.length > 0) {
        const settings = result[0];
        this.dateFormat = settings.date_format;
      }
    })
  }
}
