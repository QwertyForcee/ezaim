import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Currency } from 'src/app/models/currency';
import { UserSettings } from 'src/app/models/user-settings';
import { ProfileDataService } from '../../profile/services/profile-data.service';
import { LoansService } from '../loans.service';

@Component({
  selector: 'app-new-loan-form',
  templateUrl: './new-loan-form.component.html',
  styleUrls: ['./new-loan-form.component.scss']
})
export class NewLoanFormComponent implements OnInit {

  constructor(private loansService: LoansService, private profileDataService: ProfileDataService) { }

  calculatedPercent = 0;
  currencies?: Currency[];
  userSettings?: UserSettings;

  newLoanFormGroup: FormGroup = new FormGroup({
    'sum': new FormControl(0, [Validators.required, Validators.min(100), Validators.max(3_165_000)]),
    'currency': new FormControl()
  });

  get inputSum() {
    return this.newLoanFormGroup.get('sum')?.value ?? 0;
  }

  get currentCurrency() {
    return this.newLoanFormGroup.get('currency')?.value ?? '';
  }

  ngOnInit(): void {
    this.profileDataService.getCurrencies().subscribe(res => {
      this.currencies = res;
    })

    this.profileDataService.getUserSettings().subscribe(res => {
      this.userSettings = res[0];
      this.newLoanFormGroup.patchValue({
        'currency': this.userSettings?.preferred_currency
      })
    })
  }

  loadPercent(sum: number) {
    this.loansService.getPercent(sum, this.newLoanFormGroup.get('currency')?.value).subscribe(value => {
      this.calculatedPercent = value;
    });
  }

  onInputChange() {
    if (this.newLoanFormGroup.valid) {
      this.loansService.getPercent(this.newLoanFormGroup.get('sum')?.value, this.newLoanFormGroup.get('currency')?.value)
        .subscribe(result => this.calculatedPercent = result);
    }
  }

  confirmCreatingLoan() {
    if (this.newLoanFormGroup.valid) {
      const amount = this.newLoanFormGroup.get('sum')?.value;
      const currency = this.newLoanFormGroup.get('currency')?.value;

      this.loansService.createNewLoan({
        'amount': amount,
        'currency': currency,
        'return_url': 'http://localhost:4200/loans',
      }).subscribe(res => {
        if (res) {
          window.open(res, "_self");
        }
      })
    }
  }
}
