import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { AbstractControl, FormControl, FormGroup, ValidationErrors, Validators } from '@angular/forms';
import { AuthService } from '../auth.service';
import { AddressModel } from '../models/address-model';
import { SignUpModel } from '../models/sign-up-model';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
  encapsulation: ViewEncapsulation.None,
})
export class LoginComponent implements OnInit {

  isLoginMode = false;
  showAgreement = false;

  get invalidLogInForm(): boolean {
    return this.loginFormGroup.invalid;
  }

  get invalidSignUpForm(): boolean {
    return this.signUpFormGroup.invalid;
  }

  loginFormGroup: FormGroup = new FormGroup(
    {
      email: new FormControl(null, [Validators.required, Validators.email]),
      password: new FormControl(null, [Validators.required, Validators.minLength(6), Validators.maxLength(150)])
    }
  )

  signUpFormGroup: FormGroup = new FormGroup(
    {
      personalDataTermsAgreement: new FormControl(false),
      email: new FormControl(null, [Validators.required, Validators.email]),
      phoneNumber: new FormControl(null, [Validators.required, Validators.minLength(12), Validators.maxLength(12)]),  //Validators.minLength(12), Validators.maxLength(12)
      password: new FormControl(null, [Validators.required, Validators.minLength(6), Validators.maxLength(150)]),
      confirmPassword: new FormControl(null, [Validators.required, Validators.minLength(6), Validators.maxLength(150)]),

      name: new FormControl(null, [Validators.required, Validators.minLength(2)]),
      surname: new FormControl(null, [Validators.required, Validators.minLength(2)]),
      passportNumber: new FormControl(null, [Validators.required, Validators.minLength(9), Validators.maxLength(9)]),
      identificationNumber: new FormControl(null, [Validators.required, Validators.minLength(14), Validators.maxLength(14)]),
      issueDate: new FormControl(null, [Validators.required]),
      expiryDate: new FormControl(null, [Validators.required]),
      authority: new FormControl(null, [Validators.required]),
      nationality: new FormControl(null, [Validators.required]),

      sex: new FormControl(null, [Validators.required]),
      resident: new FormControl(null, [Validators.required]),
      birthDate: new FormControl(new Date()),

      birth_country: new FormControl(null, [Validators.required]),
      birth_state: new FormControl(null, [Validators.required]),
      birth_city: new FormControl(null, [Validators.required]),

      registration_country: new FormControl(null, [Validators.required, Validators.minLength(2)]),
      registration_state: new FormControl(null, [Validators.required, Validators.minLength(2)]),
      registration_city: new FormControl(null, [Validators.required, Validators.minLength(2)]),
      registration_codeSoato: new FormControl(null, [Validators.required, Validators.minLength(10), Validators.maxLength(10)]),
      registration_street: new FormControl(null, [Validators.required, Validators.minLength(3)]),
      registration_house: new FormControl(null, [Validators.required]),
      registration_flat: new FormControl(null, [Validators.required]),
      registration_mailIndex: new FormControl(null, [Validators.required]),

      residential_country: new FormControl(null, [Validators.required, Validators.minLength(2)]),
      residential_state: new FormControl(null, [Validators.required, Validators.minLength(2)]),
      residential_city: new FormControl(null, [Validators.required, Validators.minLength(2)]),
      residential_codeSoato: new FormControl(null, [Validators.required, Validators.minLength(10), Validators.maxLength(10)]),
      residential_street: new FormControl(null, [Validators.required, Validators.minLength(3)]),
      residential_house: new FormControl(null, [Validators.required]),
      residential_flat: new FormControl(null, [Validators.required]),
      residential_mailIndex: new FormControl(null, [Validators.required]),

    }, { validators: this.passwordsValidation }
  )

  constructor(private authService: AuthService) { }

  ngOnInit(): void {
  }

  onSwitch() {
    this.isLoginMode = !this.isLoginMode;
  }

  onSubmit() {
    if (this.isLoginMode) {
      if (this.loginFormGroup.valid) {
        this.authService.login(this.loginFormGroup.value);
      }
    } else {
      if (this.signUpFormGroup.valid) {
        const birthAddress = {
          country: this.signUpFormGroup.get('birth_country')?.value,
          state: this.signUpFormGroup.get('birth_state')?.value,
          city: this.signUpFormGroup.get('birth_city')?.value
        } as AddressModel;

        const registrationAddress = {
          country: this.signUpFormGroup.get('registration_country')?.value,
          state: this.signUpFormGroup.get('registration_state')?.value,
          city: this.signUpFormGroup.get('registration_city')?.value,
          codeSoato: this.signUpFormGroup.get('registration_codeSoato')?.value,
          street: this.signUpFormGroup.get('registration_street')?.value,
          house: this.signUpFormGroup.get('registration_house')?.value,
          flat: this.signUpFormGroup.get('registration_flat')?.value,
          mailIndex: this.signUpFormGroup.get('registration_mailIndex')?.value
        } as AddressModel;

        const residentialAddress = {
          country: this.signUpFormGroup.get('residential_country')?.value,
          state: this.signUpFormGroup.get('residential_state')?.value,
          city: this.signUpFormGroup.get('residential_city')?.value,
          codeSoato: this.signUpFormGroup.get('residential_codeSoato')?.value,
          street: this.signUpFormGroup.get('residential_street')?.value,
          house: this.signUpFormGroup.get('residential_house')?.value,
          flat: this.signUpFormGroup.get('residential_flat')?.value,
          mailIndex: this.signUpFormGroup.get('residential_mailIndex')?.value
        } as AddressModel;

        const signUpModel = this.signUpFormGroup.value as SignUpModel;
        signUpModel.birthAddress = birthAddress;
        signUpModel.registrationAddress = registrationAddress;
        signUpModel.residentialAddress = residentialAddress;
        console.log(signUpModel);
        
        this.authService.signUp(signUpModel);
      }
    }
  }

  duplicate() {
    this.signUpFormGroup.patchValue({
      residential_country: this.signUpFormGroup.get('registration_country')?.value,
      residential_state: this.signUpFormGroup.get('registration_state')?.value,
      residential_city: this.signUpFormGroup.get('registration_city')?.value,
      residential_codeSoato: this.signUpFormGroup.get('registration_codeSoato')?.value,
      residential_street: this.signUpFormGroup.get('registration_street')?.value,
      residential_house: this.signUpFormGroup.get('registration_house')?.value,
      residential_flat: this.signUpFormGroup.get('registration_flat')?.value,
      residential_mailIndex: this.signUpFormGroup.get('registration_mailIndex')?.value
    })
  }
  
  switchShowAgreement(){
    this.showAgreement = !this.showAgreement;
  }

  private passwordsValidation(group: AbstractControl): ValidationErrors | null {
    const pass = group.get('password')?.value;
    const confirmPass = group.get('confirmPassword')?.value
    return pass === confirmPass ? null : { notSame: true }
  }
}
