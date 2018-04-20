'''Ihmis- ja tietokonepelaaja -luokka'''

class Pelaaja():
    '''Ihmis- ja tietokonepelaaja -luokka'''

    def __init__(self, nimi):
        self.kasi = []
        self.yhtpisteet = 0
        self.kierpisteet = 0
        self.nimi = nimi
        self.vuoro = None
        self.otetut_kortit = []
        self.mokit = 0
        self.padat = 0
        self.assat = 0
        self.ruutu10 = 0
        self.pata2 = 0
        
        
        self.set_brain()
    
    def set_brain(self):
        if self.nimi[:-1] == 'Tietokonepelaaja':
            self.brain = 'Bot'
        
        else:
            self.brain = 'Human'
            
    def get_brain(self):
        
        if self.brain:
            return self.brain
        
    #def pelaa_vuoro(self):
        
        
        