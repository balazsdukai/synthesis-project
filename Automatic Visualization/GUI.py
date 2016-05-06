import Tkinter
import ttkcalendar
import tkSimpleDialog
import datetime
import ttk
import test
#import Automatic_Visualization as AV


class CalendarDialog(tkSimpleDialog.Dialog):
    """Dialog box that displays a calendar and returns the selected date"""
    def body(self, master):
        self.calendar = ttkcalendar.Calendar(master)
        self.calendar.pack()

    def apply(self):
        self.result = self.calendar.selection

class CalendarFrame(Tkinter.LabelFrame):
    def __init__(self, master):
        Tkinter.LabelFrame.__init__(self, master, text="Pick a date")
        self.dates = []
        self.mondays = []
        self.combo()
        
        def getdate():
            cd = CalendarDialog(self)
            result = cd.result
            self.dates.append(result)
            string = ''
            for date in self.dates:
                date = date.strftime("%Y-%m-%d")
                string += '%s, ' % (date)
            self.selected_date.set(string)
        self.selected_date = Tkinter.StringVar()
        
        Tkinter.Entry(self, textvariable=self.selected_date).pack(side=Tkinter.LEFT)
        Tkinter.Button(self, text="1.Add dates", command=getdate).pack(side=Tkinter.LEFT)
        Tkinter.Button(self, text="2.All days of week", command=self.getmondays).pack(side=Tkinter.RIGHT)
        Tkinter.Button(self, text="3.Run visualization", command=self.run).pack(side=Tkinter.LEFT)
        Tkinter.Button(self, text="4.Clear dates", command=self.clear).pack(side=Tkinter.LEFT)
        
    def getmondays(self):
        now = datetime.datetime.now().date()
        begin = datetime.datetime(2016,3,31).date()
        dayspassed = (now - begin).days
        for i in range(dayspassed/6):
            j = int(self.box.get()[0])
            dayofweek = datetime.timedelta(j,0,0)
            next_mon = begin + dayofweek + datetime.timedelta(7*i,0,0)
            if next_mon < now:
                self.mondays.append(next_mon)
        
    def combo(self):
        self.box_value = Tkinter.StringVar()
        self.box_value.set('Pick a day')
        self.box = ttk.Combobox(self, textvariable=self.box_value, state='readonly')
        self.box['values'] = ((4,'Monday'),
                                       (5,'Tuesday'),
                                       (6,'Wednesday'),
                                       (0,'Thursday'),
                                       (1,'Friday'),
                                       (2,'Saturday'),
                                       (3,'Sunday'))
        self.box.pack(side=Tkinter.RIGHT)

    def run(self):
        sep_dates = self.dates
        rec_dates = self.mondays
        dates = sep_dates + rec_dates
        #print 'dates',dates
        var = test.myfunc(dates)

    def clear(self):
        self.dates = []

def main():
    root = Tkinter.Tk()
    root.wm_title("Date Picker Dialog")
    CalendarFrame(root).pack()
    root.mainloop()
    

if __name__ == "__main__":
    main()
