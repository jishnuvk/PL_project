from treelib import Node, Tree

count = 0

class Node_Obj():

    def __init__(self, name, value, parent, terminal = False):
        
        self.name = name
        self.value = value
        if self.value != None:
            self.name = "(" + name +"," + str(self.value) + ")"
        global count
        count += 1
        self.ID = count
        self.parent = parent
        self.finished = terminal
        self.children = []
        self.tail_symbols = []
        
    def set_children(self,children):

        self.children = children

    def set_tail_symbols(self, tail_symbols):

        self.tail_symbols = tail_symbols    

    def __str__(self):
        string = self.name

        if(self.children != [] and self.children[0].name != 'epsilon'):
            string = " [ "

            for i in self.children:
                string+= str(i) + " "

            string += "] "

        return string    
        
class Tree_Obj():

    def __init__(self,root):

        self.root = root
        self.current = root

    def next(self, tail_symbols = []):
        
        for i in self.current.children:
            if(i.finished == False):
                self.current = i
                self.current.finished = True
                return i, tail_symbols    
                                    
        tail_symbols.extend(self.current.tail_symbols)
        self.current = self.current.parent
        
        if self.current == 0:
            return 0
        
        return self.next(tail_symbols)  

    def __str__(self):

        return str(self.root)          

def display_tree(tree, treeobj_root,idx_list):
    count = 0
    for i in treeobj_root.children:
        tree.create_node(str(count) + " " + i.name, i.ID, parent = treeobj_root.ID)
        count += 1
    for i in treeobj_root.children:    
        display_tree(tree, i,idx_list)


if __name__ == "__main__":

    node = Node_Obj("root",0)

    ''' 
    tree = Tree(node)
    children = [Node("child1",node),Node("child2",node),Node("child3",node)]
    node.set_children(children)

    node = tree.next()
    children = [Node("child11",node),Node("child21",node),Node("child31",node)]
    node.set_children(children)

    children = [Node("child11",node),Node("child21",node),Node("child31",node)]
    '''
