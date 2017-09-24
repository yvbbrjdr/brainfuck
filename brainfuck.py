#!/usr/bin/env python3

import readline
import sys

class LinkedList(object):
    def __init__(self, value=0, left=None, right=None):
        self.value, self._left, self._right = value, left, right

    @property
    def left(self):
        if not self._left:
            self._left = LinkedList(right=self)
        return self._left

    @property
    def right(self):
        if not self._right:
            self._right = LinkedList(left=self)
        return self._right

    def has_left(self):
        return self._left != None

    def has_right(self):
        return self._right != None

class Environment(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.ptr, self.buf = LinkedList(), ''

    def nontrivial(self):
        return self.ptr.value != 0

    def left(self):
        self.ptr = self.ptr.left

    def right(self):
        self.ptr = self.ptr.right

    def inc(self):
        self.ptr.value = (self.ptr.value + 1) % 256

    def dec(self):
        self.ptr.value = (self.ptr.value + 255) % 256

    def output(self):
        print(chr(self.ptr.value), end='')
        sys.stdout.flush()

    def input(self):
        try:
            if not self.buf:
                self.buf = input()
                self.buf += '\n'
        except EOFError:
            self.buf = '\0'
        self.ptr.value, self.buf = ord(self.buf[0]), self.buf[1:]

    def dump(self):
        temp = self.ptr
        while temp.has_left():
            temp = temp.left
        while temp.has_right():
            if temp == self.ptr:
                print('[%d]' % (temp.value), end=' ')
            else:
                print(temp.value, end=' ')
            temp = temp.right
        if temp == self.ptr:
            print('[%d]' % (temp.value))
        else:
            print(temp.value)

def read_line(start=True):
    return input('bf> ' if start else '    ')

def complete_statement(statement):
    nested = 0
    for c in statement:
        if c == '[':
            nested += 1
        elif c == ']':
            nested -= 1
        assert nested >= 0, 'invalid statement'
    return nested == 0

def exec_brainfuck(statement, env):
    i, length = 0, len(statement)
    while i < length:
        if statement[i] == '<':
            env.left()
        elif statement[i] == '>':
            env.right()
        elif statement[i] == '+':
            env.inc()
        elif statement[i] == '-':
            env.dec()
        elif statement[i] == '.':
            env.output()
        elif statement[i] == ',':
            env.input()
        elif statement[i] == '[':
            nested = 1
            for j in range(i + 1, length):
                if statement[j] == '[':
                    nested += 1
                elif statement[j] == ']':
                    nested -= 1
                if not nested:
                    break
            while env.nontrivial():
                exec_brainfuck(statement[i + 1:j], env)
            i = j
        elif statement[i] == '`':
            env.reset()
            print('Environment reset.')
        elif statement[i] == '?':
            env.dump()
        i += 1

def interactive(env=Environment()):
    buf = ''
    while True:
        try:
            buf += read_line(buf == '')
            buf = ''.join([c for c in buf if c in '<>+-.,[]`?'])
            if complete_statement(buf):
                exec_brainfuck(buf, env)
                buf = ''
        except AssertionError as e:
            print('BrainfuckError:', e)
            buf = ''
        except KeyboardInterrupt:
            print('\nKeyboardInterrupt')
            buf = ''
        except EOFError:
            print()
            return

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Brainfuck Interpreter')
    parser.add_argument('-load', '-i', action='store_true',
                        help='run file interactively')
    parser.add_argument('file', nargs='?',
                        type=str, default=None,
                        help='Brainfuck file to run')
    args = parser.parse_args()
    if args.file is not None:
        with open(args.file) as f:
            statement = f.read()
        statement = ''.join([c for c in statement if c in '<>+-.,[]`?'])
        env = Environment()
        try:
            assert complete_statement(statement), 'invalid statement'
            exec_brainfuck(statement, env)
        except AssertionError as e:
            print('BrainfuckError:', e)
        except KeyboardInterrupt:
            print('\nKeyboardInterrupt')
        except EOFError:
            print()
        if args.load:
            interactive(env)
    else:
        interactive()

if __name__ == '__main__':
    main()
