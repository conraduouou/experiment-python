import pandas

data = pandas.read_csv("DAY 26 - NATO Alphabet/nato_phonetic_alphabet.csv")
phonetics = {row["letter"]:row["code"] for (index, row) in data.iterrows()}

while True:
    user_input = input("Enter a word: ").upper()
    try:
        coded_word = [phonetics[letter] for letter in user_input]
    except KeyError:
        print("Sorry, only letters in the alphabet please.")
    else:
        print(coded_word)
        break