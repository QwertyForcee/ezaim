export class DateHelper {
    private static toMonthsNames = [
        'Январю',
        'Февралю',
        'Марту',
        'Апрелю',
        'Маю',
        'Июню',
        'Июлю',
        'Августу',
        'Сентябрю',
        'Октябрю',
        'Ноябрю',
        'Декабрю'
    ]

    private static monthsNames = [
        'Январь',
        'Февраль',
        'Март',
        'Апрель',
        'Май',
        'Июнь',
        'Июль',
        'Август',
        'Сентябрь',
        'Октябрь',
        'Ноябрь',
        'Декабрь'
    ]

    static getMonthName(monthNumber: number, useToName = false) {
        if (useToName) {
            return this.toMonthsNames[monthNumber];
        }
        else {
            return this.monthsNames[monthNumber];
        }
    }

    static parseMonthNumber(currentMonth: number, addValue: number) {
        while (addValue > 11) {
            addValue = addValue - 11;
        }
        //11 + 3
        if (currentMonth + addValue > 11) {
            return currentMonth + addValue - 12;
        }
        if (currentMonth + addValue < 0) {
            console.log(`${currentMonth} , ${addValue}, ${11 + currentMonth + addValue}`);

            return 11 + currentMonth + addValue + 1;
        }
        else {
            return currentMonth + addValue;
        }
    }

    static parseYearNumber(currentYear: number, currentMonth: number, addValue: number) {
        while (addValue > 11) {
            addValue = addValue - 11;
            currentYear++;
        }
        if (currentMonth + addValue > 11) {
            currentYear++;
        }
        return currentYear;
    }

    static getDays(year: number, month: number): number {
        return new Date(year, month + 1, 0).getDate();
    }
}