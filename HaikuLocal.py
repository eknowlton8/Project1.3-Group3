import requests
import syllapy
import random

# Constants
NEWS_API_KEY = "cb6c0f61bdfd428bb5bf12ac15a730c9"
NEWS_API_URL = f"https://newsapi.org/v2/top-headlines?country=us&apiKey=cb6c0f61bdfd428bb5bf12ac15a730c9"

# Fetch headlines from NewsAPI
def get_headlines():
    response = requests.get(NEWS_API_URL)
    if response.status_code == 200:
        data = response.json()
        return [article["title"] for article in data["articles"] if article["title"]]
    else:
        print("Error fetching news:", response.status_code, response.text)
        return []

# Count syllables in a sentence
def count_syllables(sentence):
    words = sentence.split()
    return sum(syllapy.count(word) for word in words)

# Assemble haiku lines flexibly
def assemble_line(headlines, target_syllables):
    line = []
    current_syllables = 0

    while headlines and current_syllables < target_syllables:
        headline = headlines.pop(0)
        syllables = count_syllables(headline)

        if current_syllables + syllables <= target_syllables:
            line.append(headline)
            current_syllables += syllables

        elif syllables > target_syllables:
            # If a single headline exceeds the limit, split it
            words = headline.split()
            partial_line = []
            for word in words:
                word_syllables = syllapy.count(word)
                if current_syllables + word_syllables > target_syllables:
                    break
                partial_line.append(word)
                current_syllables += word_syllables
            line.append(" ".join(partial_line))
            break

    return " ".join(line) if current_syllables == target_syllables else None

# Create a haiku from multiple headlines
def create_haiku(headlines):
    random.shuffle(headlines)
    syllable_targets = [5, 7, 5]
    haiku = [assemble_line(headlines, target) for target in syllable_targets]

    return haiku if all(haiku) else None

# Main function
if __name__ == "__main__":
    headlines = get_headlines()
    if not headlines:
        print("No headlines retrieved.")
    else:
        haiku = create_haiku(headlines)
        if haiku:
            print("\nGenerated Haiku:\n")
            print("\n".join(haiku))
        else:
            print("Couldn't create a haiku, but at least some headlines were available.")
