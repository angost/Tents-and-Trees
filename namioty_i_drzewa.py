#GRA NAMIOTY I DRZEWA

#REPREZENTACJA
'''
  = wartosc domyslna
- = puste pole
o = drzewo
x = namiot

elementy listy [] to kolejne pola
'''
#PLAN
'''
I Generowanie poziomu
II Uzupełnianie poziomu (gra)
    Sprawdzanie wyniku po każdym ruchu
III Koniec gdy wszystkie pola uzupełnione

2 listy, 1. z gotowym poziomem, 2. wypełniana przez gracza
domyślne wartości = " "
'''

from random import *
from math import *
import pygame

def znajdz_otoczenie(plansza, nr, rodzaj):
    #rodzaj = 4 (boki) v 9 (boki i skosy)
    rozmiar = int(sqrt(len(plansza)))
    otoczenie = []
    czy_istnieje_skos = {"lewo_gora": 1, "prawo_gora": 1, "lewo_dol": 1, "prawo_dol": 1}
    #Sprawdzam czy nr nie leży na krawędzi:
    #górnej
    if not (0 <= nr <= (rozmiar-1)):
        otoczenie.append(nr-rozmiar)
    else:
        czy_istnieje_skos["lewo_gora"] = 0
        czy_istnieje_skos["prawo_gora"] = 0
    #dolnej
    if not ((rozmiar**2-rozmiar) <= nr <= (rozmiar**2-1)):
        otoczenie.append(nr+rozmiar)
    else:
        czy_istnieje_skos["lewo_dol"] = 0
        czy_istnieje_skos["prawo_dol"] = 0
    #lewej
    if nr % rozmiar != 0:
        otoczenie.append(nr-1)
    else:
        czy_istnieje_skos["lewo_gora"] = 0
        czy_istnieje_skos["lewo_dol"] = 0
    #prawej
    if (nr+1) % rozmiar != 0:
        otoczenie.append(nr+1)
    else:
        czy_istnieje_skos["prawo_gora"] = 0
        czy_istnieje_skos["prawo_dol"] = 0

    if rodzaj == 9:
        if czy_istnieje_skos["lewo_gora"]:
            otoczenie.append(nr-rozmiar-1)
        if czy_istnieje_skos["prawo_gora"]:
            otoczenie.append(nr-rozmiar+1)
        if czy_istnieje_skos["lewo_dol"]:
            otoczenie.append(nr+rozmiar-1)
        if czy_istnieje_skos["prawo_dol"]:
            otoczenie.append(nr+rozmiar+1)

    return(otoczenie)

#Zlicza namioty w rzedach i kolumanch
def zlicz(plansza, symbol):
    rozmiar = int(sqrt(len(plansza)))
    kolumny = [[plansza[i + j*rozmiar] for j in range(rozmiar)].count(symbol) for i in range(rozmiar)]
    rzedy = []
    for i in range(rozmiar):
        rzedy.append(plansza[i*rozmiar:(i+1)*rozmiar].count(symbol))
    return(kolumny,rzedy)

#I GENEROWANIE POZIOMU
def generuj_plansze(rozmiar):
    nowa_plansza = [" " for i in range(rozmiar**2)]
    #for i in range(rozmiar):
    #    print(pusta_plansza[i*rozmiar:(i+1)*rozmiar])

    kolejnosc_uzupelniania = [i for i in range(rozmiar**2)]
    shuffle(kolejnosc_uzupelniania)
    for kandydat_na_drzewo in kolejnosc_uzupelniania:
        #Czy spróbować wstawić drzewo
        if choice([True, False]):
            #Czy jest miejsce na drzewo
            if nowa_plansza[kandydat_na_drzewo] == " ":
                #Patrzę na otoczenie potencjalnego drzewa
                for kandydat_na_namiot in znajdz_otoczenie(nowa_plansza, kandydat_na_drzewo, 4):
                    #Czy jest tam puste pole
                    if nowa_plansza[kandydat_na_namiot] == " ":
                        #W którego otoczeniu nie ma innego namiotu
                        otoczenie_kandydata_na_namiot = [nowa_plansza[i] for i in znajdz_otoczenie(nowa_plansza, kandydat_na_namiot, 9)]
                        if "x" not in otoczenie_kandydata_na_namiot:
                            #WYGRANA ALERT, ZNALEZIONO IDEALNE DRZEWO
                            nowa_plansza[kandydat_na_namiot] = "x"
                            nowa_plansza[kandydat_na_drzewo] = "o"
                            break
    for i in range(rozmiar**2):
        if nowa_plansza[i] == " ":
            nowa_plansza[i] = "-"

    return(nowa_plansza)

