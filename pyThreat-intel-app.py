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
        urlToCheck = client.get_object("/urls/"+url_id)
        return urlToCheck
    except Exception as e:
        raise Exception(f"URL lookup failed: {e}")

def format_analysis_stats(stats):
	order = ["malicious","suspicious","undetected","harmless","timeout"]

	line = []

	for key in order:
		value = stats.get(key,0)
		line.append(f"{key.capitalize()}: {value}")

	return "\n".join(line)

def format_categories(categories):
	lines = []

	for vendor, category in categories.items():
		lines.append(f"{vendor}: {category}")
	return "\n".join(lines)

def make_verdict(stats):
	malicious_count = stats.get("malicious",0)
	suspicious_count = stats.get("suspicious",0)

	if malicious_count > 0:
		return "Potentially Malicious"
	if suspicious_count >0:
		return "Suspicious"
	else:
		return "Clean"

def detection_ratio(stats):
	malicious_count = stats.get("malicious",0)
	total = sum(stats.values())
	return f"{malicious_count} / {total}"

def build_url_output(urlChecked):
	stats = urlChecked.last_analysis_stats
	categories = urlChecked.get("categories",{})
	reputation = urlChecked.get("reputation","N/A")

	stats_text = format_analysis_stats(stats)
	categories_text = format_categories(categories)
	verdict = make_verdict(stats)
	ratio = detection_ratio(stats)

	output = f"""
Initial URL: {urlChecked.url}

~~ Verdict ~~
{verdict}

~~ Detection Ration ~~
{ratio}

~~ Analysis Summary ~~
{stats_text}

~~ Categories ~~
{categories_text}

~~ Reputation ~~
Score: {reputation}
"""
	return output.strip()

def build_file_output(file):
	stats = file.last_analysis_stats

	stats_text = format_analysis_stats(stats)
	verdict = make_verdict(stats)
	ratio = detection_ratio(stats)

	output = f"""
File Names: {file.names}
SHA256: {file.sha256}
Size(in bytes): {file.size}

~~ Verdict ~~
{verdict}

~~ Detection Ratio ~~
{ratio}

~~ Analysis Summary ~~
{stats_text}
"""
	return output.strip()
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

window = sg.Window("Day-Dz | The Check-a-matic 2000", layout, icon=icon_path)

while True:
	event, values = window.read()
	if event == "Exit" or event == sg.WIN_CLOSED:
		break

	if event == "-FILEBUTTON-":
		try:
			file = fetch_file_data(values["-FILEHASH-"])
			formatted_output = build_file_output(file)
			window["-OUTPUT1-"].update(formatted_output)
		except Exception as e:
			window["-OUTPUT1-"].update(str(e))

	elif event == "-URLBUTTON-":
		print("> Attempting to pull URL information...")
		try:
			urltoCheck = fetch_URL_data(values["-URL-"])
			formatted_output = build_url_output(urltoCheck)
			window["-OUTPUT2-"].update(formatted_output)
		except Exception as e:
			window["-OUTPUT2-"].update(str(e))

window.close()