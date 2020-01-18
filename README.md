# Installation
1. Download https://sites.google.com/a/chromium.org/chromedriver/downloads
2. Put chromedriver.exe in the same path as OligoAnalyzer.py
3. Optionally put your user name and pw to `user.ini`
4. Execute the `OligoAnalyzer.py`
5. You will be asked for data. Copy there ex. these columns from the Excel:

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

6. Program will connect to https://eu.idtdna.com/calc/analyzer and click hairpie button for each sequence. All the images will be written to an output HTML file that will be displayed in the browser.