def wyswietl_plansze_basic(plansza):
    rozmiar = int(sqrt(len(plansza)))
    for i in range(rozmiar):
        print(plansza[i*rozmiar:(i+1)*rozmiar])

def wyswietl_plansze(plansza, kolumny, rzedy, kolumny_czy_dobrze, rzedy_czy_dobrze):
    rozmiar = int(sqrt(len(plansza)))
    print("   ", "    ".join([str(i) for i in kolumny]))

    for i in range(rozmiar):
        print(rzedy[i], plansza[i*rozmiar:(i+1)*rozmiar], rzedy_czy_dobrze[i])

    print("   ", "    ".join([i for i in kolumny_czy_dobrze]))



def nowy_poziom(rozmiar, width, height, screen):
    plansza = generuj_plansze(rozmiar)
    kolumny, rzedy = zlicz(plansza, "x")
    #wyswietl_plansze(plansza, kolumny, rzedy, ["✓" for i in range(rozmiar)], ["✓" for i in range(rozmiar)])

    plansza_gracza = [" " for i in range(rozmiar**2)]
    for i in range(rozmiar**2):
        if plansza[i] == "o":
            plansza_gracza[i] = "o"

    #grafika
    dom_ikona = pygame.image.load('./pliki/dom.png')
    kosz_ikona = pygame.image.load('./pliki/kosz.png')
    info_ikona = pygame.image.load('./pliki/info.png')
    hint_ikona = pygame.image.load('./pliki/hint.png')
    tryb_ikona = pygame.image.load('./pliki/tryb.png')
    
    if 1 <= rozmiar <= 7:
        plik_drzewo = "./pliki/drzewo_4.png"
        plik_namiot = "./pliki/namiot_4.png"
    elif 8 <= rozmiar <= 12:
        plik_drzewo = "./pliki/drzewo_3.png"
        plik_namiot = "./pliki/namiot_3.png"
    elif 13 <= rozmiar <= 17:
        plik_drzewo = "./pliki/drzewo_2.png"
        plik_namiot = "./pliki/namiot_2.png"
    else:
        plik_drzewo = "./pliki/drzewo_1.png"
        plik_namiot = "./pliki/namiot_1.png"
        
    drzewo = pygame.image.load(plik_drzewo)
    namiot = pygame.image.load(plik_namiot)

    wymiary_planszy = 450
    wymiary_pola = wymiary_planszy / (rozmiar * 6/5  - 1/5)
    x_0, y_0 = (width - wymiary_planszy)/2, (height - wymiary_planszy)/2
    x, y = x_0, y_0
    
    #Tryb: 0 = uproszczony, 1 = graficzny
    tryb = 1
    symbole = {" ": (112, 66, 77), "-": (31, 135, 88), "o": (73, 235, 119), "x": (240, 67, 19)}
    menu_kolor = (140, 184, 255)

    wymiary_tekstu = min(int(y_0/2), int(wymiary_pola))
    font = pygame.font.Font('freesansbold.ttf', wymiary_tekstu)
    font2 = pygame.font.Font('./pliki/Inter-Medium.ttf', wymiary_tekstu)
    font3 = pygame.font.Font('./pliki/Inter-Medium.ttf', 18)
    #print(wymiary_tekstu, font.size("1"), font2.size("✓"))

    wyswietl_info = False
    tekst_info = ["- Do każdego drzewa należy przyporządkować namiot",
                  "- Czyli położyć namiot przy jednym z boków drzewa, nie po skosie",
                  "- Liczby pokazują ile namiotów powinno być w danym rzędzie/kolumnie",
                  "- Namioty nie mogą stykać się ze sobą (bokami ani skosami)"]
                    
    run = True
    odkliknieto_myszke = True
    sproboj_poprawic = False
    zakoncz = False
    nowa_gra = False
    dopiero_zmieniono_z_namiotu = False
    
    #PETLA 1, SPRAWDZENIE POPRAWNOSCI, NOWA GRA, WYJSCIE Z GRY 
    while True:
        #PETLA 2, WYKONANIE RUCHU, ZLICZANIE NAMIOTOW, WYSWIETLENIE PLANSZY, MENU
        while (" " in plansza_gracza or sproboj_poprawic) and run:

            #grafika
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    zakoncz = True
                    break
            sproboj_poprawic = False

            #Nowy ruch
            poz_myszy = pygame.mouse.get_pos()
            if (x_0 <= poz_myszy[0] <= x_0+wymiary_planszy) and (y_0 <= poz_myszy[1] <= y_0+wymiary_planszy):
                if pygame.mouse.get_pressed()[0]:
                    klikniete_pole = int((poz_myszy[0]-x_0)/(wymiary_planszy/rozmiar)) + rozmiar*int((poz_myszy[1]-y_0)/(wymiary_planszy/rozmiar))
                    #jeśli wystąpi jakiś błąd
                    if klikniete_pole <= rozmiar**2 - 1:
                        if odkliknieto_myszke:
                            dopiero_zmieniono_z_namiotu = False
                            if plansza_gracza[klikniete_pole] == " ":
                                plansza_gracza[klikniete_pole] = "-"
                            elif plansza_gracza[klikniete_pole] == "-":
                                plansza_gracza[klikniete_pole] = "x"
                            elif plansza_gracza[klikniete_pole] == "x":
                                plansza_gracza[klikniete_pole] = " "
                                dopiero_zmieniono_z_namiotu = True
                        else:
                            if plansza_gracza[klikniete_pole] == " " and not dopiero_zmieniono_z_namiotu:
                                plansza_gracza[klikniete_pole] = "-"
                                dopiero_zmieniono_z_namiotu = False
                    odkliknieto_myszke = False
                    #print(poz_myszy[0])
            if not pygame.mouse.get_pressed()[0]:
                odkliknieto_myszke = True

            #Sprawdza czy dobrze
            kolumny_gracza, rzedy_gracza = zlicz(plansza_gracza, "x")
            rzedy_czy_dobrze = [rzedy[i] == rzedy_gracza[i] for i in range(rozmiar)]
            for i in range(rozmiar):
                if rzedy_czy_dobrze[i]:
                    rzedy_czy_dobrze[i] = "✓"
                else:
                    rzedy_czy_dobrze[i] = "✗"

            kolumny_czy_dobrze = [kolumny[i] == kolumny_gracza[i] for i in range(rozmiar)]
            for i in range(rozmiar):
                if kolumny_czy_dobrze[i]:
                    kolumny_czy_dobrze[i] = "✓"
                else:
                    kolumny_czy_dobrze[i] = "✗"

            #Wyświetla planszę
            #wyswietl_plansze(plansza_gracza, kolumny, rzedy, kolumny_czy_dobrze, rzedy_czy_dobrze)
            pygame.draw.rect(screen, (130, 242, 179), (0,0, width, height))
            
            y = y_0
            for j in range(rozmiar):
                for i in range(rozmiar):
                    if tryb == 0:
                        pygame.draw.rect(screen, symbole[plansza_gracza[j*rozmiar + i]], (x, y, wymiary_pola, wymiary_pola))
                    elif tryb == 1:
                        #kolor
                        if plansza_gracza[j*rozmiar + i] == " ":
                            pygame.draw.rect(screen, (112, 66, 77), (x, y, wymiary_pola, wymiary_pola))
                            
                        else:
                            #pygame.draw.rect(screen, (73, 235, 119), (x, y, wymiary_pola, wymiary_pola))
                            pygame.draw.rect(screen, (50, 217, 121), (x, y, wymiary_pola, wymiary_pola))
                            #symbol
                            if plansza_gracza[j*rozmiar + i] == "o":
                                screen.blit(drzewo, (x+wymiary_pola/2 - drzewo.get_rect().size[0]/2 ,y+wymiary_pola/2 - drzewo.get_rect().size[1]/2))
                            elif plansza_gracza[j*rozmiar + i] == "x":
                                screen.blit(namiot, (x+wymiary_pola/2 - drzewo.get_rect().size[0]/2 ,y+wymiary_pola/2 - drzewo.get_rect().size[1]/2))
                        
                    x += wymiary_pola + wymiary_pola/5
                x = x_0
                y += wymiary_pola + wymiary_pola/5
            #Wyświetla napisy
            for i in range(rozmiar):
                tekst = font.render(str(kolumny[i]), True, (0,0,0))
                screen.blit(tekst, ((x_0 + wymiary_pola/2 - font.size("1")[0]/2 + (wymiary_pola*6/5)*i), (y_0 - wymiary_tekstu - wymiary_pola/5/4)))
                tekst = font2.render(str(kolumny_czy_dobrze[i]), True, (0,0,0))
                screen.blit(tekst, ((x_0 + wymiary_pola/2 - font2.size("✓")[0]/2 + (wymiary_pola*6/5)*i), (y_0 + wymiary_planszy)))
            for i in range(rozmiar):
                tekst = font.render(str(rzedy[i]), True, (0,0,0))
                screen.blit(tekst, ((x_0 - font.size("1")[0] - wymiary_pola/5/4), (y_0 + wymiary_pola/2 - font.size("1")[1]/2 + (wymiary_pola*6/5)*i)))
                tekst = font2.render(str(rzedy_czy_dobrze[i]), True, (0,0,0))
                screen.blit(tekst, ( (x_0 + wymiary_planszy + wymiary_pola/5/4), (y_0 + wymiary_pola/2 - font2.size("✓")[1]/2 + (wymiary_pola*6/5)*i) ))

            #Menu lewe (nowa gra, wyczyść)
            wymiary_menu = 60
            x_menu = x_0/2 - wymiary_menu/2
            y_menu = height/2 - wymiary_menu*3/2
            
            pygame.draw.rect(screen, menu_kolor, (x_menu, y_menu, wymiary_menu, wymiary_menu))
            screen.blit(dom_ikona, (x_menu + (wymiary_menu-48)/2, y_menu + (wymiary_menu-48)/2))
            pygame.draw.rect(screen, menu_kolor, (x_menu, y_menu + wymiary_menu*2, wymiary_menu, wymiary_menu))
            screen.blit(kosz_ikona, (x_menu + (wymiary_menu-48)/2, y_menu + + wymiary_menu*2 + (wymiary_menu-48)/2))

            if (x_menu <= poz_myszy[0] <= x_menu+wymiary_menu) and (y_menu <= poz_myszy[1] <= y_menu+wymiary_menu):
                if pygame.mouse.get_pressed()[0] and odkliknieto_myszke:
                    run = False
                    nowa_gra = True
                    
            if (x_menu <= poz_myszy[0] <= x_menu+wymiary_menu) and (y_menu + wymiary_menu*2 <= poz_myszy[1] <= y_menu + wymiary_menu*2+wymiary_menu):
                if pygame.mouse.get_pressed()[0] and odkliknieto_myszke:
                    plansza_gracza = [" " for i in range(rozmiar**2)]
                    for i in range(rozmiar**2):
                        if plansza[i] == "o":
                            plansza_gracza[i] = "o"
                            
            #Menu prawe (info, hint, tryb)
            wymiary_menu2 = 48
            x_menu2 = width - wymiary_menu2
            y_menu2 = height - wymiary_menu2*5/2


            #hint
            pygame.draw.circle(screen, menu_kolor, (int(x_menu2), int(y_menu2)), int(wymiary_menu2/2))
            screen.blit(hint_ikona, (int(x_menu2 - wymiary_menu2/2), int(y_menu2 - wymiary_menu2/2)))
            
            if (x_menu2-wymiary_menu2/2 <= poz_myszy[0] <= x_menu2+wymiary_menu2/2) and (y_menu2-wymiary_menu2/2 <= poz_myszy[1] <= y_menu2+wymiary_menu2/2):
                if pygame.mouse.get_pressed()[0] and odkliknieto_myszke:
                    odkliknieto_myszke = False
                    #Wybiera pole do którego dać wskazówkę (najbiższe puste lub losowe)
                    try:
                        hint_pole = plansza_gracza.index(' ')
                    except:
                        hint_pole = randint(0,rozmiar**2-1)
                    if plansza_gracza[hint_pole] != plansza[hint_pole]:
                        plansza_gracza[hint_pole] = plansza[hint_pole]
                    
            
            #tryb
            if (x_menu2-wymiary_menu2/2 <= poz_myszy[0] <= x_menu2+wymiary_menu2/2) and (y_menu2-wymiary_menu2/2 + wymiary_menu2*3/2  <= poz_myszy[1] <= y_menu2+wymiary_menu2/2 + wymiary_menu2*3/2):
                if pygame.mouse.get_pressed()[0] and odkliknieto_myszke:
                    odkliknieto_myszke = False
                    tryb = not tryb
                    
            pygame.draw.circle(screen, menu_kolor, (int(x_menu2), int(y_menu2 + wymiary_menu2*3/2)), int(wymiary_menu2/2))
            screen.blit(tryb_ikona, (int(x_menu2 - wymiary_menu2/2), int(y_menu2 + wymiary_menu2*3/2 - wymiary_menu2/2)))
            
            #info
            if wyswietl_info:
                pygame.draw.rect(screen, (130, 242, 179), (0,0, width, height))
                for i in range(len(tekst_info)):
                    tekst = font3.render(tekst_info[i], True, (0,0,0))
                    screen.blit(tekst, (width/2 - font3.size(tekst_info[i])[0]/2, height/2 - 50 + i*25))
                    
            if (x_menu2-wymiary_menu2/2 <= poz_myszy[0] <= x_menu2+wymiary_menu2/2) and (y_menu2-wymiary_menu2/2 - wymiary_menu2*3/2 <= poz_myszy[1] <= y_menu2+wymiary_menu2/2 - wymiary_menu2*3/2):
                if pygame.mouse.get_pressed()[0] and odkliknieto_myszke:
                    odkliknieto_myszke = False
                    wyswietl_info = not wyswietl_info
            
            pygame.draw.circle(screen, menu_kolor, (int(x_menu2), int(y_menu2 - wymiary_menu2*3/2)), int(wymiary_menu2/2))
            screen.blit(info_ikona, (int(x_menu2 - wymiary_menu2/2), int(y_menu2 - wymiary_menu2*3/2 - wymiary_menu2/2)))

            if not pygame.mouse.get_pressed()[0]:
                odkliknieto_myszke = True
            
            pygame.display.update()

        #Wszystko wypełniono
        #Dokładnie takie samo rozwiązanie
        if plansza_gracza == plansza or not run:
            break
        #Inne, ale poprawne rozwiązanie
        elif "✗" not in kolumny_czy_dobrze and "✗" not in rzedy_czy_dobrze:
            dobrze_uzupelnione = True
            for nr_pola in range(rozmiar**2):
                #Sprawdzam czy każdy namiot stoi obok jakiegoś drzewa i nie dotyka innych namiotów
                if plansza_gracza[nr_pola] == "x":
                    otoczenie_namiotu = [plansza_gracza[i] for i in znajdz_otoczenie(plansza_gracza, nr_pola, 9)]
                    if ("x" not in otoczenie_namiotu) and ("o" in otoczenie_namiotu):
                        pass
                    else:
                        dobrze_uzupelnione = False
                        break
            if dobrze_uzupelnione:
                break

        #Błędne rozwiązanie
        #print("Coś jest ŹLE!!!")
        sproboj_poprawic = True

    #Wygrana, wyszarza planszę
    if run:
        #print("Brawo, wszystko DOBRZE!!!")
        y = y_0
        for j in range(rozmiar):
            for i in range(rozmiar):
                if tryb == 0:
                    kolory = [min(symbole[plansza_gracza[j*rozmiar + i]][k] + 50, 255) for k in range(3)]
                    pygame.draw.rect(screen, tuple(kolory), (x, y, wymiary_pola, wymiary_pola)) 
                elif tryb == 1:
                    pygame.draw.rect(screen, (143, 222, 109), (x, y, wymiary_pola, wymiary_pola))
                    if plansza_gracza[j*rozmiar + i] == "o":
                        screen.blit(drzewo, (x+wymiary_pola/2 - drzewo.get_rect().size[0]/2 ,y+wymiary_pola/2 - drzewo.get_rect().size[1]/2))
                    elif plansza_gracza[j*rozmiar + i] == "x":
                        screen.blit(namiot, (x+wymiary_pola/2 - drzewo.get_rect().size[0]/2 ,y+wymiary_pola/2 - drzewo.get_rect().size[1]/2))

                x += wymiary_pola + wymiary_pola/5       
            x = x_0
            y += wymiary_pola + wymiary_pola/5

        tekst = font2.render("brawo!", True, (0,0,0))
        screen.blit(tekst, (width/2 - font2.size("brawo!")[0]/2, height/2 - font2.size("brawo!")[1]/2))
        pygame.display.update()

        #Opcje po wygranej: nowa gra i zamknięcie gry
        while run:
            if not pygame.mouse.get_pressed()[0]:
                odkliknieto_myszke = True
            poz_myszy = pygame.mouse.get_pos()
            if (x_menu <= poz_myszy[0] <= x_menu+wymiary_menu) and (y_menu <= poz_myszy[1] <= y_menu+wymiary_menu):
                if pygame.mouse.get_pressed()[0] and odkliknieto_myszke:
                    run = False
                    nowa_gra = True
                    break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    zakoncz = True
                    break
    if nowa_gra:
        pass
    elif zakoncz:
        pygame.quit()

