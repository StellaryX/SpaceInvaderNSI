########################################################################
#   Nom du projet : Space Invader                                      #
#   Nom de l'auteur : Théo BLANDIN                                     #
#   Date de création : Du 07/09 au 09/10                               #
#                                                                      #
#   Entrée : Touches du clavier                                        #
#   Sortie : Fenêtre graphique + partie non graphique                  #
#                                                                      #
#   Détail du projet : Reconstitution du jeu Space Invader. Le but est #
#   donc de tuer tout les ennemis présent à chaque vagues sans perdre  #
#   ses trois vie mais tout en gagnant un maximum de points.           #
#                                                                      #
#   Lien externe du projet : #
#                                                                      #
########################################################################

import random
import pygame  # Importation de la bibliothèque "pygame"
from pygame.locals import *  # Importation de toutes les class "pygame"

pygame.init()

#On initialise une  "clock" pour définir la vitesse de notre jeu
clock = pygame.time.Clock()

#On défini les variables hauteur et largeur pour notre fenêtre
largeur_fenetre = 500   #Nombre de pixels en largeur
hauteur_fenetre = 800   #Nombre de pixels en hauteur

police_écriture_principale = pygame.font.Font("SpaceInvader/SpaceInvaderIMG/DS-DIGII.TTF", 32)

logo = pygame.image.load("SpaceInvader/SpaceInvaderIMG/vaisseau.png")
pygame.display.set_icon(logo)

#On créer la fenêtre avec pour paramètre, hauteur et largeur
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
#On ajoute un nom à la fenêtre
pygame.display.set_caption('Space Invader')

#On charge l'image de fond pour la fenêtre
fond = pygame.image.load("SpaceInvader/SpaceInvaderIMG/BackgroundInvader.png")

#On charge une autre image qui elle servira de GUI
borne = pygame.image.load("SpaceInvader/SpaceInvaderIMG/borne.png")
joystick = pygame.image.load("SpaceInvader/SpaceInvaderIMG/Joystick.png")
joystick_droit = pygame.image.load("SpaceInvader/SpaceInvaderIMG/Joystick_droit.png")
joystick_gauche = pygame.image.load("SpaceInvader/SpaceInvaderIMG/Joystick_gauche.png")
spacebuttonoff = pygame.image.load("SpaceInvader/SpaceInvaderIMG/SpaceButtonOff.png")
spacebuttonon = pygame.image.load("SpaceInvader/SpaceInvaderIMG/SpaceButtonOn.png")
life_barre = pygame.image.load("SpaceInvader/SpaceInvaderIMG/life_barre.png")
gameoverscreen = pygame.image.load("SpaceInvader/SpaceInvaderIMG/GameOverScreen.png")

#On défini quelques variables pour nos class/fonction
rangés = 4   #La variable "rangés" vaut 4
colonne = 6 #La variable "colonne" vaut 6
ennemies_laser_cooldown = 500   #Le cooldown(temps d'attente) est défini à 500ms
dernier_tir_ennemies = pygame.time.get_ticks()  #La variable est égale à la fonction "get_ticks"(on récupère le nombre de ticks) du module pygame.time

class MainGame(pygame.sprite.Sprite):
    print("############################ Début de la partie ############################")
    print("Tu commence à la vague 1")
    print("Tu commence avec 3 vies")
    print("Tu commence avec 0 point")
    print("#######################################################################")
    
    def __init__(self,point_player=0, vague=1, fps=60):
        pygame.sprite.Sprite.__init__(self) #La methode "__init__" est donc associer à un groupe avec sprite
        self.point_joueur = point_player
        self.dernier_tir = pygame.time.get_ticks()  #La variable est égale à la fonction "get_ticks"(on récupère le nombre de ticks) du module pygame.time
        self.vagues = vague
        self.getfps = fps

