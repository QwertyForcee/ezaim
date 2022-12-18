import { Component, HostListener, OnInit } from '@angular/core';
import { environment } from 'src/environments/environment';
import { ProfileDataService } from '../../profile/services/profile-data.service';

@Component({
  selector: 'app-common-menu',
  templateUrl: './common-menu.component.html',
  styleUrls: ['./common-menu.component.scss']
})
export class CommonMenuComponent implements OnInit {
  menuItems = [
    { title: 'главная', url: '' },
    { title: 'личный кабинет', url: '/profile' },
    { title: 'мои займы', url: '/loans' },
    { title: 'новый займ', url: '/new-loan', star: true },

  ]
  expanded = false;
  constructor() { }

  @HostListener('window:scroll')
  onScroll() {
    this.expanded = false;
  }

  ngOnInit(): void {
  }

  expandMenu(): void {
    this.expanded = true;
  }

  closeMenu(): void {
    this.expanded = false;
  }

  get isAuthorized() {
    const token = localStorage.getItem(environment.access_token_key);
    return token !== null && token !== undefined;
  }
}
