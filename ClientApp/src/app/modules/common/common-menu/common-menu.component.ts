import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-common-menu',
  templateUrl: './common-menu.component.html',
  styleUrls: ['./common-menu.component.scss']
})
export class CommonMenuComponent implements OnInit {
  expanded = false;
  constructor() { }

  ngOnInit(): void {
  }

  expandMenu(): void {
    this.expanded = true;
  }
}