#On créer une Class Vaisseau pour paramètre la Class Sprite du module sprite lui même dans le module pygame. Permettre d'ajouter la Class Vaisseau à un groupe
class Vaisseau(pygame.sprite.Sprite):
    #On défini la methode "__init__" avec self, x et y en paramètre
    def __init__(self, x, y, life, cooldown_spawn=0, vitesse_joueur=5, cooldown=1):
        pygame.sprite.Sprite.__init__(self) #La methode "__init__" est donc associer à un groupe avec sprite
        self.image = pygame.image.load("SpaceInvader/SpaceInvaderIMG/vaisseau.png")  #On charge l'image "vaisseau.png" à la fonction "image" qui sera mis sur la surface de la fenêtre
        self.rect = self.image.get_rect()   #On récupère avec "get.rect", la zone de collision de l'image pour l'associer à la fonction "rect" qui est donc la collision
        self.rect.center = [x, 600] #On place donc la collision qui contient l'image, donc au centre de la fenêtre et à 600 pixels en y
        self.vie_début = life
        self.vie_restante = life
        self.dernier_tir = pygame.time.get_ticks()  #La variable est égale à la fonction "get_ticks"(on récupère le nombre de ticks) du module pygame.time
        self.cooldownspawn = cooldown_spawn
        self.vitesse_joueur = vitesse_joueur
        self.cooldawntir = cooldown
        
    #On défini la fonction "update" avec self en paramètre pour que la fonction soit associer seulement à la Class Vaisseau
    def update(self):
        #On initialise les variables qu'on va utiliser dans "update"
        touche = pygame.key.get_pressed()   #On créer la variable qui est égale à la fonction "get_pressed" qui permet de détécter si une touche est pressé
        temps_laser = pygame.time.get_ticks()   #La variable est égale à la fonction "get_ticks"(on récupère le nombre de ticks) du module pygame.time
        
        #On ajoute des "if" qui vérifient si une touche est préssée, si oui une action va s'effectuer
        if touche[pygame.K_q] and self.rect.left > 0:   #Si la touche "a" est préssée et que la zone de collision soit supérieur à 0 en partant de la gauche
            self.rect.x -= self.vitesse_joueur   #On enlève la valeur de vitesse_joueur à la zone de collision en x
        if touche[pygame.K_d] and self.rect.right < largeur_fenetre:    #Si la touche "d" est préssée et que la zone de collision soit inférieur à la largeur de la fenêtre (droite)
            self.rect.x += self.vitesse_joueur  #On ajoute la valeur de vitesse_joueur à la zone de collision en x
        if touche[pygame.K_SPACE] and temps_laser - self.dernier_tir > self.cooldawntir:    #Si la touche "espace" est préssée et que le temps du laser - le temps du dernier tir soit supérieur au temps de rechargement
            laser = Laser(self.rect.centerx, self.rect.top) #On créer la variable laser qui est égale à la Class Laser avec la zone de collision centre en x et tout en haut pour le laser
            laser_group.add(laser)  #On ajoute la variable laser au groupe "laser_group"
            self.dernier_tir = temps_laser #On défini que la variable dernier_tir de __init__ est égale au temps de temps_laser

#On créer une Class Laser pour paramètre la Class Sprite du module sprite lui même dans le module pygame. Permettre d'ajouter la Class Laser à un groupe
class Laser(pygame.sprite.Sprite):
    #On défini la methode "__init__" avec self, x et y en paramètre
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) #La methode "__init__" est donc associer à un groupe avec sprite
        self.image = pygame.image.load("SpaceInvader/SpaceInvaderIMG/laser.png") #On charge l'image "laser.png" à la fonction "image" qui sera mis sur la surface de la fenêtre
        self.rect = self.image.get_rect()   #On récupère avec "get.rect", la zone de collision de l'image pour l'associer à la fonction "rect" qui est donc la collision
        self.rect.center = [x, y]   #On place donc la collision qui contient l'image, donc au centre de la fenêtre en x et à une valeur de y
        
    #On défini la fonction "update" avec self en paramètre pour que la fonction soit associer seulement à la Class Laser
    def update(self):
        self.rect.y -= 5    #On défini la valeur de y de la zone de collision de l'image "laser.png" avec un déplacement de -5 en y
        if self.rect.bottom < 0:    #On vérifie sur le bas de la zone de collision est inferieur à 0
            self.kill() #Alors ici, on utilise la méthode "kill" pour supprimer l'image qui répond à la condition if
        if pygame.sprite.spritecollide(self, ennemies_group, True): #Si la zone de collision d'un groupe(sprite) ici du groupe ennemies_group. Avec le paramètre "True" et bien il faut que la condition soit absolument Vrai
            self.kill() #On supprime l'image du vaisseau ennemies touché par le laser du joueur
            maingame.point_joueur += random.randint(25, 50)
            vaisseau.cooldownspawn += 1
            
