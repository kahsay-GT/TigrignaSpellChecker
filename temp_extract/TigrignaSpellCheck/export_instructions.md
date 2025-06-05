# Local Installation Instructions

## Files Needed
1. `tigrigna_dictionary.txt` - The dictionary file
2. `improved_tigrigna_keyboard.ipynb` - The Jupyter notebook with the keyboard
3. `tigrigna_spell_checker.ipynb` - The main spell checker notebook

## Installation Steps

### 1. Install Python
If you don't have Python installed:
- Download and install Python from [python.org](https://www.python.org/downloads/)
- Make sure to check "Add Python to PATH" during installation

### 2. Install Required Libraries
Open a command prompt or terminal and run:
```
pip install jupyter notebook ipywidgets
```

### 3. Download the Project Files
Download these files to the same folder on your computer:
- tigrigna_dictionary.txt
- improved_tigrigna_keyboard.ipynb
- tigrigna_spell_checker.ipynb

### 4. Start Jupyter Notebook
In the command prompt or terminal, navigate to the folder with your files:
```
cd path/to/your/folder
```

Then start Jupyter Notebook:
```
jupyter notebook
```

This will open Jupyter in your web browser.

### 5. Run the Notebooks
- Click on `improved_tigrigna_keyboard.ipynb` to open it
- Click the "Run" button to run each cell, or use the menu: Cell → Run All
- The keyboard will appear in the output of the last cell

## Using the Keyboard and Spell Checker
1. Type using the interactive keyboard by clicking on the Tigrigna characters
2. When you click on a character, its vowel variants will appear in green buttons
3. After entering your text, click the "Check Spelling" button
4. Misspelled words will be highlighted in red with suggestions