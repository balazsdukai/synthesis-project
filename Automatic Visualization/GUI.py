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
        ## Query database
        AV.cur.execute("SELECT id FROM buildings_new")
        self.buildings = AV.cur.fetchall()
        self.buildinglist = self.buildings[:]
        AV.cur.execute("SELECT name FROM buildings_new")
        self.bld_names = AV.cur.fetchall()
        
        ## Create Frames
        top = Tkinter.Frame(self)
        bottom = Tkinter.Frame(self)
        top.pack(side=Tkinter.LEFT, anchor='w')
        bottom.pack(side=Tkinter.LEFT, anchor='e', fill=Tkinter.BOTH, expand=True)

        ## Select All checkbox
        self.var = Tkinter.IntVar()
        sel_all = Tkinter.Checkbutton(self, text='Select All', variable=self.var)
        sel_all.pack(side=Tkinter.LEFT, anchor='e')
        
        ## Create checkboxes 1st column
        self.vara = []
        for x in range(len(self.buildings[:16])):
            self.vara.append([])
        for i,building in enumerate(self.buildings[:16]):
            self.vara[i] = Tkinter.IntVar()
            chka = Tkinter.Checkbutton(self, text=self.bld_names[i][0], variable=self.vara[i])
            chka.pack(in_=top, side = Tkinter.TOP, anchor='w')

        ## Create checkboxes 2nd column
        self.varb = []
        for x in range(len(self.buildings[16:])):
            self.varb.append([])
        for j,building in enumerate(self.buildings[16:]):
            self.varb[j] = Tkinter.IntVar()
            chkb = Tkinter.Checkbutton(self, text=self.bld_names[j+16][0], variable=self.varb[j])
            chkb.pack(in_=bottom, side = Tkinter.TOP, anchor='w')
            
        
        
    def apply(self):
        self.selected_buildings = []
        for i in range(len(self.buildings[:16])):
            if self.vara[i].get() == 1:
                self.selected_buildings.append(self.buildings[i][0])
        for j in range(len(self.buildings[16:])):
            if self.varb[j].get() == 1:
                self.selected_buildings.append(self.buildings[16+j][0])
                print self.buildings[16+j][0]
                if self.buildings[16+j][0] == 62:
                    self.selected_buildings.append(61)
        self.result = self.selected_buildings
        print self.result
        if self.var.get() == 1:
            self.result = []
            for item in self.buildings:
                self.result.append(item[0])
            return self.result
        else:
            return self.result


class CalendarFrame(Tkinter.LabelFrame):
    def __init__(self, master):
        Tkinter.LabelFrame.__init__(self, master, text="What do you want to know?")
        self.dates = []
        self.days = []
        self.combo()
        self.bld_from = []
        self.bld_to = []
        
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

        ## Buttons and stuff
        Tkinter.Entry(self, textvariable=self.selected_date).pack(side=Tkinter.TOP, expand=True)
        Tkinter.Button(self, text="1.Add dates", command=getdate).pack(side=Tkinter.TOP, anchor='w')
        Tkinter.Button(self, text="2.All days of week", command=self.getdays).pack(side=Tkinter.TOP, anchor='w')
        Tkinter.Button(self, text="3.From which buildings?", command=self.fromBld).pack(side=Tkinter.TOP, anchor='w')
        Tkinter.Button(self, text="4.To which buildings?", command=self.toBld).pack(side=Tkinter.TOP, anchor='w')
        Tkinter.Button(self, text="5.Run visualization", command=self.run).pack(side=Tkinter.TOP, anchor='w')
        Tkinter.Button(self, text="6.Clear dates", command=self.clear).pack(side=Tkinter.TOP, anchor='w')

        
    def getdays(self):
        now = datetime.datetime.now().date()
        begin = datetime.datetime(2016,3,31).date()
        dayspassed = (now - begin).days
        for i in range(dayspassed/6):
            j = int(self.box.get()[0])
            dayofweek = datetime.timedelta(j,0,0)
            next_mon = begin + dayofweek + datetime.timedelta(7*i,0,0)
            if next_mon < now:
                self.days.append(next_mon)
        
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

    def toBld(self):
        cd = checkBoxDialog(self)
        result = cd.result
        self.bld_to = result

    def fromBld(self):
        cd = checkBoxDialog(self)
        result = cd.result
        self.bld_from = result
        
    def run(self):
        sep_dates = self.dates
        rec_dates = self.days
        dates = sep_dates + rec_dates
        barplot = AV.main(self.bld_from, self.bld_to, dates)

    def clear(self):
        self.dates = []
        self.mondays = []
        self.selected_date.set('')

def main():
    root = Tkinter.Tk()
    root.geometry("210x250+400+200")
    root.wm_title("Date Picker Dialog")
    CalendarFrame(root).pack()
    root.mainloop()
    

if __name__ == "__main__":
    main()
