import random
from kortti import Kortti
from pelaaja import Pelaaja
from vuoro import tarkasta_kortit
from PyQt5.QtWidgets import QMessageBox
from pisteiden_tulostus import Pisteiden_tulostus


class Pelitilanne:
    '''Tama luokka kuvaa pelitilannetta, johon sisaltyy
    pelaajat, heidan kortit, pisteet ja pakka. Tama luokka kayttaa
    erillista vuoro-funktiota vuoron pelaamiseen. kayttoliittyma kuvantaa
    aina yhta Pelitilanne oliota.'''
    
    def __init__(self, pelaajien_nimet):
        '''Luo tyhjat listat luokan pelaajille,pakalle,poydalle ja vuorossa olevan pelaajan
        kadelle seka tyhjan stringin vuorossa olevalle pelaajalle. Lisaksi luo sanakirjan, jossa aivainsanana 
        edellisten listojen korttien nimet ja arvona kortti-olio.'''
        self.pelaajat=[]
        self.kierrosnumero = 0      #pidetaan kirjaa monesko jakokierros on menossa
        self.pakka=[]
        self.poyta=[]
        self.nakyva_kasi=[]
        self.kortit = {}
        self.kenen_vuoro = 0        #pidetaan kirjaa yhden kierroksen sisalla kuka on vuorossa, naita pelataan jaon jalkeen aina 4 kpl
        
        self.kuka_ottanut_viimeksi = None  #taman stringin avulla kierroksen lopussa tiedetaan kenella annetaan loput poyta kortit
        
        '''
        Tassa on seuraavaksi muutama lista joiden avulla pysytaan perassa mita kortteja on
        valittu/klikattu.
        '''
        self.klikatut_kasikortit = []
        self.klikatut_poytakortit = []
        
        
        self.luo_pakka() #luo uuden pakan ja alustaa samalla kaikille korteille kortti-oliot
        self.sekoita_pakka() #luonnollisesti sekoittaa pakan (eli siis listan korttien nimista)
        
        self.lisaa_pelaajat(pelaajien_nimet)
        
        
    def lisaa_pelaajat(self, pelaajien_nimet):
        '''Luo uudet pelaaja oliot ja lisaa ne pelaajat listaan.'''
        
        for i in pelaajien_nimet:
            pelaajien_nimet[i] = Pelaaja(pelaajien_nimet[i])
            
        for i in dict.values(pelaajien_nimet):
            self.pelaajat.append(i)
                    
        for i in self.pelaajat:     #maaraa pelaaja-olioille, onko ne tietokonepelaajia vai ihmisia
            i.set_brain()
        
        random.shuffle(self.pelaajat)      
        self.anna_pelaajille_vuorot()
        
    def anna_pelaajille_vuorot(self):
        '''Antaa jokaiselle luodulle pelaajalle oman 'vuoronumeron', 
        jonka avulla ohjelma pysyy mukana, missa jarjestyksessa kierrosta
        mennaan eteenpain ja kenen vuoro on aloittaa kierros.'''
        
        n=1
        for i in self.pelaajat:
            i.vuoro=n
            n=n+1
            
        #taman voisi tarkistaa luomalla oman exception tyypin, jonka tama heittaisi jos n != pelaajienLKM
        
    def vuoronumeron_siirto(self):
        "Siirtaa kaikkien pelaajien vuoronumeroa yhdella taaksepain kierroksen vaihtuessa, muuttaen kierroksen aloittajaa."   
        for i in self.pelaajat:
            i.vuoro = i.vuoro - 1
            if i.vuoro == 0:
                i.vuoro = len(self.pelaajat)        
        
    def luo_pakka(self):
        '''Luo listaan tayden pakan jossa on jokaista neljaa maata 13 korttia
        eli yhteensa 52 korttia. Alla myos alustaa kaikki kortit sanakirjaan.'''
        self.pakka = []
        for i in range(4):
            for u in range(1, 14):
                if i == 0:
                    maa = 'clubs'
                elif i == 1:
                    maa = 'diamonds'
                elif i == 2:
                    maa = 'hearts'
                elif i == 3:
                    maa = 'spades'
                
                kortin_nimi = maa + '-' + str(u) + '-75'             
                self.pakka.append(kortin_nimi)
                
                self.kortit[kortin_nimi]=Kortti(kortin_nimi)    
        '''Edellinen rivi luo sanakirjan, jossa avainsanana on kortin nimi ja 
        arvona avaimelle on aina nimea vastaava kortti-olio. 
        Eli alustaa kaikki kortit.'''
        
    def sekoita_pakka(self):
        ''' Sekoittaa pakan jos se ei ole tyhja'''
        
        if self.pakka != []:
            random.shuffle(self.pakka)
            
    def onko_kortit_pelattu(self):
        'Tarkistaa onko kaikkien pelaajien kasi tyhja, palauttaa arvon TRUE jos on ja arvon FALSE jos ei ole'
        kortit_pelattu = True
        for i in self.pelaajat:
            if i.kasi != []:
                kortit_pelattu = False
        
        return kortit_pelattu
            
    def korttien_jako(self):
        '''Tasta alkaa aina kierros. Funktio jakaa jarjestyksessa kortit pelaajille.
        2 korttia kerrallaan aloittaen kierroksen ensimmaisesta pelaajasta. Kierroksen 1 ensimmainen pelaaja arvotaan 
        funktiossa lisaa_pelaajat ja samalaa myos pelijarjestys. Muiden kierrosten kohdalla ensimmainen pelaaja on aina 
        jarjestyksessa seuraava pelaaja. Jos on 5 pelaajaa niin kortteja jaetaan vain 1 kerrallaan, jotta kortit menisivat tasan.
        Jos pelaajia on 2,3,4 tai 6 kortit menevat tasan jaettaessa 2 kerrallaan.'''
        
        if len(self.pakka) == 52:       #tarkistaa onko kierroksen eka jako
            self.kierrosnumero = self.kierrosnumero + 1
            
            for i in range(4):          # jakaa kierroksen ensimmaisella jaolla poytaan kortit
                self.poyta.append(self.pakka[0])
                self.pakka.remove(self.pakka[0])
                
        if self.onko_kortit_pelattu() == True:  #Tarkistaa onko kaikki kasikorit pelattu vai onko jakokierros kesken
        
            if len(self.pelaajat) == 5:     # jos on 5 pelaajaa jakaa yksitellen
                
                try:
                    for u in range(4):
                        for i in range(len(self.pelaajat)):
                            indeksi = i + self.kierrosnumero - 1
                            while indeksi > len(self.pelaajat) - 1:
                                indeksi = indeksi - len(self.pelaajat)
                                
                            pelaaJa = self.pelaajat[indeksi]
                    
                            pelaaJa.kasi.append(self.pakka[0])
                            self.pakka.remove(self.pakka[0])
                except IndexError:
                    if len(self.pakka) == 0:
                        pass
                    
                self.vuoron_aloitus(0)
            
            elif len(self.pelaajat) != 5:   # jos on 2,3,4 tai 6 pelaajaa jakaa 2 korttia kerrallaan   
                try:
                    for u in range(2):
                        for i in range(len(self.pelaajat)):
                            indeksi = i + self.kierrosnumero - 1
                            while indeksi > len(self.pelaajat) - 1:
                                indeksi = indeksi - len(self.pelaajat)
                                
                            pelaaJa = self.pelaajat[indeksi]
                            pelaaJa.kasi.append(self.pakka[0])
                            pelaaJa.kasi.append(self.pakka[1])
                            
                            self.pakka.remove(self.pakka[0])
                            self.pakka.remove(self.pakka[0])
                           
                except IndexError:          # jos kortteja ei riita kaikille neljaa jakaa niin monta kuin pakasta riittaa
                    if len(self.pakka)== 0:
                        pass
                    else:
                        print('ErroR')
                
                self.vuoron_aloitus(0)
                
        if self.kierrosnumero > len(self.pelaajat):                             #kierrosnumeron pitaminen ajan tasalla
            self.kierrosnumero = self.kierrosnumero - len(self.pelaajat)

        
        
    def laita_kortti(self):
        '''
        Laittaa valitun kasikortin poydalle
        '''
        for x in self.klikatut_kasikortit:
            for i in self.pelaajat:
                if i.vuoro == self.kenen_vuoro:        #valitsee vuorossa olevan pelaajan
                                                                                
                    i.kasi.remove(x)
                    self.poyta.append(x)
                    self.nakyva_kasi.remove(x)
                    
                    #i on se pelaaja kenen vuoro on
                    

                    self.klikatut_kasikortit.remove(x)
        if self.onko_kortit_pelattu() == False:   
            self.vuoron_aloitus(0)   
        
        elif self.onko_kortit_pelattu() == True and self.pakka == []:
            self.kierroksen_lopetus()
        
    def ota_kortteja(self):
        '''
        Ottaa kortteja poydasta. Tama toimii niin, etta ensin pitaa valita yksi kasikortti seka 
        vahintaan yksi poytakortti.Taman jalkeen painetaan ota kortteja -napista. 
        Jos kasikortilla ei voi ottaa poytakortteja ohjelma ilmoittaa pop up-ikkunassa siita.
        '''
        oma_lista = []
        for x in self.klikatut_kasikortit:
            for y in self.klikatut_poytakortit:
                oma_lista.append(self.kortit[y])
            if len(self.klikatut_kasikortit) == 1:
                u = tarkasta_kortit(self.kortit[x], oma_lista)
                
                if u == True:
                    for i in self.pelaajat:
                        if i.vuoro == self.kenen_vuoro :     #valitsee vuorossa olevan pelaajan
                            i.kasi.remove(x)                         
                            i.otetut_kortit.append(x)   #lisaa kasikortin pelaaja otto-pinoon
                            
                            self.nakyva_kasi.remove(x)
                            for y in self.klikatut_poytakortit: #poistaaa poydasta otetut kortit
                                self.poyta.remove(y)
                                
                                i.otetut_kortit.append(y)   #lisaa poytakortin pelaajan otto-pinoon
                                
                            self.kuka_ottanut_viimeksi = i.nimi
                            
                            if self.poyta == []:        #jos pelaaja saa mokin niin lisaan sen pelaajan tietoihin
                                i.mokit = i.mokit + 1
                    
                    self.klikkausten_nollaus()  
                    
                    
                    if self.onko_kortit_pelattu() == False:            
                        self.vuoron_aloitus(0)   #jos otto onnistuu, paattaa vuoron
                        
                    elif self.onko_kortit_pelattu() == True and self.pakka == []:
                        self.kierroksen_lopetus()
                                
                elif u == False:
                    '''
                    Tassa on seuraavaksi Popup ilmoitus ettei siirtoa voi tehda
                    '''
                    ilmoitus = QMessageBox()
                    ilmoitus.setWindowTitle(' ')
                    ilmoitus.setText('Kyseista siirtoa ei voi tehda.\nValitsemallasi kasikortilla ei voi\nottaa valitsemasia poytakortteja.   ')
                    ilmoitus.setIcon(QMessageBox.Warning)
                    ilmoitus.setGeometry(800, 400, 400, 300)
                    ilmoitus.exec()

                    self.klikkausten_nollaus()
            else:
                self.klikkausten_nollaus()   
      
        
                            
    def vuoron_aloitus(self, x):
        '''
        Tata funktiota pitaa kutsua aina jaon jalkeen ja aina kun pelaaja on pelannut vuoron
        (tai aina kun pelia jatketaan keskeneraisesta lautauksesa). Muuttuja x on joko 1 tai 0. 
        Jos se on 1 niin silloin on kyse latauksen jalkeisesta vuoron alkoituksesta, jolloin
        vuoronumeroa ei siirreta eteenpain.
        '''
        self.kenen_vuoro = int(self.kenen_vuoro) + 1         #paivittaa vuoronumeron
        if x == 1:
            self.kenen_vuoro = self.kenen_vuoro - 1 # talla valtetaan latauksesta johtuva vuoron siirtyminen    
        
        if self.kenen_vuoro > len(self.pelaajat):
            self.kenen_vuoro = self.kenen_vuoro - len(self.pelaajat) 
                    
        for i in self.pelaajat:
            if i.vuoro == self.kenen_vuoro:
                self.nakyva_kasi = []
                
                txt = i.nimi + '\non SINUN vuorosi !       '
                ilmoitus = QMessageBox()
                ilmoitus.setWindowTitle(' ')
                ilmoitus.setIcon(QMessageBox.Information)
                ilmoitus.setText(txt)
                ilmoitus.setGeometry(800, 400, 400, 300)
                ilmoitus.exec()
                #i on se pelaaja kenen vuoro on
                for u in i.kasi:                                #lisaa vuorossa olevan pelaajan kaden nakyville
                    self.nakyva_kasi.append(u)    
        
    
    def anna_nakyva_kasi(self):
        '''Palauttaa nakyvan kaden jollei se ole tyhja'''
        if self.nakyva_kasi != []:
            return self.nakyva_kasi
        else:
            return False
        
    def anna_poytakortit(self):
        '''Palauttaa poydassa olevat kortit'''
        return self.poyta
    
    def anna_pakka(self):
        '''Palauttaa pakassa olevat kortit''' 
        return self.pakka          
    
    def kortin_klikkaus(self, kortin_nimi, x):
        '''
        Jos x = 1 on kasikortti, jos x = 0 on kysessaa poytakortti.
        '''
        if kortin_nimi != '':
            if x == 1:                                          #kadessa voi olla vain 1 kortti valittu
                if kortin_nimi in self.klikatut_kasikortit:     #poistaa valinnan kortista kokonaan jos sita klikkaa uudelleen
                    self.klikatut_kasikortit.remove(kortin_nimi)
                elif self.klikatut_kasikortit != []:            #jos joku muu kortti on valittu valitsee sen sijaan uuden kortin
                    self.klikatut_kasikortit = []
                    self.klikatut_kasikortit.append(kortin_nimi)
                else:                                           #valitsee uuden kortin
                    self.klikatut_kasikortit.append(kortin_nimi)
                    
            elif x == 0:
                if kortin_nimi in self.klikatut_poytakortit:
                    self.klikatut_poytakortit.remove(kortin_nimi)
                else:
                    self.klikatut_poytakortit.append(kortin_nimi)
        
    def klikkausten_nollaus(self):
        '''
        Nollaa klikatut kortit
        '''
        self.klikatut_kasikortit = []
        self.klikatut_poytakortit = [] 

        
    def kierroksen_lopetus(self):
        '''
        Kierroksen loppuun tulevat toimenpiteet.
        - loppujen poytakorttien antaminen sille joka on viimeksi saanut poydasta kortteja
        - pisteiden lasku
        - pakan uusi alustus
        
        '''
        for i in self.pelaajat: #loppujen poytakorttien jako
            if i.nimi == self.kuka_ottanut_viimeksi:
                for u in self.poyta:
                    i.otetut_kortit.append(u)
        self.poyta=[]
        
        self.pisteiden_lasku() #pisteiden lasku
        
        "Tulostaa kierroksen lopussa pisteet"
        voittajat = self.kuka_voitti()
        self.tulostus = Pisteiden_tulostus(self.pelaajat, voittajat)
        
        self.pelaajien_resetointi() #piste-muuttujien nollaus
        self.vuoronumeron_siirto() #siirtaa kierroksen aloittajaa
        
        self.luo_pakka()    #luo uuden pakan
        self.sekoita_pakka()#sekoittaa sen

    def pisteiden_lasku(self):
        #laskee pelaajien pisteet ja lisaa ne pelaajien tietoihin
        "Jos monella pelaajalla on eniten kortteja tai eniten patoja he kaikki saavat pisteen"
        summat = [] #lista korttein lkm:sta
        patojen_lkm = []
        
        for i in self.pelaajat:
            #mokit
            i.kierpisteet = i.kierpisteet + i.mokit
            
            for u in i.otetut_kortit:   #erikoiskortit
                if self.kortit[u].onko_assa()==True:
                    i.assat += 1
                    i.kierpisteet += 1
                if self.kortit[u].onko_ruutu_10()==True:
                    i.ruutu10 = 1
                    i.kierpisteet += 2
                if self.kortit[u].onko_pata_2()==True:
                    i.pata2 = 1
                    i.kierpisteet += 1
                if self.kortit[u].maa == 'spades':      #laskee patojen maaran
                    i.padat += 1
            
            summat.append(len(i.otetut_kortit))
            patojen_lkm.append(i.padat)
            
        summat.sort(key=None, reverse=True) #antaa pelaajalle, jolla on eniten kortteja pisteen
        for x in self.pelaajat:
            if len(x.otetut_kortit) == summat[0]:
                x.kierpisteet += 1
                
        patojen_lkm.sort(key=None, reverse=True) #antaa pelaajalle, jolla on enite kortteja pisteen
        for y in self.pelaajat:
            if y.padat == patojen_lkm[0]:
                y.kierpisteet += 1
                
        for v in self.pelaajat:     #lisaa kierroksella saadut pisteet yhteispisteisiin
            v.yhtpisteet = v.yhtpisteet + v.kierpisteet
    def kuka_voitti(self):
        "Palauttaa voittajan nimen"
        lista = []
        voittajat=[]
        for i in self.pelaajat:
            lista.append(i.yhtpisteet)
            
        lista.sort(key=None, reverse=True)
        
        for u in self.pelaajat:
            if u.yhtpisteet == lista[0]:
                voittajat.append(u.nimi)
        
        return voittajat
                
    def pelaajien_resetointi(self):
        "Tyhjentaa/nollaa kaikki muuttujat joiden avulla on laskettu pisteet"
        for i in self.pelaajat:
            i.mokit = 0
            i.otetut_kortit = []
            i.padat = 0
            i.assat = 0
            i.ruutu10 = 0
            i.pata2 = 0
            i.kierpisteet = 0
            