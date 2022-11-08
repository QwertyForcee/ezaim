import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-profile-menu',
  templateUrl: './profile-menu.component.html',
  styleUrls: ['./profile-menu.component.scss']
})
export class ProfileMenuComponent implements OnInit {

  constructor(private router: ActivatedRoute) { }

  menuItems = [
    {title: 'данные об аккауте', url: 'data'},
    {title: 'мои займы', url: ''},
    {title: 'настройки', url: ''},
  ]
  ngOnInit(): void {
    console.log(this.router)
  }

}
