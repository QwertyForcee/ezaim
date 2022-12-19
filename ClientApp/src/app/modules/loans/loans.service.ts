import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { lastValueFrom, Observable } from 'rxjs';
import { LoanModel } from 'src/app/models/loan-model';
import { NewLoanModel } from 'src/app/models/new-loan-model';
import { Payment } from 'src/app/models/payment';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class LoansService {

  private readonly LOAD_CALCULATED_SUM_FOR_LOAN = `${environment.baseUrl}loans/GetCalculatedSumForLoan/`;
  private readonly LOAD_PERCENT_FOR_SUM = `${environment.baseUrl}loans/GetPercent`;

  private readonly LOAN_URL = `${environment.baseUrl}loans/`;
  private readonly PAYMENT_URL = `${environment.baseUrl}payments/`;

  constructor(private http: HttpClient) { }

  getUserLoans(): Observable<LoanModel[]> {
    return this.http.get<LoanModel[]>(this.LOAN_URL);
  }

  getUserLoanById(id: number): Observable<LoanModel> {
    return this.http.get<LoanModel>(this.LOAN_URL, {
      params: {
        id: id,
      }
    });
  }

  createNewLoan(newLoanModel: NewLoanModel): Observable<string> {
    return this.http.post<string>(this.LOAN_URL, newLoanModel);
  }

  getCalculatedSumForLoanDay(loanId: number, date: Date | string) {
    // const sum$ = await this.http.post<number>(`${environment.baseUrl}${this.LOAD_CALCULATED_SUM_FOR_LOAN}`, { loanId, date });
    // return lastValueFrom(sum$).then(v => v ?? '');
    return this.http.post<number>(this.LOAD_CALCULATED_SUM_FOR_LOAN, { loanId, date });
  }

  getPercent(sum: number, currency: number): Observable<number> {
    return this.http.get<number>(this.LOAD_PERCENT_FOR_SUM, {
      params: {
        sum,
        currency
      }
    });
  }

  createNewPayment(payment: Payment): Observable<string> {
    return this.http.post<string>(this.PAYMENT_URL, payment);
  }
}
