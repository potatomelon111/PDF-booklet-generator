# PDF-booklet-generator
Turn A4 PDF's into A5 sized booklets

This script will first turn all the A4 pages to A5, position 2 pages side to side, and order them in such a way that once you've printed, all you have to do is fold it in half to have a correctly ordered booklet. 
This is intended to be used with double sided printing. If you don't have a printer with this functionality, see [PDF Splitter](https://github.com/potatomelon111/PDF_Splitter)

## Usage:
```
pip install pypdf
python booklet.py "C:/path/to/name.pdf"
```
This will generate the "name_booklet.pdf" file in the same directory. 
