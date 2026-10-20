# Pelago example: an RPN calculator

A small, complete [Pelago](https://github.com/pelagolang/pelago) project that shows how one looks on disk: a `pelago.toml`, a few modules, formatter and build checks in CI. It is a reverse Polish notation calculator: `3 4 + 2 *` means `(3 + 4) * 2`.

It is deliberately small. For a tour of the whole syntax see [`examples/tour.pel`](https://github.com/pelagolang/pelago/blob/main/examples/tour.pel), and for more one-file programs see [`examples/programs/`](https://github.com/pelagolang/pelago/tree/main/examples/programs) in the main repository; this repository is about the project around the code.

## Layout

```
pelago.toml        project settings; here the [fmt] section for the formatter
src/main.pel       the entry point: evaluates some expressions and prints the results
src/rpn.pel        the calculator: a module imported by main.pel
expected.txt       what the program must print; CI compares against it
.github/           CI: format check, type check, interpreter run and native build
```

A file is a module and its file name is the module name, so `src/rpn.pel` is imported as `.rpn` from `src/main.pel`. The code shows an `enum` with data, `switch`, `result` values (`int ! calc_error`), `?` to pass errors up, `inout` arguments, and the comment forms `///` (plain), `//~` (doc).

### `pelago.toml`

```toml
[fmt]
indent = 4    # spaces per level, 1 to 8
width = 100   # 20 to 400
```

`pelago fmt` reads the closest `pelago.toml` above the file it formats, and so does the language server, so your editor and CI agree. Unknown sections and keys are errors.

## Run it

You need the `pelago` tool. There are no binary releases yet, so build it from source (this needs a [Rust toolchain](https://rustup.rs)):

```
cargo install --git https://github.com/pelagolang/pelago --locked pelago
```

Then, from the root of this repository (PowerShell and bash both work):

```
pelago run .                  # run in the interpreter
pelago build -o rpn .         # build a native executable (rpn.exe on Windows)
./rpn                         # PowerShell: .\rpn
pelago check .                # parse, resolve names and check types
pelago fmt --check .          # exit 1 if a file would be reformatted; drop --check to format in place
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

## CI

`.github/workflows/ci.yml` installs `pelago` from the main repository, then runs:

1. `pelago fmt --check .` (formatting follows `pelago.toml`)
2. `pelago check .`
3. `pelago run .` and a native `pelago build -o rpn .` followed by running it, each compared with `expected.txt`

## Editor setup

| Editor | How |
|---|---|
| VS Code | Install **Pelago** from the [Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=pelagolang.pelago): highlighting, snippets and the language server. The language server runs the `pelago` tool, so install it first (above) and make sure it is on your `PATH` (or set `pelago.serverPath`). Source: [vscode-pelago](https://github.com/pelagolang/vscode-pelago). |
| Zed | [zed-pelago](https://github.com/pelagolang/zed-pelago) is **not published yet**. You can install it as a dev extension from a checkout (`zed: install dev extension`). It needs `pelago` on your `PATH` for the language server. |
| Neovim, Helix | No extension yet. [tree-sitter-pelago](https://github.com/pelagolang/tree-sitter-pelago) has the grammar, and `pelago lsp` speaks the language server protocol over stdio, so you can configure it by hand. |

The language server formats with the same `pelago.toml` as `pelago fmt`, so "format on save" in your editor matches the CI check.

## Licence

MIT OR Apache-2.0, at your option: see `LICENSE-MIT` and `LICENSE-APACHE`.
