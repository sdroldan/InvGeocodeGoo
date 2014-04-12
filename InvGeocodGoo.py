#!/usr/local/bin/python2

## python LatLonGoo.py data.csv datlatlon.csv
from sys import argv
import csv
import urllib2
import csv
import re
from sys import argv
try:
  from lxml import etree
  print("running with lxml.etree")
except ImportError:
  try:
    # Python 2.5
    import xml.etree.cElementTree as etree
    print("running with cElementTree on Python 2.5+")
  except ImportError:
    try:
      # Python 2.5
      import xml.etree.ElementTree as etree
      print("running with ElementTree on Python 2.5+")
    except ImportError:
      try:
        # normal cElementTree install
        import cElementTree as etree
        print("running with cElementTree")
      except ImportError:
        try:
          # normal ElementTree install
          import elementtree.ElementTree as etree
          print("running with ElementTree")
        except ImportError:
          print("Failed to import ElementTree from any known place")
def esphttp(cadena):
	return re.sub(r"\s","%20",cadena)


#DEFINICION FUNCION
def capLatLon(ide,cas,cal,ciu,pro,pai):
	res=-1
#Construye comando 
	url='https://maps.googleapis.com/maps/api/geocode/xml?address='+str(cas)+'+'+esphttp(cal)+'+'+esphttp(ciu)+'+'+esphttp(pro)+'+'+esphttp(pai)+'&sensor=false'
#	url='https://maps.googleapis.com/maps/api/geocode/xml?address='+str(cas)+'+'+cal+'+'+ciu+'+'+pro+'+'+pai+'&sensor=false'

# Intenta aplicar comandos y si no funciona da error de excepcion
	try:
		pag=urllib2.urlopen(url) # Se conecta a la url y pone el resultado en variable
		contxml=pag.read() 
		pru= etree.fromstring(contxml) # Mete el resultado como texto un formato etree (xml)
	# Busca el tag lat y devuelve el contenido de texto separado por ";"
		lat=pru.findtext(".//lat")
		lon=pru.findtext(".//lng")		
		print("{0}|{1} {2};{3};{4};{5}\nlatitud={6}\nlongitud={7}".format(ide,cal,str(cas),ciu,pro,pai,str(lat),str(lon)))  
	except IndexError:
		print("No de conecta")
	return [ide,lat,lon]

#FIN FUNCION --------------------
fichout=open(argv[2],'w')
fichout.write("###SDRB\nFuente: GoogleMaps\nide,Latitud,Longitud\n")
fich_w=csv.writer(fichout,delimiter=';')
with open(argv[1]) as f:
	reader=csv.reader(f,delimiter=';')
	for row in reader:
		res=capLatLon(ide=row[0],cas=row[1],cal=row[2],ciu=row[3],pro=row[4],pai=row[5])
		resu="{0}\t{1} {2};{3};{4};{5};{6};{7}".format(row[0],row[2],row[1],row[3],row[4],row[5],res[1],res[2])
		fich_w.writerow(res)

fichout.close()
 
