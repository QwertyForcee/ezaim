import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { LoanModel } from 'src/app/models/loan-model';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class LoansService {

  private readonly LOAD_CALCULATED_SUM_FOR_LOAN = 'Loans/GetCalculatedSumForLoan';
  private readonly LOAN_URL = `${environment.baseUrl}loans`;

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

  createNewLoan(loan: LoanModel){
    
  }

  getCalculatedSumForLoanDay(loanId: number, date: Date | string) {
    return this.http.post<number>(`${environment.baseUrl}${this.LOAD_CALCULATED_SUM_FOR_LOAN}`, { loanId, date });
  }
}
