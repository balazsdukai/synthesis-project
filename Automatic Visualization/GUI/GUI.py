import Tkinter
import ttkcalendar
import tkSimpleDialog
import datetime


class CalendarDialog(tkSimpleDialog.Dialog):
    """Dialog box that displays a calendar and returns the selected date"""
    def body(self, master):
        self.calendar = ttkcalendar.Calendar(master)
        self.calendar.pack()

    def apply(self):
        self.result = self.calendar.selection
        
        ## Insert our module here to use it for the dates
        ## var= {module}.function(self.result)

# Demo code:


class CalendarFrame(Tkinter.LabelFrame):
    def __init__(self, master):
        Tkinter.LabelFrame.__init__(self, master, text="Pick a date")
        self.dates = []
        
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
        Tkinter.Button(self, text="Add dates", command=getdate).pack(side=Tkinter.LEFT)

        def getmondays():
            now = datetime.datetime.now().date()
            begin = datetime.datetime(2016,3,31).date()
            mondays = []
            dayspassed = (now - begin).days
            for i in range(dayspassed/6):
                dayofweek = datetime.timedelta(i,0,0).days
                print dayofweek
                next_mon = begin + datetime.timedelta(7*i,0,0)
                if next_mon < now:
                    mondays.append(next_mon)

            print mondays

        Tkinter.Button(self, text="All mondays", command=getmondays).pack(side=Tkinter.BOTTOM)

def main():
    root = Tkinter.Tk()
    root.wm_title("Date Picker Dialog")
    CalendarFrame(root).pack()
    root.mainloop()
    

if __name__ == "__main__":
    main()
