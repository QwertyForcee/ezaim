import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CommonMenuComponent } from './common-menu/common-menu.component';
import { CommonNavigationComponent } from './common-navigation/common-navigation.component';
import { RouterModule } from '@angular/router';
import { PersonalDataAgreementComponent } from './personal-data-agreement/personal-data-agreement.component';



@NgModule({
  declarations: [
    CommonMenuComponent,
    CommonNavigationComponent,
    PersonalDataAgreementComponent
  ],
  imports: [
    CommonModule,
    RouterModule
  ],
  exports: [
    CommonMenuComponent,
    CommonNavigationComponent,
    PersonalDataAgreementComponent,
    
  ]
})
export class ApplicationCommonModule { }
