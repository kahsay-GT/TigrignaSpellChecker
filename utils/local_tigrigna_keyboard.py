import tkinter as tk
from tkinter import scrolledtext, Button, Frame, Label
import re
import os

class TigrignaKeyboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Tigrigna Keyboard and Spell Checker")
        self.root.geometry("800x600")
        
        # Load dictionary
        self.dictionary = self.load_dictionary()
        print(f"Loaded {len(self.dictionary)} words from dictionary")
        
        # Create main frames
        self.create_frames()
        
        # Create text input area
        self.create_text_area()
        
        # Create keyboard layout
        self.create_keyboard()
        
        # Create variant buttons area (initially empty)
        self.create_variant_area()
        
        # Create spell check button
        self.create_spell_check_button()
        
        # Current base character (for variants)
        self.current_base = None
        
    def load_dictionary(self, file_path='tigrigna_dictionary.txt'):
        """Load the Tigrigna dictionary"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                dictionary = {line.strip() for line in file if line.strip()}
            return dictionary
        except FileNotFoundError:
            print(f"Error: Dictionary file '{file_path}' not found.")
            return set()
        except Exception as e:
            print(f"Error loading dictionary: {e}")
            return set()
    
    def create_frames(self):
        # Top frame for text area
        self.top_frame = Frame(self.root, bg="#f0f0f0")
        self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        # Middle frame for variants
        self.variant_frame = Frame(self.root, bg="#000000")
        self.variant_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        # Keyboard frame
        self.keyboard_frame = Frame(self.root, bg="#000000")
        self.keyboard_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Bottom frame for spell check button and results
        self.bottom_frame = Frame(self.root, bg="#f0f0f0")
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        # Results frame
        self.results_frame = Frame(self.root, bg="white")
        self.results_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_text_area(self):
        # Create label
        Label(self.top_frame, text="Type Tigrigna Text:", bg="#f0f0f0").pack(anchor=tk.W)
        
        # Create text area
        self.text_area = scrolledtext.ScrolledText(self.top_frame, wrap=tk.WORD, width=60, height=5)
        self.text_area.pack(fill=tk.X, padx=5, pady=5)
    
    def create_keyboard(self):
        # Define keyboard layout
        # First row (numbers)
        row1 = ['፩', '፪', '፫', '፬', '፭', '፮', '፯', '፰', '፱', '፲']
        
        # Second row (Tigrigna characters)
        row2 = ['ሀ', 'ሐ', 'ሠ', 'ረ', 'ሰ', 'ሸ', 'ቀ', 'ቐ', 'በ', 'ቨ']
        
        # Third row
        row3 = ['ተ', 'ቸ', 'ኀ', 'ነ', 'ኘ', 'አ', 'ከ', 'ኸ', 'ወ', 'ዐ']
        
        # Fourth row
        row4 = ['ዘ', 'ژ', 'የ', 'ደ', 'ጀ', 'ገ', 'ጠ', 'ጨ', 'ጰ', 'ጸ']
        
        # Fifth row
        row5 = ['ፀ', 'ፈ', 'ፐ', 'ቦ', 'ቱ', 'ሙ', 'ሉ', 'ኢ', 'ኣ', 'ኡ']
        
        # Special row
        row6 = ['⌫', ' ', '፡', '።', '↵']
        
        # Create keyboard layout
        keyboard_layout = [row1, row2, row3, row4, row5, row6]
        
        # Create buttons for each row
        for i, row in enumerate(keyboard_layout):
            row_frame = Frame(self.keyboard_frame, bg="#000000")
            row_frame.pack(pady=2)
            
            for char in row:
                if char == ' ':
                    # Space button (wider)
                    btn = Button(row_frame, text=char, width=20, height=2, 
                                 bg="#333333", fg="white", 
                                 command=lambda c=char: self.insert_character(c))
                else:
                    btn = Button(row_frame, text=char, width=4, height=2, 
                                 bg="#333333", fg="white", 
                                 command=lambda c=char: self.on_char_click(c))
                btn.pack(side=tk.LEFT, padx=2, pady=2)
    
    def create_variant_area(self):
        self.variant_buttons = []
        Label(self.variant_frame, text="Variants:", bg="#000000", fg="white").pack(side=tk.LEFT, padx=5)
    
    def create_spell_check_button(self):
        self.spell_check_btn = Button(self.bottom_frame, text="Check Spelling", 
                                     bg="#4CAF50", fg="white", height=2,
                                     command=self.check_spelling)
        self.spell_check_btn.pack(pady=10)
        
        self.results_text = scrolledtext.ScrolledText(self.results_frame, wrap=tk.WORD, width=60, height=10)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def on_char_click(self, char):
        """Handle character button click"""
        if char == '⌫':
            # Backspace functionality
            current_text = self.text_area.get("1.0", tk.END)
            if len(current_text) > 1:  # > 1 because of the newline at the end
                self.text_area.delete("end-2c", tk.END)
        elif char == '↵':
            # Enter key
            self.insert_character('\n')
        else:
            # Regular character
            self.insert_character(char)
            # Show variants if it's a Tigrigna character
            self.show_variants(char)
    
    def insert_character(self, char):
        """Insert character at cursor position"""
        self.text_area.insert(tk.INSERT, char)
        self.text_area.focus()
    
    def show_variants(self, base_char):
        """Show vowel variants for a Tigrigna base character"""
        # Clear previous variant buttons
        for btn in self.variant_buttons:
            btn.destroy()
        self.variant_buttons = []
        
        # Only show variants for Tigrigna characters
        if base_char in ['⌫', ' ', '፡', '።', '↵'] or not self.is_tigrigna_char(base_char):
            return
        
        # Generate variants
        variants = self.generate_variants(base_char)
        
        # Create buttons for variants
        for variant in variants[:7]:  # Show up to 7 variants
            btn = Button(self.variant_frame, text=variant, width=4, height=2,
                         bg="#4CAF50", fg="white",
                         command=lambda v=variant: self.insert_character(v))
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            self.variant_buttons.append(btn)
    
    def is_tigrigna_char(self, char):
        """Check if a character is a Tigrigna character"""
        if not char or len(char) != 1:
            return False
        
        code = ord(char)
        return (0x1200 <= code <= 0x137F) or (0x1380 <= code <= 0x139F) or (0x2D80 <= code <= 0x2DDF)
    
    def generate_variants(self, base_char):
        """Generate vowel variants for a Tigrigna character"""
        if not self.is_tigrigna_char(base_char):
            return [base_char]
        
        try:
            base_code = ord(base_char)
            variants = []
            for i in range(7):  # Try to generate 7 vowel forms
                try:
                    variant_code = base_code + i
                    if 0xD800 <= variant_code <= 0xDFFF or variant_code > 0x10FFFF:
                        # Skip invalid Unicode code points
                        continue
                    variant = chr(variant_code)
                    variants.append(variant)
                except:
                    pass
            
            return variants if variants else [base_char]
        except:
            return [base_char]
    
    def check_spelling(self):
        """Check spelling of the text in the text area"""
        # Get text from the text area
        text = self.text_area.get("1.0", tk.END).strip()
        
        if not text:
            self.results_text.delete("1.0", tk.END)
            self.results_text.insert(tk.END, "Please enter some text to check.")
            return
        
        # Tokenize text
        words = re.findall(r'[\u1200-\u137F\u1380-\u139F\u2D80-\u2DDF]+', text)
        words = [word for word in words if word.strip()]
        
        if not words:
            self.results_text.delete("1.0", tk.END)
            self.results_text.insert(tk.END, "No Tigrigna words found in the text.")
            return
        
        # Check each word
        results = []
        for word in words:
            is_correct = word in self.dictionary
            suggestions = [] if is_correct else self.get_suggestions(word)
            
            results.append({
                'word': word,
                'is_correct': is_correct,
                'suggestions': suggestions
            })
        
        # Display results
        self.display_results(results)
    
    def get_suggestions(self, word, max_distance=2, max_suggestions=5):
        """Get spelling suggestions for a word"""
        suggestions = []
        
        for dict_word in self.dictionary:
            distance = self.levenshtein_distance(word, dict_word)
            if distance <= max_distance:
                suggestions.append((dict_word, distance))
        
        suggestions.sort(key=lambda x: x[1])
        return [word for word, _ in suggestions[:max_suggestions]]
    
    def levenshtein_distance(self, s1, s2):
        """Calculate Levenshtein distance between two strings"""
        if len(s1) < len(s2):
            return self.levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def display_results(self, results):
        """Display spell check results"""
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert(tk.END, "Spell Check Results:\n\n")
        
        self.results_text.tag_configure("correct", foreground="green")
        self.results_text.tag_configure("incorrect", foreground="red", underline=1)
        self.results_text.tag_configure("heading", font=("Arial", 10, "bold"))
        
        for item in results:
            word = item['word']
            is_correct = item['is_correct']
            suggestions = item['suggestions']
            
            if is_correct:
                self.results_text.insert(tk.END, f"{word}: ", "heading")
                self.results_text.insert(tk.END, "Correct\n", "correct")
            else:
                self.results_text.insert(tk.END, f"{word}: ", "heading")
                self.results_text.insert(tk.END, "Incorrect\n", "incorrect")
                
                if suggestions:
                    self.results_text.insert(tk.END, "  Suggestions:\n")
                    for suggestion in suggestions:
                        self.results_text.insert(tk.END, f"    - {suggestion}\n")
                else:
                    self.results_text.insert(tk.END, "  No suggestions available.\n")
            
            self.results_text.insert(tk.END, "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = TigrignaKeyboard(root)
    root.mainloop()