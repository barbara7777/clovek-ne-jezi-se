from tkinter import *
from random import randint
import tkinter.messagebox
import time

class UI: #user interface

    def __init__(self, parent):
        self.okno = Tk()
        self.levi_del = Frame(self.okno)
        self.desni_del = Frame(self.okno)
        self.okno.title("IGRA")
        self.levi_del.grid(row=0, column=0)
        self.desni_del.grid(row=0, column=1)
        self.parent = parent

        self.gumbi = []
        self.polozajiGumbov = {}

        self.ustvari_gumbe()
        #self.okno.mainloop() more bit poklicano globalno ☺
        #nastavi gumbe      

        self.cas = Label(self.desni_del, bg='grey', text='Čas igre\n0', font=('Courier, 20'))
        self.cas.grid(row=0, column=0)

    def ustvari_gumbe(self):
        for i in range(15):
            self.gumbi.append(Button(self.levi_del, command=lambda st=i+1: self.pritisnjen_gumb(st), text=str(i+1),width=3, height=1, bg='light blue', font=('Courier, 50')))
    
    def pritisnjen_gumb(self, stevilka):
        polje = self.polozajiGumbov[stevilka]
        self.parent.prestavi(polje)

    def nastavi_gumbe (self, stevilke):
        for i in range(16):
            st = stevilke[i]
            if st == 0:
                continue
            self.nastavi_polozaj(i, self.gumbi[st-1])
            self.polozajiGumbov[st] = i
      
    def nastavi_polozaj (self, polozaj, gumb):
        '''razvrsti gumbe na plosco'''
        vrstica = polozaj // 4
        stolpec = polozaj % 4
        gumb.grid(row=vrstica, column=stolpec)


def izloci_koordinate(polje):
    return (polje // 4, polje % 4)



class IGRA: #mehanika igre (vsebije UI)

    def __init__(self):
        self.stevilke = [x for x in range(16)]

        self.premiki = 0
        self.zacetni_cas = 0
        self.zacetek_igre = False  

        self.Inter = UI(self)

        self.namesaj_stevilke()
        #self.reStart()

    def namesaj_stevilke (self):
        for i in range(len(self.stevilke)):
            nakljucno_stevilo = randint(0,15)
            self.stevilke[nakljucno_stevilo], self.stevilke[i] = self.stevilke[i], self.stevilke[nakljucno_stevilo]
        self.Inter.nastavi_gumbe(self.stevilke)

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

    def prestavi(self, polje):
        x,y = izloci_koordinate(polje)
        #nastavi_cas()
        
        if y != 3 and self.stevilke[polje + 1] == 0:
            print("desno")
            #lahko premaknem v desno
            self.stevilke[polje], self.stevilke[polje+1] = self.stevilke[polje+1], self.stevilke[polje]
        elif y != 0 and self.stevilke[polje - 1] == 0:
            print("levo")
            #lahko premaknem levo
            self.stevilke[polje], self.stevilke[polje-1] = self.stevilke[polje-1], self.stevilke[polje]
        elif x != 3 and self.stevilke[polje + 4] == 0:
            print("dol")
            #lahko premaknem dol
            self.stevilke[polje], self.stevilke[polje+4] = self.stevilke[polje+4],self. stevilke[polje]
        elif x != 0 and self.stevilke[polje - 4] == 0:
            print("gor")
            #lahko premaknem gor
            self.stevilke[polje], self.stevilke[polje-4] = self.stevilke[polje-4], self.stevilke[polje]
        else:
            print("tega gumba se ne da premakniti")
            return
        #self.Inter.nastavi_gumbe(self.stevilke)
        self.igra_poteka()

    def igra_poteka(self):
        self.Inter.nastavi_gumbe(self.stevilke)
        if not self.zacetek_igre:
            self.zacetek_igre = True
            self.zacetni_cas = time.time()
            self.premiki += 1
        #izpisi stevilo potez
        

    def reStart (self):
        self.namesaj_stevilke()
 
    def cas_igre ():
        return round(time.time() - self.zacetni_cas, 2)

    def nastavi_cas():
        self.Inter.okno.after(100,nastavi_cas)
        if self.zacetek_igre:
            self.Inter.cas.configure(text="Čas igre\n{0}".format(self.cas_igre()))
        else:
            self.Inter.cas.configure(text="Čas igre\n0")



i = IGRA()
i.Inter.okno.mainloop()
