import pandas

#TODO 1. Create a dictionary in this format:
data = pandas.read_csv("DAY 26 - NATO Alphabet/nato_phonetic_alphabet.csv")
phonetics = {row["letter"]:row["code"] for (index, row) in data.iterrows()}

#TODO 2. Create a list of the phonetic code words from a word that the user inputs.

coded_word = [phonetics[letter] for letter in input("Enter a word: ").upper()]

print(coded_word)