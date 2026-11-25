# RPN calculator: a whole project

A reverse Polish notation calculator: `3 4 + 2 *` means `(3 + 4) * 2`. It shows how a project looks on disk.

```
pelago.yaml      project settings; here the `fmt` section for the formatter
src/main.pel     the entry point: evaluates some expressions and prints the results
src/rpn.pel      the calculator: a module imported by main.pel
expected.txt     what the program must print; CI compares against it
```

A file is a module and its file name is the module name, so `src/rpn.pel` is imported as `.rpn` from `src/main.pel`. The code shows an `enum` with data, `switch`, `result` values (`int ! calc_error`), `?` to pass errors up, `inout` arguments, and the comment forms `///` (plain) and `//~` (doc).

`pelago fmt` reads the closest `pelago.yaml` above the file it formats, and so does the language server, so your editor and CI agree. Unknown sections and keys are errors.

```
pelago run projects/rpn            # native code (the default)
pelago run --interp projects/rpn   # the interpreter
pelago build -o rpn projects/rpn   # a native executable; ./rpn
pelago fmt --check projects/rpn
```

Expected output (also in `expected.txt`):

```
3 4 + 2 * = 14
10 2 8 * + 3 - = 23
5 1 2 + 4 * + 3 - = 14
1 +: an operator needs two numbers before it
4 0 /: division by zero
2 x *: not a number or operator: x
```
