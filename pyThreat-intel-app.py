# Python Threat intel App

import PySimpleGUI as sg
import os.path # used to grab folder contents

def fetch_api_data(query):
    """Simulate an API call (replace with your real API logic)."""
    time.sleep(2)  # Simulate network delay
    try:
        # Example: GET request to a public API
        response = requests.get(f"https://api.agify.io?name={query}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

icon_path = os.path.basename("favicon.ico")

#window layout in 2 columns
sg.theme('LightBlue3')
file_column = [
	[
		sg.Text("File Checker (Enter a Filehash):"),
		sg.In(size=(25,1), enable_events = True, key="-FILEHASH-"),
		sg.Button("Submit",tooltip="Please enter a Filehash")
	],
	[
		sg.Multiline("",size=(60,15), key="-OUTPUT-", disabled=True, autoscroll=True)
	],
]

URL_column = [
	[
		sg.Text("URL Checker"),
		sg.In(size=(25,1), enable_events = True, key="-URL-"),
		sg.Button("Submit",tooltip="Please enter a URL")
	],
	[
		sg.Multiline("",size=(60,15), key="-OUTPUT-", disabled=True, autoscroll=True)
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

	if event == "-FOLDER-":
		folder = values["-FOLDER-"]
		try:
			#Get list of files in folder
			file_list = os.listdir(folder)
		except:
			file_list = []

		fnames = [
			f
			for f in file_list
			if os.path.isfile(os.path.join(folder,f))
			and f.lower().endswith((".png", ".gif"))
		]
		window["-FILE LIST-"].update(fnames)

	elif event == "-FILE LIST-": # once a file is chosen
		try:
			filename = os.path.join(
				values["-FOLDER-"], values["-FILE LIST-"][0]
			)
			window["-TOUT-"].update(filename)
			window["-IMAGE-"].update(filename=filename)
		except:
			pass

window.close()