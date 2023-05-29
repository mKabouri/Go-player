# Authors:
- AHBAIZ Mouhcine <mahbaiz@enseirb-matmeca.fr>
- KABOURI Mohamed Yassine <mkabouri@enseirb-matmeca.fr>

# À propos de notre joueur:
- Notre joueur est dans le fichier `myPlayer.py`
- On a utlisé l'algorithme alpha beta pour notre joueur.
- En plus, la profondeur dépend du la limite du temps fixé (Iterative deepening): le joueur explore plus en lui offrant plus de temps.
- Concernant les heuristiques, on a implémenté trois heuristiques:
		
		- Nombre de stones: le joueur suit le chemin qui lui offre le plus des pierres.
		- Nombre de libertés: le joueur choisit le chemin qui lui offre le plus des libertés.
		- Connexité: le joueur essaie de construire une partie connexe la plus grande possible.
- Ces trois heuristiques sont mises en jeu sous différentes coefficients (entièrs), ces coefficients étaient approximé en utilisant un script shell qui lance plusieurs parties.

# Ce qu'on est fier d'avoir faire dans le projet:
- Pouvoir utiliser l'iterative deepening, nous avons pu arriver à des profondeurs maximales sont dépasser la limite du temps.
- Faire des heuristiques surtout celle de connexité.

# Sources:
- AI techniques for the game of Go [link](http://erikvanderwerf.tengen.nl/pubdown/thesis_erikvanderwerf.pdf)
