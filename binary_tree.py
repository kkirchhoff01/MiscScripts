

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class Tree:
    def __init__(self):
        self.root = None

    def insert_node(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self.recursive_insert(self.root, value)

    def recursive_insert(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self.recursive_insert(node.left, value)
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self.recursive_insert(node.right, value)

    def search_tree(self, value):
        if self.root is None:
            return self.root
        else:
            return self.recursive_search(self.root, value)

    def recursive_search(self, node, value):
        if node.value == value:
            return node
        elif node.left and value < node.value:
            return self.recursive_search(node.left, value)
        elif node.right and value > node.value:
            return self.recursive_search(node.right, value)

    def print_tree(self):
        if self.root is not None:
            self.recursive_print(self.root)

    def recursive_print(self, node):
        if node is not None:
            self.recursive_print(node.left)
            print str(node.value) + ' '
            self.recursive_print(node.right)

if __name__ == "__main__":
    import sys
    values = None
    with open(sys.argv[1], 'r') as fh:
        values = fh.readlines()

    tree = Tree()
    for value in values:
        tree.insert_node(float(value))
    tree.print_tree()
