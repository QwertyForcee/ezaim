import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-profile-data',
  templateUrl: './profile-data.component.html',
  styleUrls: ['./profile-data.component.scss']
})
export class ProfileDataComponent implements OnInit {

  constructor() {
    this.userDataForm = new FormGroup({
      "Email": new FormControl("user.example@gmail.com"),
      "Phone": new FormControl("+375 (29) 111 22 33"),
    });
  }

  userFullName = 'Максим Максимов Максимович';
  email = 'user.example@gmail.com';
  userDataForm: FormGroup;
  


  ngOnInit(): void {

  }

}
