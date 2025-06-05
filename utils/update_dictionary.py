import re

def load_dictionary(file_path='tigrigna_dictionary.txt'):
    """
    Loads the Tigrigna dictionary from the specified file path.
    
    Args:
        file_path (str): Path to the dictionary file
        
    Returns:
        set: A set containing Tigrigna words
    """
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

def tokenize_text(text):
    """
    Tokenizes Tigrigna text into words.
    
    Args:
        text (str): The input Tigrigna text
        
    Returns:
        list: A list of words
    """
    # Split text by non-Tigrigna characters and spaces
    # This regex pattern handles Tigrigna characters
    words = re.findall(r'[\u1200-\u137F\u1380-\u139F\u2D80-\u2DDF]+', text)
    
    # Remove empty strings
    words = [word.strip() for word in words if word.strip()]
    
    return words

def process_corpus(corpus_file, dictionary_file):
    """
    Process a corpus file and add new words to the dictionary
    
    Args:
        corpus_file (str): Path to the corpus file
        dictionary_file (str): Path to the dictionary file
        
    Returns:
        tuple: (total_words, new_words_added)
    """
    # Load existing dictionary
    existing_dictionary = load_dictionary(dictionary_file)
    print(f"Loaded {len(existing_dictionary)} words from existing dictionary")
    
    # New words to add
    new_words = set()
    total_words = 0
    
    # Process corpus file
    try:
        with open(corpus_file, 'r', encoding='utf-8') as file:
            content = file.read()
            
            # Tokenize the content
            tokens = tokenize_text(content)
            total_words = len(tokens)
            
            # Find new words
            for word in tokens:
                if word not in existing_dictionary and len(word) > 1:  # Ignore single characters
                    new_words.add(word)
    
        # Add new words to dictionary file
        if new_words:
            with open(dictionary_file, 'a', encoding='utf-8') as file:
                for word in sorted(new_words):
                    file.write(f"{word}\n")
            
            print(f"Added {len(new_words)} new words to the dictionary")
        else:
            print("No new words to add to the dictionary")
            
        return total_words, len(new_words)
            
    except FileNotFoundError:
        print(f"Error: Corpus file '{corpus_file}' not found.")
        return 0, 0
    except Exception as e:
        print(f"Error processing corpus: {e}")
        return 0, 0

def main():
    corpus_file = "tigrigna_corpus.txt"
    dictionary_file = "tigrigna_dictionary.txt"
    
    print(f"Processing corpus file: {corpus_file}")
    total_words, new_words = process_corpus(corpus_file, dictionary_file)
    
    print(f"\nSummary:")
    print(f"Total words processed: {total_words}")
    print(f"New words added: {new_words}")
    
    # Output the updated dictionary size
    updated_dict = load_dictionary(dictionary_file)
    print(f"Updated dictionary now contains {len(updated_dict)} words")

if __name__ == "__main__":
    main()