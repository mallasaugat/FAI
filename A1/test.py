
import random
from collections import defaultdict, Counter

class CharNGramLanguageModel:
    def __init__(self, n, data):
        self.n = n
        self.n_gram_counts = defaultdict(Counter)
        self.unigram_counts = Counter()
        self._train(data)

    def _train(self, data):
        # Add end-of-sequence character at the end of each sequence
        data = data.replace('\n', ' ') + '<EOS>'
        for i in range(len(data) - self.n):
            n_gram = data[i:i+self.n]
            next_char = data[i+self.n]
            self.n_gram_counts[n_gram][next_char] += 1
            self.unigram_counts[next_char] += 1

        # Handle the last n-gram leading to <EOS>
        self.n_gram_counts[data[-self.n:]]['<EOS>'] += 1

        # Convert counts to probabilities
        self.probabilities = {}
        for n_gram, counter in self.n_gram_counts.items():
            total = sum(counter.values())
            self.probabilities[n_gram] = {char: count/total for char, count in counter.items()}

    def generate_character(self, prompt):
        n_gram = prompt[-self.n:]
        if n_gram in self.probabilities:
            chars = list(self.probabilities[n_gram].keys())
            probs = list(self.probabilities[n_gram].values())
            next_char = random.choices(chars, weights=probs, k=1)[0]
        elif prompt[-1] in self.unigram_counts:
            # Fallback to unigram probabilities based on the last character
            total = sum(self.unigram_counts.values())
            chars = list(self.unigram_counts.keys())
            probs = [self.unigram_counts[char]/total for char in chars]
            next_char = random.choices(chars, weights=probs, k=1)[0]
        else:
            # Completely random choice if no data is available
            next_char = random.choice(list(self.unigram_counts.keys()))
        return next_char if next_char != '<EOS>' else None

    def generate(self, prompt):
        generated = prompt
        while True:
            next_char = self.generate_character(generated)
            if next_char is None:
                break
            generated += next_char
        return generated

def main():
    # Sample training data (you can replace this with your own dataset)
    with open('datasets/input.txt', 'r', encoding='utf-8') as f:
        data = f.read()

    n = int(input("Enter the value of n: "))
    model = CharNGramLanguageModel(n, data)

    prompt = input("Enter a prompt: ")
    generated_text = model.generate(prompt)
    print("Generated text:")
    print(generated_text)

if __name__ == "__main__":
    main()
