# 🐍 Snake Game in Python

## 📌 À propos du projet
Ce projet est un **jeu Snake en console** développé en Python.  
L'objectif principal était de **réviser et renforcer mes bases en Python**, notamment :
- Manipulation des **listes et tuples**
- Gestion des **entrées clavier** avec `pynput`
- Conception d'une **boucle de jeu** et mises à jour en temps réel


---

## 🎮 Fonctionnalités
- **Mécanique classique du Snake** : déplacement, fruit, croissance
- **Contrôles clavier** :
  - `W` / `↑` → Haut
  - `S` / `↓` → Bas
  - `A` / `←` → Gauche
  - `D` / `→` → Droite
  - `ESC` → Quitter
- Placement aléatoire des fruits
- Détection des collisions (murs et corps)

---

## 🛠 Prérequis
- Python 3.x
- Bibliothèque `pynput`  
Installation :
```bash
pip install pynput
```

---

## ▶️ Lancer le jeu
1. Cloner le dépôt :
   ```bash
   git clone https://github.com/tonpseudo/snake-python.git
   cd snake-python
   ```
2. Exécuter :
   ```bash
   python snake.py
   ```

---

## ✅ Objectifs d'apprentissage
Grâce à ce projet, j'ai pratiqué :
- La conception d'une **boucle de jeu**
- La **programmation événementielle**
- Les **structures de données dynamiques**
- La gestion **cross-platform** du terminal

---

## 🔮 Améliorations possibles
- Ajouter un **score**
- Mode **wrap-around** (traverser les bords)
- Passer en **programmation orientée objet** avec une classe `SnakeGame`
- Ajouter des **couleurs** avec `colorama`
