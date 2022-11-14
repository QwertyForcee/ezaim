import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-profile-data',
  templateUrl: './profile-data.component.html',
  styleUrls: ['./profile-data.component.scss']
})
export class ProfileDataComponent implements OnInit {

  constructor() { }

  userFullName = 'Максим Максимов Максимович';
  email = 'user.example@gmail.com';

  ngOnInit(): void {
  }

}
