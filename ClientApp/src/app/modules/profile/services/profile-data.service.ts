import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { TelegramAccount } from 'src/app/models/telegram-account';
import { User } from 'src/app/models/user';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ProfileDataService {

  private readonly USERS_URL = `${environment.baseUrl}users`;
  private readonly PAYMENT_CARDS_URL = `${environment.baseUrl}payment-cards`;
  private readonly TELEGRAM_ACCOUNTS_URL = `${environment.baseUrl}telegram-users`;

  constructor(private http: HttpClient) { }

  getUserData() {
    return this.http.get(this.USERS_URL);
  }

  updateUserData(user: User) {
    return this.http.put(this.USERS_URL, user);
  }

  getTelegramAccounts(): Observable<TelegramAccount[]> {
    return this.http.get<TelegramAccount[]>(this.TELEGRAM_ACCOUNTS_URL);
  }

  deleteTelegramAccount(chat_id: number) {
    return this.http.delete(this.TELEGRAM_ACCOUNTS_URL, { params: { chat_id } })
  }

  updateTelegramAccount(telegramAccount: TelegramAccount) {
    return this.http.put(this.TELEGRAM_ACCOUNTS_URL, telegramAccount);
  }
}