#On créer une Class Ennemies pour paramètre la Class Sprite du module sprite lui même dans le module pygame. Permettre d'ajouter la Class Ennemies à un groupe
class Ennemies(pygame.sprite.Sprite):
    #On défini la methode "__init__" avec self, x et y en paramètreqqqq
    def __init__(self, x, y, nbmouvement=0, mouvement=1):
        pygame.sprite.Sprite.__init__(self) #La methode "__init__" est donc associer à un groupe avec sprite
        self.image = pygame.image.load("SpaceInvader/SpaceInvaderIMG/ennemies" + str(random.randint(1, 3)) + ".png") #On défini la variable "image" au chargement de l'image "ennemies.png" mais ici avec de l'aléatoire
        self.rect = self.image.get_rect()   #On récupère avec "get.rect", la zone de collision de l'image pour l'associer à la fonction "rect" qui est donc la collision
        self.rect.center = [x, y]   #On place donc la collision qui contient l'image, donc au centre de la fenêtre en x et à une valeur de y
        self.compteur_mouvement = nbmouvement #On défini la variable compteur_mouvement à 0
        self.sens_mouvement = mouvement #On défini la variable sens_mouvement à 1

    #On défini la fonction "update" avec self en paramètre pour que la fonction soit associer seulement à la Class Ennemies
    def update(self):
        self.rect.x += self.sens_mouvement  #On ajoute la valeur de sens_mouvement à la zone de collision en x
        self.compteur_mouvement += 1    #On ajoute +1 a la variable compteur_mouvement
        if abs(self.compteur_mouvement) > 50:   #Si la fonction "abs" qui retourne une valeur absolue d'un argument avec compteur_mouvement en paramètre est plus grande que 50 pixels
            self.sens_mouvement *= -1   #On inverse le sens de sens_mouvement (-1)
            self.compteur_mouvement *= self.sens_mouvement  #On multiplie la variables compteur_mouvement à sens_mouvement

#On créer les différents groupe grâce au module sprite
vaisseau_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
ennemies_group = pygame.sprite.Group()
ennemies_laser_group = pygame.sprite.Group()
maingame_group = pygame.sprite.Group()

#On créer la variable vaisseau qui elle fait appel à la class Vaisseau et qui contient donc les position que doit prendre le vaisseau du joueur
vaisseau = Vaisseau(int(largeur_fenetre / 2), hauteur_fenetre - 150, 3)
vaisseau_group.add(vaisseau)    #On ajoute la variable vaisseau au groupe vaisseau_group

maingame = MainGame()
maingame_group.add(maingame)

ennemies = Ennemies(int(1000), 1000)
ennemies_group.add(ennemies)

#On créer une Class Ennemies_Laser pour paramètre la Class Sprite du module sprite lui même dans le module pygame. Permettre d'ajouter la Class Ennemies_Laser à un groupe
class Ennemies_Laser(pygame.sprite.Sprite):
    #On défini la methode "__init__" avec self, x et y en paramètre
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) #La methode "__init__" est donc associer à un groupe avec sprite
        self.image = pygame.image.load("SpaceInvader/SpaceInvaderIMG/ennemies_laser.png")    #On défini la variable "image" au chargement de l'image "ennemies_laser.png"
        self.rect = self.image.get_rect()   #On récupère avec "get.rect", la zone de collision de l'image pour l'associer à la fonction "rect" qui est donc la collision
        self.rect.center = [x, y]   #On place donc la collision qui contient l'image, donc au centre de la fenêtre en x et à une valeur de y
    #On défini la fonction "update" avec self en paramètre pour que la fonction soit associer seulement à la Class Ennemies_Laser
    def update(self):
        self.rect.y += 2    #On ajoute +2 en y pour la zone de collision de l'image "ennemies_laser.png"
        if self.rect.top > 650: #Si la zone de collision atteint le en partant du haut de la fenêtre, 650 pixels
            self.kill() #Alors l'image se détruit
        if pygame.sprite.spritecollide(self, vaisseau_group, False):    #Si la zone de collision du groupe vaisseau_group est touché par un laser
            self.kill() #Alors l'image se détruit
            vaisseau.vie_restante -= 1

