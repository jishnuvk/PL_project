class Node():

    def __init__(self, name, parent, terminal = False):
        
        self.name = name
        self.parent = parent
        self.finished = terminal
        self.children = []
        
    def set_children(self,children):

        self.children = children

    def __str__(self):
        
        if(self.children != []):
            string = self.name + " [ "

            for i in self.children:
                string+= str(i) + " "

            string += "] "

            return string    
        else:
            return self.name

class Tree():

    def __init__(self,root):

        self.root = root
        self.current = root

    def next(self):

        for i in self.current.children:

            if(i.finished == False):
                self.current = i
                self.current.finished = True
                return i                

        self.current = self.current.parent
        
        if self.current == 0:
            return 0
        
        return self.next()  

    def __str__(self):

        return str(self.root)          


if __name__ == "__main__":

    node = Node("root",0)

    
    tree = Tree(node)
    children = [Node("child1",node),Node("child2",node),Node("child3",node)]
    node.set_children(children)

    node = tree.next()
    children = [Node("child11",node),Node("child21",node),Node("child31",node)]
    node.set_children(children)

    children = [Node("child11",node),Node("child21",node),Node("child31",node)]


    print(tree)


