import cv2, numpy, time, tkinter, os.path
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from shutil import copy2
from os.path import *
from tkinter.ttk import *    # Widgets avec thèmes
from fenSauvegarde import *
from sys import *

#TODO:Top priority : intégrer le nommage
#Ajout bouton avant streaming => choix contexte => donne path absolu racine + le nom du dossier du geste
    #Il faut saisir lors de la sauvegarde le numero de l'échantillon et le scenario

#Nomenclature : choisir la racine de tous les gestes
#   Pour chaque geste
#Faire les fenetre : - Lister les shoot
#                    - liste postroduction (cf chgt resolution)
#                    -
#Checkbox Noir&Blanc en face de sauvegarderVideoButton
#Pour le changement de resolution =>un bouton sur la fenetre principale,
#   ouvre une autre boite de dialogue de checkbox des video prisent et des different niveau de qualité
#   un bouton run et quit
#   Bonus : Mettre des options d'affichage de liste pour prendre en compte les vid couleur et N&B
class EveryThing(Tk):

    #Creation attribut
    video = cv2.VideoCapture(0)
    path = ""
    capture = False
    r = 1

    workPath = './'     # c'est le path qui sera ajouté au nom des fichiers à enregistrer
                        # il n'est valide que si Geste et Personne ne sont pas vides
    Geste = ""          # rempli par listeGestes.get()
    Personne = ""       # rempli par listePersonnes.get()


    def __init__(self):

        Tk.__init__(self)    # On dérive de Tk, on reprend sa méthode d'instanciation

        self.lGeste = Label(self, text = 'Geste  ')
        self.lGeste.grid(row=self.r, column=0, pady=1, sticky=E)

        self.gesteSelect = StringVar()
        self.stockGestes = ('', )
        # on regarde les Gestes existants
        self.stockGestes = ('',)       # tuple vide
        for dir, nmD, nmF in os.walk(self.workPath):
            if (len(nmD) != 0):
                for rnmD in nmD:
                    if (rnmD != "__pycache__"):
                        self.stockGestes += (rnmD,)
            break           # on n'explore que la racine


        self.listeGestes = Combobox(self, textvariable = self.gesteSelect, \
                        values = self.stockGestes, state = 'normal')
        self.listeGestes.bind('<<ComboboxSelected>>', self.mSelGeste)
        self.listeGestes.bind('<Return>', self.mCreerGeste)

        # Placement des widgets
        self.listeGestes.grid(row=self.r, column=1, pady=1, sticky=W)
        self.r+=1

        self.lGeste = Label(self, text = 'Personne  ')
        self.lGeste.grid(row=self.r, column=0, pady=1, sticky=E)

        self.personneSelect = StringVar()
        self.stockPersonnes = ('', )
        self.listePersonnes = Combobox(self, textvariable = self.personneSelect, \
                        values = self.stockPersonnes, state = 'normal')
        self.listePersonnes.bind('<<ComboboxSelected>>', self.mSelPersonne)
        self.listePersonnes.bind('<Return>', self.mCreerPersonne)

        # Placement des widgets
        self.listePersonnes.grid(row=self.r, column=1, pady=1, sticky=W)
        self.r+=1

        #Bouton de streaming
        self.streamButton = Button(self, text="Streaming", command=self.streamingVideo)
        self.streamButton.grid(row=self.r, column=0, columnspan=2, padx=5, pady=8)
        self.r+=1
        #Bouton debut de sauvegarde temporaire
        self.tempSaveButton = Button(self, text="Debut enregistrement temp (s)", command=self.decodageCommande('s'))
        self.tempSaveButton.grid(row=self.r, column=0, padx=5, pady=1, sticky=E)
        #self.r+=1
        #Bouton de fin enregistrement
        self.endSaveTempButton = Button(self, text="Finir l'enregistrement (z)", command=self.decodageCommande('z'))
        self.endSaveTempButton.grid(row=self.r, column=1, sticky=W, padx=5, pady=1)
        self.r+=1
        #Bouton abort enregistrement
        self.abortSaveTempButton = Button(self, text="Annuler l'enregistrement (a)", command=self.decodageCommande('a'))
        self.abortSaveTempButton.grid(row=self.r, column=0, columnspan=2, padx=5, pady=1)
        self.r+=1
        #Bouton de visionnage de la derniere video
        self.lastVidButton = Button(self, text="Regarder derniere video", command=self.regarderDerniereVideo)
        self.lastVidButton.grid(row=self.r, column=0, padx=5, pady=8)
        #self.r+=1
        #Bouton de sauvegarde
        self.saveVidButton = Button(self, text="Sauvegarder Video", command=self.sauvegarderVideoQ)
        self.saveVidButton.grid(row=self.r, column=1, padx=5, pady=8)
        self.r+=1
        #Bouton de lecture de n'importe quelle video
        self.viewingVideoButton = Button(self, text="Lecture", command=self.viewVideo)
        self.viewingVideoButton.grid(row=self.r, column=0, columnspan=2, padx=5, pady=5)
        #self.r+=1
        #Bouton d'arret du script
        self.quitButton = Button(self, text="Quitter", command=self.finProgramme)
        self.quitButton.grid(row=self.r, column=1, sticky=E)
        self.r+=1


        #option d'affichage dans l'explorateur de fichier
        self.file_opt = options = {}
        options['filetypes'] = [('video files', '.avi')]
