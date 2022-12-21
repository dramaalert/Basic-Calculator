# assignment: programming assignment 4 - calculator.py
# author: Lucais Sanderson
# date: May 25, 2022
# file: calculator.py
# input: takes numerical algebraic expression from user. 
# output: computes expression using expression tree then returns the result.

from stack import Stack
from tree import ExpTree
import re


def infix_to_postfix(infix):
    # makes stack
    opstack = Stack()
    # orders the precedence of operators
    prec = {'(': 1, ')': 1, '^': 5, '*': 4, '/': 4, '+': 3, '-': 3}
    # makes postfix list to be appended
    postfix = []
    # splits infix expression into list with operators as delimiters
    # while retaining operator (grouping)
    infix_list = re.split(r'([+]|-|[*]|/|\^|[()])', infix)
    # for loop running through each char in infix
    for i in infix_list:
        # some blank spaces are in the list for some reason
        if i == '':
            continue
        # if number or float, append
        elif i.isnumeric() or '.' in i:
            postfix.append(i)
        # if the stack is empty, push the operator
        elif opstack.isEmpty():
            opstack.push(i)
        # if opening parentheses, push into stack
        elif i == '(':
            opstack.push(i)
         # if closing parentheses, kick out each operator
         # until opening parentheses is reached.
        elif i == ')':
            while not opstack.peek() == '(':
                postfix.append(opstack.pop())
            opstack.pop()
        # otherwise, until the stack is empty or the token takes
        # precedence over top of stack, append top of stack to
        # postfix. Then push token to stack.
        else:
            while not opstack.isEmpty() and prec[i] <= prec[opstack.peek()]:
                postfix.append(opstack.pop())
            opstack.push(i)
    # while stack isn't empty, kick top of stack to postfix
    while not opstack.isEmpty():
        postfix.append(opstack.pop())
    # join list into full string separated by ' '
    return ' '.join(postfix)


def calculate(infix):
    # convert infix to postfix notation
    postfix = infix_to_postfix(infix)
    # make expression tree from postfix, split into list
    tree = ExpTree.make_tree(postfix.split())
    # evaluate the tree to get final result and return it
    return float(tree.evaluate(tree))


# a driver to test calculate module
if __name__ == '__main__':

    # test infix_to_postfix function
    assert infix_to_postfix('(50+2)*3') == '50 2 + 3 *'
    assert infix_to_postfix('5+2*3') == '5 2 3 * +'

    # test calculate function
    assert calculate('(5+2)*3') == 21.0
    assert calculate('5+2*3') == 11.0

    print('Welcome to Calculator Program!')

    while True:
        # gets user input and calculates result
        inp = input(
            "Please enter your expression here. To quit enter 'quit' or 'q':\n")
        if inp == 'q' or inp == 'quit':
            print('Goodbye!')
            break
        print()
        print(calculate(str(inp)))
