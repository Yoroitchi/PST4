import cv2, numpy, time, tkinter, os.path
from tkinter import *
from tkinter import filedialog
from shutil import copy2
from os.path import *

class EveryThing:

    #Creation attribut
    video = cv2.VideoCapture(0)
    path = ""
    capture = False

    def __init__(self,master):

        #Definition du conteneur des widget
        frame = Frame(master)
        frame.place(x=0,y=0)

        #Bouton de streaming
        self.streamButton = Button(frame, text="Streaming", command=self.streamingVideo)
        self.streamButton.grid(row=1, column=0, sticky=W)

        #Bouton de visionnage de la derniere video
        self.lastVidButton = Button(frame, text="Regarder derniere video", command=self.regarderDerniereVideo)
        self.lastVidButton.grid(row=2, column=0, sticky=W)

        #Bouton de sauvegarde
        self.saveVidButton = Button(frame, text="Sauvegarder Video", command=self.sauvegarderVideo)
        self.saveVidButton.grid(row=3, column=0, sticky=W)

        #Bouton d'arret du script
        self.quitButton = Button(frame, text="Quitter", command=frame.quit)
        self.quitButton.grid(row=4, column=0, sticky=W)

        #option d'affichage dans l'explorateur de fichier
        self.file_opt = options = {}
        options['filetypes'] = [('video files', '.avi')]
        options['parent'] = master


    def streamingVideo(self):

        while (self.video.isOpened()):
            #Creation d'un frameobject
            check, frame = self.video.read()
            #streaming de la capture
            cv2.imshow("Capture en cours", frame)
            #Appuyer sur s pour sauvegarder
            if cv2.waitKey(5) == ord('s'):
                self.sauvegarderTempVideo()
            #Appuyer sur 'a' pour arreter le streaming
            if cv2.waitKey(5) & 0xFF == ord('a'):
                cv2.destroyAllWindows()
                break


    def sauvegarderTempVideo(self):
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
            #Appuyer sur z pour stopper l'enregistrement
            if cv2.waitKey(5) & 0xFF == ord('z'):
                #Liberation des fenetres et de l'objet de sauvegarde
                cv2.destroyAllWindows()
                out.release()
                break

    def sauvegarderVideo(self):
        #Récupération du chemin absolu de la video temporaire
        pathsrc = os.path.abspath('temp.avi')
        #Récupération du chemin absolu du dossier destination
        pathdest = filedialog.asksaveasfilename(**self.file_opt, title="Choississez le dossier destination")
        #Copie de la video
        copy2(pathsrc, pathdest)


    def regarderDerniereVideo(self):
        #Destruction des fenetre pour eviter des freezes
        cv2.destroyAllWindows()
        #Recuperation du fichier a visioner
        lastVid = cv2.VideoCapture("temp.avi")
        #boucle de visionage
        while (lastVid.isOpened()):
            #Creation d'un frameobject
            check, frame = lastVid.read()
            if(check == True):
                #Visionage de la video enregistrée
                cv2.imshow('frame',frame)
                #Appuyer sur q pour arreter le visionage de video, 50 ici defini la vitesse de lecture
                #Plus le nombre est petit, plus la video va vite
                if cv2.waitKey(50) & 0xFF == ord('q'):
                    break
            else:
                break

        #Liberation des objets
        lastVid.release()
        cv2.destroyAllWindows()



#Main effectif
mainWin = Tk()
#Taille minimale de la fenetre principale
mainWin.geometry("280x220")
mainWin.geometry('+0+0')
a = EveryThing(mainWin)
mainWin.mainloop()
