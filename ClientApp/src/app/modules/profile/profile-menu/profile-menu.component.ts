import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-profile-menu',
  templateUrl: './profile-menu.component.html',
  styleUrls: ['./profile-menu.component.scss']
})
export class ProfileMenuComponent implements OnInit {

  constructor() { }

  menuItems = [
    {title: 'данные об аккауте', url: 'data'},
    {title: 'мои займы', url: ''},
    {title: 'настройки', url: ''},
  ]
  ngOnInit(): void {
  }

}
