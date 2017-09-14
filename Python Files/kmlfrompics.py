#! python3
# kmlfrompics.py - Creates kml from pictures in a folder location

import os,exifread,re

# Image information from EXIF data
imageDataWanted = ['EXIF ExifImageWidth','EXIF ExifImageLength','EXIF DateTimeOriginal',
                   'GPS GPSLatitude','GPS GPSLongitude']

# Regexs for EXIF data
dateTimeRegex = re.compile(r'(\d\d\d\d:\d\d:\d\d) (\d\d:\d\d:\d\d)')
GPSRegex = re.compile(r'\S(\d+)\S\s(\d+)\S\s(\d+/\d+)')

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

def formate_coordinates_to_degrees(degrees,minutes,seconds):
    degrees = float(degrees)
    
    minutes = (float(minutes)/60.0)
    
    seconds = float(int(seconds.split("/")[0])/int(seconds.split("/")[1]))
    seconds = (float(seconds)/3600.0)
    
    degreeCoor = degrees+minutes+seconds
    
    return degreeCoor


def jpgs_in_folder(location):
    """ Returns list of jpgs in folder location """
    
    # get list of files in location
    files = os.listdir(location)
    
    # List for image files
    imageFiles = []
    
    # keep only jpgs from list
    for image in files:
        if image.split(".")[-1] == "jpg":
            imageFiles.append(image)
            
    return imageFiles

def pics_info_for_kml(folder):
    """ Creates dict with pictures information from folder with pictures in it. 
    folder - absolute path of folder with pictures"""
    
    # Dict for pictures information 
    imageInformation = {}
    
    # get list of jpgs in folder
    imageFiles = jpgs_in_folder(folder)
    
    # get dict of Picture information
    for image in imageFiles:

        try:
            f = open(folder+"\\"+image,'rb')
            tags = exifread.process_file(f,details=False)

            # select wanted tags
            wantedTags = { your_key: tags[your_key] for your_key in imageDataWanted }

            # formate returned wantedTags information

            # find width and height
            width = int(str(wantedTags['EXIF ExifImageWidth']))
            height = int(str(wantedTags['EXIF ExifImageLength']))

            # formate data and time
            dateTime = dateTimeRegex.search(str(wantedTags['EXIF DateTimeOriginal']))
            date = dateTime.group(1)
            time = dateTime.group(2)

            # formate Lat and Long values
            latitude = GPSRegex.search(str(wantedTags['GPS GPSLatitude']))
            latitudeCoor = formate_coordinates_to_degrees(latitude.group(1),
                                                          latitude.group(2),
                                                          latitude.group(3))
            longitude = GPSRegex.search(str(wantedTags['GPS GPSLongitude']))
            longitudeCoor = formate_coordinates_to_degrees(longitude.group(1),
                                                           longitude.group(2),
                                                           longitude.group(3))

            # Add Information Found to Picture Dict
            imageInformation[image] = {'width': width,
                                       'height': height,
                                       'date': date,
                                       'time': time,
                                       'latitude': latitudeCoor,
                                       'longitude': longitudeCoor}
            
        except:
            print("Error with",image)
            print("Did not add to kml file\n")
    
    return imageInformation
        
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

def create_kml(folder,name):
    """ creates kml file with pictures in folder location,
    kml file will be located in folder location 
    folder - absolute folder location
    name - name of kml file to create """
    
    # return dict of image information
    imageInfo = pics_info_for_kml(folder)
    
    # create kml file in folder location
    kmlFile = open(folder+'/'+name+'.kml','w')
    kmlFile.close()
    
    # Start Adding KML Information
    
    # Add start string
    kmlFile = open(folder+'/'+name+'.kml','a')
    kmlFile.write(KMLOpeningText)
    
    # Add Name string
    kmlFile.write('\t<name>'+name+'.kml'+'</name>\n')
    
    # Add Styles
    kmlFile.write(KMLStyleText)
    
    # Add Placemarks
    for key,values in sorted(imageInfo.items()):
        
        placeMarkText = make_placemark_text(key,
                                            key,
                                            "-"+str(values['longitude'])+","+str(values['latitude'])+","+"0",
                                            values['date'].replace(":", "/"),
                                            "[Insert image discription]")

        kmlFile.write(placeMarkText)
        
    # Add Closing Text
    kmlFile.write(KMLClosingText)
    
    kmlFile.close()

# User Inputs kml file name
while True:
    print("Input new kml file name [exclude .kml]:")
    fileName = input()
    print("Is this correct?[y/n]\nfile name: %s" % fileName)
    correct = input()
    if correct.lower() == "y":
        break

# User inputs folder location
while True:
    print("Input folder location of images where kml will be created:\n\
[ex: C:/folder/]")
    folderLoc = input()
    print("Is this correct?[y/n]\nfolder location:\n%s" % folderLoc)
    correct = input()
    if correct.lower() == "y":
        break

# Read Imgs and Create KML File
create_kml(folderLoc,fileName)

# Final Comments
print("Done with kml creation.")

