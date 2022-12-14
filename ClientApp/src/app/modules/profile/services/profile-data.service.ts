import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Currency } from 'src/app/models/currency';
import { Payment } from 'src/app/models/payment';
import { CompletePayment } from 'src/app/models/payment-history-model';
import { TelegramAccount } from 'src/app/models/telegram-account';
import { User } from 'src/app/models/user';
import { UserSettings } from 'src/app/models/user-settings';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ProfileDataService {

  private readonly USERS_URL = `${environment.baseUrl}users/`;
  private readonly PAYMENT_CARDS_URL = `${environment.baseUrl}payment-cards/`;
  private readonly TELEGRAM_ACCOUNTS_URL = `${environment.baseUrl}telegram-users`;
  private readonly USER_SETTINGS_URL = `${environment.baseUrl}user-settings`;
  private readonly CURRENCY_URL = `${environment.baseUrl}currencies/`;
  private readonly PAYMENTS_URL = `${environment.baseUrl}payments/`;

  constructor(private http: HttpClient) { }

  getUserData(): Observable<User[]> {
    return this.http.get<User[]>(this.USERS_URL);
  }

  updateUserData(user: User) {
    return this.http.put(this.USERS_URL + '0/', user);
  }

  getTelegramAccounts(): Observable<TelegramAccount[]> {
    return this.http.get<TelegramAccount[]>(this.TELEGRAM_ACCOUNTS_URL);
  }

  deleteTelegramAccount(chat_id: number) {
    return this.http.delete(this.TELEGRAM_ACCOUNTS_URL + '/0/', { params: { chat_id } })
  }

  updateTelegramAccount(telegramAccount: TelegramAccount) {
    return this.http.put(this.TELEGRAM_ACCOUNTS_URL  + '/0/', telegramAccount);
  }

  getUserSettings(): Observable<UserSettings[]> {
    return this.http.get<UserSettings[]>(this.USER_SETTINGS_URL);
  }

  updateUserSettings(settings: UserSettings) {
    return this.http.put(this.USER_SETTINGS_URL + '/0/', settings);
  }

  createUserSettings(settings: UserSettings) {
    return this.http.post(this.USER_SETTINGS_URL, settings);
  }

  getCurrencies(): Observable<Currency[]> {
    return this.http.get<Currency[]>(this.CURRENCY_URL);
  }

  getPayments(): Observable<CompletePayment[]> {
    return this.http.get<CompletePayment[]>(this.PAYMENTS_URL);
  }
}
