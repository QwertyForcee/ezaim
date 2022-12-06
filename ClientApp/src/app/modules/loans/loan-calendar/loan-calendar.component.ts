import { Component, OnInit } from '@angular/core';
import { DateHelper } from 'src/app/utilities/date-helper';

@Component({
  selector: 'app-loan-calendar',
  templateUrl: './loan-calendar.component.html',
  styleUrls: ['./loan-calendar.component.scss']
})
export class LoanCalendarComponent implements OnInit {

  constructor() { }
  realCurrentDate: Date = new Date();
  currentDate: Date = new Date();

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

  private getDays(count: number): number[] {
    return Array.from(Array(count)).map((e, i) => i + 1);
  }

  private getDaysObjects(year: number, month: number, days: number[]) {
    return days.map(day => {
      return {
        value: day,
        isPrev: this.isPreviousDate(year, month, day),
        isToday: this.isCurrentDate(year, month, day)
      }
    });
  }

  private isPreviousDate(year: number, month: number, day: number) {
    return this.realCurrentYear > year
      || (this.realCurrentYear === year && this.realCurrentMonth > month
        || (this.realCurrentMonth === month && this.realCurrentDay > day)
      )
  }
  private isCurrentDate(year: number, month: number, day: number) {
    return this.realCurrentYear === year && this.realCurrentMonth === month && this.realCurrentDay === day;
  }
}