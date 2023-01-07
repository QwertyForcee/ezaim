import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { JwtHelperService } from '@auth0/angular-jwt';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { LoginModel } from './models/login-model';
import { LoginResultModel } from './models/login-result-model';
import { SignUpModel } from './models/sign-up-model';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly AUTH_LOGIN = 'auth/login';
  private readonly AUTH_SIGNUP = 'auth/signup';
  constructor(private http: HttpClient, private jwtHelper: JwtHelperService, private router: Router) { }

  login(model: LoginModel): void {
    this.http.post<LoginResultModel>(`${environment.baseUrl}${this.AUTH_LOGIN}`, model)
      .subscribe({
        next: (result: LoginResultModel) => {
          if (result) {
            localStorage.setItem('access_token', result.access_token);
            this.router.navigate(['/profile']);
          }
        },
        error: (err) => {
          console.error(err);
        }
      })
  }

  signUp(model: SignUpModel): Observable<LoginResultModel> {
    return this.http.post<LoginResultModel>(`${environment.baseUrl}${this.AUTH_SIGNUP}`, model);
  }
}
