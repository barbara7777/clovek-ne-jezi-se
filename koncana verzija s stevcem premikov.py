import tkinter as tk
from random import randint
import tkinter.messagebox
import time


class UI: #user interface

    def __init__(self, parent):
        self.okno = tk.Tk()
        self.levi_del = tk.Frame(self.okno, bg='#6790af')
        self.desni_del = tk.Frame(self.okno)
        self.okno.title("IGRA PETNAJST")
        self.levi_del.pack(side='left')
        self.desni_del.pack(fill='both', side='left')
        self.parent = parent

        self.font = ("Arial", 20)
        self.gumbi = []
        self.polozaji_gumbov = {}

        self.ustvari_gumbe()

        self.prikaz_casa = tk.Label(self.desni_del, text='Čas igre\n0', font=self.font)
        self.prikaz_casa.grid(row=0, column=0)

        self.prikaz_premikov = tk.Label(self.desni_del, text='Število premikov: ', font=", 12")
        self.prikaz_premikov.grid(row=2, column=0, ipady=10)

        self.restart_tipka = tk.Button(self.desni_del, bg='grey', text='Premešaj', command=self.parent.restart, font=self.font, fg='white' )
        self.restart_tipka.grid(row=1, column=0, padx=10)

    def ustvari_gumbe(self):
        for i in range(15):
            self.gumbi.append(tk.Button(self.levi_del, command=lambda st=i+1: self.pritisnjen_gumb(st), text=str(i+1),width=3, height=1, bg='light blue', font=("Arial", 50)))
    
    def pritisnjen_gumb(self, stevilka):
        polje = self.polozaji_gumbov[stevilka]
        self.parent.prestavi(polje)

    def nastavi_gumbe(self, stevilke):
        for i in range(16):
            st = stevilke[i]
            if st == 0:
                continue
            self.nastavi_polozaj_gumba(i, self.gumbi[st-1])
            self.polozaji_gumbov[st] = i
      
    def nastavi_polozaj_gumba(self, polozaj, gumb):
        '''razvrsti gumbe na plosco'''
        vrstica = polozaj // 4
        stolpec = polozaj % 4
        gumb.grid(row=vrstica, column=stolpec)

    def posodobitev_casa(self):

        if(self.parent.zacetek_igre):
            self.okno.after(100, self.posodobitev_casa)

        self.cas = round(time.time() - self.parent.zacetni_cas)
        self.prikaz_casa.configure(text="Čas igre\n{0}".format(self.cas))

    def okno_zmage(self):
        tk.messagebox.showinfo('igra je koncana', 'ODLIČNO!\n Čas igre: {0}\n Število premikov: {1}'.format(self.cas, self.parent.premiki))


class IGRA: #mehanika igre (vsebije GUI)

    def __init__(self):
        self.stevilke = [x for x in range(16)]  
        self.GUI = UI(self)

        self.restart()

    def restart(self):
        self.premiki = 0
        self.zacetni_cas = time.time()
        self.zacetek_igre = False
        self.namesaj_stevilke()
        self.GUI.posodobitev_casa()

    def namesaj_stevilke(self):
        for i in range(len(self.stevilke)):
            nakljucno_stevilo = randint(0,15)
            self.stevilke[nakljucno_stevilo], self.stevilke[i] = self.stevilke[i], self.stevilke[nakljucno_stevilo]
        self.GUI.nastavi_gumbe(self.stevilke)

    def izloci_koordinate(self, polje):
        return (polje // 4, polje % 4)

    def preveri(self):
        n = 0
        for i in self.stevilke:
            if i == 0:
                continue
            elif i > n:
                n = i
            else:
                return False
        return True

    def posodobi_premike(self):
        self.GUI.prikaz_premikov.configure(text='Število premikov: {}'.format(self.premiki))


    def prestavi(self, polje):
        x,y = self.izloci_koordinate(polje)
        if y != 3 and self.stevilke[polje + 1] == 0:
            print("desno")
            self.stevilke[polje], self.stevilke[polje+1] = self.stevilke[polje+1], self.stevilke[polje]
        elif y != 0 and self.stevilke[polje - 1] == 0:
            print("levo")
            self.stevilke[polje], self.stevilke[polje-1] = self.stevilke[polje-1], self.stevilke[polje]
        elif x != 3 and self.stevilke[polje + 4] == 0:
            print("dol")
            self.stevilke[polje], self.stevilke[polje+4] = self.stevilke[polje+4],self. stevilke[polje]
        elif x != 0 and self.stevilke[polje - 4] == 0:
            print("gor")
            self.stevilke[polje], self.stevilke[polje-4] = self.stevilke[polje-4], self.stevilke[polje]
        else:
            print("tega gumba se ne da premakniti")
            return

        #nastavimo gumbe na njihove polozaje
        self.GUI.nastavi_gumbe(self.stevilke)

        if not self.zacetek_igre:
            self.zacetek_igre = True
            self.zacetni_cas = time.time()
            self.GUI.posodobitev_casa()
        
        self.premiki += 1
        self.posodobi_premike()

        if self.preveri():
            #smo zmagali!
            self.zacetek_igre = False
            self.GUI.okno_zmage()
            self.restart()


igra = IGRA()
igra.GUI.okno.mainloop()