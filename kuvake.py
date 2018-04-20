'''
Tassa on luokka QLabel() muokattu siten, etta siina oleva mousePressEvent funktio
on muokattu vastaamaan ohjelma tarpeita.
'''
from PyQt5.Qt import QLabel

class Kuvake(QLabel):
    def __init__(self, peli__, x):
        super().__init__()
        self.pelitilanne = peli__
        self.nimi = ''
        
        #onko kasi vai poytakortti, 1 niin kasi, 0 niin poyta
        self.laji = x
        
    def aseta_nimi(self, nimi):
        self.nimi = nimi
        
    def nollaa_nimi(self):
        self.nimi = ''
    
    def mousePressEvent(self, *args, **kwargs):
        
        self.pelitilanne.kortin_klikkaus(self.nimi, self.laji)
        