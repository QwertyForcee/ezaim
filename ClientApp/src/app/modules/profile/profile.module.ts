import { NgModule } from '@angular/core';
import { ProfileDataComponent } from './profile-data/profile-data.component';
import { ProfileComponent } from './profile/profile.component';
import { RouterModule, Routes } from '@angular/router';
import { ApplicationCommonModule } from '../common/common.module';
import { ProfileMenuComponent } from './profile-menu/profile-menu.component';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    ProfileDataComponent,
    ProfileComponent,
    ProfileMenuComponent
  ],
  imports: [
    ApplicationCommonModule,
    RouterModule,
    CommonModule,
    ReactiveFormsModule
  ]
})
export class ProfileModule { }
