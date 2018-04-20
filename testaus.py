import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtWidgets
from PyQt5.Qt import QLabel, QMessageBox


class Pelaaja():
    def __init__(self,nimi,vuoro,assat,ruutu10,pata2,mokit,padat,kortit,kierpisteet, yhtpisteet):
        self.vuoro = vuoro
        self.nimi = nimi
        self.assat = assat 
        self.ruutu10 = ruutu10
        self.pata2 = pata2
        self.mokit = mokit
        self.padat = padat
        self.kortit = kortit
        self.kierpisteet = kierpisteet
        self.yhtpisteet = yhtpisteet

class piste_ikkuna(QWidget):
    def __init__(self):
        super().__init__()
        self.tulostus()
        self.show()
    
    def tulostus(self):
        pelaajat = []
        pelaaja1 = Pelaaja('Pelaaja1',1,1,1,0,2,15,27,7,12)
        pelaaja2 = Pelaaja('Pelaaja2',2,3,0,1,1,2,27,4,5)
        pelaajat.append(pelaaja1)
        pelaajat.append(pelaaja2)
        
        self.vertical = QtWidgets.QVBoxLayout() # Vertical main layout
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.vertical)
        
        Alkuteksti = QLabel()
        Alkuteksti.setText('Seuraavaksi saadaan pelaajien pisteet:')
        
        self.vertical.addWidget(Alkuteksti)
        
        self.setWindowTitle('PISTEET')
            
        l1 = QLabel()
        l1.setText('Assat')
        l2 = QLabel()
        l2.setText('kpl Ruutu-10')
        l3 = QLabel()
        l3.setText('kpl Pata-2')
        l4 = QLabel()
        l4.setText('mokit')
        l5 = QLabel()
        l5.setText('padat')
        l6 = QLabel()
        l6.setText('kortit')
        l7 = QLabel()
        l7.setText('kierrospisteet')
        l8 = QLabel()
        l8.setText('yhteispisteet')
            
        self.grid.addWidget(l1,1,0)
        self.grid.addWidget(l2,2,0)
        self.grid.addWidget(l3,3,0)
        self.grid.addWidget(l4,4,0)
        self.grid.addWidget(l5,5,0)
        self.grid.addWidget(l6,6,0)
        self.grid.addWidget(l7,7,0)
        self.grid.addWidget(l8,8,0)
            
        for i in pelaajat:
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
            l6.setText('{:d}'.format(i.kortit))
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

        self.setGeometry(800, 400, 400, 300)
    
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = piste_ikkuna()
    sys.exit(app.exec_()) 


    