# PyAutoClock
---
## Overview
Use Selenium module to  locate the buttons, inputs of the Aurora ERP system to automatically punch the clock.

## Download
($ git clone https://github.com/DiuDiuDangAr/PyAutoClock)

## Usage
($ py3 main.py)
1. Enter the login credentials on the login window interface.
2. Select a start date in the calendar, and then press the "Get Start Date" button (same for the end date)
3. Press the "Start Clockin and clockout!" button to start punching clock
Note: **Please don't close the Chrome browser during the process going**

## Files
1. holidays.csv: list the national holidays in Taiwan that'll be skipped if included in the period of selected start-end date
2. config.ini: stores the login credential with encrypted format
3. history.log: log file

## Dependencies
1. Chrome browser installed
2. Chrome driver installed
