import tkinter as tk
import random
import json
import os
import time

# Fenetre princiaple
racine = tk.Tk()
racine.title("PROJET SUDOKU")
racine.geometry("500x600")

# Tableaux de Sudoku complétes
tableaux = {
    "Tableau 1": [
        [1, 4, 8, 2, 7, 5, 6, 9, 3],
        [3, 9, 6, 4, 1, 8, 7, 5, 2],
        [5, 7, 2, 3, 9, 6, 1, 4, 8],
        [8, 5, 7, 6, 2, 4, 3, 1, 9],
        [6, 1, 9, 8, 3, 7, 5, 2, 4],
        [2, 3, 4, 9, 5, 1, 8, 7, 6],
        [4, 6, 1, 5, 8, 2, 9, 3, 7],
        [9, 2, 5, 7, 6, 3, 4, 8, 1],
        [7, 8, 3, 1, 4, 9, 2, 6, 5]
    ],
    "Tableau 2": [
        [1, 2, 3, 7, 8, 9, 4, 5, 6],
        [4, 5, 6, 1, 2, 3, 7, 8, 9],
        [7, 8, 9, 4, 5, 6, 1, 2, 3],
        [2, 3, 1, 8, 9, 7, 5, 6, 4],
        [5, 6, 4, 2, 3, 1, 8, 9, 7],
        [8, 9, 7, 5, 6, 4, 2, 3, 1],
        [3, 1, 2, 9, 7, 8, 6, 4, 5],
        [6, 4, 5, 3, 1, 2, 9, 7, 8],
        [9, 7, 8, 6, 4, 5, 3, 1, 2],
    ],
    "Tableau 3": [
        [7, 3, 6, 4, 5, 2, 9, 8, 1],
        [1, 9, 8, 6, 3, 7, 4, 5, 2],
        [4, 2, 5, 9, 8, 1, 3, 7, 6],
        [3, 6, 4, 5, 2, 8, 1, 9, 7],
        [9, 5, 2, 7, 1, 4, 6, 3, 8],
        [8, 1, 7, 3, 9, 6, 2, 4, 5],
        [2, 8, 9, 1, 7, 3, 5, 6, 4],
        [6, 7, 3, 2, 4, 5, 8, 1, 9],
        [5, 4, 1, 8, 6, 9, 7, 2, 3]
    ],
    "Tableau 4": [
        [8, 4, 9, 1, 5, 6, 2, 3, 7],
        [3, 2, 5, 9, 8, 7, 1, 6, 4],
        [7, 6, 1, 4, 3, 2, 8, 9, 5],
        [6, 3, 8, 7, 4, 5, 9, 2, 1],
        [4, 1, 7, 2, 6, 9, 3, 5, 8],
        [9, 5, 2, 8, 1, 3, 4, 7, 6],
        [2, 8, 6, 3, 7, 1, 5, 4, 9],
        [5, 9, 4, 6, 2, 8, 7, 1, 3],
        [1, 7, 3, 5, 9, 4, 6, 8, 2]
    ],
    "Tableau 5": [
        [2, 3, 6, 5, 8, 7, 9, 1, 4],
        [8, 1, 7, 9, 4, 3, 2, 6, 5],
        [5, 9, 4, 6, 1, 2, 3, 7, 8],
        [4, 7, 9, 3, 5, 8, 6, 2, 1],
        [6, 5, 2, 7, 9, 1, 8, 4, 3],
        [3, 8, 1, 4, 2, 6, 5, 9, 7],
        [1, 4, 3, 2, 6, 5, 7, 8, 9],
        [9, 6, 5, 8, 7, 4, 1, 3, 2],
        [7, 2, 8, 1, 3, 9, 4, 5, 6]
    ]
}


# Variables globales
Taille = 9
entrées = []
solution = []
cases_cachées = []
tableau_actuel = []
message_correspondant = None
erreurs=0
temps_debut = None
temps_ecoule = 0
temps_pause = False
temps_label = None


# Crée Grille 9x9 avce des cases d'entrée

def créer_grille():
    global entrées
    for lin in range(Taille): #lin=lignes
        ligne = []
        for col in range(Taille): #col=colonnes
            case = tk.Entry(racine, width=2, font=("Arial", 20), justify="center")
            case.grid(row=lin, column=col, padx=(4 if col % 3 == 0 else 1, 1), pady=(4 if lin % 3 == 0 else 1, 1))
            ligne.append(case)
        entrées.append(ligne)

# Cahrge le tableau de Sudoku sélectionné, parteillement remplie et ...