def gra():
    pygame.init()
    width = 800
    height = 600
    screen = pygame.display.set_mode((width, height))
    pygame.draw.rect(screen, (130, 242, 179), (0,0, width, height))
    pygame.display.update()

    szer_start, wys_start = 200, 100
    x_start = width/2 - szer_start/2
    y_start = wys_start
    wymiary_wybor = (width - 200)*5/47
    y_wybor0 = y_start + wys_start + (height - (y_start+wys_start))/2 - wymiary_wybor*6/5
    x_wybor0 = 100

    font = pygame.font.Font('./pliki/Inter-Medium.ttf', int(wymiary_wybor/2))
    font2 = pygame.font.Font('./pliki/Inter-Medium.ttf', int(wymiary_wybor*2/5))
    font4 = pygame.font.Font('freesansbold.ttf', 60)

    drzewo = pygame.image.load("./pliki/drzewo_5.png")
    namiot = pygame.image.load("./pliki/namiot_5.png")

    menu_kolor = (140, 184, 255)
    
    run2 = True
    kliknieto_start = False
    while run2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run2 = False
                break

        #Przycisk START
        if not kliknieto_start:
            pygame.draw.rect(screen, (130, 242, 179), (0,0, width, height))
        pygame.draw.rect(screen, menu_kolor, (x_start, y_start, szer_start, wys_start))
        tekst = font.render("START", True, (0,0,0))
        screen.blit(tekst, (x_start + szer_start/2 - font.size("START")[0]/2, y_start + wys_start/2 - font.size("START")[1]/2))
    
        if (x_start <= pygame.mouse.get_pos()[0] <= x_start + szer_start) and (y_start <= pygame.mouse.get_pos()[1] <= y_start + wys_start) and pygame.mouse.get_pressed()[0]:
            kliknieto_start = True
            y_wybor = y_wybor0
            wybor_r, wybor_g, wybor_b = 150, 190, 255
            tekst = font2.render("wybierz rozmiar planszy (nxn)", True, (34, 46, 71))
            screen.blit(tekst, (width/2 - font2.size("wybierz rozmiar planszy (nxn)")[0]/2, y_start + wys_start + (y_wybor0 - y_start - wys_start)/2 - font2.size("wybierz rozmiar planszy (nxn)")[1]/2))
            for j in range(2):
                x_wybor = x_wybor0
                for i in range(8):
                    pygame.draw.rect(screen, (wybor_r,wybor_g,wybor_b), (x_wybor, y_wybor, wymiary_wybor, wymiary_wybor))
                    tekst = font.render(str(i+8*j+5), True, (255, 255, 255))
                    screen.blit(tekst, (x_wybor + wymiary_wybor/2 - font.size(str(i+8*j+5))[0]/2, y_wybor + wymiary_wybor/2 - font.size(str(i+8*j+5))[1]/2))
                    x_wybor += wymiary_wybor*6/5
                    wybor_r -= 10
                    wybor_g -= 8
                y_wybor += wymiary_wybor*6/5
        
        #Wybór poziomu
        if kliknieto_start:
            poz_myszy_wybor = pygame.mouse.get_pos()
            if (x_wybor0 <= poz_myszy_wybor[0] <= x_wybor0 + (width - 200)) and (y_wybor0 <= poz_myszy_wybor[1] <= y_wybor0+(wymiary_wybor*11/5)) and pygame.mouse.get_pressed()[0]:
                wybor_poziomu = int((poz_myszy_wybor[0]-x_wybor0)/((width - 200)/8)) + 8*int((poz_myszy_wybor[1]-y_wybor0)/(wymiary_wybor*11/5/2))       
                #jeśli wystąpi jakiś błąd
                if wybor_poziomu > 15:
                    pass
                else:
                    #ROZPOCZYNA POZIOM
                    nowy_poziom(wybor_poziomu+5, width, height, screen)
                    #nowa gra
                    try:
                        kliknieto_start = False
                        pygame.draw.rect(screen, (130, 242, 179), (0,0, width, height))
                    #koniec, już zamknięto pygame
                    except:
                        break
        else:
            screen.blit(namiot, (width/2 - namiot.get_rect().size[0] - 20, y_start + wys_start + (height - y_start - wys_start)/2 - namiot.get_rect().size[1]/2))
            screen.blit(drzewo, (width/2 + 20, y_start + wys_start + (height - y_start - wys_start)/2 - drzewo.get_rect().size[1]/2))
            tekst = font4.render("i", True, (34, 46, 71))
            screen.blit(tekst, (width/2 - font4.size("i")[0]/2, y_start + wys_start + (height - y_start - wys_start)/2 - namiot.get_rect().size[1]/4))

        pygame.display.update()
        
    #koniec, jeszcze nie zamknięto pygame
    if not run2:
        pygame.quit()

############################################
gra()
############################################
#TESTY
a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p']
def t(litera, rodzaj):
    for i in znajdz_otoczenie(a, ord(litera)-97, rodzaj):
            print(a[i])

def srednia_drzew(rozmiar, proba):
    stats = [generuj_plansze(rozmiar).count("o") for i in range(proba)]
    print(sum(stats)/proba)

['-', '-', '-', 'x', '-', 'x', '-', 'x', '-', '-', 'o', '-', 'o', '-', 'o', 'o', '-', '-', 'o', '-', '-', '-', 'x', '-', '-', 'x', 'o', 'x', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'o', '-', '-', 'x', '-', '-', '-', 'x', '-', '-', 'o', '-']

#https://www.flaticon.com/free-icons/tent tent icons Tent icons created by Freepik - Flaticon
