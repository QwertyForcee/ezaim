import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { LoanModel } from 'src/app/models/loan-model';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class LoansService {

  private readonly GET_LOANS = 'api/Loans/GetUserLoans';

  constructor(private http: HttpClient) { }

  getUserLoans(): Observable<LoanModel[]> {
    return this.http.get<LoanModel[]>(`${environment.baseUrl}${this.GET_LOANS}`);
  }
}
