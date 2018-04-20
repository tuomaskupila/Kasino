class Kortti():
    def __init__(self, kortti):
        '''Muuttuja 'kortti' pitaisi olla muodossa esim. clubs-10-75'''
        if len(kortti.split('-'))==3:
            kortin_tiedot = kortti.split('-')
            self.arvo = int(kortin_tiedot[1])
            self.maa = kortin_tiedot[0]
            self.kuva = kortti + '.png'
            self.kuva2 = kortti + 'hl.png'
            self.kortin_nimi = kortti
            
        else:
            return False   
    def onko_ruutu_10(self):
        
        if self.arvo == 10 and self.maa == 'diamonds':
            return True
        else:
            return False
        
    def onko_pata_2(self):
        
        if self.arvo == 2 and self.maa == 'spades':
            return True
        else:
            return False
        
    def onko_assa(self):
        if self.arvo == 1:
            return True
        else:
            return False     
        
    def anna_kortin_arvo(self):
        
        if self.arvo:
            return self.arvo
    
    def anna_kuva(self):
        
        if self.kuva:
            return self.kuva
    
    def anna_klikattu_kuva(self):
        
        if self.kuva2:
            return self.kuva2
    