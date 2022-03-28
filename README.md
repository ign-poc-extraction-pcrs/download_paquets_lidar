# download_paquets_lidar

## Initialisation projet

installation de l'environnement virtuel et des packages
```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt 
```

Lancer serveur :
- dev (test-dev-sidc) : http://test-dev-sidc:5000/download/lidar
```
python run.py
```
- prod (test-prod-sidc) : http://test-prod-sidc:5000/download/lidar
```
python run_prod.py
```


## Architecture

- run.py & run_prod.py : fichier qui lance le serveur en dev et en prod
- requirements.txt : fichier qui contient les packages à installer pour que le projet fonctionne
- app.py : script en flask, qui recupere la grille lidar, la met sous forme de shapefile et la telecharge en zip
- templates/ : contient la page html pour l'affichage avec le bouton
- static/ : contient le style (css) de la page html 



