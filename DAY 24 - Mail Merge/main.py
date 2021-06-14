#TODO: Create a letter using starting_letter.txt 
#for each name in invited_names.txt
#Replace the [name] placeholder with the actual name.
#Save the letters in the folder "ReadyToSend".
    
#Hint1: This method will help you: https://www.w3schools.com/python/ref_file_readlines.asp
    #Hint2: This method will also help you: https://www.w3schools.com/python/ref_string_replace.asp
        #Hint3: THis method will help you: https://www.w3schools.com/python/ref_string_strip.asp

with open("Input/Letters/starting_letter.txt") as letter:
    with open("Input/Names/invited_names.txt") as names:
        
        names_to_strip = names.readlines()
        names_list = []
        for i in range(len(names_to_strip)):
            names_list.append(names_to_strip.pop().strip())

        names_list.reverse()

    letter_lines = letter.readlines()

    for name in names_list:
        line_to_insert = letter_lines[0].replace("[name]", name)
        with open(f"Output/ReadyToSend/Letter For {name}.txt", mode="w") as file:
            file.write(line_to_insert)
            for i in range(1, len(letter_lines)):
                file.write(letter_lines[i])