#        options['parent'] = master

    # Méthodes de sélection ou de création des gestes et des personnes

    def mSelGeste(self, event):
        self.Geste = self.gesteSelect.get()
        # si on a changé de geste, on ne sait plus pour a priori quelle personne
        self.personneSelect.set(self.stockPersonnes[0])
        # mais on peut rechercher quelles sont celles qui existent déjà
        wrkPath = self.workPath + self.Geste + "/"
        self.stockPersonnes = ('',)       # tuple vide
        for dir, nmD, nmF in os.walk(wrkPath):
            if (len(nmD) != 0):
                self.stockPersonnes += (nmD,)
        # mise à jour de la liste
        self.listePersonnes.configure(values = self.stockPersonnes)


    def mCreerGeste(self, event):
        #print(event)
        nvGeste = self.gesteSelect.get()
        self.stockGestes += nvGeste,
        self.listeGestes.configure(values = self.stockGestes)
        # le répertoire n'existe pas, on le crée
        os.mkdir(self.workPath + nvGeste)
        # on sait alors que la liste des personnes est vide
        self.stockPersonnes = ('',)       # tuple vide
        self.Geste = nvGeste


    def mSelPersonne(self, event):
        self.Personne = self.personneSelect.get()
        #print(event)

    def mCreerPersonne(self, event):
        #print(event)
        self.stockPersonnes += self.personneSelect.get(),
        self.listePersonnes.configure(values = self.stockPersonnes)
        nvPersonne = self.personneSelect.get()
        self.stockPersonnes += nvPersonne,
        self.listePersonnes.configure(values = self.stockPersonnes)
        # le répertoire n'existe pas, on le crée
        os.mkdir(self.workPath + self.Geste + "/" + nvPersonne)
        self.Personne = nvPersonne

#Ouverture du flux camera et affichage a l'ecran
    def streamingVideo(self):
        while (self.video.isOpened()):
            #Creation d'un frameobject
            check, frame = self.video.read()
            #streaming de la capture
            cv2.imshow("Streaming en cours", frame)
            c = cv2.waitKey(1)
            cde = self.decodageCommande(c)
            if(cde == -3):
                cv2.destroyAllWindows()
                break

    def setCapture(self, capture):
        if(capture):
            pass
        else:
            pass

    def decodageCommande(self,c):
        if(c == -1): #pas de caractere disponible
            return 0
        #Retourne 0 quand une commande est executee, retourne -1 pour cacher le flux video
        if (self.capture == False):
            #Appuyer sur s pour sauvegarder
            if c == ord('s'):
                self.capture = True
                self.sauvegarderTempVideo()
                return -3
        else:
            #Appuyer sur 'z' pour arreter le streaming et garder le fichier temporaire
            if c & 0xFF == ord('z'):
                cv2.destroyAllWindows()
                return -1
        #Appuyer sur 'a' pour arreter le streaming et detruire le fichier temporaire
        if c == ord('a'):
            cv2.destroyAllWindows()
            return -2

#Sauvegarde dans un fichier temporaire
    def sauvegarderTempVideo(self):
        #TODO: Si le fichier temp existe => Demander à l'écraser ou a le sauvegarder malgre tout
        self.capture = True
        #Destruction des fenetre pour eviter des freezes
        cv2.destroyAllWindows()
        #Definition du codec et creation de l'objet de sauvegarde de la video
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter('temp.avi',fourcc, 15.0, (640,480))
        while(self.video.isOpened()):
            #Creation d'un frameobject
            check, frame = self.video.read()
            cv2.imshow("Sauvegarde en cours", frame)
            #Enregistrement des images composant la video
            out.write(frame)
            #recuperation entree clavier
            c = cv2.waitKey(1)
            cde = self.decodageCommande(c)
            #Appuyer sur z pour stopper l'enregistrement
            if (cde == -1):
                #Liberation des fenetres et de l'objet de sauvegarde
                self.capture = False
                cv2.destroyAllWindows()
                out.release()
                break
            #Appuer sur a pour arreter la sauvegarde et destuire le fichier temporaire
            elif (cde == -2):
                self.capture = False
                cv2.destroyAllWindows()
                out.release()
                os.remove(os.path.abspath("temp.avi"))
                break

