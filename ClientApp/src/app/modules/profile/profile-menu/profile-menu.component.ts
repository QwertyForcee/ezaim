import { Component, OnInit } from '@angular/core';
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
    { title: 'данные об аккауте', url: 'profile' },
    { title: 'мои займы', url: '' },
    { title: 'настройки', url: '' },
    { title: 'выйти', url: '' },
  ]
  ngOnInit(): void {
    this.router.url.subscribe({
      next: (value) => {
        this.currentUrl = value[0].path;
        console.log(value);
      }
    })
  }

  isSelectedUrl(url: string): boolean {
    return url === this.currentUrl;
  }

}
