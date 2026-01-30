import re
import requests
from collections import Counter

# Common words to exclude (articles, pronouns, prepositions, conjunctions, etc.)
STOP_WORDS = {
    # Articles
    'a', 'an', 'the',
    # Pronouns
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves',
    'you', 'your', 'yours', 'yourself', 'yourselves',
    'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself',
    'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
    'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those',
    # Common prepositions
    'in', 'on', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
    'into', 'through', 'during', 'before', 'after', 'above', 'below',
    'to', 'from', 'up', 'down', 'out', 'off', 'over', 'under', 'upon',
    'until', 'till', 'along',
    # Conjunctions
    'and', 'but', 'or', 'nor', 'so', 'yet', 'both', 'either', 'neither', 'though',
    # Common verbs (auxiliary/modal)
    'is', 'am', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
    'will', 'would', 'shall', 'should', 'may', 'might', 'must', 'can', 'could',
    'cannot', 
    # Other common words
    'of', 'as', 'if', 'then', 'than', 'because', 'while', 'although',
    'where', 'when', 'how', 'all', 'each', 'every', 'any', 'some',
    'no', 'not', 'only', 'own', 'same', 'just', 'now', 'here', 'there',
    'very', 'too', 'also', 'well', 'back', 'even', 'still', 'way', 'yes',
    'day', 'one', 'two', 'three', 'other', 'like', 'much', 'most', 'many',
    'more', 'less', 'man', 'men', 'great', 'such', 'little', 'why', 'per',
    # relative pronouns
    'which', 'whom',
    # Contractions (partial)
    's', 't', 'd', 'll', 've', 're', 'm',
}

# Sample list of Project Gutenberg book IDs (plain text URLs)
GUTENBERG_BOOKS = [
    84,      # Frankenstein
    1342,    # Pride and Prejudice
    11,      # Alice's Adventures in Wonderland
    1661,    # Sherlock Holmes
    2701,    # Moby Dick
    36,      # The War of the Worlds
    98,      # A Tale of Two Cities
    2554,    # Crime and Punishment
    28553,   # How it Works by Archibald Williams
    71693,   # The Cambridge natural history,
    1228,    # On the Origin of Species By Means of Natural Selection
    30107,   # Principles of Political Economy
    3300,    # An Inquiry into the Nature and Causes of the Wealth of Nations
    41360,   # The Elementary Forms of the Religious Life by Émile Durkheim
    2529,    # The Analysis of Mind
    4763,    # The Game of Logic
    50100,   # How to Do Chemical Tricks
]


def get_gutenberg_url(book_id):
    """Generate the plain text URL for a Gutenberg book."""
    return f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"


