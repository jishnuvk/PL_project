import Grammar
from Tree import Tree, Node

grammar = Grammar.grammar

Grammar.find_first_and_follow_set(grammar)

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

    def __init__(self, grammar):

        Grammar.find_first_and_follow_set(grammar)
        self.production_table, self.parse_table = build_parse_table(grammar)

    def parse(self, token_list, start):
    
 
        if(type(token_list
        tree = Tree(Node(start,0))
        current_node = tree.root
        i = 0

        while(i < len(token_list)):
            
            production_id = self.parse_table[current_node.name][token_list[i]]
            children = []

            if(Grammar.terminal(self.production_table[production_id][1][0])):
                i+=1
            
            if(self.production_table[production_id][1] == 'epsilon'):

                children.append(Node('epsilon',current_node,True))
            else:
                for j in self.production_table[production_id][1]:
                    node = 0
                    if Grammar.terminal(j):
                        if(type(
                        node = Node(j,current_node,True)
                    else:
                        node = Node(j,current_node)
                    children.append(node)        

                    
            current_node.set_children(children)

            current_node = tree.next()

            if(current_node == 0):
                break
        
        return tree

if __name__ == "__main__":

    parser = Parser(grammar)

    token_list = ['id','*','id','+','id',"$"]
    print(token_list)
    tree = parser.parse(token_list, 'E')    


    print(tree)
