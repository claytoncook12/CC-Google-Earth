#Creates list of images

import os
import sys

def main():

	#finds present working dir
	pwd = os.getcwd()

	#Opens file
	fileList = open("imageList.txt","w")

	for file in os.listdir(pwd):
		if os.path.splitext(file)[1].lower() in ('.jpg', '.jpeg'):
			fileList.write(file+",\n")
	
	#Close File
	fileList.close()

	print ("Done")

if __name__ == "__main__":
	main()