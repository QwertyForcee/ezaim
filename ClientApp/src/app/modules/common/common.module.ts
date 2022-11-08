import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CommonMenuComponent } from './common-menu/common-menu.component';
import { CommonNavigationComponent } from './common-navigation/common-navigation.component';



@NgModule({
  declarations: [
    CommonMenuComponent,
    CommonNavigationComponent
  ],
  imports: [
    CommonModule
  ],
  exports: [
    CommonMenuComponent,
    CommonNavigationComponent
  ]
})
export class ApplicationCommonModule { }
