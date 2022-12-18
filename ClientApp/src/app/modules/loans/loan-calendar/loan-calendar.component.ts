import { Component, Input, OnInit, ViewEncapsulation } from '@angular/core';
import { DateHelper } from 'src/app/utilities/date-helper';
import { LoansService } from '../loans.service';

@Component({
  selector: 'app-loan-calendar',
  templateUrl: './loan-calendar.component.html',
  styleUrls: ['./loan-calendar.component.scss'],
  encapsulation: ViewEncapsulation.None,
})
export class LoanCalendarComponent implements OnInit {

  @Input() loanId?: number;

  constructor(private loansService: LoansService) { }

  realCurrentDate: Date = new Date();
  currentDate!: Date;

  get realCurrentYear(): number {
    return this.realCurrentDate.getFullYear();
  }

  get realCurrentMonth(): number {
    return this.realCurrentDate.getMonth();
  }

  get realCurrentDay(): number {
    return this.realCurrentDate.getDate();
  }

  ngOnInit(): void {
    this.currentDate = new Date();
    // this.currentDate.setDate(0);
  }

  getMonthName(toAdd: number, useToName = false): string {
    const monthIndex = DateHelper.parseMonthNumber(this.currentDate.getMonth(), toAdd);
    return DateHelper.getMonthName(monthIndex, useToName);
  }

  getMonthDaysCount(toAdd: number) {
    const year = DateHelper.parseYearNumber(this.currentDate.getFullYear(), this.currentDate.getMonth(), toAdd);
    const monthIndex = DateHelper.parseMonthNumber(this.currentDate.getMonth(), toAdd);
    return this.getDaysObjects(year, monthIndex, this.getDays(DateHelper.getDays(year, monthIndex)));
  }

  get currentMonthDays() {
    return this.getMonthDaysCount(0);
  }

  get nextMonthDays() {
    return this.getMonthDaysCount(1);
  }

  get nextNextMonthDays() {
    return this.getMonthDaysCount(2);
  }

  dayToolTip(day: number, month: number, year: number) {
    // if (this.loanId) {
      return this.loansService.getCalculatedSumForLoanDayAsync(this.loanId ?? 0, new Date(year, month, day))
      // return ``
    // }
    // return '';
  }

  trackByDay(index: any, item: any) {
    return item.id;
  }

  shiftMonthLeft(): void {
    this.currentDate.setMonth(this.currentDate.getMonth() - 1, this.currentDate.getDate());
  }

  shiftMonthRight(): void {
    this.currentDate.setMonth(this.currentDate.getMonth() + 1, 1);
  }

  private getDays(count: number): number[] {
    return Array.from(Array(count)).map((e, i) => i + 1);
  }

  private getDaysObjects(year: number, month: number, days: number[]) {
    return days.map(day => {
      return {
        id: `${year}_${month}_${day}`,
        value: day,
        isPrev: this.isPreviousDate(year, month, day),
        isToday: this.isCurrentDate(year, month, day),
        year: year,
        month: month,
      }
    });
  }

  private isPreviousDate(year: number, month: number, day: number) {
    return this.realCurrentYear > year
      || (this.realCurrentYear === year && (this.realCurrentMonth > month
        || (this.realCurrentMonth === month && this.realCurrentDay > day))
      )
  }
  private isCurrentDate(year: number, month: number, day: number) {
    return this.realCurrentYear === year && this.realCurrentMonth === month && this.realCurrentDay === day;
  }
}