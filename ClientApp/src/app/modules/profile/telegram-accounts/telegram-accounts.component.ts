import { Component, OnInit } from '@angular/core';
import { TelegramAccount } from 'src/app/models/telegram-account';
import { ProfileDataService } from '../services/profile-data.service';

@Component({
  selector: 'app-telegram-accounts',
  templateUrl: './telegram-accounts.component.html',
  styleUrls: ['./telegram-accounts.component.scss']
})
export class TelegramAccountsComponent implements OnInit {

  constructor(private profileDataService: ProfileDataService) { }

  accounts?: TelegramAccount[];

  get confirmedAccounts() {
    return this.accounts?.filter(a => a.confirmed);
  }

  get notConfirmedAccounts() {
    return this.accounts?.filter(a => !a.confirmed);
  }

  ngOnInit(): void {
    this.loadAccounts();
  }

  onConfirm(account: TelegramAccount) {
    if (account) {
      account.confirmed = true;
      this.profileDataService.updateTelegramAccount(account).subscribe(() => {
        this.loadAccounts();
      })
    }
  }

  onDelete(id?: number) {
    if (id) {
      this.profileDataService.deleteTelegramAccount(id).subscribe(() => {
        this.loadAccounts();
      })
    }
  }

  private loadAccounts() {
    this.profileDataService.getTelegramAccounts().subscribe((result) => {
      this.accounts = result;
    })
  }
}