class FinPartie:
    def gameover():
        if vaisseau.vie_restante <= 0:
            vaisseau.vitesse_joueur = 0
            vaisseau.cooldawntir = 100000000000
            fenetre.blit(gameoverscreen, (0, 0))
            fenetre.blit(gameover_text, (largeur_fenetre / 2 - 75, 200))
            fenetre.blit(gameover_vagues, (largeur_fenetre / 2 - 180, 300))
            fenetre.blit(gameover_points, (largeur_fenetre / 2 - 100, 350))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        vaisseau.vie_restante = 3
                        vaisseau.vitesse_joueur = 5
                        vaisseau.cooldawntir = 500
                        maingame.point_joueur = 0
                        maingame.vagues = 1
                        maingame.getfps = 60
                        pygame.display.update()
                    if event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                        pygame.quit()
        else:
            pygame.display.update()
            
#On défini la fonction "créer_ennemies
def créer_ennemies():
    for nbrangés in range(rangés):    #Ici, pour la variable nbrangés, qui prends pour valeur la taille de rangés, qui corresponds au nombre de rangés ou les ennemies appraissent
        for nbcolonnes in range(colonne): #Ici, pour la variable nbcolonnes, qui prends pour valeur la taille de colonnes, qui corresponds au nombre de colonnes ou les ennemies appraissent
            ennemies = Ennemies(50 + nbcolonnes * 80, 100 + nbrangés * 80)    #La variable ennemies fait appelle à la class Ennemies et qui défini le placement des ennemies en fonction de la valeur de rangé et de colonne
            ennemies_group.add(ennemies)    #On ajoute la variable ennemies créer juste au dessus au groupe ennemies_group
créer_ennemies()    #On execute la fonction des l'execution du code

def vie():
    if vaisseau.vie_restante == 3:
        fenetre.blit(life_barre, (largeur_fenetre / 2 - 70.495,745))
    else:
        if vaisseau.vie_restante == 2:
            fenetre.blit(life_barre, (largeur_fenetre / 2 - 110.495,745))
        else:
            if vaisseau.vie_restante == 1:
                fenetre.blit(life_barre, (largeur_fenetre / 2 - 160.495,745))
            else:
                fenetre.blit(life_barre, (largeur_fenetre / 2 - 210.495,745))
                FinPartie.gameover()

def cooldown_apparition():
    if vaisseau.cooldownspawn == 24:
        vaisseau.cooldownspawn = vaisseau.cooldownspawn - 24
        créer_ennemies()
        print("############################ Nouvelle vague ##############################")
        maingame.getfps += 5
        print("La vitesse du jeu augmente de 5 -> " + str(maingame.getfps))
        vaisseau.vitesse_joueur = vaisseau.vitesse_joueur - 1
        print("Ton vaisseau perd 1 point de vitesse :" + str(vaisseau.vitesse_joueur))
        maingame.vagues += 1
        print("Tu es a la vague : " + str(maingame.vagues))
        print("#######################################################################")
        if vaisseau.vitesse_joueur < 3:
            vaisseau.vitesse_joueur += 1
        else:
            vaisseau.vitesse_joueur == vaisseau.vitesse_joueur
    else:
        vaisseau.cooldownspawn == vaisseau.cooldownspawn

def gui_button():
    if joystick_touche[pygame.K_q] and joystick_touche[pygame.K_d]:
        fenetre.blit(joystick_gauche, (1000,689))
        fenetre.blit(joystick_droit, (1000,689))
        fenetre.blit(joystick, (62,681))
        fenetre.blit(spacebuttonoff, (392,710))
    else:
        if joystick_touche[pygame.K_q]:
            fenetre.blit(joystick_gauche, (42,689))
            
        if joystick_touche[pygame.K_d]:
            fenetre.blit(joystick_droit, (55,689))
            
        if joystick_touche[pygame.K_q] or joystick_touche[pygame.K_d]:
            fenetre.blit(joystick, (1000,689))
        else:
            fenetre.blit(joystick, (62,681))
            
        if joystick_touche[pygame.K_SPACE]:
            fenetre.blit(spacebuttonon, (392,710))
        else:
            fenetre.blit(spacebuttonoff, (392,710))

