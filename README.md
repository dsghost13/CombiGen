# CombiGen

### Conda Environment Setup
Run the following commands in the terminal:
```bash
    conda create -n CombiGen python=3.11
    conda activate CombiGen
    pip install pyqt6==6.10.1 pyqt6-qscintilla==2.14.1 pyqtdarktheme==0.1.7
    pip install pandas==2.3.3 rdkit==2025.9.3
```
The listed package versions are the last confirmed working versions. <br>
Use other versions at your own discretion. 

### Usage Specifications
#### CombiGen
Text entries may contain quotations (e.g. "CCC(O)CN") or not (e.g. CCC(O)CN). <br>
Text entries must be comma-separated when applicable (e.g. CC(C)\[NH2:10], CC(C)(C)\[NH2:10], \[NH2:10]C1CCCCC1). <br>
Whitespace, newline characters, and tab characters are automatically filtered out. <br>
Cores and arrow pushing cannot be left blank. <
All other fields may be left blank. <br>
Toggle pareto front cells by clicking or dragging your mouse. <br>
NOTE: Executing with unconventional values may result in undefined behavior. <br>
#### Script Editor
An example script is provided in the code editor. <br>
You may paste in your own pre-existing script. <br>
Press "Load Configs" to autofill CombiGen fields by extracting values from the code editor. <br>
NOTE: Scripts that do not follow the generated format may result in undefined behavior. <br>
#### Output SMIRKS
Output proportion should fall between 0 and 1 inclusive. <br>
Generated SMIRKS are saved in a CSV file. <br>
SMIRKS strings can be depicted at the following website:
```
https://cdb.ics.uci.edu/cgibin/Smi2DepictWeb.py
```

### Google Colab Template Script
The following link is provided for running generated scripts and saving results independent of this GUI: 
```
https://colab.research.google.com/drive/1aM069_xXhUgoOAZ5gK61LJIyEz0_YTkj?usp=sharing
```