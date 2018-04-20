import sys

from PyQt5 import QtWidgets, QtGui, QtCore
from pelitilanne import Pelitilanne
from PyQt5.Qt import QColor, QLabel, QPixmap, QIcon
from kuvake import Kuvake
from PyQt5.QtWidgets import QMessageBox

class Kayttoliittyma(QtWidgets.QMainWindow):
    '''Kayttoliittyma luokka luo uuden kayttoliittyman (ikkunan), jossa
    nakyy peli kyseisessa tilanteessa (alussa kun tietenkin ei nay mitaan pelia, 
    koska ei ole ladattu aloitettu viela mitaan), seka jonka kanssa kayttaja
    pystyy keskustelemaan.'''
    
    def __init__(self):
        super().__init__()
        
        'Tassa luodaan ns. paawidget (QVBoxLayout) ja sille 1. alawidget (QHBoxLayout)'
        self.setCentralWidget(QtWidgets.QWidget())
        self.vertical = QtWidgets.QVBoxLayout() # Vertical main layout
        self.horizontal = QtWidgets.QHBoxLayout() # Horizontal layout ingame napeille
        self.centralWidget().setLayout(self.vertical)
        '''kuuluuko tama tahan?'''
        
        
        
        pelin_nimi='Kasino'
        
        '''
        Tassa luodaan seuraavaksi pelaajien nimille sanakirja,
        mutta tata kaytetaan vain ennen pelitilanteen luomista.
        Kun pelitilanne on luotu kaytetaan pelitilanteen sisalla 
        olevaa listaa Pelaaja-olioista, joilla on itsellaan 
        tieto omasta nimestaan.
        '''
        self.pelaajien_nimet={} 
        self.pelaajienLKM = 0
        self.HumanLKM = -1
        self.PELI = None

       
        ikoni = QIcon('casino3.jpg')
        self.paaikkuna(pelin_nimi, ikoni) # toinen muuttuja on ikkunan ikoni

        '''
        Set a timer to call the update function periodically
        '''
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.paivita_kaikki())
        self.timer.start(10) # Milliseconds
    
    
        
    def paaikkuna(self,pelin_nimi, ikoni):
        '''Luo uuden ikkunan kayttoliittymaan'''
        
        self.setGeometry(200,40,1500,900) #asettaa ikkunan mitat ja paikan
        self.setWindowTitle(pelin_nimi) #lisaa otsikon ikkunalle (sama kuin pelitallennuksen nimi)
        self.setWindowIcon(ikoni) #lisaa kuvakkeen ikkunan oikeaan ylakulmaan
        
        self.menu = self.menuBar() #luo valikon
        self.valikko = self.menu.addMenu('&Valikko')
        self.statusBar().showMessage('Valmis')
        
        self.luo_menu_napit()
        
        self.taustavari = QColor(39, 119, 20)
        paletti = QtGui.QPalette()
    
        paletti.setColor(QtGui.QPalette.Background, self.taustavari)
        self.setPalette(paletti)
        
        self.show()
        
    ##########################################################################
                
    def scenen_ja_ingame_nappien_luominen(self):  
        self.luo_ingame_napit()
        self._scenen_luominen()
        
    def _scenen_luominen(self):
        '''Luo scenen ja siihen view:n jotta scene nakyy paaikkunassa.
        Tama scene lisataan widgettina viela 'paawidgetin' alle toiseksi osaksi QVBoxLayouttia.
        Scenee lisataan myohemmin omia alawidgetteja (eli kortit).'''
        
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0,0,1300,750)    
            
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.adjustSize()
        self.view.setStyleSheet("background: transparent; border: transparent;")    #muuttaa scenen taustan lapinakyvaksi
        
        self.view.show()
        
        self.vertical.addWidget(self.view)    
        
    ##########################################################################
        
    def luo_ingame_napit(self): 
        
        "Luo PushButton -napit"
        self.jaa_nappi = QtWidgets.QPushButton("Jaa uudet kortit")
        self.ota_nappi = QtWidgets.QPushButton("Ota kortteja")
        self.laita_nappi = QtWidgets.QPushButton('Laita kortteja poytaan')
        self.ohje_nappi = QtWidgets.QPushButton('Ohje ja saannot')
        
        "Liittaa niihin toiminnot"
        self.jaa_nappi.clicked.connect(lambda: self.jaa_napin_toiminta())
        self.ota_nappi.clicked.connect(lambda: self.ota_napin_toiminta())
        self.laita_nappi.clicked.connect(lambda: self.laita_napin_toiminta())
        self.ohje_nappi.clicked.connect(lambda: self.ohje_napin_toiminta())
       
        "Lisaa ne horizontal layouttiin"
        self.horizontal.addWidget(self.jaa_nappi)
        self.horizontal.addWidget(self.ota_nappi)
        self.horizontal.addWidget(self.laita_nappi)
        self.horizontal.addWidget(self.ohje_nappi)
        
        "Lisaa horizontal layoutin paalayouttiin (vertical)"
        self.vertical.addLayout(self.horizontal)
        
    def jaa_napin_toiminta(self):
        kortit_pelattu = True       #Tarkistaa onko kaikki kasikorit pelattu vai onko jakokierros kesken
        for i in self.PELI.pelaajat:
            if i.kasi != []:
                kortit_pelattu = False
                
        if kortit_pelattu == True:
            self.PELI.korttien_jako()
            self.paivita_kaikki()        
        
    def ota_napin_toiminta(self):
        #Tarkistaa onko vain yksi kasikortti valittuna, ja jos poytakorttejakin EI OLE valittuna,
        #poistaa kaikki valinnat eika tee muuta
        if self.PELI.klikatut_poytakortit == []:
            self.PELI.klikkausten_nollaus()
        elif len(self.PELI.klikatut_kasikortit) == 1:
            self.PELI.ota_kortteja()
        
    def laita_napin_toiminta(self):
        #Tarkistaa onko vain yksi kasikortti valittuna, jos poytakorttejakin JO NYT valittuna,
        #poistaa kaikki valinnat eika tee muuta
        if self.PELI.klikatut_poytakortit != []:
            self.PELI.klikkausten_nollaus()
        
        elif len(self.PELI.klikatut_kasikortit) == 1:
            self.PELI.laita_kortti()
        
    def ohje_napin_toiminta(self):
        #Luo popup ikkunan jossa on ohjeet ja saannot
        
        ilmoitus = QMessageBox()
        ilmoitus.setWindowTitle('Ohje')
        teksti = '''
Ensin on kerrottu ohje kasinon pelaamiseen ohjelmalla, sitten on kerrottu tarkemmin pelin saannot.
        
Ohje: 

Aloittaaksesi kierroksen sinun tulee painaa "Jaa uudet kortit" -nappia. Tama jakaa uudet kortit 
ja aloittaa uuden kierroksen. Pelin aikana, jos haluat ottaa poydasta tai laittaa poytaan kortteja
sinun tulee ensin valita kyseiset kortit ja sitten painaa kyseista toimintoa ylareunasta. 
            
Huomaa, etta kortit muuttuvat sinisiksi kun ne ovat valittuina!
            
Laittaessasi kortteja voit valita kortteja vain kadestasi. Vastaavasti kun haluat ottaa kortteja 
poydasta on sinun valittava yksi kortti kadesta ja vahintaan yksi kortti poydasta. 
            
Pisteet tulevat nakyviin aina kierroksen lopussa. Uuden kierroksen voi aloittaa painamalla taas
"Jaa uudet kortit". Kierroksia voi pelata kuinka monta vain.
            
            
Saannot:

Saannoissa noudatetaan ns. pakka-kasinon saantoja.
Perusohejeet kasinon peluuseen loytyvat sivulta 
            
http://www.korttipeliopas.fi/kasino
            
Huomaa kuitenkin, etta tassa pelaajia voi olla 2-6 ja mokkeja saa myos viimeiselta kierrokselta.
        '''
        
        
        ilmoitus.setText(teksti)
        ilmoitus.setIcon(QMessageBox.Information)
        ilmoitus.setGeometry(700, 100, 400, 800)
        ilmoitus.exec()
    
    ##########################################################################################      
        
    def luo_menu_napit(self):
        '''Luo valikkoon kaikki napit'''
        
        self.luo_poistu_nappi()
        self.luo_uusi_peli_nappi()
        self.luo_tallenna_peli_nappi()
        self.luo_lataa_peli_nappi()
    
    ###########################################################################
        
    def luo_poistu_nappi(self):
         
        exitAction = QtWidgets.QAction(QtGui.QIcon(None), 'Lopeta', self)
        exitAction.setStatusTip('Poistu ohjelmasta (HUOM! Tallenna pelisi ennen poistumista valttaaksesi tietojen haviamisen!)')
        exitAction.triggered.connect(QtWidgets.qApp.quit)
            
        self.valikko.addAction(exitAction)
    
    ##########################################################################
        
    def luo_lataa_peli_nappi(self):
        loadGame = QtWidgets.QAction(QtGui.QIcon(None), 'Lataa', self)
        loadGame.setStatusTip('Lataa aikaisemmin tallennettu peli')
        loadGame.triggered.connect(lambda: self.lataa_peli())

        self.valikko.addAction(loadGame)
    
    def lataa_peli(self):
        '''
        Kysyy pelaajalta minka-nimisen tallennuksen han haluaa ladata ja lukee siina tiedostossa olevat tiedot ja alustaa uuden 
        pelin niiden tietojen pohjalta
        '''
        tallennuksen_nimi = self.dialogi_ikkuna('Lataa peli', 'Anna talleennustiedoston nimi ilman paatetta ".txt":')
        if tallennuksen_nimi is not False:
            tallennuksen_nimi += '.txt'
            self.tallennuksen_luku(tallennuksen_nimi)
            self.PELI.vuoron_aloitus(1)
            
    def tallennuksen_luku(self, tallenteen_nimi):
        '''Yrittaa avata tallennuksen ja lukea sen tiedot. Jos ei onnistu, antaa popup-ilmoituksen.
        '''
        x=0
        try: 
            self.alusta_peli_uudelleen(False) #alustaa pelin
            with open(tallenteen_nimi) as file:   
                for x in file:
                    x = x.rstrip('\n') #poistaa rivin perasta rivinvaihdon
                    lista = x.split(';')
                    
                    "Ensin kayttoliittymatason muuttujat"
                    if lista[0] == 'PELIN_NIMI':
                        self.pelin_nimi = lista[1]
                    elif lista[0] == 'PELAAJIENLKM':
                        self.pelaajienLKM = int(lista[1])
                    elif lista[0] == 'HUMANLKM':
                        self.HumanLKM = int(lista[1])
                    elif lista[0] =='PELAAJAT':
                        self.pelaajien_uudelleen_nimeaminen(lista[1])
                        "Seuraava rivi suorittaa ne funkitot mitka olisi normaalisti tehty funktion luo_uusi_peli lopussa"
                        self.pelin_luomiseen_liittyvien_asioiden_luonti()
                    
                    "Seuraavaksi pelitilannetason muuttujat"
                    if lista[0] == 'KIERROSNUMERO':
                        self.PELI.kierrosnumero = int(lista[1])
                    elif lista[0] == 'KENEN_VUORO':
                        self.PELI.kenen_vuoro = int(lista[1])
                    elif lista[0] == 'KUKA_OTTANUT_VIIMEKSI':
                        self.PELI.kuka_ottanut_viimeksi = lista[1]
                        
                    "Seuraavana pelaajien tietojen paivitys"
                    if lista[0] == 'PELAAJIEN_TIEDOT':
                        for p in range(self.pelaajienLKM):                            
                            lista2 = lista[p + 1].split(',')
                            
                            for y in self.PELI.pelaajat:    
                                if y.nimi == lista2[0]: #etsii yhden pelaajan kerrallaan
                                    y.yhtpisteet = int(lista2[1])
                                    y.vuoro = int(lista2[2])
                                    
                                    lista3 = lista2[3].split('*')
                                    if lista3[0] == 'KASI': #kay ensin lapi kasikortit
                                        y.kasi = []                                        
                                        for i in lista3:
                                            if i != 'KASI':
                                                y.kasi.append(i) 
                                    
                                    lista3 = lista2[4].split('*')                                    
                                    if lista3[0] == 'OTETUT_KORTIT': #sitten kay lapi otetut kortit
                                        y.otetut_kortit = []                                        
                                        for i in lista3:
                                            if i != 'OTETUT_KORTIT':
                                                y.otetut_kortit.append(i)
                    
                    "Seuraavana poyta"
                    if lista[0] == 'POYTA':
                        self.PELI.poyta = []
                        for i in lista:
                            if i != 'POYTA':
                                self.PELI.poyta.append(i)
                                
                    "Lopuksi pakka"
                    if lista[0] == 'PAKKA':
                        self.PELI.pakka = []
                        for i in lista:
                            if i != 'PAKKA':
                                self.PELI.pakka.append(i)
                        self.PELI.sekoita_pakka()   #pakka viela sekoitetaan, jotta valtytaan huijaamiselta

    
                    
        except Exception:
            teksti = '\nAntamaasi tiedostonimea ei loydy\ntai se on vioittunut!\nTarkasta antamasi nimi ja kokeile uudelleen. '
            ilmoitus = QMessageBox()
            ilmoitus.setWindowTitle('ERROR')
            ilmoitus.setIcon(QMessageBox.Warning)
            ilmoitus.setText(teksti)
            ilmoitus.setGeometry(800, 400, 400, 300)
            ilmoitus.exec()        
    
    def pelaajien_uudelleen_nimeaminen(self, nimet):
        'Luo uuden sanakirjan pelaajista vanhan paalle'
        self.pelaajien_nimet = {}
        nimet = nimet.split(',')
        
        for i in range(len(nimet)):
            x = nimet[i]
            self.pelaajien_nimet["Pelaaja{:d}".format(i+1)]= x
            
    ###################################################################3            
        
    def luo_tallenna_peli_nappi(self):
        saveGame = QtWidgets.QAction(QtGui.QIcon(None), 'Tallenna', self)
        saveGame.setStatusTip('Tallenna keskenerainen pelisi')
        saveGame.triggered.connect(lambda: self.tallenna_peli())
        
        self.valikko.addAction(saveGame)
    
    def tallenna_peli(self):
        '''Kysyy pelaajalta tallennukselle nimea ja sitten tallentaa pelitilanteen tiedot uuteen .txt tiedostoon
        '''
        
        tallennuksen_nimi = self.dialogi_ikkuna('Tallenna peli','Anna tallennustiedostolle nimi:' ) # pelin nimen kysyminen
        if tallennuksen_nimi is not False:
            tallennuksen_nimi = tallennuksen_nimi + '.txt'
            f = open(tallennuksen_nimi,'w')
            tiedot = self.tallennustiedoston_teksti()
            if tiedot is not False:
                f.write(str(tiedot))
                f.close()
            
    def tallennustiedoston_teksti(self):
        '''Luo stringin johon on kirjoitettu kaikkia tarvittavat tiedot pelin tallentamiseen
        '''
        if self.PELI != None:
            try:
                "ensin tallennetaan pelin yleistiedot kayttoliittyma tasolta"
                txt = ''
                txt += 'PELIN_NIMI;' + str(self.pelin_nimi) + '\n' 
                txt += 'PELAAJIENLKM;' + str(self.pelaajienLKM) + '\n'
                txt += 'HUMANLKM;' + str(self.HumanLKM) + '\n'
                
                "sitten tallennetaan yhdelle riville kaikki pelaajien nimet"
                txt += 'PELAAJAT;'
                for i in self.PELI.pelaajat:
                    txt += i.nimi + ','
                txt = txt[:-1] #poistaa viimeisen pilkun
                txt += '\n'
                
                "sitten tallennetaan yleistiedot pelitilanteen tasolta"
                txt += 'KIERROSNUMERO;' + str(self.PELI.kierrosnumero) + '\n'
                txt += 'KENEN_VUORO;' + str(self.PELI.kenen_vuoro) + '\n'
                txt += 'KUKA_OTTANUT_VIIMEKSI;' + str(self.PELI.kuka_ottanut_viimeksi) + '\n'                
                
                "sitten tallennetaan yhden pelaajan kaikkie tiedot aina pelaaja kerrallaan"
                txt += 'PELAAJIEN_TIEDOT;'
                for i in self.PELI.pelaajat:
                    txt += i.nimi + ','
                    txt += str(i.yhtpisteet) + ','
                    txt += str(i.vuoro) + ','
                    
                    txt += 'KASI*'  #tahan tallennetaan pelaajan kasi
                    for u in i.kasi:
                        txt += str(u) + '*'
                    txt = txt[:-1] #poistaa viimeisen * -merkin
                    txt += ','
                    
                    txt += 'OTETUT_KORTIT*'  #tahan tallennetaan pelaajan talla kierroksella ottamat kortit
                    for u in i.otetut_kortit:
                        txt += str(u) + '*'
                    txt = txt[:-1] #poistaa viimeisen *-merkin
                    txt += ';'
                    
                txt = txt[:-1] #poistaa viimeisen ;-merkin
                txt += '\n'
                
                "sitten tallennetaan poyta ja pakka"
                txt += 'POYTA;'
                for i in self.PELI.poyta:
                    txt += str(i) +';'
                txt = txt[:-1]
                txt += '\n'
                
                txt += 'PAKKA;'
                for i in self.PELI.pakka:
                    txt += str(i) + ';'
                txt = txt[:-1] #poistaa viimeisen ;-merkin
                
                return txt
                
            except:
                print('exception tapahtui')
                return False
                
        else:
            return False
        
    #########################################################################    
        
    def luo_uusi_peli_nappi(self):
        
        newGame = QtWidgets.QAction(QtGui.QIcon(None), 'Luo uusi peli', self)
        newGame.setStatusTip('Luo uusi peli (HUOM! Tallenna keskenerainen pelisi ennen uuden luomista valttaaksesi tietojen haviamisen!)')
        newGame.triggered.connect(lambda: self.luo_uusi_peli())
        
        self.valikko.addAction(newGame) 
        
    def luo_uusi_peli(self):
        '''Kysyy kayttajalta uudessa ikkunassa pelille nimen, pelaajien lukumaaran,
        ihmispelaajien lukumaaran, seka ihmispelaajien nimet.'''
        
        if self.PELI == None:
            self.pelin_nimi = self.dialogi_ikkuna('Uusi peli','Anna pelille nimi:' ) # pelin nimen kysyminen
            if self.pelin_nimi is not False:
                while True: # kysyy pelaajien lukumaaran
                    try:    # talla rakenteella saadaan kysytta niin monta kertaa etta syote on virheeton
                        while not 1 < self.pelaajienLKM < 7: 
                            self.pelaajienLKM = int(self.dialogi_ikkuna(self.pelin_nimi, 'Anna seuraavaksi pelaajien maara. Suositeltu\npelaajien maara on 2-4, maksimi on 6.'))
                        break
                    except:
                        pass
                
                '!!!!!'    
                self.HumanLKM = self.pelaajienLKM   #jos tietokonepelaajat otetaan mukaan tama rivi tulee poistaa
                '!!!!!'
                
                while True: # kysyy ihmispelaajien maaran
                    try:   
                        while not 0 <= self.HumanLKM <= self.pelaajienLKM:
                            self.HumanLKM = (self.dialogi_ikkuna(self.pelin_nimi, 'Kuinka monta edellisista on ''ihmispelaajia''? \n(Loput ovat tietokonevastuksia)'))
                            if self.HumanLKM == False:
                                self.HumanLKM = -1
                            else:
                                self.HumanLKM = int(self.HumanLKM)
                        break
                    except:
                        pass
                    
                for i in range(self.HumanLKM): #'''Ihmispelaajien nimeaminen ja littaminen sanakirjaan'''
                    
                    kasky = 'Anna ' + str(i+1) +'. pelaajalle nimi:'
                    x = self.dialogi_ikkuna(self.pelin_nimi, kasky)
                    self.pelaajien_nimet["Pelaaja{:d}".format(i+1)]=x
                    
                for i in range(self.pelaajienLKM - self.HumanLKM): #'''Tietokonepelaajien automaattinen nimeaminen'''
                    
                    x='Tietokonepelaaja' + str(i+1)  
                    self.pelaajien_nimet["Pelaaja{:d}".format(i+1+self.HumanLKM)]=x 
                    
                self.pelin_luomiseen_liittyvien_asioiden_luonti()
        else:
            self.alusta_peli_uudelleen(True) #jos aloitetaan uusi peli vanhan paalle niin vanha pitaa poistaa
            
    def dialogi_ikkuna(self, toiminta, kasky):
        '''Tama toimii pohjana kaikille dialogeille, mihin kayttajan tulee antaa
        jokin syote, esim. Pelaajien nimet ja lukumaarat'''
        
        
        kasky = kasky + '\n(kentta hyvaksyy 1-15 numeroa/kirjainta)'
        text, ok = QtWidgets.QInputDialog.getText(self, toiminta, kasky)
        
        if ok:
            while 0 >= len(str(text)) or len(str(text)) > 16:
                
                text, ok = QtWidgets.QInputDialog.getText(self, toiminta, kasky)
            
            return str(text)
                  
        else:
            return False               
            
    def alusta_peli_uudelleen(self, onko_uusi_peli):
        '''"Koeilin ensin vanhojen widgettien, layouttien, scenene ja viewin poistamista
        mutta koska se osoittautui vaikeaksi enka saanut sita oikein toimimaan, paatin vain
        luoda kaikki suoraan uudestaan.'''
        
        self.PELI = None
        
        "luo uudet paawidgetit"
        self.setCentralWidget(QtWidgets.QWidget())
        self.vertical = QtWidgets.QVBoxLayout() # Vertical main layout
        self.horizontal = QtWidgets.QHBoxLayout() # Horizontal layout ingame napeille
        self.centralWidget().setLayout(self.vertical)
        
        
        self.pelaajien_nimet={} 
        self.pelaajienLKM = 0
        self.HumanLKM = -1
        
        if onko_uusi_peli == True:  #talla tarkastetaan ollaanko luomassa kokonaan uutta pelia vai vain lataamassa, jos ollaan lataamassa tama osuus
            self.luo_uusi_peli()    #suoritetaan vasta palattua takaisin tallennuksen luku metodiin
            
    def pelin_luomiseen_liittyvien_asioiden_luonti(self):
        self.pelitilanteen_luonti()
                
        self.scenen_ja_ingame_nappien_luominen() # luo scenen ja ingame - napit vasta pelitilanteen luomisen jalkeen
        self.kasikortti_widgettien_luonti() #taalla luodaan self.tyhjakuva, joten taman pitaa olla ennen poytakorttien luomista
        self.poytakortti_widgettien_luonti()
        self.pakan_luonti()
    
    def kasikortti_widgettien_luonti(self):
        
        self.kasikortit = []
        kasikortti1 = Kuvake(self.PELI, 1)
        kasikortti2 = Kuvake(self.PELI, 1)
        kasikortti3 = Kuvake(self.PELI, 1)
        kasikortti4 = Kuvake(self.PELI, 1)
        
        self.tyhja_kuva = QPixmap('tyhja.png')
        
        self.kasikortit.append(kasikortti1)
        self.kasikortit.append(kasikortti2)
        self.kasikortit.append(kasikortti3)
        self.kasikortit.append(kasikortti4)

        for i in self.kasikortit:
            i.setPixmap(self.tyhja_kuva)
            self.scene.addWidget(i)
            
        for i in range(len(self.kasikortit)):
            self.kasikortit[i].move(250 + i * 100,550) 

        
    def poytakortti_widgettien_luonti(self):
        
        self.poytakortit = []
        poytakortti1 = Kuvake(self.PELI, 0)
        poytakortti2 = Kuvake(self.PELI, 0)
        poytakortti3 = Kuvake(self.PELI, 0)
        poytakortti4 = Kuvake(self.PELI, 0)
        poytakortti5 = Kuvake(self.PELI, 0)
        poytakortti6 = Kuvake(self.PELI, 0)
        poytakortti7 = Kuvake(self.PELI, 0)  
        poytakortti8 = Kuvake(self.PELI, 0)
        poytakortti9 = Kuvake(self.PELI, 0)
        poytakortti10 = Kuvake(self.PELI, 0)

        
        self.poytakortit.append(poytakortti1)
        self.poytakortit.append(poytakortti2)
        self.poytakortit.append(poytakortti3)
        self.poytakortit.append(poytakortti4)
        self.poytakortit.append(poytakortti5)
        self.poytakortit.append(poytakortti6)
        self.poytakortit.append(poytakortti7)
        self.poytakortit.append(poytakortti8)
        self.poytakortit.append(poytakortti9)
        self.poytakortit.append(poytakortti10)
        
        for i in self.poytakortit:
            i.setPixmap(self.tyhja_kuva)
            self.scene.addWidget(i)
            
        for i in range(len(self.poytakortit)):
            self.poytakortit[i].move(50 + i * 100, 100)
            
    def pakan_luonti(self):
        
        self.korttipinon_kuva = QPixmap('deck')
        self.pakan_kuva__ = QLabel()
        self.pakan_kuva__.setPixmap(self.korttipinon_kuva)
        self.scene.addWidget(self.pakan_kuva__)
        
        self.pakan_kuva__.move(1000, 535)

    def pelitilanteen_luonti(self):
        self.setWindowTitle('Kasino - ' + self.pelin_nimi) #vaihtaa ikkunaan pelaajan antaman nimen
        
        self.PELI = Pelitilanne(self.pelaajien_nimet) #luo uuden pelitilanteen  
        
    #################################################################################################    
        
    def paivita_kaikki(self):
        '''
        Paivittaa nakyvan kaden, poytakortit seka pakan tilanteen tasalle, jos pelitilanne on luotu ja kierros aloitettu jakamalla kortit.
        '''
        try:
            if self.PELI:
                if self.scene:
                    if self.poytakortit:
                        if self.kasikortit:
                            self.nakyvien_kasikorttien_paivitys()
                            self.nakyvien_poytakorttien_paivitys()
                            self.pakan_paivitys()
        except AttributeError:
            pass
        
    def nakyvien_kasikorttien_paivitys(self):
        if self.PELI.anna_nakyva_kasi() != False:
            
            
            for i in range(len(self.PELI.anna_nakyva_kasi())):
                if self.PELI.kortit[self.PELI.anna_nakyva_kasi()[i]].kortin_nimi in self.PELI.klikatut_kasikortit:
                    kuva_ = QPixmap(self.PELI.kortit[self.PELI.anna_nakyva_kasi()[i]].kuva2)
                else:
                    kuva_ = QPixmap(self.PELI.kortit[self.PELI.anna_nakyva_kasi()[i]].kuva)
                nimi_ = self.PELI.kortit[self.PELI.anna_nakyva_kasi()[i]].kortin_nimi
                self.kasikortit[i].setPixmap(kuva_)
                self.kasikortit[i].aseta_nimi(nimi_)
                 
            if len(self.PELI.anna_nakyva_kasi()) != 4:
                for i in range(4 - len(self.PELI.anna_nakyva_kasi())):
                    self.kasikortit[3 - i].setPixmap(self.tyhja_kuva)
                    self.kasikortit[3 - i].nollaa_nimi()
        
        elif self.PELI.anna_nakyva_kasi() == False:
            for i in self.kasikortit:
                i.setPixmap(self.tyhja_kuva)
                i.nollaa_nimi()
     
    def nakyvien_poytakorttien_paivitys(self):
        
        for i in range(len(self.PELI.anna_poytakortit())):
            if self.PELI.kortit[self.PELI.anna_poytakortit()[i]].kortin_nimi in self.PELI.klikatut_poytakortit:
                kuv_a = QPixmap(self.PELI.kortit[self.PELI.anna_poytakortit()[i]].kuva2)
            else:
                kuv_a = QPixmap(self.PELI.kortit[self.PELI.anna_poytakortit()[i]].kuva)
            nim_i = self.PELI.kortit[self.PELI.anna_poytakortit()[i]].kortin_nimi 
            self.poytakortit[i].setPixmap(kuv_a)
            self.poytakortit[i].aseta_nimi(nim_i)
            
        if len (self.PELI.anna_poytakortit()) != 10:
            for i in range(10 - len(self.PELI.anna_poytakortit())):
                self.poytakortit[9 - i].setPixmap(self.tyhja_kuva)  
                self.poytakortit[9 - i].nollaa_nimi()  
                
    def pakan_paivitys(self):
        self.tyhja_pakka = QPixmap('deck-tyhja')
        
        if self.PELI.anna_pakka() == []:
            self.pakan_kuva__.setPixmap(self.tyhja_pakka)
        
        elif self.PELI.anna_pakka() != []:
            self.pakan_kuva__.setPixmap(self.korttipinon_kuva)
            
    ##########################################################################################        
            
if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    ex = Kayttoliittyma()
    sys.exit(app.exec_()) 
        