#Sauvegarde definitive du fichier temporaire
#avant l'appel de cette (a l'appui)
    def sauvegarderVideoQ(self):
        if (self.Geste == "" or self.Personne == ""):
            # on indique qu'il manque des infos
            messagebox.showwarning("Sauvegarde impossible","Les cases 'Geste' ou 'Personne' n'ont pas été remplies")
        else:
            self.fenS = FenSauvegarde(self)
            self.fenS.grid(row=1, column=6, padx=10, pady=5, rowspan=6, sticky=E)


    def sauvegarderVideo(self):

        #TODO: Si le fichier temp n'existe pas => ouvrir boite de message et retour
        #Récupération du chemin absolu de la video temporaire
        pathsrc = os.path.abspath('temp.avi')
        #Récupération du chemin absolu du dossier destination

        # TODO : il faut regarder si on enregistre en couleur seult ou aussi en niveaux de gris
        # TODO : il faut qu'il y ait une liste des scénarios

        Scenario = 'BLANC'      # pour le test, en attendant la liste déroulante

        #pathdest = filedialog.asksaveasfilename(**self.file_opt, title="Choississez le dossier destination")
        if (self.Geste != "" and self.Personne != ""):
            pathdest = self.workPath + self.Geste+ "/" + self.Personne + "/" + Scenario + '-' + 'COUL' + '_' + '00' + '.avi'
        else:
            # on indique qu'il manque des infos
            messagebox.showwarning("Sauvegarde impossible","Les cases 'Geste' ou 'Personne' n'ont pas été remplies")
            return

        #Copie de la video
        copy2(pathsrc, pathdest)

    #Test de l'existence du fichier temp.avi
    def existTemp(self, mfile):
        return os.path.exists(os.path.abspath(mfile))

    #Test de l'existence d'un fichier deja enregistré
    def existFileRegistered(self, mfile):
        return os.path.exists(os.path.abspath(mfile))

    def regarderDerniereVideo(self):
        #TODO: Si le fichier temp n'existe pas => ouvrir boite de message et retour
        #Destruction des fenetre pour eviter des freezes
        cv2.destroyAllWindows()
        #test existence du fichier temp
        if(self.existTemp('temp.avi')):
            #Recuperation du fichier a visioner
            lastVid = cv2.VideoCapture("temp.avi")
            #boucle de visionage
            while (lastVid.isOpened()):
                #Creation d'un frameobject
                check, frame = lastVid.read()
                #Visionage de la video enregistrée
                if(check==True):
                    cv2.imshow('Derniere video capturee',frame)
                #Appuyer sur q pour arreter le visionage de video, 50 ici defini la vitesse de lecture
                #Plus le nombre est petit, plus la video va vite
                    if cv2.waitKey(35) & 0xFF == ord('q'):
                        break
                else:
                    break
        else:
            print("file doesn't exist")

        #Liberation des objets
        lastVid.release()
        cv2.destroyAllWindows()

    def viewVideo(self):
        #Destruction des fenetre pour eviter des freezes
        cv2.destroyAllWindows()
        ##Selection du fichier a visioner
        fichier = filedialog.askopenfilename(**self.file_opt)
        try:
            os.path.exists(fichier)
        except FileNotFoundError:
            pass
        else:
            vid = cv2.VideoCapture(fichier)
            #boucle de visionage
            while (vid.isOpened()):
                #Creation d'un frameobject
                check, frame = vid.read()
                if(check == True):
                    #Visionage de la video enregistrée
                    cv2.imshow(fichier,frame)
                    #Appuyer sur q pour arreter le visionage de video, 50 ici defini la vitesse de lecture
                    #Plus le nombre est petit, plus la video va vite
                    if cv2.waitKey(50) & 0xFF == ord('q'):
                        break
                else:
                    break

            #Liberation des objets
            vid.release()
            cv2.destroyAllWindows()


    def fermerSauver(self):
        self.fenS.destroy()

    def finProgramme(self):
        self.quit()

#Main effectif
#mainWin = Tk()
#Taille minimale de la fenetre principale
#mainWin.geometry("320x300")
#mainWin.geometry('+0+0')
a = EveryThing()
a.mainloop()
#a.quit()
