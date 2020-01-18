# Hairpin generator
Script for generating structures of two-tailed primers from imported sequences.

Program will connect to https://eu.idtdna.com/calc/analyzer and click hairpie button for each sequence. All the images will be written to an output HTML file that will be displayed in the browser.

# Installation
Python3 + Selenium (Chrome) application are prerequisited.
1. Download https://sites.google.com/a/chromium.org/chromedriver/downloads
2. `pip3 install git+https://github.com/raradek/oligo_analyzer_hairpin.git`
3. Put chromedriver.exe in the same path as OligoAnalyzer.py
4. Optionally put your user name and pw to `user.ini`
5. Execute the `OligoAnalyzer.py`
6. You will be asked for data. Copy there ex. these columns from the Excel:

```
Name  Sequence
test1 AGAGAGAGAGCCC
test2 AGAGAGAGAGCCCTATAGAGAGAGAGAGCCCTTTTT
test3 AGAGAGAGAGCCCTAGAGAGAGAGAGAG
test4 AGAGAGAGAGAGCCCCCCCTTTT
test5 AGAGAGAGAGAGAGCCCCCC
test6 CCCTTTTTTAAGAGAGAG
test7 AGAGAGAGAGCCCCTAGAGAGAGAGAGAGGGGGGG
test8 GGGAGAGAGAGAGAGAGAGAGAGAG
test9 TAGAGAGAGAGAGAGAGAGAGAG
test10  ACCCCTAGAGAGAGAGAGAGAGAG
```
(note that each line is in format: `name TAB sequence`)
