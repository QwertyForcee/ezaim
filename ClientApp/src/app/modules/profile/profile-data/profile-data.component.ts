import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ProfileDataService } from '../services/profile-data.service';

@Component({
  selector: 'app-profile-data',
  templateUrl: './profile-data.component.html',
  styleUrls: ['./profile-data.component.scss']
})
export class ProfileDataComponent implements OnInit {

  constructor(private profileDataService: ProfileDataService) { }

  get userFullName() {
    return `${this.userDataFormGroup.get('surname')?.value} ${this.userDataFormGroup.get('name')?.value}`;
  }
  email = 'user.example@gmail.com';
  userDataFormGroup: FormGroup = new FormGroup({
    "id": new FormControl(),
    "name": new FormControl(),
    "surname": new FormControl(),
    "email": new FormControl(null, [Validators.required, Validators.email]),
    "phone_number": new FormControl(null, [Validators.required, Validators.minLength(12), Validators.maxLength(12)]),
  });

  cards = [];
  editMode = false;

  ngOnInit(): void {
    this.loadUserData();
  }

  switchMode() {
    this.editMode = !this.editMode;
  }

  onSave() {
    if (this.userDataFormGroup.valid) {
      this.profileDataService.updateUserData(this.userDataFormGroup.value).subscribe(() => {
        this.loadUserData();
      });
    }
  }

  private loadUserData() {
    this.profileDataService.getUserData().subscribe((result) => {
      if (result && result.length > 0) {
        const user = result[0]
        this.userDataFormGroup.setValue({
          "id": user.id,
          "name": user.name,
          "surname": user.surname,
          "email": user.email,
          "phone_number": user.phone_number,
        });
      }
    })
  }
}
