import os,json,folium
from folium.plugins import FastMarkerCluster,HeatMap
from datetime import datetime

div = 10**7
path = os.getcwd()
dataPath = path + "/data/"
mapsPath = path + "/maps/"


def test(file,mode=1,date=""):

    #ficheiro json
    jFile = file + ".json"

    #caminho para o ficheiro json
    filePath = dataPath+jFile

    #abre o ficheiro
    readFile = open(filePath)
    locations = json.load(readFile)

    #cria o mapa
    map = folium.Map(zoom_start=6)

    #numero de localizacoes
    #print (len(locations['locations']))

    #para todos os locais,
    #retira latitude/longitude
    #e insere na lista de pontos
    points = []
    for location in locations['locations']:
        if(date != ""):
            time = getTime(location)
            if date in time:
                appendPoint(points,location)
        else:
            appendPoint(points,location)

    if mode:# =1 , desenha os pontos
        map.add_child(FastMarkerCluster(points))
        map.save(mapsPath+file+"_points"+".html")
    else:   # =0 , desenha o heatmap
        map.add_child(HeatMap(points,max_val=50))
        map.save(mapsPath+file+"_heat"+".html")

    #fecha o ficheiro
    readFile.close()

#adiciona o ponto a lista
def appendPoint(points,location):
    lat = location['latitudeE7']  / div
    lon = location['longitudeE7'] / div
    points.append([lat,lon])

#retorna a data e tempo usando o timestamp
def getTime(location):
    time = int(location['timestampMs'][:-3])
    time = str(datetime.fromtimestamp(time))
    return time
