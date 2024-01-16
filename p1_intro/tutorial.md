# LOG725 H2024 - Labo 1
Bienvenue dans le laboratoire LOG725 H2024. Au cours de cette session, nous explorerons les principes fondamentaux de la conception et du développement de jeux, la programmation de jeux en utilisant Godot (moteur de jeux) et PyGame (bibliothèque), ainsi que les techniques d'assurance qualité d'un jeu. Les étudiants auront l'occasion de mettre en pratique ces concepts à travers des activités interactives et la création de leurs propres prototypes de jeux. Préparez-vous à libérer votre créativité et à plonger dans l'univers captivant du développement de jeux vidéo.

## Préparer votre environment
- Installez Python 3.1 ou supérieur
- Installez PyGame

```bash
  pip3 install pygame
  python intro.py
```

## Dessiner une fenêtre
Dans le fichier intro.py, nous allons commencer très simplement en dessinant une fenêtre vide. Même si nous n'avons pas encore de logique de jeu, nous devons implémenter une méthode pour gérer la fermeture de la fenêtre, que nous appelons ici "gererFermeture". Dans cette méthode, nous utilisons le système d'événements de pygame pour vérifier quand nous essayons de fermer la fenêtre. Nous n'allons pas encore étudier ce système en profondeur dans ce laboratoire, mais il est important de savoir qu'il existe et qu'il est nécessaire pour fermer la fenêtre.

```python
import pygame
import sys

# Constants
WIDTH = 400
HEIGHT = 300

pygame.init()
ecran = pygame.display.set_mode((WIDTH, HEIGHT))

def gererFermeture():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

while True:
    gererFermeture()

    # voir la resolution de la fenêtre
    print(ecran)
```

En utilisant un "while True", notre jeu s'exécute à chaque frame et nous avons des mises à jour continuelles. C'est ce qu'on appelle la boucle de jeu (game loop). Pourquoi l'utiliser ? Il n'est pas possible de déssiner en dehors de la loop. Toutes les mises à jour se déroulent à l'intérieur de la loop.

## Dessiner une image sur la fenêtre
Nous allons utiliser la méthode "blit" pour cela. Le nom vient de la routine BitBLT de l'ordinateur Xerox Alto (des anées 70), ce qui signifie 'bit-boundary block transfer'. Elle prend deux arguments :

- La ressource que nous voulons dessiner doit d'abord être chargée en mémoire en utilisant le méthode pygame.image.load, puis nous pouvons la dessiner. Il est crucial de réaliser le chargement en dehors de la loop, afin de ne pas répéter cette opération inutilement à chaque frame.

- Les coordonnées (x, y) déterminent le point où PyGame commencera à dessiner l'image. Les coordonnées (0,0) indiquent "en haut à gauche". Vous pouvez les imaginer comme l'origine du plan cartésien.

```python
# Constants
WIDTH = 800
HEIGHT = 480

pygame.init()
ecran = pygame.display.set_mode((WIDTH, HEIGHT))

tableSprite = pygame.image.load("images/table.png")

while True:
  gererFermeture()

  ecran.blit(tableSprite, (0, 0))
  pygame.display.flip()
```

Nous pouvons expérimenter avec différents noms et positions. Pouvez-vous observer ce qui se passe lorsque vous augmentez x ou y ?

## Comprendre l'ordre de dessin
Les applications en général utilisent un système de couches pour dessiner. Après que la première image ait été dessinée, les suivantes seront ajoutées par-dessus. Par exemple, observez ce qui se passe lorsque l'on dessine un carré au-dessus de la table.
```python
tableSprite = pygame.image.load("images/table.png")
squareSprite = pygame.image.load("images/square.png")

while True:
  gererFermeture()

  ecran.blit(tableSprite, (0, 0))
  ecran.blit(squareSprite, (0, 0))
  pygame.display.flip()
```

Il faut s'assurer de suivre l'ordre de dessin pour éviter que les images se chevauchent. Que se passe-t-il si nous appelons ces commandes dans l'ordre inverse ?

## Les dispositifs d'entrée
Dans un jeu vidéo, nous changeons ce qui est dessiné à l'écran en fonction des actions de l'utilisateur. L'utilisateur interagit avec le jeu en utilisant des dispositifs d'entrée tels que le clavier, la souris, les joysticks ou les écrans tactiles.

Avec la pièce de code suivante, nous pouvons faire en sorte que le carré soit dessiné uniquement lorsque la barre d'espace est appuyée. Avant de dessiner, nous utilisons le méthode pygame.key.get_pressed pour obtenir l'état de toutes les touches du clavier et ensuite vérifier si la barre d'espace est appuyée. La liste complète des touches de clavier supportées est dans [la documentation oficielle](https://www.pygame.org/docs/ref/key.html).

Rappelons que, comme toutes les mises à jour se déroulent à l'intérieur de la loop, il faut placer le code suivant dans la loop.
```python
  keys = pygame.key.get_pressed()
  if keys[pygame.K_SPACE]:
    ecran.blit(squareSprite, (250, 250))
```

