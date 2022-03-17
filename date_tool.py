import csv
import logging
from datetime import date, datetime, timedelta

class DateTool:
    def __init__(self) -> None:
        self.logger = logging.getLogger("date_tool")

        self._file_name = 'holidays.csv'
        self._workday_list = None
        self._workday_cnt = 0
        self._holiday_list = []
        self._holiday_cnt = 0

    def _check_holidays(self, date_list) -> int:
        self._holiday_cnt = 0
        # check whether a day is a holiday in Taiwan holiday calendar or not
        with open(self._file_name, newline='') as holidaycsv:
                rows = csv.reader(holidaycsv)
                for row in rows:
                    self._holiday_list.append([int(row[0]),int(row[1]),int(row[2])])
        self.logger.info(f"[Done] read all the holidays from the holidays.csv: {self._holiday_list}")
        
        self._workday_list = date_list
        for date in self._workday_list[:]:
                if date in self._holiday_list:
                    self._workday_list.remove(date)
                    self.logger.info(f"[Checked] remove date: {date}")
                    self._holiday_cnt +=1
        self.logger.info(f"[Checked] total holiday count: {self._holiday_cnt}")

    def generate_date_list(self, start, end, date_list) -> list:
        self._workday_list = date_list
        self._workday_cnt = (end - start).days + 1
        res = 0
        for d in range(self._workday_cnt):
                day = start + timedelta(days=d)
                if day.weekday() < 5:
                    res += 1
                    date_list.append([int(day.strftime("%Y")),int(day.strftime("%m")),int(day.strftime("%d"))])
        
        self._check_holidays(date_list)
        self.logger.info(f"[Checked] Total business days in range: {str(res-self._holiday_cnt)}; the date list: {str(date_list)}")
        return self._workday_list

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    date_tool = DateTool()
    date_list = []
    date_tool.generate_date_list(start= date.today(), end= date.today(), date_list=date_list)
    print(date_list)