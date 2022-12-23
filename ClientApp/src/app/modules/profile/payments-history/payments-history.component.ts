import { Component, OnInit } from '@angular/core';
import * as moment from 'moment';
import { CompletePayment } from 'src/app/models/payment-history-model';
import { ProfileDataService } from '../services/profile-data.service';

@Component({
  selector: 'app-payments-history',
  templateUrl: './payments-history.component.html',
  styleUrls: ['./payments-history.component.scss']
})
export class PaymentsHistoryComponent implements OnInit {

  constructor(private profileDataService: ProfileDataService) { }
  payments?: CompletePayment[];
  dateFormat: string = 'MM/DD/YYYY';

  ngOnInit(): void {
    this.profileDataService.getPayments().subscribe(res=> {
      this.payments = res;
    })

    this.profileDataService.getUserSettings().subscribe(res=>{
      this.dateFormat = res[0].date_format;
    })
  }

  formattedDate(date:string) {
    return moment(date).format(this.dateFormat)
  }

}
