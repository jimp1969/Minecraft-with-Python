# par défaut, les mouvements se font avec les touches WASD
# ce qui n'est pas adapté aux claviers français
# la fonction suivante permet l'utilisation des flèches au lieu de WASD


def modifier_touches():
    input_handler.rebind('left arrow', 'a')
    input_handler.rebind('right arrow', 'd')
    input_handler.rebind('up arrow', 'w')
    input_handler.rebind('down arrow', 's')
    input_handler.rebind('w', '&')
    input_handler.rebind('a', '&')
    input_handler.rebind('s', '&')
    input_handler.rebind('d', '&')

# fonction pour délimiter la zone et ne pas tomber dans le vide


def sol_et_murs():
    # construction du sol
    # sous-sol (indestructible)
    sol = Entity(
        model='assets/block',
        color=color.gray,
        scale=(LARG//2, 0.5, LONG//2),
        # position = (LARG//2-0.5, -2, LONG//2-0.5),
        # origin = Vec3(0,0,0),
        position=Vec3(LARG//2-0.5, -2, LONG//2-0.5),
        collider='box'
    )

    # sol en "terre" (destructible)
    for y in range(LONG):
        for x in range(LARG):
            construire_bloc(x, y, -1)
            # Bloc(position = (x, -1, z))

    # construction des murs
    mur_1 = Entity(model='cube', collider='box', scale=(
        LARG, 5, 0.5), x=LARG//2-0.5, y=0.5, z=-0.75, color=color.rgba(0, 255, 0, 20))
    mur_2 = duplicate(mur_1, z=LONG-0.25)
    mur_3 = Entity(model='cube', collider='box', scale=(
        0.5, 5, LONG), z=LONG//2-0.5, x=-0.75, y=0.5, color=color.rgba(0, 255, 0, 20))
    mur_4 = duplicate(mur_3, x=LARG-0.25)


def construire_bloc(x, y, z, cote=1, couleur=color.color(0, 0, random.uniform(0.9, 1)), texture=texture_bloc):
    cote = cote * 0.5  # l'unité est, dans ce fichier, de 0.5
    base = 1.5*cote-0.75  # permet de placer le bloc au sol
    BLOCS[(x, y, z)] = Bloc(position=(x, base + z, y),
                            texture=texture, taille=cote, couleur=couleur)


def detruire_bloc(x, y, z):
    '''
    cette fonction permet de détruire le bloc placé aux coordonnées (x,y,z)
    '''
    if (x, y, z) in BLOCS:
        destroy(BLOCS[(x, y, z)])
        del (BLOCS[(x, y, z)])


def creer_monde(longueur=50, largeur=50):  # par défaut, les dimensions sont 50x50
    global sky, player, hand, LONG, LARG
    LONG = longueur  # stockage des valeurs choisies par l'utilisateur dans des variables globales donc accessibles dans toutes les fonctions
    LARG = largeur
    # ajout des différents objets présents dans le monde
    sky = Sky()
    sol_et_murs()
    creer_aide()
    # la commande suivante lance la construction de 3 collines :
    # construire_collines(3)
    player = FirstPersonController(position=(2, 2, 2), speed=5)
    player.gravity = 0
    hand = Hand()
    modifier_touches()
    app.run()


def mur_x(x0, y0, longueur, hauteur):
    for y in range(y0, y0+longueur):
        for z in range(hauteur):
            construire_bloc(x0, y, z)


def mur_y(x0, y0, longueur, hauteur):
    for x in range(x0, x0+longueur):
        for z in range(hauteur):
            construire_bloc(x, y0, z)


def enceinte(x, y, taille, hauteur):
    mur_x(x, y, taille, hauteur)
    mur_x(x+taille-1, y, taille, hauteur)
    mur_y(x, y, taille, hauteur)
    mur_y(x, y+taille-1, taille, hauteur)


def tour(x0, y0, cote, hauteur):
    # mur selon x
    mur_x(x0, y0, cote, hauteur)
    mur_x(x0+cote-1, y0, cote, hauteur)

    # murs selon y
    mur_y(x0, y0, cote, hauteur)
    mur_y(x0, y0+cote-1, cote, hauteur)

    # creneau
    for y in range(y0+1, y0+cote, 2):
        detruire_bloc(x0, y, hauteur-1)
        detruire_bloc(x0+cote-1, y, hauteur-1)
    for x in range(x0+1, x0+cote, 2):
        detruire_bloc(x, y0, hauteur-1)
        detruire_bloc(x, y0+cote-1, hauteur-1)
    # plateforme
    for x in range(x0+1, x0+cote-1):
        for y in range(y0+1, y0+cote-1):
            construire_bloc(x, y, hauteur-3)


def tour(x, y, taille, hauteur):
    enceinte(x, y, taille, hauteur)


def creneau(x, y, taille, hauteur):
    # creneau
    for y in range(y+1, y+taille, 2):
        detruire_bloc(x, y, hauteur-1)
        detruire_bloc(x+taille-1, y, hauteur-1)
    for x in range(x+1, x+taille, 2):
        detruire_bloc(x, y, hauteur-1)
        detruire_bloc(x, y+taille-1, hauteur-1)
    # plateforme
    for x in range(x+1, x+taille-1):
        for y in range(y+1, y+taille-1):
            construire_bloc(x, y, hauteur-3)


def quatre_tours(x, y, largeur_tour, taille_chateau, hauteur_tour):
    for i in [x, x+taille_chateau-5]:
        for j in [y, y+taille_chateau-5]:
            tour(i, j, largeur_tour, hauteur_tour)


def douves(x, y, largeur_douves, taille_chateau):
    for i in range(x-largeur_douves, x+taille_chateau+largeur_douves):
        for j in range(y-largeur_douves, y):
            detruire_bloc(i, j, -1)
            detruire_bloc(i, j+taille_chateau+largeur_douves, -1)
            construire_bloc(i, j, -1, texture=water_texture)
            construire_bloc(i, j+taille_chateau +
                            largeur_douves, -1, texture=water_texture)
    for j in range(y, y+taille_chateau+largeur_douves):
        for i in range(x-largeur_douves, x):
            detruire_bloc(i, j, -1)
            detruire_bloc(i+taille_chateau+largeur_douves, j, -1)
            construire_bloc(i, j, -1, texture=water_texture)
            construire_bloc(i+taille_chateau+largeur_douves,
                            j, -1, texture=water_texture)


def entree(x, y, largeur, hauteur, largeur_douves):
    for i in range(x, x+largeur):
        for k in range(0, hauteur):
            detruire_bloc(i, y, k)


def pont(x, y, largeur, hauteur, largeur_douves):
    for i in range(x, x+largeur):
        for j in range(y-largeur_douves, y):
            detruire_bloc(i, j, -1)
            construire_bloc(i, j, -1, texture=stone_texture)

# fonction liée à la touche magique "m"


def magique():

    x_chateau = 10
    y_chateau = 10
    largeur_douves = 5
    hauteur_mur = 6
    taille_chateau = 30
    hauteur_tour = 8

    enceinte(x_chateau, y_chateau, taille_chateau, hauteur_mur)
    quatre_tours(x_chateau, y_chateau, 5, taille_chateau, hauteur_tour)
    douves(x_chateau, y_chateau, largeur_douves, taille_chateau)
    entree(x_chateau+10, y_chateau, 4, 4, largeur_douves)