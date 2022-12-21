# assignment: programming assignment 4 - stack.py
# author: Lucais Sanderson
# date: May 25, 2022
# file: stack.py
# input: the class stack requires no inital parameters.
# output: returns stack object for use in tree.py and calculator.py

class Stack:

    # initiates Stack object
    def __init__(self):
        self.list = []

    # returns True if list/stack is empty
    def isEmpty(self):
        return self.list == []

    # adds item to top of stack
    def push(self, item):
        self.list.append(item)

    # removes and returns item at top of stack
    def pop(self):
        return self.list.pop()

    # returns item at top of stack. If stack empty, returns None
    def peek(self):
        if self.list == []:
            return None
        else:
            return self.list[len(self.list) - 1]

    # returns size of stack
    def size(self):
        return len(self.list)

# a driver program for class Stack


if __name__ == '__main__':

    data_in = ['hello', 'how', 'are', 'you']
    s = Stack()
    for i in data_in:
        s.push(i)

    print(s.peek)
    assert s.size() == len(data_in)
    assert s.peek() == data_in[-1]

    data_out = []
    while not s.isEmpty():
        data_out.append(s.pop())

    assert data_out == data_in[::-1]
    assert s.size() == 0
    assert s.peek() == None
