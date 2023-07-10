# PyAutoClock
---
## Overview
Use Selenium module to  locate the buttons, inputs of the Aurora ERP system, and try to automatically punch the clock according to the user's selection on start & end dates.

## Demo & 操作步驟
1. 點擊兩下開啟程式
2. 輸入帳號(員工編號)與密碼 (預設為身份證字號開頭英文為大寫)
3. 連線成功後 點擊開始日期 -> 點擊Get Start Date -> 點擊結束日期 -> 點擊Get End Date
4. 按下 Start Clockin and clockout! 按鈕程式將開始自動打卡

![SOP](https://github.com/DiuDiuDangAr/PyAutoClock/blob/main/appendix/sop_.gif)

Note: 程式自動打卡時, 相關視窗皆可縮小, 但切記別關閉! 完成後會彈出視窗顯示打卡完成

![finished](https://github.com/DiuDiuDangAr/PyAutoClock/blob/main/appendix/finished.PNG)

## Download
點擊此處下載[AuroraAutoClockPunching.exe](https://github.com/DiuDiuDangAr/PyAutoClock/releases/)

or

    $ git clone https://github.com/DiuDiuDangAr/PyAutoClock

FireFox Geckdriver [Download location](https://github.com/mozilla/geckodriver/releases)

Chrome Driver [Download location](https://chromedriver.chromium.org/downloads)

## Installation & Usage
### 2.0.X - 安裝與操作細節請參考 [Aurora打卡小工具2.0.pdf](https://github.com/DiuDiuDangAr/PyAutoClock/blob/main/Aurora%E6%89%93%E5%8D%A1%E5%B0%8F%E5%B7%A5%E5%85%B72.0%E8%AA%AA%E6%98%8E.pdf)
### 1.0.X - 安裝與操作細節請參考 [Aurora打卡小工具說明.pdf](https://github.com/DiuDiuDangAr/PyAutoClock/blob/main/Aurora%E6%89%93%E5%8D%A1%E5%B0%8F%E5%B7%A5%E5%85%B7%E8%AA%AA%E6%98%8E.pdf)


## Dependencies - For 2.0.X
1. FireFox browser installed (version shall be 114 or 115)

## Dependencies - For 1.0.X
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
