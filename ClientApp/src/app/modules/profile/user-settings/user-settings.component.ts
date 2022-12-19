import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Currency } from 'src/app/models/currency';
import { UserSettings } from 'src/app/models/user-settings';
import { ProfileDataService } from '../services/profile-data.service';

@Component({
  selector: 'app-user-settings',
  templateUrl: './user-settings.component.html',
  styleUrls: ['./user-settings.component.scss']
})
export class UserSettingsComponent implements OnInit {

  constructor(private profileDataService: ProfileDataService) { }

  userSettings?: UserSettings;
  userSettingsGroup: FormGroup = new FormGroup(
    {
      user: new FormControl(0),
      date_format: new FormControl(null, [Validators.required]),
      week_start: new FormControl(null, [Validators.required]),
      preferred_currency: new FormControl(null, [Validators.required]),
    }
  );

  daysOfWeek = [
    { name: "Воскресенье", id: 0 },
    { name: "Понедельник", id: 1 }
  ]
  currencies?: Currency[];

  ngOnInit(): void {
    this.loadUserSettings();
  }

  onSave() {
    if (this.userSettingsGroup && this.userSettingsGroup.valid) {

      this.userSettingsGroup.patchValue({ 'week_start': parseInt(this.userSettingsGroup.get('week_start')?.value.toString()) })
      this.userSettingsGroup.patchValue({ 'preferred_currency': parseInt(this.userSettingsGroup.get('preferred_currency')?.value.toString()) })

      if (this.userSettings !== undefined) {
        this.profileDataService.updateUserSettings(this.userSettingsGroup.value).subscribe(() => {
          this.loadUserSettings();
        });
      } else {
        this.profileDataService.createUserSettings(this.userSettingsGroup.value).subscribe(() => {
          this.loadUserSettings();
        });
      }
    }
  }

  loadUserSettings() {
    this.userSettings = undefined;
    this.profileDataService.getCurrencies().subscribe(currencies => {
      this.currencies = currencies;
      this.profileDataService.getUserSettings().subscribe(res => {
        if (res && res.length > 0) {
          this.userSettings = res[0];
          this.userSettingsGroup.setValue(this.userSettings);
        }
      })
    })

  }
}
