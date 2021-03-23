import pandas as pd
import json
import re
import os
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# import files
folder = os.getcwd() + '/parsed doc/'
chat_folders = [chat_folder for chat_folder in os.listdir(folder) if not chat_folder.startswith('.')]

paths = []
for i in range(len(chat_folders)):
    pattern = str(folder) + chat_folders[i]
    paths.append(pattern)
    
sesi_paths = []
for i in range(len(paths)):
    for roots, dirs, files in os.walk(paths[i]):
        if "checkpoints" not in roots:
            for file in files:
                sesi_paths.append(roots + '/' + file)
      
chats = [pd.read_csv(sesi, sep='|', names = ['sender', 'messages', 'sentiment']) for sesi in sesi_paths]
messages = [chats[i].messages.values.tolist() for i in range(len(sesi_paths))]

def tokenize(messages):
    """ This function will turns all sentences into token or word.
        Each messages will saved in a list.
    """
    token_per_sesi = []
    for sesi in messages:
        token_per_chat = []
        for chat in sesi:
            token_per_chat.append(re.split('\s+',chat))
        token_per_sesi.append(token_per_chat)
    return token_per_sesi
 
def casefolding(token):
    """ This function will turn all the letters into lowercase. """
    token_per_sesi = []
    for sesi in token:
        token_per_chat = []
        for chat in sesi:
            token = []
            for word in chat:
                token.append(word.lower())
            token_per_chat.append(token)
        token_per_sesi.append(token_per_chat)
    return token_per_sesi

def cleaning(token):
    """ This function will remove unnecessaries values in the sentence i.e links, emails, and punctuations
    """
    link = r'(https?:\/\/[^\s]+)|(www\.[^\s]+)|(meet\.google\.[^\s]+)|(bit\.ly[^\s]+)'
    email = r'([a-zA-Z0-9\.\_\-]+@+[a-zA-Z0-9.]+)'
    punct = r'[^a-zA-Z0-9\[\]]'
    
    token_per_sesi = []
    for sesi in token:
        token_per_chat = []
        for chat in sesi:
            token = []
            for word in chat:
                if '<doc>' in word:
                    token.append(word)
                else:
                    temp = re.sub(link, '', word)
                    # remove email
                    temp = re.sub(email, '', temp)
                    # remove punctuation
                    temp = re.sub(punct, ' ', temp)
            #         temp = re.sub(r'\-', ' ', temp)
                    # remove numbers
                    temp = re.sub(r'\b[0-9]+\b\s*', '', temp)
                token.append(temp)
            token_per_chat.append(token)
        token_per_sesi.append(token_per_chat)
    return token_per_sesi
  
def normalize(token):
    """ This function will normalize the tokens,
        it will turn the slang words or typos to its normal values.
        NOTE: you could add the values into json files.
    """
    with open('slang_words.json', 'r') as f:
        dict = json.load(f)
        
    token_per_sesi = []
    for sesi in token:
        token_per_chat = []
        for chat in sesi:
            token = []
            for word in chat:
                slang_dict = {v:k for v, k in dict.items()}
                normal = slang_dict.get(word, word)
                token.append(normal)
            token_per_chat.append(token)
        token_per_sesi.append(token_per_chat)
    return token_per_sesi
  
def filtering(token):
    """ Filtering: removing stopwords from tokens.
        In this project, we will use tala stopwords list.
    """
    with open('stopword_list_tala.txt', 'r') as tala:
        stoplist = tala.read()
        
    token_per_sesi = []
    for sesi in token:
        token_per_chat = []
        for chat in sesi:
            token = []
            for word in chat:
                if not word in stoplist:
                    token.append(word)
            token_per_chat.append(token)
        token_per_sesi.append(token_per_chat)
    return token_per_sesi
  
def stemming(token):
    """ Stemming: returns words to its original form.
        Since non-alphanumeric will be discarded by using StemmerFactory(),
        This function will do stemming if the token values neither [dosen] nor [mhs].
    """
    stemmer = StemmerFactory().create_stemmer()
    
    token_per_sesi = []
    for sesi in token:
        token_per_chat = []
        for chat in sesi:
            token = []
            for word in chat:
                if word.startswith('['): #for [mhs] and [dosen]
                    token.append(word)
            else:
                token_per_chat.append(stemmer.stem(word))
        token_per_sesi.append(token_per_chat)
    return token_per_sesi
  
def main():
    token = tokenize(messages)
    token_lower = casefolding(token)
    token_clean = cleaning(token_lower)
    token_normal = normalize(token_clean)
    token_filtered = filtering(token_normal)
    token_stemmed = stemming(token_filtered)
  
main()
