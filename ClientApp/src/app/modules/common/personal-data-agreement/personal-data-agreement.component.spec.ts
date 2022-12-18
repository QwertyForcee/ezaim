import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PersonalDataAgreementComponent } from './personal-data-agreement.component';

describe('PersonalDataAgreementComponent', () => {
  let component: PersonalDataAgreementComponent;
  let fixture: ComponentFixture<PersonalDataAgreementComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PersonalDataAgreementComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PersonalDataAgreementComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
