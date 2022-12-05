import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  isLoginMode = false;
  constructor() { }

  ngOnInit(): void {
  }

  onSwitch() {
    this.isLoginMode = !this.isLoginMode;
  }
}
