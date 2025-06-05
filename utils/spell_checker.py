"""
Tigrigna Spell Checker Utility Functions
This module contains the core functionality for Tigrigna spell checking.
"""

import re
import os
from collections import Counter
from typing import List, Dict, Set, Tuple, Optional

class TigrignaSpellChecker:
    """
    A spell checker for the Tigrigna language that provides error detection
    and correction suggestions based on a dictionary of Tigrigna words.
    """
    
    def __init__(self, dictionary_path: str = None):
        """
        Initialize the spell checker with a dictionary of Tigrigna words.
        
        Args:
            dictionary_path: Path to a file containing Tigrigna words, one per line
        """
        self.dictionary_path = dictionary_path or os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                                            'data', 'tigrigna_words.txt')
        self.word_dict: Set[str] = set()
        self.load_dictionary()
        
    def load_dictionary(self) -> None:
        """Load the Tigrigna dictionary from file."""
        try:
            with open(self.dictionary_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                self.word_dict = {line.strip() for line in lines if line.strip()}
            print(f"Loaded {len(self.word_dict)} Tigrigna words from dictionary.")
        except FileNotFoundError:
            print(f"Dictionary file not found at: {self.dictionary_path}")
            self.word_dict = set()
        except Exception as e:
            print(f"Error loading dictionary: {str(e)}")
            self.word_dict = set()

    def add_to_dictionary(self, word: str) -> None:
        """
        Add a new word to the dictionary.
        
        Args:
            word: The word to add to the dictionary
        """
        word = word.strip()
        if word:
            self.word_dict.add(word)
            # Optionally save to file
            try:
                with open(self.dictionary_path, 'a', encoding='utf-8') as f:
                    f.write(f"\n{word}")
            except Exception as e:
                print(f"Could not save word to dictionary file: {str(e)}")

    def tokenize_text(self, text: str) -> List[str]:
        """
        Split Tigrigna text into individual words.
        
        Args:
            text: The Tigrigna text to tokenize
            
        Returns:
            List of individual words
        """
        # This is a simple tokenizer that splits on whitespace and punctuation
        # For a more sophisticated approach, a Tigrigna-specific tokenizer could be developed
        cleaned_text = re.sub(r'[፡።፣፤፥፧፦፨፠፟]', ' ', text)  # Replace Ethiopic punctuation with space
        words = re.split(r'\s+', cleaned_text)
        return [word for word in words if word]  # Remove empty strings

    def check_word(self, word: str) -> bool:
        """
        Check if a word is correctly spelled.
        
        Args:
            word: Word to check
            
        Returns:
            True if the word is in the dictionary, False otherwise
        """
        return word in self.word_dict

    def edit_distance(self, s1: str, s2: str) -> int:
        """
        Calculate the Levenshtein edit distance between two words.
        
        Args:
            s1: First word
            s2: Second word
            
        Returns:
            The edit distance as an integer
        """
        if len(s1) < len(s2):
            return self.edit_distance(s2, s1)
            
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

    def generate_suggestions(self, word: str, max_distance: int = 2, max_suggestions: int = 5) -> List[str]:
        """
        Generate spelling correction suggestions for a word.
        
        Args:
            word: The misspelled word
            max_distance: Maximum edit distance for suggestions
            max_suggestions: Maximum number of suggestions to return
            
        Returns:
            List of suggested corrections
        """
        if not word or self.check_word(word):
            return []
            
        candidates = []
        for dict_word in self.word_dict:
            distance = self.edit_distance(word, dict_word)
            if distance <= max_distance:
                candidates.append((dict_word, distance))
                
        # Sort by edit distance (closest matches first)
        candidates.sort(key=lambda x: x[1])
        return [candidate[0] for candidate in candidates[:max_suggestions]]

    def check_text(self, text: str) -> Dict[str, List[str]]:
        """
        Check a text for spelling errors and provide suggestions.
        
        Args:
            text: The Tigrigna text to check
            
        Returns:
            Dictionary mapping misspelled words to suggestion lists
        """
        words = self.tokenize_text(text)
        result = {}
        
        for word in words:
            if word and not self.check_word(word):
                suggestions = self.generate_suggestions(word)
                result[word] = suggestions
                
        return result

    def get_statistics(self, text: str) -> Dict[str, int]:
        """
        Get statistics about the text.
        
        Args:
            text: The input text
            
        Returns:
            Dictionary with statistics
        """
        words = self.tokenize_text(text)
        misspelled = [word for word in words if word and not self.check_word(word)]
        
        return {
            'total_words': len(words),
            'unique_words': len(set(words)),
            'misspelled_words': len(misspelled),
            'unique_misspelled': len(set(misspelled))
        }
