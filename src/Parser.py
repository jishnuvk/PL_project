import Grammar
from Tree import Node, Tree, Tree_Obj, Node_Obj, display_tree    

grammar = Grammar.rule_generator('grammar.txt')

# Grammar.find_first_and_follow_set(grammar)

def build_parse_table(grammar):

    parse_table = {}
    production_table = []

    for i in grammar.keys():
        
        parse_table[i] = {}

        for j in range(len(grammar[i].tails)):
            
            production_id = len(production_table)
            production_table.append( (grammar[i].head,grammar[i].tails[j]) )

            if(grammar[i].tails[j] == 'epsilon'):
                
                for k in grammar[i].follow:
                    if(k in parse_table[i]):
                        print("multiple entries in same cell.", grammar[i], k, parse_table[i][k])
                    else:
                        parse_table[i][k] = production_id    

            else:

                first = grammar[i].tails[j][0]
                
                if Grammar.terminal(first):
                    parse_table[i][first] = production_id
                else:
                    for k in grammar[first].first:
                        parse_table[i][k] = production_id    

    return production_table, parse_table


class Parser():

    def __init__(self, grammar, start):

        Grammar.find_first_and_follow_set(grammar, start)
        self.production_table, self.parse_table = build_parse_table(grammar)

    def parse(self, token_list, start):

        token_list2 = []
        for i in token_list:
            if type(i) != tuple:
                token_list2.append( (i,None))
            else:
                token_list2.append(i)

        print(token_list2) 
        tree = Tree_Obj(Node_Obj(start,None, 0 ))
        current_node = tree.root
        i = 0

        while(i < len(token_list)):
            
           
            production_id = self.parse_table[current_node.name][token_list2[i][0]]
            children = []
            tail_symbols = []

            for symbol in self.production_table[production_id][1]:
                if(Grammar.terminal(symbol)):
                    i+=1
                else:
                    break   
            
            if(self.production_table[production_id][1] == 'epsilon'):

                children.append(Node_Obj('epsilon',None, current_node,True))
            else:
                for j in self.production_table[production_id][1]:   
                    if Grammar.terminal(j):
                        if j in token_list:
                            node = Node_Obj(j,token_list2[token_list.index(j)][1], current_node,True)
                        else:
                            node = Node_Obj(j, None, current_node, True)
                    else:
                        if j in token_list:
                            print("This is me")
                            node = Node_Obj(j,token_list2[token_list.index(j)][1], current_node)
                        else:
                            node = Node_Obj(j, None,current_node)
                    children.append(node)
                
                temp = []
                for j in reversed(self.production_table[production_id][1]):
                    
                    if Grammar.terminal(j):
                        temp.append(j)
                    else:
                        tail_symbols = temp
                        break
            

                    
            current_node.set_children(children)
            current_node.set_tail_symbols(list(reversed(tail_symbols)))
            current_node, tail_symbols = tree.next([])

            for symbol in tail_symbols:
                if(symbol == token_list[i]):
                    i+=1
                else:
                    break


            if(current_node == 0 or token_list[i] == '$'):
                break
        
        return tree


if __name__ == "__main__":

    # print(grammar.keys())
    parser = Parser(grammar, "Statement")

    token_list = ['(', ('id','print'), '+' , ('literal','Hello World'), '+', ('literal', 'Hello world'), ')', '+', '(', ('id', 'print'), '+', ('id', 'print'), ')', '$']
    tree = parser.parse(token_list, 'Statement')    
    
    print(tree)
    tree2 = Tree()
    tree2.create_node(tree.root.name, tree.root.ID)
    display_tree(tree2, tree.root)
    print("This is the final tree")

    tree2.show()
