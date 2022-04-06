# PyAutoClock
---
## Overview
Use Selenium module to  locate the buttons, inputs of the Aurora ERP system, and try to automatically punch the clock according to the user's selection on start & end dates.

## Download
點擊此處下載[AuroraAutoClockPunching.exe](https://github.com/DiuDiuDangAr/PyAutoClock/releases/)

or

    $ git clone https://github.com/DiuDiuDangAr/PyAutoClock

Chrome Driver [Download location](https://chromedriver.chromium.org/downloads)

## Installation & Usage
#安裝與操作細節請參考 [Aurora打卡小工具說明.pdf](https://github.com/DiuDiuDangAr/PyAutoClock/blob/main/Aurora%E6%89%93%E5%8D%A1%E5%B0%8F%E5%B7%A5%E5%85%B7%E8%AA%AA%E6%98%8E.pdf)

## Dependencies
1. Chrome browser installed
2. Chrome driver installed

## Files
1. **holidays.csv**: list the national holidays in Taiwan that'll be skipped if included in the period of selected start-end date
2. **config.ini**: stores the login credential with encrypted format
3. **history.log**: log file

## Source Code
    $ py3 main.py
1. Enter the login credentials on the login window interface.
2. Select a start date in the calendar, and then press the "Get Start Date" button (same for the end date)
3. Press the "Start Clockin and clockout!" button to start punching clock
Note: **Please don't close the Chrome browser during the process going**
