class Rule():

    def __init__(self, head, tails):

        self.head = head
        self.tails = tails
        self.first = set()
        self.follow = set()

    def __str__(self):
        return "RULE:"+self.head

grammar = {}

# grammar['operator'] = Rule("operator", [ '+' , '-' , '*' , '/' ])
# grammar['expression'] = Rule("expression", [ 'id' , ['id', 'operator', 'expression']] )

# E  -> TE’
# E’ -> +T E’|Є
# T  -> F T’
# T’ -> *F T’ | Є
# F  -> (E) | id

# grammar["E"] = Rule("E", [ ["T","E'"] ])
# grammar["E'"] = Rule("E'", [ ["+","T","E'"],"epsilon"])
# grammar["T"] = Rule("T", [["F","T'"]])
# grammar["T'"] = Rule("T'", [ ["*","F","T'"], "epsilon" ])
# grammar["F"] = Rule("F", [ ["(","E",")"] , ["id"] ])

def rule_generator(src):
    #All characters are separated by space.
    with open(src,'r') as f:
        src_string = f.read()
    buff = ""
    para = []#The final parameters of Rule, first element being heads, second element being tails
    curr = []#appending of list of lists
    gram = {} 
    string_ongoing = True
    r_list = src_string.split("\n")
    for j in range(len(r_list)):
        r = r_list[j]
        buff = ""
        para = []#The final parameters of Rule, first element being heads, second element being tails
        curr = []#appending of list of lists
        string_ongoing = True
        for i in range(len(r)):
            char = r[i]
            if(char=='@'):
                para.append(buff)
                buff=''
                continue
            if(char == ' '):
                string_ongoing = False
            if(char=='?'):
                string_ongoing = False
                if(buff!=''):
                    curr.append(buff)
                if(len(curr)==1 and curr[0]=='epsilon'):
                    para.append(curr[0])
                elif(len(curr)>0):
                    para.append(curr)
                buff=""
                curr = []
                continue
            if(string_ongoing):
                buff+=char
            else:
                if(buff!=''):
                    curr.append(buff)
                buff = ''
            string_ongoing = True
        if(buff!=''):
            curr.append(buff)
        if(len(curr)==1 and curr[0]=='epsilon'):
            para.append(curr[0])
            curr = []
        elif(len(curr)>0):
            para.append(curr)
            curr = []
        gram[para[0]] = Rule(para[0],para[1:])
        #print(para)
    #print(gram)
    return gram

reserved = [
    "if",
    "else",
    "repeat",
    "while",
    "function",
    "for",
    "return",
    "in",
    "next",
    "break",
    "newline",
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
    "^",
    "=",
    "|",
    "&",
    "&&",
    "||",
    "%%",
    "!"
]

def terminal(x):


    if( (x == 'id') or (x == 'literal') or (x in reserved) or (x in symbols)):
        return True
    else:
        return False    

def find_first_set(rule, grammar):

    contains_epsilon = False

    
    for i in rule.tails:
        if(terminal(i)):
            
            rule.first.add(i)
        else:
            if(i == 'epsilon'):
                rule.first.add('epsilon')
                contains_epsilon = True
            else:
                for j in i:
                    if(terminal(j)):
                        rule.first.add(j)
                        break
                    else:
                        tail_contains_epsilon , tail_first_set = find_first_set(grammar[j], grammar)
                        rule.first.update(tail_first_set)
                        if(not tail_contains_epsilon):
                            break
                        else:
                            contains_epsilon = True 


    return contains_epsilon, rule.first

def initialize_follow_set(rule, start, grammar):

    if(rule.head == start):
        rule.follow.add("$")

    for i in (rule.tails):
        for j in range(len(i) - 1):

            if(not terminal(i[j])):
                if(terminal(i[j+1])):
                    grammar[i[j]].follow.add(i[j+1])            


def follow_recursive(rule, history, grammar):

    change = False
    history.add(rule.head)
    for i in rule.tails:
        if(terminal(i) or i=='epsilon'):
            continue

        follow = rule.follow.copy()
        for j in range(len(i)-1, -1, -1):
            if(terminal(i[j])):
                follow = set([i[j]])
            else:
                
                if(i[j] in history):
                    if('epsilon' in grammar[i[j]].first):
                        follow.update(grammar[i[j]].first - set(['epsilon']))
                        
                    else:
                        follow = grammar[i[j]].first 
                    continue
                
                if(len( follow - set('epsilon') -  grammar[i[j]].follow  ) != 0):

                    grammar[i[j]].follow.update(follow - set(['epsilon']))
                    change = True
                    

                if('epsilon' in grammar[i[j]].first):
                    follow.update(grammar[i[j]].first - set(['epsilon']))
                else:
                    follow = grammar[i[j]].first
                


                c = follow_recursive(grammar[i[j]], history, grammar)
                change = change or c     
    return change        


def find_first_and_follow_set(grammar, start):


    for i in grammar.keys():
        find_first_set(grammar[i], grammar)
        initialize_follow_set(grammar[i], start, grammar)
    


    change = True
    while(change):
        change = follow_recursive(grammar[start], set(), grammar)




if __name__ == "__main__":

    find_first_and_follow_set(grammar)
    print(grammar["E"].first)
    print(grammar["E'"].first)
    print(grammar["T"].first)
    print(grammar["T'"].first)
    print(grammar["F"].first)


    print(grammar["E"].follow)
    print(grammar["E'"].follow)
    print(grammar["T"].follow)
    print(grammar["T'"].follow)
    print(grammar["F"].follow)


