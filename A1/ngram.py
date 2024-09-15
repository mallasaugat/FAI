import numpy as np
import random


class CharNGramLanguageModel:
    
    def __init__(self, n, data, prompt):
        self.n = n + 1
        self.data = data
        self.prompt = prompt
        self.sequence_occurences = self.count_occurences()

    def count_occurences(self):
        
        sequences = {}
        total = len(self.data) / self.n

        for i in range(len(self.data)-self.n):
            
            prev_word  = ''.join(self.data[i:i+self.n-1])
            
            if (prev_word, self.data[i+self.n]) in sequences.keys():
                sequences[(prev_word, self.data[i+self.n])] += 1
            else:
                sequences[(prev_word, self.data[i+self.n])] = 1

            i += self.n + 1
        i -= self.n 
        prev_word = "".join(self.data[i:i+self.n])
        sequences[(prev_word, "<eos>")] = 1 

        for keys in sequences:
            sequences[keys] = ( sequences[keys] / total  ) * 100
       
        
        #print(sequences)

        return sequences

    def generate_character(self):

        last_n = self.prompt[len(self.prompt)-self.n+1:len(self.prompt)]
#        print(last_n)
        
        next_n_probs = []
        for keys in self.sequence_occurences:
            if keys[0] == last_n:
                next_n_probs.append([(keys), self.sequence_occurences[keys]])

        
       # print(next_n_probs)
        

        return (last_n, "<eos>") if len(next_n_probs) == 0 else random.choices(next_n_probs)[0]
        

    def generate(self):

        total_new_char = ""
        
        while True: 

            new_char = self.generate_character()
            total_new_char += new_char[0][1]  
            
            if(new_char[0][1] == "<eos>" or len(total_new_char) == 100 ):
                break

            self.prompt = self.prompt + new_char[0][1]
            
            

        return self.prompt

if __name__ == '__main__':
   
    user_prompt = input("Enter prompt: ")
    num_gram =  int(input("Enter the number of previous characters to check:"))

    file = open("datasets/input.txt", "r") 
    data = list(file.read())

    model = CharNGramLanguageModel(num_gram, data, user_prompt)
    print(model.generate())
