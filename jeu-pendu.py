import tkinter as tk
from tkinter import messagebox, ttk
import random

class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Le Jeu du Pendu")
        self.root.geometry("800x600")
        self.root.configure(bg='#1E272E')
        
        # Frame principale du menu avec bordure
        self.frame = tk.Frame(root, bg='#1E272E', 
                            highlightbackground="#808e9b", 
                            highlightthickness=2)
        self.frame.pack(expand=True, fill='both', padx=40, pady=40)
        
        # Container pour le contenu
        content_frame = tk.Frame(self.frame, bg='#1E272E')
        content_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Titre du jeu avec effet d'ombre
        titre_frame = tk.Frame(content_frame, bg='#1E272E')
        titre_frame.pack(pady=20)
        
        # Ombre du titre
        tk.Label(titre_frame, 
                text="LE JEU DU PENDU", 
                font=('Helvetica', 50, 'bold'), 
                fg='#2d3436', 
                bg='#1E272E').pack(pady=1)
        
        # Titre principal
        tk.Label(titre_frame, 
                text="LE JEU DU PENDU", 
                font=('Helvetica', 50, 'bold'), 
                fg='#dfe6e9', 
                bg='#1E272E').place(relx=0.5, rely=0.5, anchor='center')
        
        # Créateur avec style moderne
        tk.Label(content_frame, 
                text="Créé par M.C-G et JUJUTÉMU", 
                font=('Helvetica', 16, 'italic'), 
                fg='#808e9b', 
                bg='#1E272E').pack(pady=20)
        
        # Frame pour la sélection de la difficulté
        diff_frame = tk.Frame(content_frame, bg='#1E272E')
        diff_frame.pack(pady=30)
        
        # Label pour la difficulté avec icône
        diff_label = tk.Label(diff_frame, 
                            text="⚙️ Sélectionnez la difficulté", 
                            font=('Helvetica', 14), 
                            fg='#dfe6e9', 
                            bg='#1E272E')
        diff_label.pack(pady=10)
        
        # Variable pour stocker la difficulté
        self.difficulte_var = tk.StringVar(value="Moyen")
        
        # Style pour le combobox
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.TCombobox', 
                       fieldbackground='#34495e',
                       background='#2d3436',
                       foreground='#dfe6e9',
                       arrowcolor='#dfe6e9')
        
        # Combobox avec descriptions des niveaux
        niveaux = [
            "Facile - Première et dernière lettres données",
            "Moyen - Première lettre donnée",
            "Difficile - Aucune lettre donnée"
        ]
        
        self.difficulte = ttk.Combobox(diff_frame, 
                                      textvariable=self.difficulte_var,
                                      values=niveaux,
                                      font=('Helvetica', 12),
                                      state='readonly',
                                      width=40,
                                      style='Custom.TCombobox')
        self.difficulte.pack(pady=10)
        
        # Bouton pour commencer le jeu
        self.creer_bouton_stylise(content_frame, "▶ JOUER", self.demarrer_jeu)

    def creer_bouton_stylise(self, parent, texte, commande):
        btn_frame = tk.Frame(parent, bg='#1E272E')
        btn_frame.pack(pady=20)
        
        btn = tk.Button(btn_frame, 
                       text=texte,
                       command=commande,
                       font=('Helvetica', 16, 'bold'),
                       bg='#0984e3',
                       fg='white',
                       activebackground='#74b9ff',
                       activeforeground='white',
                       relief='flat',
                       padx=30,
                       pady=10,
                       cursor='hand2')
        btn.pack()
        
        # Effet hover
        def on_enter(e):
            btn['background'] = '#74b9ff'
            
        def on_leave(e):
            btn['background'] = '#0984e3'
            
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)

    def demarrer_jeu(self):
        difficulte_selection = self.difficulte_var.get().split(' - ')[0]  # Prend juste le niveau
        self.frame.destroy()
        JeuPendu(self.root, difficulte_selection)

