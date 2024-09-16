import random
from collections import defaultdict

class CharNGramLanguageModel:
    
    def __init__(self, n, data):
        self.n = n
        self.data = data
        self.sequence_occurences = self.count_occurences()

    def count_occurences(self):
        

        sequences = defaultdict(int)
        total = len(self.data) - self.n

        for i in range(total):
            
            prev_word  = ''.join(self.data[i:i+self.n-1])
            next_char = self.data[i+self.n-1] if (i+self.n-1) < len(self.data) else "<eos>"
            sequences[(prev_word, next_char)] += 1

        total_sequences = sum(sequences.values())
        for keys in sequences:
            sequences[keys] = sequences[keys] / total_sequences  
       
        
        #print(sequences)

        return sequences

    def generate_character(self, prompt):

        last_n = prompt[-(self.n-1):]
#        print(last_n)
        
        next_n_probs = [(key, prob) for key, prob in self.sequence_occurences.items() if key[0] == last_n]
        
        if next_n_probs:
            return random.choices(
                [key for key, _ in next_n_probs],
                [weight for _, weight in next_n_probs]
            )[0]
        
       
        # Fallback to unigram
        unigram_counts = defaultdict(int)
        for (prev_word, next_char), prob  in self.sequence_occurences.items():
            unigram_counts[next_char] += prob

        total = sum(unigram_counts.values())

        for char in unigram_counts:
            unigram_counts[char] /= total
        
        chars = list(unigram_counts.keys())
        probs = list(unigram_counts.values())

        return (prompt[-1], random.choice(chars, weights=probs)[0])
        

    def generate(self, prompt):
        
        generated = prompt 
        
        while True: 

            new_char = self.generate_character(generated)
            
            if(new_char[1] == "<eos>" or len(generated) >= 100 ):
                break

            generated += new_char[1]
            
        return generated

def main():
    user_prompt = input("Enter prompt: ")
    num_gram =  int(input("Enter the number of previous characters to check:"))

    with open("datasets/input.txt", "r") as file:
        data = file.read()

    data = data.replace('\n',' ') + '<eos>'
    model = CharNGramLanguageModel(num_gram, list(data) )
    print(model.generate(user_prompt))

if __name__ == '__main__':
    main()
