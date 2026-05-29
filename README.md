# PyTIA-D

A small personal project: a desktop app that looks up file hashes and URLs against the [VirusTotal](https://www.virustotal.com/) API and shows a short summary (verdict, detection ratio, analysis stats, and related fields).

This is not a production tool—just something I built for my own use and learning.

## Requirements

- Windows (the packaged build is a Windows executable)
- A [VirusTotal](https://www.virustotal.com/) API key, set as the environment variable `VirusTotal_API_Key`

## Option 1: Use the executable

1. Obtain a VirusTotal API key and set `VirusTotal_API_Key` in your user or system environment variables.
2. Run `dist/pyThreat-intel-app.exe` (or `pyThreat-intel-app.exe` if you have a copy at the project root).

The app opens a simple window with two panels: file hash lookup and URL lookup. Enter a SHA256 hash or URL and click Submit.

## Option 2: Run from source

1. Install [Python](https://www.python.org/) (the project was developed with a recent Python 3 release).
2. Set the `VirusTotal_API_Key` environment variable as above.
3. Install dependencies:

   ```bash
   pip install PySimpleGUI vt-py
   ```

4. From the project directory:

   ```bash
   python pyThreat-intel-app.py
   ```

## Building the executable

If you change the source and want a new `.exe`, install [PyInstaller](https://pyinstaller.org/) and run:

```bash
pyinstaller pyThreat-intel-app.spec
```

The output is written under `dist/`.

## Notes

- API lookups are subject to VirusTotal rate limits and account permissions.
- The console may print status messages when the app starts or when a URL check runs; the main interface is the GUI window.
