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
<kml xmlns="http://www.opengis.net/kml/2.2" 
xmlns:gx="http://www.google.com/kml/ext/2.2"
xmlns:kml="http://www.opengis.net/kml/2.2" 
xmlns:atom="http://www.w3.org/2005/Atom">
<Document>\n"""

KMLClosingText = """</Document>\n
                    </kml>"""

KMLStyleText = """\t<StyleMap id="1052804">\n\t\t<Pair>\n\t\t\t<key>normal</key>\n\t\t\t<styleUrl>#pano_cluster3n</styleUrl>\n\t\t</Pair>\n\t\t<Pair>\n\t\t\t<key>highlight</key>\n\t\t\t<styleUrl>#pano_cluster3h</styleUrl>\n\t\t</Pair>\n\t</StyleMap>\n\t<Style id="pano_cluster3n">\n\t\t<IconStyle>\n\t\t\t<scale>0.4</scale>\n\t\t\t<Icon>\n\t\t\t\t<href>http://kh.google.com:80/flatfile?lf-0-icons/panoramio_cluster_n2.png</href>\n\t\t\t\t<gx:w>32</gx:w>\n\t\t\t\t<gx:h>32</gx:h>\n\t\t\t</Icon>\n\t\t</IconStyle>\n\t\t<LabelStyle>\n\t\t\t<scale>0</scale>\n\t\t</LabelStyle>\n\t\t<LineStyle>\n\t\t\t<color>ff000000</color>\n\t\t\t<width>0</width>\n\t\t\t<gx:labelVisibility>1</gx:labelVisibility>\n\t\t</LineStyle>\n\t\t<PolyStyle>\n\t\t\t<color>ff000000</color>\n\t\t</PolyStyle>\n\t</Style>\n\t<Style id="pano_cluster3h">\n\t\t<IconStyle>\n\t\t\t<scale>0.6</scale>\n\t\t\t<Icon>\n\t\t\t\t<href>http://kh.google.com:80/flatfile?lf-0-icons/panoramio_cluster_n2.png</href>\n\t\t\t\t<gx:w>32</gx:w>\n\t\t\t\t<gx:h>32</gx:h>\n\t\t\t</Icon>\n\t\t</IconStyle>\n\t\t<LabelStyle>\n\t\t</LabelStyle>\n\t\t<LineStyle>\n\t\t\t<color>ff000000</color>\n\t\t\t<width>0</width>\n\t\t\t<gx:labelVisibility>1</gx:labelVisibility>\n\t\t</LineStyle>\n\t\t<PolyStyle>\n\t\t\t<color>ff000000</color>\n\t\t</PolyStyle>\n\t</Style>"""

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
            print("Did not add to kml file")
            print("")
    
    return imageInformation
        
def make_placemark_text(name,date,height,latitude,longitude,ratio):
    """ returns text for placemark """ 
    
    ratioedHeight = str(int(ratio * height))
    
    text1 = """<Placemark>\n"""
    text2 = """<name>""" + name + """</name>\n"""
    text3 = """<description><![CDATA[\n"""
    text4 = """Image was taken on """ + date.replace(':','/')
    text5 = '<p><img src="' +  name + '"' +' width= "500" height="'+ ratioedHeight + '"/></p>]]>\n'
    text6 = """</description>\n
<styleUrl>#1052804</styleUrl>\n
<Point>\n"""
    text7 = """\t<coordinates> -"""+str(longitude)+""","""+str(latitude)+""",0</coordinates>\n
</Point>\n
</Placemark>\n"""
    
    return text1+text2+text3+text4+text5+text6+text7 
    
    
def find_image_ratio_for_kml(imageDict, imageWidth=700):
    """ scales image to imageWidth
    while keeping ratio """
    
    for key,values in imageDict.items():

        width = values['width']

        ratio = imageWidth/width

        imageDict[key]['ratio'] = ratio
        
    return imageDict

def create_kml(folder,name):
    """ creates kml file with pictures in folder location,
    kml file will be located in folder location 
    folder - absolute folder location
    name - name of kml file to create """
    
    # return dict of image information
    imageInfo = pics_info_for_kml(folder)
    
    # find ratio to use for image scaling
    imageInfo =  find_image_ratio_for_kml(imageInfo)
    
    # create kml file in folder location
    kmlFile = open(folder+'\\'+name+'.kml','w')
    kmlFile.close()
    
    # Start Adding KML Information
    
    # Add start string
    kmlFile = open(folder+'\\'+name+'.kml','a')
    kmlFile.write(KMLOpeningText)
    
    # Add Name string
    kmlFile.write('\t<name>'+name+'.kml'+'</name>\n')
    
    # Add Styles
    kmlFile.write(KMLStyleText)
    
    # Add PLacemarks
    for key,values in sorted(imageInfo.items()):
        
        placeMarkText = make_placemark_text(key,
                                            values['date'],
                                            values['height'],
                                            values['latitude'],
                                            values['longitude'],
                                            values['ratio'])
        
        
        kmlFile.write(placeMarkText)
        
    # Add Closing Text
    kmlFile.write(KMLClosingText)
    
    kmlFile.close()
    
        
        
        
        
        
        
        