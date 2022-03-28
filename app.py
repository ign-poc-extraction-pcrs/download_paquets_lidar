from distutils import extension
from flask import Flask, render_template, request, send_file
import requests
import json
import xmltodict
from io import BytesIO
from zipfile import ZipFile
import os, glob

from librairie_commune.io.ShpService import create_shp_file, update_shp_file


app = Flask(__name__)

@app.route('/download/lidar', methods=['GET'])
def download_lidar():
    return render_template('shape_lidar.html')


@app.route('/download/lidar/shp', methods=['GET', 'POST'])
def download_shp():
    # path and file du shp
    PATH_SHP = "/tmp/api_dispo_produit_tmp_file"
    file_shp = "TA_diff_pkk_lidarhd"

    # recuperation des paquets lidar
    get_paquets_lidar(PATH_SHP, file_shp)  
    # chemin absolue du shp
    file = f"{PATH_SHP}/{file_shp}"
    # les extensions du shp
    extensions = ["dbf", "shp", "prj", "shx"]  
    # creation du zip
    memory_file = BytesIO()
    zip_folder =  ZipFile(memory_file, 'w')
    #  on insere chaque fichier par extension dans le zip
    for extension in extensions:
        # on ajoute le fichier dans le zip qui sera envoyé
        zip_folder.write(f"{file}.{extension}", os.path.basename(f"{file}.{extension}"))

    zip_folder.close()
    memory_file.seek(0)
    return send_file(memory_file, download_name=f'grille.zip', as_attachment=True)


def get_paquets_lidar(path_shp, file_shp):
    """ recupere les paquets lidar
    """
    # on recupere le xml
    SIZE = 2000  
    data = ""
    key = "c90xknypoz1flvgojchbphgt"
    r = requests.get(f"https://wxs.ign.fr/{key}/telechargement/prepackage?request=GetCapabilities")
    # on parse et on transforme le xml en dict
    obj = xmltodict.parse(r.content)
    json_lidar = json.dumps(obj)
    json_lidar = json.loads(json_lidar)
    # on recupere les differents paquets lidar [list]
    paquets_lidar = json_lidar["Download_Capabilities"]["Capability"]["Resources"]["Resource"]
    # on boucle sur chaque paquet pour recuperer les coordonnées
    data = []
    for key , paquet in enumerate(paquets_lidar) :
        # on recupere le x et y du nom du paquet
        name = paquet["Name"]
        x, y = name.split("-")[2].split("_")
        name = paquet["Name"].split("$")[-1]


        # on convertit les bonnes coordonnées
        x_min = int(x) * 1000
        y_min = int(y) * 1000
        x_max = x_min + SIZE
        y_max = y_min - SIZE

        # ce qui va etre envoyer dans ls shp
        name_colonne = "nom_pkk"
        colonne = [{"nom_colonne": name_colonne, "type": "C"}]
        data.append({name_colonne: name, "Geometry": {'type': 'Polygon', 'coordinates': [[(x_min, y_max), (x_max, y_max), (x_max, y_min), (x_min, y_min), (x_min, y_max)]]}})
    
    # creation du shapefile
    create_shp_file(f"{path_shp}/{file_shp}", colonne, data, 2154)