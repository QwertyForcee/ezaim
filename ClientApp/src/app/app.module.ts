import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AuthModule } from './modules/auth/auth.module';
import { ApplicationCommonModule } from './modules/common/common.module';
import { LoansModule } from './modules/loans/loans.module';
import { ProfileModule } from './modules/profile/profile.module';
import { HomeComponent } from './shared/home/home.component';


@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ApplicationCommonModule,
    CommonModule,
    AuthModule,
    ProfileModule,
    LoansModule,
    BrowserAnimationsModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
