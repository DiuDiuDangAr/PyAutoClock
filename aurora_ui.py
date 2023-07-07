from sqlite3 import Date
import tkinter as tk
import babel.numbers
import logging
from datetime import date, datetime, timedelta
from tkcalendar import Calendar
from tkinter import messagebox
from aurora_auto_clocker import AuroraAutoClocker
from credential_tool import CredentialRWTool
from date_tool import DateTool

class UIClock:
       def __init__(self) -> None:
       # create AuroraAutoClocker obj
              self._auto_clk = None
              self.logger = logging.getLogger("clocker-UI")
              self._cred_rw_tool = CredentialRWTool()
              self._date_tool = DateTool()

       # create tkinter object
              self.root = tk.Tk()
              self.root.iconphoto(True, tk.PhotoImage(file='misc/ni.png'))
              self.root.title("Aurora自動化打卡系統")
              self.root.protocol("WM_DELETE_WINDOW", self.close_action)

       # set geometry
              self.root.geometry("300x400-10-200")
              self.root.resizable(0,0)

       # set menubar
              self.menubar = tk.Menu(self.root)
              self.filemenu = tk.Menu(self.menubar)
              self.filemenu.add_command(label="Login", command=self.login_ui)
              self.filemenu.add_command(label="About", command=self.about_tool)
              self.menubar.add_cascade(label="File", menu=self.filemenu)
              self.root.config(menu=self.menubar)

       # get today's date
              self.today = date.today()
              self.month = int(self.today.strftime("%m"))
              self.date = int(self.today.strftime("%d"))
              self.year = int(self.today.strftime("%Y"))

       # connection status label
              self.label_conn_status = tk.Label(self.root, text="Disconnected", bg='red')
              self.label_conn_status.place(x=120, y=2)

       # calendar
              self.cal = Calendar(self.root, selectmode = 'day',
                     year = self.year, month = self.month,
                     day = self.date)
              self.cal.place(x=30, y = 40)

              self.date_start = None
              self.date_end = None
              self.date_list = []
              
       # start date button and label
              self.btn_get_start = tk.Button(self.root, text = "Get Start Date",
                     command = self.grad_date_start).place(x=40, y= 220)
              self.label_date_start = tk.Label(self.root, text = "")
              self.label_date_start.place(x=140, y=220)

       # end date Button and Label
              self.btn_get_end = tk.Button(self.root, text = "Get End Date",
                     command = self.grad_date_end).place(x=40, y= 270)     
              self.label_date_end = tk.Label(self.root, text = "")
              self.label_date_end.place(x=140, y=270)

       # start clocking button
              self.btn_start_clock_inout = tk.Button(self.root, text = "Start Clockin and clockout!",
                     command = self.send_start_end_date, bg="gray").place(x=65,y=320)
              self.login_ui()

       # start the Tkinter UI       
              self.root.mainloop()

       def about_tool(self) -> None:
              messagebox.showinfo("About","Powered by NI Engineer")

       def login_ui(self) -> None:
              if self._auto_clk is None:
                     self._auto_clk = AuroraAutoClocker()
              if self._auto_clk.browser_title is None:
                     self.logger.info("the browser title is none")
                     self._auto_clk.__init__()
              self._id, self._pwd = self._cred_rw_tool.read_ini()
              self.compid = tk.StringVar()
              self.compid.set('qd9323')
              self.userid = tk.StringVar()
              self.userid.set(self._id)
              self.userpwd = tk.StringVar()
              self.userpwd.set(self._pwd)

              self.login_page = tk.Toplevel(self.root)
              self.login_page.geometry('300x200-10-250')
              self.login_page.title('Aurora打卡系統登入')
              self.login_page.resizable(0,0)
              self.login_page.attributes('-topmost', True)

              self.label_compid = tk.Label(self.login_page, text ="Company ID").place(x=10, y=10)
              self.entry_compid = tk.Entry(self.login_page, textvariable=self.compid).place(x=110,y=10)
              self.label_userid = tk.Label(self.login_page, text ="User number").place(x=10, y=50)
              self.entry_userid = tk.Entry(self.login_page, textvariable=self.userid).place(x=110,y=50)
              self.label_userpwd = tk.Label(self.login_page, text ="User password").place(x=10, y=90)
              self.entry_userpwd = tk.Entry(self.login_page, textvariable=self.userpwd, show="*").place(x=110,y=90)

              self.btn_login = tk.Button(self.login_page, text = "Login", command = self.login, bg = 'gray').place(x=140,y=130)
              self.logger.info("[Done] show the login window")

       def close_action(self):
              try:
                     self._auto_clk.close()
              except Exception as e:
                     self.logger.warning(f"closing Chrome browser error {e}")
              finally:
                     self.root.quit()
                     self.logger.info("[Done] close all tkinter objs")

       def _check_year_position(self, date) -> date:
              if int(date[0]) in range(2022,2050):
                     self.logger.info("[Checked]: 1st param is the 'year'")
                     date = datetime(int(date[0]),int(date[1]),int(date[2]))
                     return date
              elif int(date[2]) in range(22,50):
                     self.logger.info("[Checked]: 3rd param is the 'year'")
                     date[2] = str(2000 + int(date[2]))
                     date = datetime(int(date[2]),int(date[0]),int(date[1]))
                     return date   

       def grad_date_start(self):
              self.date_start = self.cal.get_date()
              self.label_date_start.config(text = f"Start Date is: {self.date_start}")
              self.date_start = self.date_start.split("/")
              self.date_start = self._check_year_position(self.date_start)

       def grad_date_end(self):
              self.date_end = self.cal.get_date()
              self.label_date_end.config(text = f"End Date is: {self.date_end}")
              self.date_end = self.date_end.split("/")
              self.date_end = self._check_year_position(self.date_end)
    
       def send_start_end_date(self):
              msg_chk = False
              try:
                     assert (self.date_start - self.date_end).days <= 0
                     msg_chk = messagebox.askokcancel('日期確認', f'初始日期為:{self.date_start.strftime("%Y/%m/%d")} 結束日期為:{self.date_end.strftime("%Y/%m/%d")}')
              except Exception as e:
                     messagebox.showinfo(f'填錯了喔!', f'請選擇正確的起始與結束日期!!')
              if msg_chk:
                     self._date_tool.generate_date_list(self.date_start, self.date_end, self.date_list)
                     self.clock_in_out()

       def clock_in_out(self):
              try:
                     for t in self.date_list:
                            self.logger.info(f"[Checked] sending date: {str(t)} to the AutoClocker")
                            self._auto_clk.gen_random_duty_time()
                            self._auto_clk.press_button('申請')
                            self._auto_clk.select_time(clkin=True, y=t[0], m=t[1], d=t[2])
                            self._auto_clk.press_button('送出')
                            self._auto_clk.press_button('關閉')

                            self._auto_clk.press_button('申請')
                            self._auto_clk.select_time(clkin=False, y=t[0], m=t[1], d=t[2])
                            self._auto_clk.press_button('送出')
                            self._auto_clk.press_button('關閉')          
              except Exception as e:
                     self.logger.error(f"during clock in/out process: {e}")
                     return
              messagebox.showinfo('打卡完成!', '已完成打卡')
              self.date_list = []
              self.logger.info("[Done] clockin/out all the dates")

       def login(self):
              comp = self.compid.get()
              user = self.userid.get()
              pwd = self.userpwd.get()
              if comp != "qd9323":
                     messagebox.showinfo("Warning","公司代號輸入有誤, 應為qd9323")
              elif len(user) != 6:
                     messagebox.showinfo("Warning","個人工號長度輸入有誤, 長度應為6")
              elif len(pwd) < 1:
                     messagebox.showinfo("Warning","密碼不可為空")
              else:
                     if self._auto_clk.login(credentials=[comp,user,pwd]):
                            self.label_conn_status.config(text = "Connected", bg='green')
                            self.login_page.destroy()
                            self._cred_rw_tool.write_ini(user,pwd)
                            self.logger.info("[Done] login to Aurora ERP system")

if __name__ == "__main__":
       ui_user = UIClock()   