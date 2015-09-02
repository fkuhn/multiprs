***NOTES ON FILES AND MODULES USED***
...

***TREETAGGER SCRIPT HIERARCHY FOR TAGGING MULTILIT-EXMARALDA FILES***

1. tierExtract.py <exmafolder> (processes a folder with multiple non-annotated exmaralda files)
2. multitaggercore.py (using taggerscript/tree-tagger-multi\_buero.sh)
3. corpusMethods.py is imported by multitaggercore.py



***HOW TO CREATE A TRAINING INPUT FILE FROM ANNOTATED MULTILIT EXMARALDA FILES***

1. createTrainInputFile.py <annotated-exma-docs> #extracts student verbal tiers 



