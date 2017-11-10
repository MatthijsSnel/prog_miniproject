import requests
import xmltodict
from tkinter import *
from tkinter.tix import *

def menu(foutePoging):                                                                                                  #BeginMenu
    root = Tk()
    root.geometry('{}x{}'.format(285, 500))                                                                             #Formaat van frame
    global beginFrame                                                                                                   #Maakt globaal zodat ze buiten de functie aangeroepen kunnen worden
    beginFrame = Frame(master=root, background='DarkGoldenrod1')                                                        #Leeg frame met NS Geel
    beginFrame.pack(fill="both", expand=True)
    global beginEntry                                                                                                   #Maakt globaal zodat ze buiten de functie aangeroepen kunnen worden
    beginEntry = Entry(master=beginFrame, background='royal blue')                                                      #Tekst vak die vraagt naar stationsnaam van welk je de vertrektijden wilt weten, achtergrond Blauw
    beginEntry.pack(side=LEFT,pady=10)
    global beginButton                                                                                                  #Maakt globaal zodat ze buiten de functie aangeroepen kunnen worden
    beginButton = Button(master=beginFrame, text='Vertrektijden', command=vertrekTijdenApi, background='royal blue')    #Knop die gaat naar volgend frame
    beginButton.pack(side=RIGHT, pady=10)
    if foutePoging == True:                                                                                             #Zodra er een keer een foute invoer is geweest print "Foute invoer"
        print('Foute invoer')
        foutePoging = False
        global foutMelding
        foutMelding = Label(root, text='Foute invoer, probeer opnieuw.', justify='left')
        foutMelding.pack()
    else:                                                                                                               #Zo niet print "Voer een stationnaam in..."
        global helpMelding
        helpMelding = Label(root, text='Voer een Stationnaam in om vertrektijden te zien.', justify='left')
        helpMelding.pack()
    root.mainloop()

def vertrekTijdenApi():                                                                                                 #Aanvragen van vertrektijden
    with open('afkortingen.txt', 'r') as afk:                                                                           #Opent de lijst met afkortingen van stationsnamen
        afkortingen = {}                                                                                                #Maakt een dictionary
        for line in afk:                                                                                                #Zorgt ervoor dat alle waardes van de TXT file in de dictionary terecht komen
            splitted = line.split(':')
            afkortingen[splitted[1]] = splitted[0]
        try:
            stationAfk = afkortingen[beginEntry.get()+'\n']                                                             #Zoekt binnen de dictionary naar de juiste afkorting die bij het eerder benoemde station hoort
        except KeyError:
            foutePoging = True                                                                                          #Mocht er binnen de dictionary geen dergelijke naam bestaat zorgt het ervoor dat er een melding in het scherm komt
            menu(foutePoging)
    auth_details = ('julian-buursink@hotmail.com', 'aTeJTE91dPyeU0lLsZtHR1l4bw5w8qXPKBLlc7un54hbRsmp7E6lDQ')            #Inloggegevens voor API                                                                                   #Maakt van de invoer een variabele
    api_url = 'http://webservices.ns.nl/ns-api-avt?station=' + stationAfk                                               #neemt de var en maakt de link er mee af
    response = requests.get(api_url, auth=auth_details)                                                                 #Neemt de ontvangen response en zet deze in een variabele
    vertrekXML = xmltodict.parse(response.text)                                                                         #Vervolgens wordt er een XML file van gemaakt
    vertrekTijdenNaarTxt(vertrekXML)                                                                                    #Volgende functie wordt aangeroepen

def vertrekTijdenNaarTxt(vertrekXML):                                                                                   # XML -> TXT -> TKinter
    with open('tekst.txt', 'w') as tekst:                                                                               # Maakt een nieuw TXT file aan
        for vertrek in vertrekXML['ActueleVertrekTijden']['VertrekkendeTrein']:                                         # Alle informatie van het XML file wordt overzichtelijk genoteerd in een txt file
            eindbestemming = vertrek['EindBestemming']
            vertrektijd = vertrek['VertrekTijd'] # 2016-09-27T18:36:00+0200
            vertrektijd = vertrektijd[11:16] # 18:36
            treinsoort = vertrek['TreinSoort']
            try:                                                                                                        #Mocht er vertraging zijn, wordt dat er ook bij vermeld
                routetekst = 'Via ' + vertrek['RouteTekst']
            except KeyError:
                routetekst = 'Zonder tussenstop'
            try:
                vertrekVertraging = vertrek['VertrekVertragingTekst'] + ' vertraging' + '\n \n'
            except KeyError:
                vertrekVertraging = '\n'
            tekst.write('{} {}\n      {}\n      {}\n      {}'.format(vertrektijd,eindbestemming,treinsoort,routetekst,vertrekVertraging))    #Maakt er een Text file van
    helpMelding.pack_forget()
    beginEntry.pack_forget()
    beginButton.pack_forget()
    beginFrame.pack_forget()
    printTkinter()

def printTkinter():                                                                                                     #Het eindresultaat wordt geprint op het scherm
    with open('tekst.txt', 'r') as tekst1:                                                                              #Opent de eerder gemaakte TXT file en haalt hieruit de informatie
        uitlezen = tekst1.readlines()
        uitlezen1 = ''
        for i in uitlezen:                                                                                              #Haalt onnodige tekens weg
            if i == '{' or i == '}':
                i = ''
            uitlezen1 += i
    frame = Frame(width="500", height="500")
    frame.pack()
    swin = ScrolledWindow(frame, width=500, height=500)
    swin.pack()
    win = swin.window
    label = Label(win, text=uitlezen1, justify='left',background='DarkGoldenrod1')                                      #Print in TKinter
    label.pack()

foutePoging = False
menu(foutePoging)