def download_book(book_id):
    """Download a book from Project Gutenberg."""
    url = get_gutenberg_url(book_id)
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        # Try alternative URL format
        alt_url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
        try:
            response = requests.get(alt_url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Failed to download book {book_id}: {e}")
            return None


def strip_gutenberg_header_footer(text):
    """Remove Project Gutenberg header and footer."""
    # Find start of actual content
    start_markers = [
        "*** START OF THIS PROJECT GUTENBERG",
        "*** START OF THE PROJECT GUTENBERG",
        "*END*THE SMALL PRINT",
    ]
    end_markers = [
        "*** END OF THIS PROJECT GUTENBERG",
        "*** END OF THE PROJECT GUTENBERG",
        "End of the Project Gutenberg",
        "End of Project Gutenberg",
    ]
    
    start_idx = 0
    for marker in start_markers:
        idx = text.find(marker)
        if idx != -1:
            start_idx = text.find('\n', idx) + 1
            break
    
    end_idx = len(text)
    for marker in end_markers:
        idx = text.find(marker)
        if idx != -1:
            end_idx = idx
            break
    
    return text[start_idx:end_idx]


def extract_words(text):
    """Extract and clean words from text."""
    # Convert to lowercase
    text = text.lower()
    
    # Extract words (only alphabetic characters)
    words = re.findall(r'\b[a-z]+\b', text)
    
    # Filter out very short words and stop words
    words = [w for w in words if len(w) > 2 and w not in STOP_WORDS]
    
    return words


def load_common_names():
    """
    Load a set of common names to filter out.
    You can expand this list or load from a file.
    """
    # Common English first names (sample - expand as needed)
    names = {
        # Male names
        'john', 'james', 'william', 'henry', 'george', 'charles', 'thomas',
        'edward', 'robert', 'richard', 'joseph', 'david', 'michael', 'peter',
        'paul', 'mark', 'steven', 'andrew', 'daniel', 'matthew', 'christopher',
        'frank', 'harry', 'jack', 'tom', 'bill', 'bob', 'jim', 'joe', 'sam',
        'ben', 'fred', 'walter', 'arthur', 'albert', 'alfred', 'ernest', 'darcy',
        # Female names
        'mary', 'elizabeth', 'margaret', 'anne', 'jane', 'sarah', 'alice',
        'emma', 'catherine', 'charlotte', 'emily', 'helen', 'lucy', 'susan',
        'nancy', 'betty', 'dorothy', 'ruth', 'rose', 'grace', 'clara', 'ellen',
        # Common surnames
        'smith', 'jones', 'brown', 'wilson', 'taylor', 'johnson', 'white',
        'martin', 'anderson', 'thompson', 'garcia', 'martinez', 'robinson',
        'clark', 'lewis', 'lee', 'walker', 'hall', 'allen', 'young', 'king',
        # Titles often attached to names
        'mr', 'mrs', 'miss', 'ms', 'sir', 'lord', 'lady', 'dr', 'professor',
    }
    return names


def build_word_frequency(book_ids=None, min_word_length=3, exclude_names=True):
    """
    Build a word frequency dictionary from multiple Gutenberg books.
    
    Args:
        book_ids: List of Gutenberg book IDs to process
        min_word_length: Minimum word length to include
        exclude_names: Whether to filter out common names
    
    Returns:
        Counter object with word frequencies
    """
    if book_ids is None:
        book_ids = GUTENBERG_BOOKS
    
    word_counter = Counter()
    names = load_common_names() if exclude_names else set()
    
    for book_id in book_ids:
        print(f"Processing book {book_id}...")
        text = download_book(book_id)
        
        if text is None:
            continue
        
        # Strip Gutenberg header/footer
        text = strip_gutenberg_header_footer(text)
        
        # Extract words
        words = extract_words(text)
        
        # Filter out names if requested
        if exclude_names:
            words = [w for w in words if w not in names]
        
        # Filter by minimum length
        words = [w for w in words if len(w) >= min_word_length]
        
        # Update counter
        word_counter.update(words)
        print(f"  Added {len(words)} words from book {book_id}")
    
    return word_counter


def save_frequency_dict(counter, filename="word_frequencies.txt", top_n=None):
    """Save the frequency dictionary to a file."""
    words = counter.most_common(top_n)
    
    with open(filename, 'w', encoding='utf-8') as f:
        for word, count in words:
            f.write(f"{word}\t{count}\n")
    
    print(f"Saved {len(words)} words to {filename}")


def main():
    # Build frequency dictionary
    print("Building word frequency dictionary from Project Gutenberg...\n")
    
    word_freq = build_word_frequency(
        book_ids=GUTENBERG_BOOKS,
        min_word_length=3,
        exclude_names=True
    )
    
    # Display results
    print(f"\nTotal unique words: {len(word_freq)}")
    print(f"Total word occurrences: {sum(word_freq.values())}")
    
    print("\nTop 50 most common words:")
    print("-" * 30)
    for word, count in word_freq.most_common(50):
        print(f"{word:20} {count:>8}")
    
    # Save to file
    save_frequency_dict(word_freq, "word_frequencies.txt")
    
    # Also save just the word list (top 10000)
    save_frequency_dict(word_freq, "top_10000_words.txt", top_n=10000)
    
    return word_freq


if __name__ == "__main__":
    word_freq = main()