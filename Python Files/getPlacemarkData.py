# File for reading placemark data in google earth kml file

import xml.etree.ElementTree as ET
import re
import os, sys

# Create file for writing placemarks data
# finds present working dir
pwd = os.getcwd()

#Opens file
fileName = "placemarksFound.txt"
fileList = open(fileName,"w")

# Read in data From KML
tree = ET.parse('Work Projects.kml')
root = tree.getroot()

# Find Placemarks
foundPlacemarks = root.findall('.//{http://www.opengis.net/kml/2.2}Placemark')

# Print Placemark Data
count = 0
for placemark in foundPlacemarks:

        # Find if name has image extension
        name = placemark.find('{http://www.opengis.net/kml/2.2}name').text
        name = name.lower()
        if ".jpg" in name:

                # Count of Files Wrote
                count += 1

                # Find Coordinates and Date Image Was Taken
                coord = placemark.find('{http://www.opengis.net/kml/2.2}Point').find('{http://www.opengis.net/kml/2.2}coordinates').text
                date = placemark.find('{http://www.opengis.net/kml/2.2}description').text

                # Parse Out Data From date text
                m = re.search('Image was taken on (\d\d\d\d/\d\d/\d\d)',date)
                date = m.group(1)

                # Write Placemark Info Found to File
                fileList.write(name + ",,[" + coord + "]," + date + ",\n")

# Close File
fileList.close()

print("Wrote %d to %s" % (count,fileName))
