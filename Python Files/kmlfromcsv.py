#! python3
# kmlfromcsv.py - Creates kml from csv data
# csv formate: [imageName,URLLink,coordinates,imgDate,imageDisc]

import os, csv

# Text for KML file creation
KMLOpeningText = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2"
xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
<name>Photos</name>\n"""

KMLClosingText = """</Document>\n
</kml>"""

KMLStyleText = """\t\t<Style id="h_photo">
		<IconStyle>
			<scale>0.6</scale>
			<Icon>
				<href>https://github.com/claytoncook12/CC-Google-Earth/blob/master/Icons/Panoramio%20Icon.png?raw=true</href>
				<gx:w>32</gx:w>
				<gx:h>32</gx:h>
			</Icon>
		</IconStyle>
		<LineStyle>
			<color>ff000000</color>
			<width>0</width>
			<gx:labelVisibility>1</gx:labelVisibility>
		</LineStyle>
		<PolyStyle>
			<color>ff000000</color>
		</PolyStyle>
		<BalloonSytle>
			<text>$[description]</text>
		</BalloonSytle>
	</Style>
	<Style id="n_photo">
		<IconStyle>
			<scale>0.4</scale>
			<Icon>
				<href>https://github.com/claytoncook12/CC-Google-Earth/blob/master/Icons/Panoramio%20Icon.png?raw=true</href>
				<gx:w>32</gx:w>
				<gx:h>32</gx:h>
			</Icon>
		</IconStyle>
		<LabelStyle>
			<scale>0</scale>
		</LabelStyle>
		<LineStyle>
			<color>ff000000</color>
			<width>0</width>
			<gx:labelVisibility>1</gx:labelVisibility>
		</LineStyle>
		<PolyStyle>
			<color>ff000000</color>
		</PolyStyle>
		<BalloonSytle>
			<text>$[description]</text>
		</BalloonSytle>
	</Style>
	<StyleMap id="photo">
		<Pair>
			<key>normal</key>
			<styleUrl>#n_photo</styleUrl>
		</Pair>
		<Pair>
			<key>highlight</key>
			<styleUrl>#h_photo</styleUrl>
		</Pair>
	</StyleMap>\n"""

KMLPhotoFolderOpen = "\t<Folder>\n<name>Photo List</name>\n"

KMLPhotoFolderClose = "\t</Folder>"

def make_placemark_text(imageName,URLLink,coordinate,imgDate,imgDisc):
    """ returns text for placemark """ 

    if imgDisc == "":
        imgDisc = "[Insert image discription]"
    
    text = """<Placemark>
			<name>""" + imageName + """</name>
			<Snippet maxLines="0"></Snippet>
			<description><![CDATA[<html><head><link rel="stylesheet" type="text/css" href="https://github.com/claytoncook12/CC-Google-Earth/blob/master/styles/style.css?raw=true"/><head><body><div class="container">
						<h1>$[imgName1]</h1>
						<div class="photo-frame"><img style="height:400px" src=$[imgURL1]></div>
						<h2><em>Picture Details<em></h2>
						<div class="caption">
							<table>
							<tr bgcolor="#E3E3F3"><th>Date Taken</th><td>$[imgDate1]</td></tr>
							<tr bgcolor=""><th>Description</th><td>$[imgDisc1]</td></tr>
							<tr bgcolor="#E3E3F3"><th>Img URL</th><td><a href="$[imgURL1]">$[imgURL1]</a></td></tr>
							</table>
						</div>
						</body></html>]]></description>
			<styleUrl>#photo</styleUrl>
			<ExtendedData>
				<Data name="imgName1">
					<value>""" + imageName + """</value>
				</Data>
				<Data name="imgDate1">
					<value>""" + imgDate + """</value>
				</Data>
				<Data name="imgDisc1">
					<value>""" + imgDisc + """</value>
				</Data>
				<Data name="imgURL1">
					<value>""" + URLLink + """</value>
				</Data>
			</ExtendedData>
			<Point>
				<coordinates>""" + coordinate + """</coordinates>
			</Point>
		</Placemark>\n"""
    
    return text

# Introduction Text
print("Will be creating a kml file from a formated CSV file.\n\
The CSV must have heading and data in the order show here:\n\
[imageName,URLLink,coordinates,imgDate,imageDisc]\n")

# User Inputs file location
while True:
    print("Input new kml file name:")
    fileName = input()
    print("Is this correct?[y/n]\nfile name: %s" % fileName)
    correct = input()
    if correct.lower() == "y":
        break

# User inputs folder location
while True:
    print("Input folder location for new kml file:\n\
[ex: C:/folder/]")
    folderLoc = input()
    print("Is this correct?[y/n]\nfolder location:\n%s" % folderLoc)
    correct = input()
    if correct.lower() == "y":
        break

# User Inputs csv location
while True:
    print("Input csv file location and name:\n\
[ex: C:/folder/file.csv]")
    csvFile = input()
    print("Is this correct?[y/n]\n%s" % csvFile)
    correct = input()
    if correct.lower() == "y":
        break

# Read in CSV data
dataCSV = open(csvFile)
dataReader = csv.reader(dataCSV)

# Creat kml file in named location
os.chdir(folderLoc)
createKML = open(folderLoc+'/'+fileName+'.kml','w')
createKML.write(KMLOpeningText)
createKML.write(KMLStyleText)
createKML.write(KMLPhotoFolderOpen)

# Add Placemark Data to KML from csv file
for row in dataReader:

    # ignore Csv first line
    if row[0] != "imageName":
        
        placeMarkText = make_placemark_text(row[0],row[1],row[2],row[3],row[4])

        createKML.write(placeMarkText)

# Closing KML Text Addition
createKML.write(KMLPhotoFolderClose)
createKML.write(KMLClosingText)
createKML.close()

# Close CSV file
dataCSV.close()

# Final comments
print("Done")
