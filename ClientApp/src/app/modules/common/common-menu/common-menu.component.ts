import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-common-menu',
  templateUrl: './common-menu.component.html',
  styleUrls: ['./common-menu.component.scss']
})
export class CommonMenuComponent implements OnInit {
  menuItems = [
    { title: 'личный кабинет', url: '/profile' },
    { title: 'мои займы', url: '' },
    { title: 'настройки', url: '' },
    { title: 'выйти', url: '' },
  ]
  expanded = false;
  constructor() { }

  ngOnInit(): void {
  }

  expandMenu(): void {
    this.expanded = true;
  }

  closeMenu(): void {
    this.expanded = false;
  }
}
