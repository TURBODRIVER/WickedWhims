#!/bin/bash

echo "Welcome to the TURBODRIVER Translation Creator."
echo "This tool will convert your translated JSON files into a usable PACKAGE file mod."
echo "To use this tool you need to install Python and place translated JSON file into the folder you're running this tool from."
echo "If Python is installed and JSON files are present, input the language code you want to create the PACKAGE file for."
echo.

if ! command -v python3 &> /dev/null
then
    echo "Error - Python is not installed on your system."
    echo "Please install Python from https://www.python.org/ to proceed."
    exit 1
else
    echo "Python installation found. Good."
fi

jsonFileCount=$(ls *.json 2> /dev/null | wc -l)
if [ "$jsonFileCount" -eq 0 ]; then
    echo ""
    echo "Error - No JSON files were found in the folder you're running this tool from."
    echo "Please place all of the JSON files you translated into the folder you're running this tool from."
    exit 1
else
    echo "JSON files found. Good."
fi

echo ""

echo "Language Codes:"
echo "  ENG - English (English)"
echo "  CHS - Chinese Simplified (简体中文)"
echo "  CHT - Chinese Traditional (繁體中文)"
echo "  CZE - Czech (Čeština)"
echo "  DAN - Danish (Dansk)"
echo "  DUT - Dutch (Nederlands)"
echo "  FIN - Finnish (Suomi)"
echo "  FRE - French (Français)"
echo "  GER - German (Deutsch)"
echo "  ITA - Italian (Italiano)"
echo "  JPN - Japanese (日本語)"
echo "  KOR - Korean (한국어)"
echo "  NOR - Norwegian (Norsk)"
echo "  POL - Polish (Polski)"
echo "  POR - Portuguese (Português)"
echo "  RUS - Russian (Русский)"
echo "  SPA - Spanish (Español)"
echo "  SWE - Swedish (Svenska)"
echo ""

while true; do
    read -p "Please enter 3-characters long language code: " langInput
    if [[ ${#langInput} -eq 3 ]]; then
        break
    else
        echo "The language code has to be 3-characters long."
    fi
done

echo "Converting JSON files into PACKAGE file..."
python3 ConvertJSONtoPACKAGE.py "$langInput"
echo "PACKAGE file with translation has been created."
exit 1
