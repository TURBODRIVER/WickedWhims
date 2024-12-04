# INTRO

<p>Welcome to the TURBODRIVER Translation Package Creator.<br>
This tool will convert your translated JSON files into a usable PACKAGE file mod.<br>
To use this tool you need to install Python and place translated JSON file into the folder you're running this tool from.<br>
If Python is installed and a JSON file is present, input the language code you want to create the PACKAGE file for.</p>

Python Download: https://www.python.org/ <br>
JSON Validator: https://jsonlint.com

**You can skip using the TURBODRIVER Translation Package Creator if you're using the [Voky's Translator JSON tool](https://github.com/TURBODRIVER/sims4-translator/releases) for Windows.**

# HOW TO USE THIS TOOL

1. Create a folder for translations on your computer.
2. Download the **ConvertJSONtoPACKAGE.py** file into your translations folder.
3. Download either **RunMeOnWindows.bat** if you're on Windows or **RunMeOnMac.sh** if you're on MacOS.
4. Proceed to the [String Tables page](https://github.com/TURBODRIVER/WickedWhims/tree/master/String%20Tables).
5. Choose the JSON translation file with the language you are translating and download it to your translations folder.
6. Open the downloaded JSON translation file with any text editor and translate the "Value" text strings.
7. Run **RunMeOnWindows.bat** on Windows or **RunMeOnMac.sh** on MacOS and follow the displayed instructions.
8. The created PACKAGE file is your ready to use translation.

# WHAT IF I WANT TO USE OTHER TOOLS

I recommend using the [Voky's Translator JSON tool](https://github.com/TURBODRIVER/sims4-translator/releases) for Windows. It's a modified version of Voky's Translator to be capable of loading JSON files that then can be directly saved as a PACKAGE file.

<p>If you're looking to use other tools for translating, follow the instructions above but skip points 4, 5, and 6.<br>
Doing so will create you a PACKAGE file with text string that were not translated. From there you can load the PACKAGE file into other translation tools.<br>
If you want to use this tool again, you can open your PACKAGE file in Sims 4 Studio and directly copy the String Tables Text output into JSON files. The ConvertJSONtoPACKAGE.py tool will still process it. If the tool you're using can save to a PACKAGE file then use that functionality instead.</p>

# HOW TO SUBMIT TRANSLATIONS

If you're looking to contribute your translation efforts, proceed to the [String Tables page](https://github.com/TURBODRIVER/WickedWhims/tree/master/String%20Tables) for details.
