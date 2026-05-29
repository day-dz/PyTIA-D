# Python Threat intel App

import PySimpleGUI as sg
import os.path # used to grab folder contents
import os
import vt
import time

try:
	client = vt.Client(os.getenv("VirusTotal_API_Key"))
	print("> API key found...")
	print("> Booting application...")
except:
	print("> No API key found at environment variable VirusTotal_API_Key")



def fetch_file_data(filehash):
    time.sleep(2)  # Simulate network delay
    try:
        file = client.get_object("/files/" + filehash)
        return file
    except Exception as e:
        raise Exception(f"file lookup failed: {e}")

def fetch_URL_data(url):
    time.sleep(2)  # Simulate network delay
    try:
        url_id = vt.url_id(url)
        print("> Attempting to pull information about "+ url_id + " ...")
        urlToCheck = client.get_object("/urls/"+url_id)
        return urlToCheck
    except Exception as e:
        raise Exception(f"URL lookup failed: {e}")

icon_path = os.path.basename("favicon.ico")

#window layout in 2 columns
sg.theme('LightBlue3')
file_column = [
	[
		sg.Text("File Checker (Enter a Filehash):"),
		sg.In(size=(25,1), enable_events = True, key="-FILEHASH-"),
		sg.Button("Submit",tooltip="Please enter a Filehash", key="-FILEBUTTON-")
	],
	[
		sg.Multiline("",size=(60,15), key="-OUTPUT1-", disabled=True, autoscroll=True)
	],
]

URL_column = [
	[
		sg.Text("URL Checker"),
		sg.In(size=(25,1), enable_events = True, key="-URL-"),
		sg.Button("Submit",tooltip="Please enter a URL", key="-URLBUTTON-")
	],
	[
		sg.Multiline("",size=(60,15), key="-OUTPUT2-", disabled=True, autoscroll=True)
	],
]

layout = [
	[
		sg.Column(file_column),
		sg.VSeperator(),
		sg.Column(URL_column),
	]
]

window = sg.Window("Day-Dz | Threat Intel App", layout, icon=icon_path)

while True:
	event, values = window.read()
	if event == "Exit" or event == sg.WIN_CLOSED:
		break

	if event == "-FILEBUTTON-":
		try:
			file = fetch_file_data(values["-FILEHASH-"])
			window["-OUTPUT1-"].update("File Names: "+file.names+
			"\nFile size: "+str(file.size)+" bytes" +
			"\nFile Sha256: "+str(file.sha256) +
			"\nFile Type: "+str(file.type_tag) +
			"\nFile Last Analysed Statistics: "+str(file.last_analysis_stats))
		except Exception as e:
			window["-OUTPUT1-"].update(str(e))

	elif event == "-URLBUTTON-":
		print("> Attempting to pull URL information...")
		try:
			urltoCheck = fetch_URL_data(values["-URL-"])
			
		except Exception as e:
			window["-OUTPUT2-"].update(str(e))

window.close()