class JeuPendu:
    def __init__(self, root, difficulte):
        self.root = root
        self.difficulte = difficulte
        
        # Liste de mots
        self.mots = ["python", "programmation", "ordinateur", "algorithme", "développeur",
                     "interface", "application", "logiciel", "internet", "intelligence", 
                     "commencement", "corde", "secrétaire", "vaincre", "saison", "precieux",
                     "precis", "consulter", "air", "repousse","Julien", "calvicie", "Matthais"]
        
        # Variables du jeu
        self.mot = ""
        self.lettres_trouvees = set()
        self.lettres_proposees = set()  # Nouveau set pour toutes les lettres proposées
        self.erreurs = 0
        self.max_erreurs = 7
        
        # Interface graphique
        self.creer_interface()
        
        # Démarrer une nouvelle partie
        self.nouvelle_partie()

    def creer_interface(self):
        # Frame principale avec bordure
        self.frame_principale = tk.Frame(self.root, bg='#1E272E',
                                       highlightbackground="#808e9b",
                                       highlightthickness=2)
        self.frame_principale.pack(expand=True, fill='both', padx=20, pady=20)

        # Barre supérieure avec difficulté et retour
        barre_sup = tk.Frame(self.frame_principale, bg='#2d3436')
        barre_sup.pack(fill='x', padx=10, pady=5)

        # Bouton retour
        btn_retour = tk.Button(barre_sup,
                              text="↩ Menu",
                              command=self.retour_menu,
                              font=('Helvetica', 10),
                              bg='#0984e3',
                              fg='white',
                              relief='flat',
                              padx=10,
                              cursor='hand2')
        btn_retour.pack(side='left', padx=5)

        # Label difficulté
        tk.Label(barre_sup,
                text=f"Niveau : {self.difficulte}",
                font=('Helvetica', 12),
                fg='#dfe6e9',
                bg='#2d3436').pack(side='right', padx=10)

        # Zone de dessin du pendu
        self.canvas = tk.Canvas(self.frame_principale, 
                              width=300, 
                              height=300, 
                              bg='#2d3436',
                              highlightthickness=0)
        self.canvas.pack(pady=20)

        # Mot à deviner
        self.label_mot = tk.Label(self.frame_principale, 
                                text="", 
                                font=('Helvetica', 32, 'bold'), 
                                fg='#dfe6e9',
                                bg='#1E272E')
        self.label_mot.pack(pady=20)

        # Zone de saisie
        self.frame_saisie = tk.Frame(self.frame_principale, bg='#1E272E')
        self.frame_saisie.pack(pady=20)

        self.entry_lettre = tk.Entry(self.frame_saisie, 
                                   font=('Helvetica', 18), 
                                   width=5,
                                   bg='#2d3436',
                                   fg='#dfe6e9',
                                   insertbackground='#dfe6e9',
                                   justify='center')
        self.entry_lettre.pack(side=tk.LEFT, padx=10)
        self.entry_lettre.bind('<Return>', lambda e: self.proposer_lettre())

        # Bouton proposer
        btn_proposer = tk.Button(self.frame_saisie,
                                text="Proposer",
                                command=self.proposer_lettre,
                                font=('Helvetica', 12),
                                bg='#0984e3',
                                fg='white',
                                relief='flat',
                                padx=15,
                                pady=5,
                                cursor='hand2')
        btn_proposer.pack(side=tk.LEFT)

        # Frame pour les lettres proposées
        self.frame_lettres = tk.Frame(self.frame_principale, bg='#2d3436')
        self.frame_lettres.pack(fill='x', padx=20, pady=10)
        
        # Titre pour les lettres proposées
        tk.Label(self.frame_lettres,
                text="Lettres déjà proposées:",
                font=('Helvetica', 12),
                fg='#dfe6e9',
                bg='#2d3436').pack(pady=5)
        
        # Label pour afficher les lettres
        self.label_lettres = tk.Label(self.frame_lettres,
                                    text="",
                                    font=('Helvetica', 14, 'bold'),
                                    fg='#74b9ff',
                                    bg='#2d3436',
                                    wraplength=700)
        self.label_lettres.pack(pady=5)

        # Bouton nouvelle partie
        btn_nouveau = tk.Button(self.frame_principale,
                               text="🔄 Nouvelle Partie",
                               command=self.nouvelle_partie,
                               font=('Helvetica', 12),
                               bg='#00b894',
                               fg='white',
                               relief='flat',
                               padx=15,
                               pady=5,
                               cursor='hand2')
        btn_nouveau.pack(pady=10)

    def retour_menu(self):
        self.frame_principale.destroy()
        MenuPrincipal(self.root)

    def dessiner_pendu(self):
        self.canvas.delete("all")
        style = {'fill': '#dfe6e9', 'width': 3}
        
        # Support
        self.canvas.create_line(50, 250, 250, 250, **style)
        
        # Dessins progressifs selon le nombre d'erreurs
        if self.erreurs >= 1:
            self.canvas.create_line(150, 250, 150, 50, **style)
        if self.erreurs >= 2:
            self.canvas.create_line(150, 50, 200, 50, **style)
        if self.erreurs >= 3:
            self.canvas.create_line(200, 50, 200, 80, **style)
        if self.erreurs >= 4:
            self.canvas.create_oval(185, 80, 215, 110, **style)
        if self.erreurs >= 5:
            self.canvas.create_line(200, 110, 200, 170, **style)
        if self.erreurs >= 6:
            self.canvas.create_line(200, 130, 180, 150, **style)
            self.canvas.create_line(200, 130, 220, 150, **style)
        if self.erreurs >= 7:
            self.canvas.create_line(200, 170, 180, 210, **style)
            self.canvas.create_line(200, 170, 220, 210, **style)

    def nouvelle_partie(self):
        self.mot = random.choice(self.mots).upper()
        self.lettres_trouvees = set()
        self.lettres_proposees = set()  # Réinitialiser les lettres proposées
        self.erreurs = 0
        
        # Ajout des lettres selon la difficulté
        if self.difficulte == "Facile":
            self.lettres_trouvees.add(self.mot[0])
            self.lettres_trouvees.add(self.mot[-1])
            self.lettres_proposees.update([self.mot[0], self.mot[-1]])
        elif self.difficulte == "Moyen":
            self.lettres_trouvees.add(self.mot[0])
            self.lettres_proposees.add(self.mot[0])
        
        self.actualiser_affichage()
        self.entry_lettre.delete(0, tk.END)
        self.dessiner_pendu()

    def actualiser_affichage(self):
        # Affichage du mot
        mot_affiche = " ".join(lettre if lettre in self.lettres_trouvees else "_" 
                              for lettre in self.mot)
        self.label_mot.config(text=mot_affiche)
        
        # Affichage des lettres proposées
        lettres = " ".join(sorted(self.lettres_proposees))
        self.label_lettres.config(text=lettres)

    def proposer_lettre(self):
        lettre = self.entry_lettre.get().upper()
        self.entry_lettre.delete(0, tk.END)
        
        if not lettre.isalpha() or len(lettre) != 1:
            messagebox.showwarning("Erreur", "Veuillez entrer une seule lettre !")
            return
        
        if lettre in self.lettres_proposees:
            messagebox.showinfo("Déjà proposée", "Vous avez déjà proposé cette lettre !")
            return
        
        self.lettres_proposees.add(lettre)
        
        if lettre in self.mot:
            self.lettres_trouvees.add(lettre)
        else:
            self.erreurs += 1
            self.dessiner_pendu()
            
            if self.erreurs >= self.max_erreurs:
                messagebox.showinfo("Perdu !", f"Le mot était : {self.mot}")
                self.nouvelle_partie()
                return
        
        self.actualiser_affichage()
        
        if all(lettre in self.lettres_trouvees for lettre in self.mot):
            messagebox.showinfo("Gagné !", "Félicitations ! Vous avez trouvé le mot !")
            self.nouvelle_partie()

if __name__ == "__main__":
    root = tk.Tk()
    menu = MenuPrincipal(root)
    root.mainloop()