EXTRA: Nous pouvons également combiner différentes entrées du clavier en utilisant des opérateurs booléens.
```python
  keys = pygame.key.get_pressed()
  if keys[pygame.K_LCTRL] and keys[pygame.K_x]:
    ecran.blit(squareSprite, (250, 250))
```

## Dessiner des primitives
Au lieu de dessiner des images au format .jpg ou .png créées dans d'autres logiciels (par exemple, Photoshop), on peut également donner des instructions à PyGame pour dessiner des formes géométriques directement. Nous appelons ces formes des "primitives" parce qu'elles sont très basiques. Par exemple, en utilisant le code suivant, nous pouvons dessiner un carré bleu :
```python
  pygame.draw.rect(ecran, (0, 0, 255), (0,0,100,100))
```

Le méthode pygame.draw.rect reçoit trois arguments :
- L'objet qui représente l'écran (où dessiner).
- La couleur RGB.
- Les positions des points de début et de fin pour dessiner.

En utilizant un logique similaire, nous pouvons aussi déssiner un circle rouge:
```python
  pygame.draw.circle(ecran, (255, 0, 0), (50, 50), 10)
```
Le méthode pygame.draw.circle reçoit quatre arguments :
- L'objet qui représente l'écran (où dessiner).
- La couleur RGB.
- La position du centre du circle.
- Le rayon du circle, en pixels.

Faite attention pour l'order de dessin. Que se passe-t-il si nous appelons ces commandes dans l'ordre inverse ?

## Concevoir des objets du jeu
En tant que développeurs de jeux, il nous incombe d'identifier les objets dans notre jeu qui auront des logiques spécifiques de dessin et d'interaction avec les entrées. Après avoir identifié ces objets, nous pouvons les transformer en classes Python pour encapsuler leur logique et aussi tirer avantage des caractéristiques des langages orientés objet, comme l'héritage. Les objets de jeu (game objects), sont aussi désignés sous le terme "acteurs" (actors) dans quelques game engines. En effet, nous façonnons des acteurs qui évoluent au sein d'une scène que nous avons conçue.

Par exemple, créons deux classes dans un fichier appelé "objets". La première, plus générique : "Forme". La deuxième, plus spécifique : "Cercle". Dans la classe "Forme", nous implémenterons une logique de touches qui sera utilisée pour toutes les classes qui héritent de "Forme". La logique est très simple : si la barre d'espace est appuyée, nous changeons l'attribut "couleur" de rouge à vert. Sinon, il reste vert.
```python
import pygame

class Forme:
    couleur = (255, 0, 0)

    def __init__(self, couleur):
        self.couleur = couleur

    def verifierEspace(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.couleur = (0, 255, 0)
        else:
            self.couleur = (255, 0, 0)
```

Ensuite, créons une classe "Cercle" qui hérite de "Forme". Dans cette classe, nous effectuons également une vérification des touches du clavier. Si la touche "x" est appuyée, nous augmentons le rayon du cercle. Sinon, il reste le même.
```python
import pygame
from objets.forme import Forme

class Cercle(Forme):
    rayon = 100

    def __init__(self, couleur):
        Forme.__init__(self, couleur)

    def retournerOriginal(self):
        if self.rayon > 0:
            self.rayon -= 10
        else:
            self.rayon = 10

    def verifierX(self, ecran):
        ecran.fill((0, 0, 0))
        self.verifierEspace()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_x]:
            self.rayon += 10
        else:
            self.retournerOriginal()
        print(self.rayon)

        pygame.draw.circle(ecran, self.couleur, (200, 200), self.rayon, 0)
```

Pour utiliser les classes, il faut les instancier et appeler les méthodes dans la loop du jeu.

EXTRA: nous pouvons jouer avec le structure e logique qui ces classes containent.
- Que se passe-t-il si, dans la classe "Cercle", nous créons une méthode appelée "verifierEspace" ?
- Que pouvons-nous faire pour ramener le cercle à son rayon original ?

## La grande finale: jouer un son
De la même manière que pour les images, nous devons charger les sons avant de les jouer. Nous devons également les appeler dans la loop.

```python
piano = pygame.mixer.Sound("sons/piano.mp3")

while True:
  keys = pygame.key.get_pressed()
  if keys[pygame.K_z]:
    piano.play()
```

## Exercices
Maintenant, à vous ! Veuillez compléter les exercices suivants pour pratiquer vos connaissances en dessin et gestion d'entrées :

- Créez un nouveau fichier, exercises.py. Suivez les étapes de configuration comme indiqué dans la section "Préparer votre environnement".
- Créez une fenêtre et dessinez l'image "table.png". Suivez les étapes comme indiqué dans la section "Dessiner une image sur la fenêtre".
- En suivant les étapes que nous avons présentées dans les sections "Concevoir des objets du jeu" et "Dessiner une image sur la fenêtre", créez une classe appelée "Plateforme" et dessinez une plateforme rectangulaire verte de 200 pixels de hauteur (y) et 50 pixels de largeur (x).
- En suivant les étapes que nous avons présentées dans la section "Les dispositifs d'entrée", faites déplacer la plateforme vers le haut et vers le bas à l'écran en utilisant les flèches du clavier.
- EXTRA : Complétez les sections marquées comme EXTRA dans les instructions.