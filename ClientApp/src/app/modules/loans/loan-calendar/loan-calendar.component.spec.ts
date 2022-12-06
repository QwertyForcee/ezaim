import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LoanCalendarComponent } from './loan-calendar.component';

describe('LoanCalendarComponent', () => {
  let component: LoanCalendarComponent;
  let fixture: ComponentFixture<LoanCalendarComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LoanCalendarComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LoanCalendarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
