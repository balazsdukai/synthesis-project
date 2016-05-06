import Tkinter
import ttkcalendar
import tkSimpleDialog
import datetime
import ttk
import Automatic_Visualization as AV


class CalendarDialog(tkSimpleDialog.Dialog):
    """Dialog box that displays a calendar and returns the selected date"""
    def body(self, master):
        self.calendar = ttkcalendar.Calendar(master)
        self.calendar.pack()

    def apply(self):
        self.result = self.calendar.selection

class checkBoxDialog(tkSimpleDialog.Dialog):
    """Dialog box that displays a checkboxes and returns the selected checkboxes"""
    def body(self, master):
        pass
        AV.cur.execute("SELECT buildingid FROM buildings")
        buildings = AV.cur.fetchall()
        temp = []
        for i,building in enumerate(buildings[:10]):
            buildings[i] = Tkinter.Variable()
            l = ttk.Checkbutton(self, text=building[0], variable=buildings[i])
            l.pack()
    def apply(self):
        pass
##        self.result = 'konijn'


class CalendarFrame(Tkinter.LabelFrame):
    def __init__(self, master):
        Tkinter.LabelFrame.__init__(self, master, text="Pick a date")
        self.dates = []
        self.mondays = []
        self.combo()
        self.combo_bld_from()
        self.combo_bld_to()
        
        def getdate():
            cd = CalendarDialog(self)
            result = cd.result
            self.dates.append(result.date())
            string = ''
            for date in self.dates:
                date = date.strftime("%Y-%m-%d")
                string += '%s, ' % (date)
            self.selected_date.set(string)
        self.selected_date = Tkinter.StringVar()
        
        Tkinter.Entry(self, textvariable=self.selected_date).pack(side=Tkinter.TOP, expand='YES')
        Tkinter.Button(self, text="1.Add dates", command=getdate).pack(side=Tkinter.TOP, expand='YES')
        Tkinter.Button(self, text="2.All days of week", command=self.getmondays).pack(side=Tkinter.TOP, expand='YES')
        Tkinter.Button(self, text="3.Run visualization", command=self.run).pack(side=Tkinter.TOP, expand='YES')
        Tkinter.Button(self, text="4.Clear dates", command=self.clear).pack(side=Tkinter.TOP, expand='YES')
        Tkinter.Button(self, text="5.Checkboxes", command=self.checkBoxes).pack(side=Tkinter.TOP, expand='YES')
        
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
        self.box.pack(side=Tkinter.TOP)

    def combo_bld_from(self):
        AV.cur.execute("SELECT buildingid FROM buildings")
        buildings = AV.cur.fetchall()
        self.bld_from_value = Tkinter.StringVar()
        self.bld_from_value.set('From which building?')
        self.bld_from_box = ttk.Combobox(self, textvariable=self.bld_from_value, state='readonly')
        temp = []
        for i in range(len(buildings)):
            temp.append(buildings[i][0])
        self.bld_from_box['values'] = temp
        self.bld_from_box.pack(side=Tkinter.BOTTOM)

    def combo_bld_to(self):
        AV.cur.execute("SELECT buildingid FROM buildings")
        buildings = AV.cur.fetchall()
        self.bld_to_value = Tkinter.StringVar()
        self.bld_to_value.set('To which building?')
        self.bld_to_box = ttk.Combobox(self, textvariable=self.bld_to_value, state='readonly')
        temp = []
        for i in range(len(buildings)):
            temp.append(buildings[i][0])
        self.bld_to_box['values'] = temp
        self.bld_to_box.pack(side=Tkinter.BOTTOM)

    def checkBoxes(self):
        cd = checkBoxDialog(self)
##        AV.cur.execute("SELECT buildingid FROM buildings")
##        buildings = AV.cur.fetchall()
##        print buildings
##        temp = []
##        for i,building in enumerate(buildings):
##            print buildings[i]
##            buildings[i] = Tkinter.Variable()
##            l = ttk.Checkbutton(self, text=building[0], variable=buildings[i])
##            l.pack()
            
        

    def getBuildings(self):
        return self.bld_from_box.get(), self.bld_to_box.get()
        
    def run(self):
        sep_dates = self.dates
        rec_dates = self.mondays
        dates = sep_dates + rec_dates
        from_bld, to_bld = self.getBuildings()
        from_bld = [from_bld]
        to_bld = [to_bld]
        var = AV.main(from_bld, to_bld, dates)

    def clear(self):
        self.dates = []
        self.mondays = []
        self.selected_date.set('')

def main():
    root = Tkinter.Tk()
    root.geometry("600x350+300+300")
    root.wm_title("Date Picker Dialog")
    CalendarFrame(root).pack()
    root.mainloop()
    

if __name__ == "__main__":
    main()
