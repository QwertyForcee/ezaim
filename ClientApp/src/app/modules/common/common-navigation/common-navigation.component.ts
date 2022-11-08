import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-common-navigation',
  templateUrl: './common-navigation.component.html',
  styleUrls: ['./common-navigation.component.scss']
})
export class CommonNavigationComponent implements OnInit {

  @Input() title: string = 'Title';
  constructor() { }

  ngOnInit(): void {
  }

}
