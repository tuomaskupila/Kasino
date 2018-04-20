'''Tahan tulee korttien tarkastukseen littyva funktio.
Se tarkistaa voiko valitulla kortilla (kasi) ottaa poydasta valitut kortit.
Palauttaa Boolean -arvon.'''

    
def tarkasta_kortit(kasi_kortti, poyta_kortit):
    '''
    Funktion input arvot ovat valittuja kortti-olioita. Kadesta valitaan yksi ja poydasta vahintaan yksi.
    '''
    
    kasi_kortin_arvo = int(kasi_kortti.arvo)
    
    poyta_korttien_arvot = []       
    for i in poyta_kortit:              #muuttaa poyta korttien luokka-listan, arvolistaksi, jota on helpompi tutkia
        poyta_korttien_arvot.append(int(i.arvo))
        
    
    if kasi_kortti.onko_ruutu_10() == True: #tarkistaa erilaiset erikoiskortit , ruutu-10
        kasi_kortin_arvo = 16
        
    if kasi_kortti.onko_assa() == True:     #assa
        kasi_kortin_arvo = 14
        
    if kasi_kortti.onko_pata_2() == True:   #pata-2
        kasi_kortin_arvo = 15
    
    for u in poyta_korttien_arvot:          #tutkii onko poytakorteista, joku suurempi kuin kasikortti
        if u > kasi_kortin_arvo:
            return False
        
    summa = 0 
    for i in poyta_korttien_arvot:
        summa = summa + i
        
    if float(summa / kasi_kortin_arvo) - int(summa / kasi_kortin_arvo) != 0:    #tutkii onko poytakorttien summa jaollinen kasikortin arvolla
        return False
    poyta_korttien_arvot=sorted(poyta_korttien_arvot, reverse = True) # jarjestetaan suurimmasta pienimpaan
        
    
    while kasi_kortin_arvo in poyta_korttien_arvot:     #ottaa kasikortin kanssa samanarvoiset kortit suoraan pois poytakorteista
        poyta_korttien_arvot.remove(kasi_kortin_arvo)
    '''
    Seuraavaksi tulisi tutkia loytyyko valituista poytakorteista yhdistelmia, 
    jotka olisi mahdollista ottaa kasikortilla.
    '''
    
    if len(poyta_korttien_arvot) > 1:
        kierros_tehty = True
        while len(poyta_korttien_arvot) > 0:        #looppi pyorii niin kauan kuin poytakortteja on jaljella tai kunnes ei enaa loydy yhdistelmaa
            if kierros_tehty == False:
                return False
            kierros_tehty = False
            x = poyta_korttien_arvot[0]
            poyta_korttien_arvot.remove(poyta_korttien_arvot[0])
            '''                     
                                    README!                             
            seuraava looppihelvetti tutkii muut mahdolliset yhdistelmat kun poytakortteja on
            3-6 kappaletta valittu 
            Kun looppi loytaa yhdistelman, kierros_tehty boolean muuttuu todeksi,
            talloin for loopit eivat voi poistaa enaa kortteja ja while loop alkaa
            aikanaan alusta etsien uutta yhdistelmaa
            Systeemi etsii aina suurimmalle kortille listassa sopivaa yhdistelmaa ja nain
            se ei missaa mitaan kortteja... Nain kavisi jos otettaisiin pienimmasta kortista
            loytyvia yhdistelmia esim. jos olisi koritt 4, 3, 3, 6, 7, 7 ja yritettaisiin ottaa
            niita kortilla 10. Jos alotettaisiin pienimmasta loytyisi vain yhdistelma 4+3+3 ja
            muut eivat kavisi. Jos kuitenkin aloitetaan suurimmasta, loytyy ensin 7+3 sitten 
            toinen 7+3 ja lopuksi viela 6+4 ja nain kaikki kortit loytyvat.   
            '''
            w = 0
            if kasi_kortin_arvo - x in poyta_korttien_arvot:        #tutkii kahden kortin muodostamat yhdistelmat (ja poistaa ne poytakorteista)
                poyta_korttien_arvot.remove(kasi_kortin_arvo - x) 
                kierros_tehty = True
                w=1   
            if len(poyta_korttien_arvot) == 1 and w == 0:
                print('Taalla')
                return False
            else:                                                    
                for a in poyta_korttien_arvot:
                    if kierros_tehty == False:
                        y=[]
                        for i in poyta_korttien_arvot:
                            if i != a:     
                                y.append(i)
                        if y == []: #tarkistaa onko jaljella samaa arvoa olevia poytakortteja
                            if x + poyta_korttien_arvot[0] + poyta_korttien_arvot[1] == kasi_kortin_arvo:
                                poyta_korttien_arvot.remove(poyta_korttien_arvot[0])
                                poyta_korttien_arvot.remove(poyta_korttien_arvot[0])
                                kierros_tehty = True
                        for b in y:
                            if kierros_tehty == False:
                                z=[]
                                if x + a + b == kasi_kortin_arvo:   #3 kortin yhdistelmat
                                    poyta_korttien_arvot.remove(a)
                                    poyta_korttien_arvot.remove(b)
                                    kierros_tehty = True
                                else:
                                    for i in y:
                                        if i != b:
                                            z.append(i)
                                    if z == []: #tarkistaa onko jaljella samaa arvoa olevia poytakortteja
                                        if x + poyta_korttien_arvot[0] + poyta_korttien_arvot[1] + poyta_korttien_arvot[2] == kasi_kortin_arvo:
                                            poyta_korttien_arvot.remove(poyta_korttien_arvot[0])
                                            poyta_korttien_arvot.remove(poyta_korttien_arvot[0])
                                            poyta_korttien_arvot.remove(poyta_korttien_arvot[0])
                                            kierros_tehty = True
                                    for c in z:
                                        if kierros_tehty == False:
                                            q=[]
                                            if x + a + b + c == kasi_kortin_arvo: #4 kortin yhdistelmat
                                                poyta_korttien_arvot.remove(a)
                                                poyta_korttien_arvot.remove(b)
                                                poyta_korttien_arvot.remove(c)
                                                kierros_tehty =True
                                            else:
                                                for i in z:
                                                    if i != c:
                                                        q.append(i)
                                                if q == []: #tarkistaa onko jaljella samaa arvoa olevia poytakortteja
                                                    if x + poyta_korttien_arvot[0]+poyta_korttien_arvot[1]+poyta_korttien_arvot[2]+poyta_korttien_arvot[3]==kasi_kortin_arvo:
                                                        poyta_korttien_arvot.remove(poyta_korttien_arvot[0])
                                                        poyta_korttien_arvot.remove(poyta_korttien_arvot[0])
                                                        poyta_korttien_arvot.remove(poyta_korttien_arvot[0])
                                                        poyta_korttien_arvot.remove(poyta_korttien_arvot[0])
                                                        kierros_tehty = True
                                                for d in q:
                                                    if kierros_tehty == False:
                                                        r=[]
                                                        if x + a + b + c + d == kasi_kortin_arvo: #5 kortin yhdistelmat
                                                            poyta_korttien_arvot.remove(a)
                                                            poyta_korttien_arvot.remove(b)
                                                            poyta_korttien_arvot.remove(c)
                                                            poyta_korttien_arvot.remove(d)
                                                            kierros_tehty = True
                                                        else:
                                                            for i in q:
                                                                if i != d:
                                                                    r.append(i)
                                                            for e in r:
                                                                if kierros_tehty == False:
                                                                    if x + a + b + c + d + e == kasi_kortin_arvo:    #6 koritn yhdistelmat
                                                                        poyta_korttien_arvot.remove(a)   
                                                                        poyta_korttien_arvot.remove(b)
                                                                        poyta_korttien_arvot.remove(c)
                                                                        poyta_korttien_arvot.remove(d) 
                                                                        poyta_korttien_arvot.remove(e)
                                                                        kierros_tehty = True
        return True # palauttaa True arvon jos kaikille pytakortteille loytyi sopivat yhdistelmat
    
    else:
        return True
