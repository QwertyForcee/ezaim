import { Component, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-profile-menu',
  templateUrl: './profile-menu.component.html',
  styleUrls: ['./profile-menu.component.scss']
})
export class ProfileMenuComponent implements OnInit {

  constructor(private router: ActivatedRoute) { }

  currentUrl = '';
  menuItems = [
    { title: 'данные об аккауте', url: '/profile' },
    { title: 'мои займы', url: 'loans' },
    { title: 'настройки', url: '' },
    { title: 'выйти', url: '' },
  ]
  ngOnInit(): void {
    this.currentUrl = window.location.href.split('/').pop() ?? '';
  }

  isSelectedUrl(url: string): boolean {
    return url.replace('/', '') === this.currentUrl;
  }

  onMenuItemClicked() {
    setTimeout(() => {
      this.currentUrl = window.location.href.split('/').pop() ?? '';
    }, 0)
  }

}
