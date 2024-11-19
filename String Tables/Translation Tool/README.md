# INTRO

Welcome to the TURBODRIVER Translation Creator.
This tool will convert your translated JSON files into a usable PACKAGE file mod.
To use this tool you need to install Python and place translated JSON file into the folder you're running this tool from.
If Python is installed and a JSON file is present, input the language code you want to create the PACKAGE file for.

Python Download: https://www.python.org/
JSON Validator: https://jsonlint.com

# HOW TO TRANSLATE

1. Create a folder for translations on your computer
2. Download the ConvertJSONtoPACKAGE.py file into your translations folder
3. Download either RunMeOnWindows.bat if you're on Windows or RunMeOnMac.sh if you're on MacOS
4. Proceed to https://github.com/TURBODRIVER/WickedWhims/tree/master/String%20Tables
5. Choose the JSON translation file with the language you are translating and download it to your translations folder
6. Open the downloaded JSON translation file with any text editor and translate the "Value" text strings
7. Run RunMeOnWindows.bat on Windows or RunMeOnMac.sh on MacOS and follow the displayed instructions
8. The created PACKAGE file is your ready to use translation

# WHAT IF I WANT TO USE OTHER TOOLS

If you're looking to use other tools for translating, follow the instructions above but skip points 4, 5, and 6.
Doing so will create you a PACKAGE file with text string that were not translated. From there you can load the PACKAGE file into other translation tools.
If you want to use this tool again, you can open your PACKAGE file in Sims 4 Studio and directly copy the String Tables Text output into JSON files. The ConvertJSONtoPACKAGE.py tool will still process it.
