import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { LoansService } from '../loans.service';

@Component({
  selector: 'app-new-loan-form',
  templateUrl: './new-loan-form.component.html',
  styleUrls: ['./new-loan-form.component.scss']
})
export class NewLoanFormComponent implements OnInit {

  constructor(private loansService: LoansService) { }

  calculatedPercent = 0;

  newLoanFormGroup: FormGroup = new FormGroup({
    'sum': new FormControl(0,[Validators.required, Validators.min(100), Validators.max(3_165_000)])
  });

  get inputSum(){
    return this.newLoanFormGroup.get('sum')?.value ?? 0;
  }

  ngOnInit(): void {

  }

  loadPercent(sum: number) {
    this.loansService.getPercent(sum).subscribe(value => {
      this.calculatedPercent = value;
    });
  }
}
