with open("input.r",'r') as f:
    string = f.read()

reserved = [
    "if",
    "else",
    "repeat",
    "while",
    "function",
    "for",
    "in",
    "next",
    "break",
    "TRUE",
    "FALSE",
    "NULL",
    "Inf",
    "NaN",
    "NA",
    "NA_integer_",
    "NA_real_",
    "NA_complex_",
    "NA_character_",
    "...",

]

symbols = [
    "+",
    "-",
    "*",
    "/",
    "(",
    ")",
    "{",
    "}",
    "==",
    "!=",
    ">",
    "<",
    "<=",
    ">=",
    "<-",
    '"',
    ":",
]

token_list = []

def add_token(buffer):

    if(buffer == ''):
        return
    
    if(buffer in reserved):
        token_list.append(("keyword", buffer))
    elif(buffer in symbols):
        token_list.append((buffer))
    elif(buffer.isdigit() or buffer[0] == '"'):
        token_list.append(("literal", buffer))
    elif(buffer == ';'):
        token_list.append(("endline"))
 
    else:
        token_list.append(("id", buffer))    

def tokenize():


    buffer = ""
    current_type = "*"
    string_ongoing = False

    if(string.isalpha()):
        current_type = 'a'
    elif(string.isdigit()):
        current_type = 'n'
    else:    
        current_type = 's'    



    for i in range(len(string)):

        char = string[i]

        if(string_ongoing):
            buffer += char

            if(char == '"'):
                add_token(buffer)
                buffer = ''
                current_type = '*'
                string_ongoing = False
            continue

        if(char == '"'):
            string_ongoing = True
            add_token(buffer)
            buffer = '"'
            continue

        if(char == " " or char == "\n"):
            add_token(buffer)
            if(char == "\n"):
                add_token(";")    
            buffer = ""
            current_type = "*"
            continue
        if(char.isalpha()):
            new_type = 'a'
        elif(char.isdigit()):
            new_type = 'n'
        else:    
            new_type = 's'


        if(current_type == new_type or current_type == "*"):
            
            if(current_type == 's' and new_type == 's' and not( (buffer+char) in symbols)):
                add_token(buffer)
                buffer = char
            else:
                buffer += char
        else:
            add_token(buffer)
            buffer = char
                   
        current_type = new_type  

    add_token(buffer)


tokenize()
print(token_list)