def charger_tableau(tableau_x):
    global solution, cases_cachées, tableau_actuel, erreurs, temps_pause, temps_debut, temps_ecoule
    tableau_actuel = tableau_x
    solution = [ligne.copy() for ligne in tableau_x]
    cases_cachées = []
    erreurs = 0  # Réinitialise le compteur d'erreurs
    mettre_a_jour_erreur_label()
    while len(cases_cachées) < 30: # genere aleatoirement 30 cases cachées 
        l, c = random.randint(0, Taille - 1), random.randint(0, Taille - 1)
        if (l, c) not in cases_cachées:
            cases_cachées.append((l, c))

    for l in range(Taille):
        for c in range(Taille):
            entré = entrées[l][c]
            entré.config(state="normal", fg="black", bg="white", disabledforeground="black")
            entré.config(disabledbackground="light gray") 
            entré.delete(0, tk.END)
            if (l, c) in cases_cachées:
                entré.config(bg="white", fg="black")
                entré.bind("<KeyRelease>", lambda e, l=l, c=c: vérifier_valeur(e, l, c))
            else:
                entré.insert(0, str(tableau_x[l][c]))
                entré.config(state="disabled", disabledforeground="black", disabledbackground="light gray", bg= "white")
    
    temps_pause = False
    temps_ecoule = 0
    temps_debut = time.time()
    mettre_a_jour_temps()
                
# verifie la valeur saisie par l'utilisateur et affcihe le message correspondant

def vérifier_valeur(e, lin, col): #
    global erreurs
    val = entrées[lin][col].get()
    if val == "":
        return
    if not val.isdigit() or not (1 <= int(val) <= 9):
        entrées[lin][col].config(bg="red")
         entrées[lin][col].delete(0,tk.End)
        afficher_message("La valeur saisie, doit être un chiffre de 1 à 9.")
        return
    if int(val) != solution[lin][col]:
        erreurs += 1  # Incrémente le compteur d'erreurs
        mettre_a_jour_erreur_label()
        entrées[lin][col].config(bg="red")
        afficher_message("La valeur saisie est incorrecte.")
    else:
        entrées[lin][col].config(state="disabled", disabledforeground="black",disabledbackground="light green")
        if (lin, col) in cases_cachées:
            cases_cachées.remove((lin, col))
        afficher_message("La valeur saisie est correcte.")
    vérifier_si_termine()

# Afficghe les messages correspondant dans la zone de message

def afficher_message(msg):
    message_correspondant.config(text=msg)

# Met a pause le jeu, désactive les cases, met a jour le message et le temps.

def bouton_pause():
    global temps_pause, temps_ecoule
    temps_pause = True
    temps_ecoule += int(time.time() - temps_debut)
    afficher_message("Jeu mis en pause.")
    for l in range(Taille):
        for c in range(Taille):
            entrées[l][c].config(state="disabled")

# Reprend le jeu, réactive les cases, met a jour le message et le temps.

def bouton_reprendre():
    global temps_pause, temps_debut
    temps_pause = False
    temps_debut = time.time()
    mettre_a_jour_temps()
    for (l, c) in cases_cachées:
        entrées[l][c].config(state="normal")
    afficher_message("Jeu repris.")

# Fournit une aide en révélant une case cachée, désactive la case et met à jour le message.

def bouton_aide():
    if not cases_cachées:
        afficher_message("Le jeu est terminé, aucune aide est disponible.")
        return
    l, c = random.choice(cases_cachées)
    entrées[l][c].delete(0, tk.END)
    entrées[l][c].insert(0, str(solution[l][c]))
    entrées[l][c].config(state="disabled", disabledforeground="green")
    cases_cachées.remove((l, c))
    afficher_message("Aide fournie.")

# Sauvegarde l'état actuel du jeu dans un fichier JSON, incluant les erreurs et le temps écoulé.

def bouton_sauvegarder():
    if not tableau_actuel:
        afficher_message("Aucune grille à sauvegarder.")
        return

    sauvegarde = {
        "tableau": tableau_actuel,
        "cases_cachées": cases_cachées,
        "grille": [
            [
                {
                    "val": e.get(),
                    "etat": str(e.cget("state")),
                    "bg": e.cget("bg"),
                    "fg": e.cget("fg"),  # <-- on sauvegarde aussi la couleur du texte normale
                    "dfg": e.cget("disabledforeground") if e.cget("state") == "disabled" else e.cget("fg"),
                    "dbg": e.cget("disabledbackground") if e.cget("state") == "disabled" else e.cget("bg"),
                } for e in ligne
            ] for ligne in entrées
        ],
        "erreurs": erreurs,
        "temps": int(time.time() - temps_debut)
    }

    # Créer le dossier si besoin
    dossier = "revison_py"
    if not os.path.exists(dossier):
        os.makedirs(dossier)

    chemin_fichier = os.path.join(dossier, "sauvegarde.json")

    with open(chemin_fichier, "w") as f:
        json.dump(sauvegarde, f)

    afficher_message("Jeu sauvegardé.")

# Charge l'état du jeu à partir d'un fichier JSON, incluant les erreurs et le temps écoulé.

