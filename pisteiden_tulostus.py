import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtWidgets
from PyQt5.Qt import QLabel

class Pisteiden_tulostus(QWidget):
    '''Tulostaa kierroksen ja koko pelin pistetilanteet uuteen ikkunaan. Luokka
    kayttaa GridLayouttia, jotta tulostuksesta tulisi mahdollisimman kaunis.
    '''
    
    def __init__(self, pelaajat, voittaja):
        super().__init__()
        
        self.pelaajat = pelaajat
        self.voittaja = voittaja
        
        self.tulostus()
        self.show()
        
    
    
    def tulostus(self):
        
        self.vertical = QtWidgets.QVBoxLayout() # Vertical main layout
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.vertical)
        
        Alkuteksti = QLabel()
        Alkuteksti.setText('Pelaajien pisteet kierroksen paatyttya:\n(Huomaa etta ruutu-10:sta saa 2 pistetta)')
        
        self.vertical.addWidget(Alkuteksti)
        
        self.setWindowTitle('PISTEET')
            
        ##Luo ensin otsikkorivin
        l1 = QLabel()
        l1.setText('Assat')
        l2 = QLabel()
        l2.setText('Ruutu-10')
        l3 = QLabel()
        l3.setText('Pata-2')
        l4 = QLabel()
        l4.setText('Mokit')
        l5 = QLabel()
        l5.setText('Padat')
        l6 = QLabel()
        l6.setText('Kortit')
        l7 = QLabel()
        l7.setText('Kierrospisteet')
        l8 = QLabel()
        l8.setText('Yhteispisteet')
            
        self.grid.addWidget(l1,1,0)
        self.grid.addWidget(l2,2,0)
        self.grid.addWidget(l3,3,0)
        self.grid.addWidget(l4,4,0)
        self.grid.addWidget(l5,5,0)
        self.grid.addWidget(l6,6,0)
        self.grid.addWidget(l7,7,0)
        self.grid.addWidget(l8,8,0)
        
        ##Luo seuraavaksi jokaiselle pelaajalle oman pisterivin    
        for i in self.pelaajat:
            l0 = QLabel()
            l0.setText('{:s}'.format(i.nimi))
            l1 = QLabel()
            l1.setText('{:d}'.format(i.assat))
            l2 = QLabel()
            l2.setText('{:d}'.format(i.ruutu10))
            l3 = QLabel()
            l3.setText('{:d}'.format(i.pata2))
            l4 = QLabel()
            l4.setText('{:d}'.format(i.mokit))
            l5 = QLabel()
            l5.setText('{:d}'.format(i.padat))
            l6 = QLabel()
            l6.setText('{:d}'.format(len(i.otetut_kortit)))
            l7 = QLabel()
            l7.setText('{:d}'.format(i.kierpisteet))
            l8 = QLabel()
            l8.setText('{:d}'.format(i.yhtpisteet))
                
            h=i.vuoro   #maaraa korkeuden
                
            self.grid.addWidget(l0,0,h)
            self.grid.addWidget(l1,1,h)
            self.grid.addWidget(l2,2,h)
            self.grid.addWidget(l3,3,h)
            self.grid.addWidget(l4,4,h)
            self.grid.addWidget(l5,5,h)
            self.grid.addWidget(l6,6,h)
            self.grid.addWidget(l7,7,h)
            self.grid.addWidget(l8,8,h)
        
        self.vertical.addLayout(self.grid)
        
        #######
        # x on teksti joka tulee ikkunan alaosaan, kertoo pelaajan jolla eniten pisteita
        if len(self.voittaja)==1:
            x = ('\n\n{:s} johtaa!!! (Voitti jos peli paatetaan tahan.)\nJos haluat pelata seuraavan kierroksen aloita jakamalla kortit.'.format(self.voittaja[0]))
        else:
            x = '\n\n'
            for p in self.voittaja:
                x = x + str(p) + ' ja '
            x = x[:-4]
            
            x = x + ' johtavat!!! (Voittivat jos peli paatetaan tahan.)\nJos haluat pelata seuraavan kierroksen aloita jakamalla kortit'
        
        Lopputeksti = QLabel()
        Lopputeksti.setText(x)
        
        self.vertical.addWidget(Lopputeksti)
        #######
        
        self.setGeometry(700, 400, 400, 300)


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Pisteiden_tulostus()
    sys.exit(app.exec_())
    