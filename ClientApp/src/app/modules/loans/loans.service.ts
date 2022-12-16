import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { LoanModel } from 'src/app/models/loan-model';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class LoansService {

  private readonly LOAD_LOANS = 'loans/GetUserLoans';
  private readonly LOAD_CALCULATED_SUM_FOR_LOAN = 'Loans/GetCalculatedSumForLoan';
  private readonly LOAD_LOAN = 'loans'

  constructor(private http: HttpClient) { }

  getUserLoans(): Observable<LoanModel[]> {
    return this.http.post<LoanModel[]>(`${environment.baseUrl}${this.LOAD_LOANS}`, {});
  }

  getUserLoanById(id: number): Observable<LoanModel> {
    return this.http.get<LoanModel>(`${environment.baseUrl}${this.LOAD_LOAN}`, {
      params: {
        id: id,
      }
    });
  }

  getCalculatedSumForLoanDay(loanId: number, date: Date | string) {
    return this.http.post<number>(`${environment.baseUrl}${this.LOAD_CALCULATED_SUM_FOR_LOAN}`, { loanId, date });
  }
}
