# assignment: programming assignment 4 - tree.py
# author: Lucais Sanderson
# date: May 25, 2022
# file: tree.py
# input: the class BinaryTree and ExpTree requires a name for the root.
# output: ExpTree returns tree object for use in calculator.py. ExpTree takes
# infix expresion and creates an expression tree for it. then it can be accessed
# via preorder, inorder, and postorder and the expression can also be evaluated.
# __str__ method returns string of the expression in infix ordrer.

from stack import Stack


class BinaryTree:
    def __init__(self, rootObj=None):
        self.key = rootObj
        self.leftChild = None
        self.rightChild = None

    def insertLeft(self, newNode):
        if isinstance(newNode, BinaryTree):
            # don't make new tree
            # set left child to node as is
            node = newNode
        else:
            node = BinaryTree(newNode)
        if self.leftChild == None:
            self.leftChild = node
        else:
            t = node
            t.leftChild = self.leftChild
            self.leftChild = t

    def insertRight(self, newNode):
        if isinstance(newNode, BinaryTree):
            node = newNode
        else:
            node = BinaryTree(newNode)

        if self.rightChild == None:
            self.rightChild = node
        else:
            t = node
            t.rightChild = self.rightChild
            self.rightChild = t

    def getRightChild(self):
        return self.rightChild

    def getLeftChild(self):
        return self.leftChild

    def setRootVal(self, obj):
        self.key = obj

    def getRootVal(self):
        return self.key

    def __str__(self):
        s = f"{self.key}"
        s += '('
        if self.leftChild != None:
            s += str(self.leftChild)
        s += ')('
        if self.rightChild != None:
            s += str(self.rightChild)
        s += ')'
        return s


class ExpTree(BinaryTree):

    def make_tree(postfix):
        # nums: push
        # operations:  pop, pop, join, push
        # pop and return final stack value
        s = Stack()
        for i in postfix:
            # checks if the item is digit or decimal
            # if yes, push
            if i.isnumeric() or '.' in i:
                s.push(i)
            # else if operator, create subtree and make its
            # children the previous two items in stack
            # then push back into stack
            elif i in '*/+-^':
                t = ExpTree(i)
                t.insertRight(s.pop())
                t.insertLeft(s.pop())
                s.push(t)
        # final pop is the full expression tree
        return s.pop()

    def preorder(tree):
        s = ''
        # tree value not None, recursively extract 
        # preorder version of expression 
        if tree != None:
            s += tree.getRootVal()
            s += ExpTree.preorder(tree.getLeftChild())
            s += ExpTree.preorder(tree.getRightChild())
        return s

    def inorder(tree):
        s = ''
        # tree value not None, recursively extract 
        # inroder version of expression. including '()'
        if tree != None:
            if tree.getRootVal() in '*/+-':
                s = '('
            s = s + ExpTree.inorder(tree.getLeftChild())
            s += tree.getRootVal()
            s = s + ExpTree.inorder(tree.getRightChild())
            if tree.getRootVal() in '*/+-':
                s += ')'
        return s

    def postorder(tree):
        s = ''
        # tree value not None, recursively extract 
        # postorder version of expression 
        if tree != None:
            s += ExpTree.postorder(tree.getLeftChild())
            s += ExpTree.postorder(tree.getRightChild())
            s += tree.getRootVal()
        return s

    def evaluate(self, tree):
        # recursive function
        # same way traversals are recursive

        # base case : tree.getRootVal().isNumeric() or float
        if tree.getRootVal().isnumeric():
            return int(tree.getRootVal())
        elif '.' in tree.getRootVal():
            return float(tree.getRootVal())

        # recursive case: if tree.getRootVal() is a operation: '+-*/^'
        if tree.getRootVal() == '+':
            return self.evaluate(tree.leftChild) + self.evaluate(tree.rightChild)
        if tree.getRootVal() == '-':
            return self.evaluate(tree.leftChild) - self.evaluate(tree.rightChild)
        if tree.getRootVal() == '*':
            return self.evaluate(tree.leftChild) * self.evaluate(tree.rightChild)
        if tree.getRootVal() == '/':
            return self.evaluate(tree.leftChild) / self.evaluate(tree.rightChild)
        if tree.getRootVal() == '^':
            return self.evaluate(tree.leftChild) ** self.evaluate(tree.rightChild)

    def __str__(self):
        return ExpTree.inorder(self)


# a driver for testing BinaryTree and ExpTree
if __name__ == '__main__':

    # test a BinaryTree

    r = BinaryTree('a')
    assert r.getRootVal() == 'a'
    assert r.getLeftChild() == None
    assert r.getRightChild() == None
    assert str(r) == 'a()()'

    r.insertLeft('b')
    assert r.getLeftChild().getRootVal() == 'b'
    assert str(r) == 'a(b()())()'

    r.insertRight('c')
    assert r.getRightChild().getRootVal() == 'c'
    assert str(r) == 'a(b()())(c()())'

    r.getLeftChild().insertLeft('d')
    r.getLeftChild().insertRight('e')
    r.getRightChild().insertLeft('f')
    assert str(r) == 'a(b(d()())(e()()))(c(f()())())'

    assert str(r.getRightChild()) == 'c(f()())()'
    assert r.getRightChild().getLeftChild().getRootVal() == 'f'

    # test an ExpTree

    infix = ''

    postfix = '50 2 3 * +'.split()
    tree = ExpTree.make_tree(postfix)
    assert str(tree) == '(50+(2*3))'
    assert ExpTree.inorder(tree) == '(50+(2*3))'
    assert ExpTree.postorder(tree) == '5023*+'
    assert ExpTree.preorder(tree) == '+50*23'
    assert tree.evaluate(tree) == 56.0

    postfix = '5 2 + 3 *'.split()
    tree = ExpTree.make_tree(postfix)
    assert str(tree) == '((5+2)*3)'
    assert ExpTree.inorder(tree) == '((5+2)*3)'
    assert ExpTree.postorder(tree) == '52+3*'
    assert ExpTree.preorder(tree) == '*+523'
    assert tree.evaluate(tree) == 21.0
