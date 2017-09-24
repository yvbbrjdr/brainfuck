# brainfuck

Play with BF!

## Contents

### [brainfuck.py](brainfuck.py)

A rich-featured interactive Brainfuck interpreter.

Type
```bash
$ ./brainfuck.py
```
to start an interactive Brainfuck session. You can type `?` to dump the RAM and <code>`</code> to reset the environment. These two instructions can also appear in Brainfuck code.

Demo:
```
bf> ++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.
Hello World!
bf> ?
0 87 100 33 [10]
bf> [-]
bf> ?
0 87 100 33 [0]
bf> `
Environment reset.
bf> ?
[0]
```

You can also load and run a Brainfuck source file by typing
```bash
$ ./brainfuck.py somefile.b
```

If you want to go to the interactive session after executing a file, you can type
```bash
$ ./brainfuck.py -i somefile.b
```

### [bfbf.b](bfbf.b)

A self-interpreter for Brainfuck. Use `!` to mark the end of the source code and the beginning of input.

Demo:
```
$ ./brainfuck.py bfbf.b
,>++++++[<-------->-],,[<+>-],<.>.!4+3
7
```

###### [Reference](https://arxiv.org/html/cs/0311032)

### [bf2c.b](bf2c.b)

A Brainfuck to C compiler.

Demo:
```
$ echo ,[.,] | ./brainfuck.py bf2c.b
#include <unistd.h>
char r[65536],*e=r;
main(){
read(0,e,1);
while(*e){
write(1,e,1);
read(0,e,1);
}
exit(0);
}
```

###### [Reference](http://www.hevanet.com/cristofd/brainfuck/)

## Dependencies

[Python 3](https://www.python.org/downloads/)
