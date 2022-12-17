import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TelegramAccountsComponent } from './telegram-accounts.component';

describe('TelegramAccountsComponent', () => {
  let component: TelegramAccountsComponent;
  let fixture: ComponentFixture<TelegramAccountsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TelegramAccountsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TelegramAccountsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
