import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { JwtHelperService } from '@auth0/angular-jwt';
import { environment } from 'src/environments/environment';
import { LoginModel } from './models/login-model';
import { LoginResultModel } from './models/login-result-model';
import { SignUpModel } from './models/sign-up-model';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly AUTH_LOGIN = 'api/Auth/LogIn';
  private readonly AUTH_SIGNUP = 'api/Auth/SignUp';
  constructor(private http: HttpClient, private jwtHelper: JwtHelperService, private router: Router) { }

  login(model: LoginModel): void {
    this.http.post<LoginResultModel>(`${environment.baseUrl}${this.AUTH_LOGIN}`, model)
      .subscribe({
        next: (result: LoginResultModel) => {
          if (result) {
            localStorage.setItem('access_token', result.access_token);
            this.router.navigate(['']);
          }
        },
        error: (err) => {
          console.error(err);
        }
      })
  }

  signUp(model: SignUpModel): void {
    this.http.post<LoginResultModel>(`${environment.baseUrl}${this.AUTH_SIGNUP}`, model)
      .subscribe({
        next: (result: LoginResultModel) => {
          if (result) {
            localStorage.setItem('access_token', result.access_token);
            this.router.navigate(['']);
          }
        }
      })
  }
}
