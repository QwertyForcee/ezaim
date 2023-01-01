import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, MinValidator, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import * as moment from 'moment';
import { Currency } from 'src/app/models/currency';
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
  currencies?: Currency[];
  isPaymentFormOpened = false;

  paymentFormGroup: FormGroup = new FormGroup({
    'amount': new FormControl(0, [Validators.required, Validators.max(3_165_000)])
  });

  constructor(private profileDataService: ProfileDataService, private loansService: LoansService, private route: ActivatedRoute) { }

  get getFormattedDate() {
    return moment(this.loan?.created_at).format(this.dateFormat);
  }

  get isActiveLoan() {
    return this.loan?.is_active;
  }
  
  getCurrencyName(currencyId: number | string | undefined) {
    if (currencyId !== undefined){
      return this.currencies?.find(c => c.id.toString() == currencyId.toString())?.name;
    }
    else {
      return '';
    }
  }

  getPercentValue(percent?: number) {
    if (percent) {
      return (percent * 100).toLocaleString('en-EN')
    }
    else {
      return '';
    }
  }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.loanId = params['id'];
      if (this.loanId) {
        this.loansService.getUserLoanById(this.loanId).subscribe({
          next: (loans) => {
            this.loan = loans.find(loan => loan.id.toString() === this.loanId?.toString());

            this.paymentFormGroup.get('amount')?.setValidators([Validators.min(1), Validators.max(this.loan?.remaining_amount ?? 3_165_000)])
          }
        })
      }

      this.profileDataService.getCurrencies().subscribe(res => {
        this.currencies = res;
      })
    })

    this.profileDataService.getUserSettings().subscribe(result => {
      if (result && result.length > 0) {
        const settings = result[0];
        this.dateFormat = settings.date_format;
      }
    })
  }

  onStartMakingPayment() {
    this.isPaymentFormOpened = true;
  }

  closePaymentForm() {
    this.isPaymentFormOpened = false;
  }

  confirmPayment() {
    if (this.paymentFormGroup.valid && this.loanId) {
      const payment = {
        'loan': this.loanId,
        'amount': this.paymentFormGroup.get('amount')?.value?.toString(),
        'return_url': window.location.href
      };
      this.loansService.createNewPayment(payment).subscribe(result => {
        if (result) {
          window.open(result, "_self");
        }
      });
    }
  }
}
