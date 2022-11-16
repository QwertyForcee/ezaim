import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-common-menu',
  templateUrl: './common-menu.component.html',
  styleUrls: ['./common-menu.component.scss']
})
export class CommonMenuComponent implements OnInit {
  menuItems = [
    { title: 'главная', url: '' },
    { title: 'личный кабинет', url: '/profile' },
    { title: 'мои займы', url: '' },
    { title: 'новый займ', url: '', star: true },

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