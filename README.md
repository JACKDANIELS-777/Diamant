# Diamant

A programming language with an interpreter written in Python (built with [SLY](https://github.com/dabeaz/sly)).
It aims for Python's simplicity with some systems-language control, and it has a few features you won't find in
most languages: variables that remember their history, blocks that react when a variable changes, custom infix
operators, and calling straight into C or Python code.

Keywords can be written in **English or Afrikaans**.

```
MEM x = 5;
x = 10;
x = 20;
print(x@0);      # 5   (oldest value)
print(x@2);      # 20
```

## Features

### Variables with memory (`MEM`)

A `MEM` variable keeps every value it has held, and `x@n` reads its history.

### React to changes (`WATCH`)

```
MEM a = 0;
WATCH a { print("a changed to", a) };
a = 1;           # a changed to 1
a = 2;           # a changed to 2
```

### Custom infix operators (`INFIX`)

```
INFIX "sum"(a, b) => { ret a + b + 10 };
print(1 "sum" 2);        # 13
```

### Functions

```
fun add(a, b) { ret a + b };
print(add(5, 10));       # 15
```

Functions can also be overloaded by number of parameters.

### Types and casts

Optional types with C-style casts:

```
INT a = 10;
FLOAT b = (FLOAT) a;
```

### Loops, ranges and comprehensions

```
for i in [1..5] { print(i) };            # 1 2 3 4
x = 0; while x < 3 { print(x), x = x + 1 };
print([i*2 for i in [1..5]]);            # [2, 4, 6, 8]
```

### Timing a block (`TIME`)

```
TIME t { for i in [1..1000] { a = i } };
print(t);                                # seconds taken
```

### Control blocks

`DEFER` (run at the end of a function), `ONCE` (run only the first time), `match`, `if / elif / else`.

### Python interop

```
import "math";
print($math_sqrt(49));   # 7.0
```

### C interop

Write C inside a Diamant program. It's compiled with `gcc` into a shared library and loaded with `ctypes`, and its
functions become callable as `$_C_name(...)`. Return and argument types (`int`, `int*`, `float`, `double`, `char`)
are read from the C signatures.

```
C->{"""
int* hello(int c){
    int *a = malloc(sizeof(int))\s
    *a = c\s
    return a\s
}
"""};
a = $_C_hello(9);
```

Statements are split on `;` before parsing, so inside a C block write `\s` where C needs a semicolon.

### Also

Structs, classes, enums, dictionaries, tuples, null-coalescing `??`, `with` scopes, inline `ASM` blocks, and GUI
windows (Tkinter).

## English or Afrikaans

| English | Afrikaans |
|---|---|
| `if` / `then` / `else` | `As` / `Dan` / `Anders` |
| `while` | `terwyl` |
| `break` | `breek` |
| `struct` | `strukt` |
| `and` / `or` / `not` | `En` / `Of` / `Nie` |

## Running it

```sh
pip install sly soupsieve beautifulsoup4
python Updated_NoConflicts/old3.py program.dia
```

C interop needs `gcc` on the PATH.

`Updated_NoConflicts/old3.py` is the current interpreter. The `Lexer/`, `Parser/` and `ParseTree/` folders hold an
earlier, modular version, and `docs/` is the project's website, including a tutorial.

---

Part of my Diamant projects. Each repository is its own separate project.
