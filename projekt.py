from tkinter import *
from tkinter.ttk import *
from os import *
from os.path import *
from shutil import *
from papier import *

del globals()['open']

def bind(widget, event):
    def decorator(func):
        widget.bind(event, func)
        return func
    return decorator

class Okno(object):
    def __init__(self):
        self.okno = Tk()
        self.okno.title('RP (1) (c) Krajčovič')
        self.okno_x = 600
        self.okno_y = 613
        self.okno.minsize(height = 600, width = 613)
        self.okno.geometry(str(self.okno_x)+ "x" + str(self.okno_y))
        self.okno.resizable(0,1)
        obrazok_pozadia = PhotoImage(file = 'asd.png')
        pozadie = Label(self.okno, image = obrazok_pozadia)
        pozadie.place(x=0, y=0, relwidth=1, relheight=1)
        
        ## buttony
        self.buttony = []
        self.premenuj = Button(self.okno, command = self.rename, width = 25, text = 'Premenuj')
        self.zapamataj = Button(self.okno, command = self.zapamataj, width = 25, text = 'Zapamätaj')
        najdi = Button(self.okno, command = self.najdi, width = 50, text = 'Nájdi')
        self.reset = Button(self.okno, command = self.reset_metoda, width = 50, text = 'Reset', state = DISABLED)
        self.pridaj_entry = Button(self.okno, command = self.pridaj_entry_metoda, width = 4, text = ' + ', state = DISABLED)
        najdi.place(x = 265, y = 225)
        self.reset.place(x = 265, y = 200)
        self.pridaj_entry.place(x = 207, y = 120)
        self.buttony.extend([self.premenuj, self.zapamataj, najdi, self.pridaj_entry, self.reset])

        ## entries
        self.uz_navyse = False
        self.ent_y = 175
        self.navyse_entries = list()
        self.entries = []
        self.meno = Entry(self.okno, width = 30)
        self.rc_ico = Entry(self.okno, width = 30)
        self.cislo_entry_sv = StringVar()
        self.cislo_entry = Entry(self.okno, width = 30, textvariable = self.cislo_entry_sv, state = DISABLED)
        self.meno.place(x = 20, y = 30)
        self.rc_ico.place(x = 20, y = 85)
        self.cislo_entry.place(x = 20, y = 140)
        self.entries.extend([self.meno, self.rc_ico, self.cislo_entry])
        
        ## radiobuttony
        self.radia = []
        self.var = IntVar()
        WK = Radiobutton(self.okno, value = 1, variable = self.var, width = 20, text = "WK", command = self.radio_callback)
        PREVOD = Radiobutton(self.okno, value = 2, variable = self.var, width = 20, text = "PREVOD", command = self.radio_callback, state = DISABLED)
        OP = Radiobutton(self.okno, value = 3, variable = self.var, width = 20, text = "OP", command = self.radio_callback, state = DISABLED)
        TP = Radiobutton(self.okno, value = 4, variable = self.var, width = 20, text = "TP", command = self.radio_callback, state = DISABLED)
        PZ = Radiobutton(self.okno, value = 5, variable = self.var, width = 20, text = "PZ", command = self.radio_callback, state = DISABLED)
        CP = Radiobutton(self.okno, value = 6, variable = self.var, width = 20, text = "CP", command = self.radio_callback, state = DISABLED)
        VP = Radiobutton(self.okno, value = 7, variable = self.var, width = 20, text = "VP", command = self.radio_callback, state = DISABLED)
        EXC = Radiobutton(self.okno, value = 8, variable = self.var, width = 20, text = "EXC", command = self.radio_callback, state = DISABLED)
        WH = Radiobutton(self.okno, value = 9, variable = self.var, width = 20, text = "WH", command = self.radio_callback, state = DISABLED)
        self.radia.extend([WK, PREVOD, OP, TP, PZ, CP, VP, EXC, WH])
        r_x = 265
        r_x1 = 442
        WK.place(x = r_x, y = 9)
        PREVOD.place(x = r_x, y = 34)
        OP.place(x = r_x, y = 59)
        TP.place(x = r_x, y = 84)
        PZ.place(x = r_x, y = 109)
        CP.place(x = r_x1, y = 9)
        VP.place(x = r_x1, y = 34)
        EXC.place(x = r_x1, y = 59)
        WH.place(x = r_x1, y = 84)

        ## labely
        self.labely = []
        meno_label = Label(self.okno, text = 'Meno')
        rcICO_label = Label(self.okno, text = 'Rodné číslo/IČO')
        cisloENTRY_label = Label(self.okno, text = 'Číslo PZ/prevodu')
        meno_label.place(x = 21, y = 9, width = 183)
        rcICO_label.place(x = 21, y = 64, width = 183)
        cisloENTRY_label.place(x = 21, y = 119, width = 183)
        self.labely.extend([meno_label, rcICO_label])

        ## listbox + scrollbar
        l_x = r_x
        listbox_frame = Frame(self.okno)
        listbox_frame.place(x = l_x, y = 250)
        self.listbox = Listbox(listbox_frame, selectmode = SINGLE, height = 15, width = 51)
        self.scrollbar = Scrollbar(listbox_frame, takefocus = 0, command = self.listbox.yview)
        self.listbox['yscrollcommand'] = self.scrollbar.set          

        ## stavovy LABEL
        self.stav = StringVar()
        self.stav.set('Začnite kliknutím na "Nájdi".')
        self.stavovy = Label(self.okno, textvariable = self.stav)
        self.stavovy.pack(fill = 'both', side = 'bottom')

        self.meno.focus_set()
        self.odrb = True
        WK.invoke()
        self.subory = list()
        self.last_index = 0
        self.odrb = True
                
        tf = open('config.txt', 'r')
        self.konfiguracia = tf.readline()         
        tf.close()

        @bind(self.listbox, '<<ListboxSelect>>')
        def onselect(evt):
            w = evt.widget
            index = int(self.listbox.curselection()[0])
            subor = w.get(index)
            #print('You selected item %d: "%s"' % (index, subor))
            if self.subory[index].typ != 'PREVOD' and self.subory[index].typ != 'PZ' and self.subory[index].typ != 'WH':
                self.cislo_entry['state'] = DISABLED
                self.pridaj_entry['state'] = DISABLED
                self.cislo_entry_sv.set('')
                self.zmaz_entries()
            else:
                self.cislo_entry['state'] = NORMAL
                self.pridaj_entry['state'] = NORMAL
            if self.subory[index].typ == 'WK':
                self.odrb = True
                WK.invoke()
            elif self.subory[index].typ == 'PREVOD':
                self.odrb = True
                PREVOD.invoke()                
            elif self.subory[index].typ == 'OP':
                self.odrb = True
                OP.invoke()
            elif self.subory[index].typ == 'TP':
                self.odrb = True
                TP.invoke()
            elif self.subory[index].typ == 'PZ':
                self.odrb = True
                PZ.invoke()
            elif self.subory[index].typ == 'CP':
                self.odrb = True
                CP.invoke()
            elif self.subory[index].typ == 'VP':
                self.odrb = True
                VP.invoke()
            elif self.subory[index].typ == 'EXC':
                self.odrb = True
                EXC.invoke()
            elif self.subory[index].typ == 'WH':
                self.odrb = True
                WH.invoke()

        ## posledny riadok
        self.okno.mainloop()
     
    def radio_value(self):
        return self.var.get()
    
    def kladna_hlaska(self, string):
        self.stav.set(string)
       # self.stavovy['fg'] = 'green'

    def zaporna_hlaska(self, string):
        self.stav.set(string)
        #self.stavovy['fg'] = 'red'

    def neutralna_hlaska(self, string):
        self.stav.set(string)
       # self.stavovy['fg'] = 'black'
       
    def vypni_widgety(self):
        for button in self.buttony:
            button['state'] = DISABLED
        for entry in self.entries:
            entry['state'] = DISABLED
        for radio in self.radia:
            radio['state'] = DISABLED

    def zapni_widgety(self):
        for button in self.buttony:
            button['state'] = NORMAL
        for entry in self.entries:
            entry['state'] = NORMAL
        for radio in self.radia:
            radio['state'] = NORMAL

    def reset_metoda(self):
        for i in range(len(self.subory)):
            self.subory.pop()
        self.najdi()
    
    def najdi(self):
        self.listbox_update()
        if self.konfiguracia == '0':
            directory = filedialog.askdirectory()
            self.directory = directory.replace('/', chr(92))
            self.directory.strip()
            pot_directory = self.directory
            if self.directory == '' or pot_directory == '':
                self.zaporna_hlaska('Nezadali ste cestu k priečinku. Prosím skúste znova.')
                return
            tf = open('config.txt', 'w')
            tf.write('1\n')
            tf.write(self.directory)
            tf.close()
        else:
            tf = open('config.txt', 'r')
            tf.readline()
            self.directory = tf.readline()
            tf.close()
        self.neutralna_hlaska(self.directory)
        self.nacitaj_subory(self.directory)
        self.scrollbar.pack(side = RIGHT, fill = Y)
        self.listbox.pack()
        self.premenuj.place(x = 425, y = 495)
        self.zapamataj.place(x = 265, y = 495)
        self.reset['state'] = NORMAL
        for radio in self.radia:
            radio['state'] = NORMAL
        

    def entry_creation(self):
        next_entry = Entry(self.okno, width = 30)
        next_entry.place(x = 20, y = self.ent_y)
        self.navyse_entries.append(next_entry)

    def pridaj_entry_metoda(self):            
        if  not self.uz_navyse:
            self.entry_creation() 
            self.uz_navyse = True
            self.ent_y += 35
            self.kladna_hlaska('Entry pridaný úspešne.')
            self.navyse_entries[0].focus_set()
            return
        if self.navyse_entries != []:
            if self.ent_y > 550:
                self.okno_y += 35
                self.okno.geometry(str(self.okno_x)+ "x" + str(self.okno_y))
                self.okno.minsize(height = self.okno_y, width = 613)
                self.entry_creation() 
                self.ent_y += 35
                self.kladna_hlaska('Entry pridaný úspešne.')
                return
            self.entry_creation() 
            self.ent_y += 35
            self.kladna_hlaska('Entry pridaný úspešne.')
        self.navyse_entries[-1].focus_set()

    def zmaz_entries(self):
        for entry in self.navyse_entries:
            entry.place_forget()
            del entry
            self.ent_y = 175
            self.uz_navyse = False
            self.okno_y = 613
            self.okno.geometry(str(self.okno_x)+ "x" + str(self.okno_y))
            self.okno.minsize(height = 600, width = 613)

    def nacitaj_subory(self, path):
        for subor in listdir(path):
            if isfile(join(path, subor)):
                if subor.startswith('00'):
                    if 'txt' not in join(path, subor):
                        pass
                    else:
                        self.subory.append(Papier(subor, self.var.get(), join(path, subor)))
        self.listbox_update()

    def radio_callback(self):
        #metoda ktora sa aktivuje pri kliknuti na radiobutton 1 8
        if self.odrb == True:
            self.odrb = False
            return
        else:
            if self.listbox.size() == 0:
                return
            index = (''.join(str(i) for i in self.listbox.curselection()))
            if index == '':
                index = self.last_index
            self.last_index = index
            if self.radio_value() == 1 or self.radio_value() == 8:
                print(self.subory[int(index)].typ)
                self.pridaj_entry['state'] == DISABLED
            else:
                self.pridaj_entry['state'] == NORMAL
            for i in range(len(self.subory)):
                if int(index) == i:
                    self.subory[i].typ_update(self.radio_value())
            self.listbox_update()
            self.listbox.focus_set()
            self.listbox.activate(index)
            

    def listbox_update(self):
        self.listbox.delete(0, END)
        for i in range(len(self.subory)):
            self.listbox.insert(i, self.subory[i])

    def rename(self):
        if self.listbox.size() == 0:
            self.zaporna_hlaska('Prosím vyberte súbory.')
            return
        for subor in range(len(self.subory)):
            if (self.subory[subor].typ == 'PREVOD' and self.subory[subor].cisla == []) or (self.subory[subor].typ == 'PZ' and self.subory[subor].cisla == []):
                self.zaporna_hlaska('PREVOD alebo PZ nemajú uložené čísla, doplňťe ich, alebo zmenťe typ súboru.')
                return
        appdata_loc = str(getenv('APPDATA'))
        appdata_loc += '\SFMtemp'
        if not exists(appdata_loc):
            makedirs(appdata_loc)
        last_wk = 0
        last_exc = 0
        last_wh = 0
        last_pz = 0
        last_op = 0
        last_tp = 0
        last_cp = 0
        last_vp = 0
        #WK, PREVOD, OP, TP, PZ, CP, VP, EXC, WH
        for i in range(len(self.subory)):
            meno = self.meno.get().replace(' ', '_')
            if self.subory[i].typ == 'WK':                  
                novy_nazov = self.rc_ico.get() + '_' + self.subory[i].typ + '_' + meno + ' (' + str(last_wk+1) + ')' + '.txt'
                last_wk+=1
                rename(self.subory[i].cesta, join(self.directory, novy_nazov))
                continue
            if self.subory[i].typ == 'PREVOD':
                for j in range(len(self.subory[i].cisla)):
                    copy2(self.subory[i].cesta, appdata_loc)
                    novy_nazov = self.rc_ico.get() + '_' + self.subory[i].typ + '_' + list(self.subory[i].cisla)[j]+ '_' + meno + '.txt'
                    rename(join(appdata_loc, self.subory[i].nazov), join(appdata_loc, novy_nazov))
                    copy2(join(appdata_loc, novy_nazov), self.directory)
                remove(self.subory[i].cesta)
                for subor in listdir(appdata_loc):
                    if isfile(join(appdata_loc, subor)):
                        remove(join(appdata_loc, subor))
                continue
            if self.subory[i].typ == 'OP' or self.subory[i].typ == 'TP' or self.subory[i].typ == 'CP' or self.subory[i].typ == 'VP':
                if self.subory[i].typ == 'OP':
                    novy_nazov = self.rc_ico.get() + '_' + self.subory[i].typ + '_' + list(self.subory[i].cisla)[0] + '_'+ meno+ ' ('+ str(last_op+1) +')'+ '.txt'
                    last_op+=1
                elif self.subory[i].typ == 'TP':
                    novy_nazov = self.rc_ico.get() + '_' + self.subory[i].typ + '_' + list(self.subory[i].cisla)[0] + '_'+ meno+ ' ('+ str(last_tp+1) +')'+ '.txt'
                    last_tp+=1
                elif self.subory[i].typ == 'CP':
                    novy_nazov = self.rc_ico.get() + '_' + self.subory[i].typ + '_' + list(self.subory[i].cisla)[0] + '_'+ meno+ ' ('+ str(last_cp+1) +')'+ '.txt'
                    last_cp+=1
                elif self.subory[i].typ == 'VP':
                    novy_nazov = self.rc_ico.get() + '_' + self.subory[i].typ + '_' + list(self.subory[i].cisla)[0] + '_'+ meno+ ' ('+ str(last_vp+1) +')'+ '.txt'
                    last_vp+=1
                rename(self.subory[i].cesta, join(self.directory, novy_nazov))
                continue
            if self.subory[i].typ == 'PZ':
                for j in range(len(self.subory[i].cisla)):
                    copy2(self.subory[i].cesta, appdata_loc)
                    novy_nazov = self.rc_ico.get() + '_' + self.subory[i].typ + '_' + list(self.subory[i].cisla)[j]+ '_' + meno + ' (' + str(last_pz+1) + ')'+ '.txt'
                    rename(join(appdata_loc, self.subory[i].nazov), join(appdata_loc, novy_nazov))
                    copy2(join(appdata_loc, novy_nazov), self.directory)
                    last_pz+=1
                remove(self.subory[i].cesta)
                for subor in listdir(appdata_loc):
                    if isfile(join(appdata_loc, subor)):
                        remove(join(appdata_loc, subor))
                continue
            if self.subory[i].typ == 'EXC':                  
                novy_nazov = self.rc_ico.get() + '_' + self.subory[i].typ + '_' + meno + ' (' + str(last_exc+1) + ')' + '.txt'
                last_exc+=1
                rename(self.subory[i].cesta, join(self.directory, novy_nazov))
                continue
            if self.subory[i].typ == 'WH':
                if len(self.subory[i].cisla) == 0:
                    novy_nazov = self.rc_ico.get() + '_' + self.subory[i].typ + '_' + meno + ' (' + str(last_wh+1) + ')' + '.txt'
                    last_wh+=1
                    rename(self.subory[i].cesta, join(self.directory, novy_nazov))
                else:
                    for j in range(len(self.subory[i].cisla)):
                        novy_nazov = self.rc_ico.get() + '_' + self.subory[i].typ + '_' + meno + ' (' + str(last_wh+1) + ')' + '.txt'
                        last_wh+=1
                        rename(self.subory[i].cesta, join(self.directory, novy_nazov))
                continue
        for i in range(len(self.subory)):
            self.subory.pop()
        self.kladna_hlaska('Úspešne premenované.')
        self.reset_metoda()

    def zapamataj(self):
        if self.listbox.size() == 0:
            self.zaporna_hlaska('Prosím vyberte súbory.')
            return
        if self.listbox.curselection == ():
            self.zaporna_hlaska('Prosím vyberte do ktorého súboru sa majú čísla uložiť.')
            return
        for i in range(len(self.subory)):
            for j in range(len(self.subory[i].cisla)):
                if self.cislo_entry.get() == self.subory[i].cisla[j]:
                    self.zaporna_hlaska('Číslo PZ/PREVODU už sa nachádza v inej zmluve.')
                    return
                for k in range(len(self.navyse_entries)):
                    if self.navyse_entries[k].get() == self.subory[i].cisla[j]:
                        self.zaporna_hlaska('Číslo PZ/PREVODU už sa nachádza v inej zmluve.')
                        return
        cisla = []
        for entry in self.navyse_entries:
            cisla.append(entry.get())
        for i in range(len(self.subory)):
            if i == self.listbox.curselection()[0]:
                self.subory[i].pridaj_cisla(self.cislo_entry.get())
                self.subory[i].pridaj_cisla(cisla)
        self.zmaz_entries()
        for i in range(len(self.navyse_entries)):
            self.navyse_entries.pop()
        self.cislo_entry_sv.set('')
        self.listbox_update()
        self.kladna_hlaska('Úspešne zapamätané')

o = Okno()