def  tir_laser():
    dernier_tir_ennemies = ennemies_laser_cooldown  #On défini la variable dernier_tir_ennemies égale à la variable ennemies_laser_cooldown
    #Condition if qui gère les tirs des ennemies, donc si temps_ennemies_laser - ennemies_laser_cooldown est supérieur au dernier_tir_ennemies et que la longueur de ennemies_laser_group inférieur à 5 et que la longueur de ennemies_group supérieur à 0
    if temps_ennemies_laser - ennemies_laser_cooldown > dernier_tir_ennemies and len(ennemies_laser_group) < 5 and len(ennemies_group) > 0:
        clock.tick(maingame.getfps)
        ennemies_attaque = random.choice(ennemies_group.sprites())  #On défini pour ennemies_attaque, un element aléatoire de ennemies_group
        ennemies_laser = Ennemies_Laser(ennemies_attaque.rect.centerx, ennemies_attaque.rect.bottom)    #On défini pour ennemies_laser, la class Ennemies_Laser avec la zone de collision d'un laser ennemies
        ennemies_laser_group.add(ennemies_laser)    #On ajoute la variable ennemies_laser au groupe sprite ennemies_laser_group

def actualisation():
    #On mets à jour les variables ci_dessous grâce à la méthode update du module sprite
    vaisseau.update()
    laser_group.update()
    ennemies_group.update()
    ennemies_laser_group.update()

    #On dessine les variables ci_dessus avec la méthode draw qui permet d'afficher sur la fenetre les groupes Sprite
    ennemies_group.draw(fenetre)
    vaisseau_group.draw(fenetre)
    laser_group.draw(fenetre)
    ennemies_laser_group.draw(fenetre)
    
    fenetre.blit(afficher_vagues, (largeur_fenetre - 150, 10))
    fenetre.blit(afficher_fps, (10, 10))
    fenetre.blit(point, (largeur_fenetre / 2 - 80, 702))

y_fond = 0  #On défini la variable y_fond à 0

start = True    #On défini la variable start à True

#On créer la boucle While qui permet de lancé le jeu
while start:    #Tant que start à pour valeur True et bien la boucle continue de fonctionner
    clock.tick(maingame.getfps) #On défini la variable clock créer au tout début, on lui affècte la méthode tick avec la valeur de fps qui était de 60 (le taux de rafraichissement de la fenêtre
    y_fond += 3 #On ajoute +3 à chaque tick pour y_fond
    joystick_touche = pygame.key.get_pressed()
    point = police_écriture_principale.render(str(maingame.point_joueur), True, (255,255,255))
    gameover_text = police_écriture_principale.render("Game Over !", True, (255,255,255))
    gameover_vagues = police_écriture_principale.render("Tu as perdu a la vagues " + str(maingame.vagues), True, (255,255,255))
    gameover_points = police_écriture_principale.render("avec " + str(maingame.point_joueur) + " points", True, (255,255,255))
    afficher_fps = police_écriture_principale.render("FPS : " + str(maingame.getfps), True, (255,255,255))
    afficher_vagues = police_écriture_principale.render("Vagues : " + str(maingame.vagues), True, (255,255,255))
    #On créer cette condition if pour que le fond puisse bouger sans cesse
    if y_fond < 1080: #Si la variable y_fond est inférieur à 1080 (la taille de l'image de fond) alors:
        fenetre.blit(fond, (0, y_fond)) #On utilise la méthode blit qu'on associe à la variable fenêtre créer au début et ensuite lui associer la variable fond contenant l'image de fond
        fenetre.blit(fond, (0, y_fond-1080))    #On utilise la méthode blit qu'on associe à la variable fenêtre créer au début et ensuite lui associer la variable fond une deuxième fois contenant l'image de fond mais à 1080 pixels avant la 1er
    else:
        y_fond = 0
        fenetre.blit(fond, (0, y_fond)) #On utilise la méthode blit qu'on associe à la variable fenêtre créer au début et ensuite lui associer la variable fond contenant l'image de fond
    vie()
    cooldown_apparition()
    fenetre.blit(borne, (0, 675))   #On ajoute la variable borne qui contient une image qui fait office de GUI à la variable fenetre avec la méthode blit
    gui_button()
    temps_ennemies_laser = pygame.time.get_ticks()  #La variable est égale à la fonction "get_ticks"(on récupère le nombre de ticks) du module time de pygame
    tir_laser()
    #Cette boucle for permet de pouvoir fermer le jeu et arréter le programme avec la méthode de récupération d'une touche ou d'un bouton de la fenêtre, ici, la croix en haut à droite d'une page
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
    actualisation()
    FinPartie.gameover()
    #On met à jour tout la fenetre entièrement pour que le jeu puisse fonctionner
    pygame.display.update()
        
pygame.quit()