def bouton_charger():
    global tableau_actuel, solution, cases_cachées, erreurs, temps_debut, temps_ecoule, temps_pause

    chemin_fichier = "revison_py/sauvegarde.json"
    if not os.path.exists(chemin_fichier):
        afficher_message("Aucune sauvegarde trouvée.")
        return

    with open(chemin_fichier, "r") as f:
        sauvegarde = json.load(f)

    tableau_actuel = sauvegarde["tableau"]
    solution = [ligne.copy() for ligne in sauvegarde["tableau"]]
    cases_cachées = [tuple(c) for c in sauvegarde["cases_cachées"]]
    erreurs = sauvegarde.get("erreurs", 0)
    mettre_a_jour_erreur_label()
    temps_debut = time.time() - sauvegarde.get("temps", 0)
    mettre_a_jour_temps()

    grille = sauvegarde["grille"]
    for l in range(Taille):
        for c in range(Taille):
            case = entrées[l][c]
            data = grille[l][c]

            case.config(state="normal")
            case.delete(0, tk.END)

            val = data["val"]
            etat = data["etat"]
            bg = data.get("bg", "white")
            fg = data.get("fg", "black")
            dfg = data.get("dfg", "black")
            dbg = data.get("dbg", "light gray")

            if val:
                case.insert(0, val)

            if etat == "disabled":
                case.config(state="disabled", disabledforeground=dfg, disabledbackground=dbg)
            else:
                case.config(state="normal", fg=fg, bg=bg)
                case.bind("<KeyRelease>", lambda e, l=l, c=c: vérifier_valeur(e, l, c))

    afficher_message("Jeu chargé.")
    temps_ecoule = sauvegarde.get("temps", 0)
    temps_pause = False


# Annule le jeu en vidant tous les cases

def button_annuler():
    global erreurs, temps_debut, temps_ecoule, temps_pause  # ← Obligatoire ici !
    erreurs = 0
    mettre_a_jour_erreur_label()
    for l in range(Taille):
        for c in range(Taille):
            entrées[l][c].config(state="normal", fg="black", bg="white")  # Réactive proprement la case
            entrées[l][c].delete(0, tk.END)  # Vide le contenu
    afficher_message("Jeu annulé.")
    temps_pause = True
    temps_debut = None
    temps_ecoule = 0
    temps_label.config(text="Temps écoulé : 00:00")

# Vérifie si le jeu est terminé en comparant les valeurs saisies avec la solution.

def vérifier_si_termine():
    global temps_pause
    for l, c in cases_cachées:
        val = entrées[l][c].get()
        if not val.isdigit() or int(val) != solution[l][c]:
            return
    afficher_message("Félicitations, vous avez terminé le jeu !")
    for l in range(Taille):
        for c in range(Taille):
            entrées[l][c].config(state="disabled")

    temps_pause = True  #  Stoppe le chrono ici

# Met à jour le label d'erreur pour afficher le nombre d'erreurs commises

def mettre_a_jour_erreur_label():
    erreur_label.config(text=f"Erreurs commises : {erreurs}")

# Met à jour le label de temps écoulé toutes les secondes

def mettre_a_jour_temps():
    global temps_debut, temps_ecoule
    if temps_pause:
        return

    ecoule = int(time.time() - temps_debut) + temps_ecoule
    minutes = ecoule // 60
    secondes = ecoule % 60
    temps_label.config(text=f"Temps écoulé : {minutes:02}:{secondes:02}")

    racine.after(1000, mettre_a_jour_temps)

# Crée le menu de droite avec les boutons pour charger les tableaux, mettre en pause, reprendre, sauvegarder, charger et annuler.

def créer_menu_droite():
    global message_correspondant, erreur_label, temps_label
    for i, nom_tableau in enumerate(tableaux):
        tk.Button(racine, text=nom_tableau, command=lambda t=tableaux[nom_tableau]: charger_tableau(t)).grid(row=i, column=9, padx=5, pady=2)
    tk.Button(racine, text="Pause", command=bouton_pause).grid(row=6, column=9)
    tk.Button(racine, text="Reprendre", command=bouton_reprendre).grid(row=7, column=9)
    tk.Button(racine, text="Aide", command=bouton_aide).grid(row=8, column=9)
    tk.Button(racine, text="Sauvegarder", command=bouton_sauvegarder).grid(row=9, column=9, padx=(6,1), pady=(6,1))
    tk.Button(racine, text="Charger", command=bouton_charger).grid(row=10, column=9, padx=(6,1), pady=(6,1))
    tk.Button(racine, text="Annuler", command=button_annuler).grid(row=11, column=9, padx=(6,1), pady=(6,1))

    message_correspondant = tk.Label(racine, text="", fg="blue", justify="left", wraplength=150)
    message_correspondant.grid(row=12, column=9, padx=(6,1), pady=(6,1))
    erreur_label = tk.Label(racine, text="Erreurs commises : 0", fg="red", justify="left")
    erreur_label.grid(row=13, column=9, padx=(6,1), pady=(6,1))
    temps_label = tk.Label(racine, text="Temps écoulé : 00:00", fg="black", justify="left")
    temps_label.grid(row=14, column=9, padx=(6,1), pady=(6,1))

    


# Démarrage
créer_grille()
créer_menu_droite()
racine.mainloop()

