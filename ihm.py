import cv2, numpy, time, tkinter, os.path
from tkinter import *
from tkinter import filedialog
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

        #Bouton d'arret du script
        self.quitButton = Button(frame, text="Quitter", command=frame.quit)
        self.quitButton.grid(row=3, column=0, sticky=W)

        #option d'affichage dans l'explorateur de fichier
        self.file_opt = options = {}
        options['filetypes'] = [('all files', '.*'), ('video files', '.avi')]
        options['parent'] = master


    def streamingVideo(self):

        while (self.video.isOpened()):
            #Creation d'un frameobject
            check, frame = self.video.read()

            #streaming de la capture
            cv2.imshow("Capture en cours", frame)

            #Appuyer sur s pour sauvegarder
            if cv2.waitKey(1) == ord('s'):
                self.sauvegarderVideo()
            #Appuyer sur 'a' pour arreter le streaming
            if cv2.waitKey(1) & 0xFF == ord('a'):
                cv2.destroyAllWindows()
                break


    def sauvegarderVideo(self):
        #Creation et recuperation du chemin absolu de sauvegarde
        self.path = filedialog.asksaveasfilename(**self.file_opt)
        head, tail = os.path.split(self.path)
        if not os.path.exists(self.path):
            os.makedirs(tail)
        fichier = open(self.path + '.avi', "ab")
        #Definition du codec et creation de l'objet de sauvegarde de la video
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter(self.path +'.avi',fourcc, 20.0, (640,480))
        while(self.video.isOpened()):
            #Creation d'un frameobject
            frame = self.video.read()
            #Enregistrement des images composant la video
            out.write("frame",frame)
            #Appuyer sur z pour stopper l'enregistrement
            if cv2.waitKey(1) & 0xFF == ord('z'):
                out.close()
                fichier.close()
                break







#Main effectif
mainWin = Tk()
#Taille minimale de la fenetre principale
mainWin.geometry("280x220")
a = EveryThing(mainWin)
mainWin.mainloop()
