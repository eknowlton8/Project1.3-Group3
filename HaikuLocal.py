import requests
import syllapy
import random
import re

# Constants
NEWS_API_KEY = "cb6c0f61bdfd428bb5bf12ac15a730c9"
NEWS_API_URL = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
EXCLUDED_PHRASES = [
    "The Washington Post", "CNN", "BBC.com", "TechCrunch", "POLITICO", "NJ.com",
    "The Associated Press", "CBS News", "MarketWatch", "NESN", "Dayton Daily News", "The Seattle Times"
]

# Prohibited ending words (incomplete thoughts)
PROHIBITED_ENDINGS = [
    "is", "are", "was", "were", "be", "being", "been", "of", "with", "at", "by", "from", "up", 
    "about", "into", "over", "after", "without", "under", "within", "through", "among", "their", "as"
]

# Fetch headlines from NewsAPI
def get_headlines():
    response = requests.get(NEWS_API_URL)
    if response.status_code == 200:
        data = response.json()
        headlines = [article["title"] for article in data["articles"] if article["title"]]
        print(f"Retrieved {len(headlines)} headlines.")
        return headlines
    else:
        print("Error fetching news:", response.status_code, response.text)
        return []

# Count syllables in a sentence
def count_syllables(sentence):
    words = sentence.split()
    syllable_count = sum(syllapy.count(word) for word in words)
    return syllable_count

# Updated in the clean_headline function
def clean_headline(headline):
    # Split headline into phrases
    phrases = re.split(r'[,:;–-]', headline)
    phrases = [phrase.strip() for phrase in phrases if phrase.strip()]

    # Filter out unwanted phrases
    phrases = [phrase for phrase in phrases if not any(exclude in phrase for exclude in EXCLUDED_PHRASES)]
    
    # Remove phrases with incomplete thoughts
    phrases = [
        phrase for phrase in phrases 
        if not phrase.split()[-1].lower() in PROHIBITED_ENDINGS
    ]

    # **NEW FILTER**: Exclude phrases with exactly two words
    phrases = [phrase for phrase in phrases if len(phrase.split()) > 2]
    
    # **NEW FILTER**: Exclude phrases ending with standalone nouns
    prohibited_nouns = {"nomination", "city", "state", "plan", "report", "deal"}
    phrases = [
        phrase for phrase in phrases 
        if phrase.split()[-1].lower() not in prohibited_nouns
    ]
    
    # Return the cleaned and filtered phrases
    return phrases

# Create a phrase bank for flexible haiku creation
def create_phrase_bank(headlines):
    phrase_bank = {5: [], 7: []}
    for headline in headlines:
        phrases = clean_headline(headline)
        for phrase in phrases:
            syllable_count = count_syllables(phrase)
            if syllable_count in phrase_bank:
                phrase_bank[syllable_count].append(phrase)
            elif syllable_count > 7:
                # Try breaking down long phrases
                words = phrase.split()
                for i in range(1, len(words)):
                    part1 = " ".join(words[:i])
                    part2 = " ".join(words[i:])
                    if count_syllables(part1) in phrase_bank:
                        phrase_bank[count_syllables(part1)].append(part1)
                    if count_syllables(part2) in phrase_bank:
                        phrase_bank[count_syllables(part2)].append(part2)
    return phrase_bank

# Assemble a coherent haiku
def create_coherent_haiku(phrase_bank):
    # Ensure enough phrases are available
    if phrase_bank[5] and phrase_bank[7] and len(phrase_bank[5]) > 1:
        # Try to form a meaningful narrative
        line1 = random.choice(phrase_bank[5])
        line2 = random.choice(phrase_bank[7])
        line3_candidates = [p for p in phrase_bank[5] if p != line1]

        # Check for logical flow and coherence
        for line3 in line3_candidates:
            haiku = [line1, line2, line3]
            haiku_text = " ".join(haiku).lower()
            # The change is here: using haiku instead of line in generator expression
            if (
                not any(line in haiku_text for line in EXCLUDED_PHRASES) and
                not any(haiku_text.endswith(word) for word in PROHIBITED_ENDINGS)  
            ):
                return haiku
    
    return None

# Main function
if __name__ == "__main__":
    headlines = get_headlines()
    if not headlines:
        print("No headlines retrieved.")
    else:
        phrase_bank = create_phrase_bank(headlines)
        haiku = create_coherent_haiku(phrase_bank)
        if haiku:
            print("\nGenerated Haiku:\n")
            print("\n".join(haiku))
        else:
            print("Couldn't create a coherent haiku this time.")
