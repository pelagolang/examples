# Pelago examples

Small, complete programs for the [Pelago](https://github.com/pelagolang/pelago) language, one feature at a time, grouped by topic. Every example is checked and run with the real `pelago` tool in CI, and each one starts with a comment that says what it shows and what it prints.

New to the language? Read the [guide](https://pelagolang.github.io/website/en-US/docs/guide/values) first, or the [tour](https://pelagolang.github.io/website/en-US/docs/tour). The full [documentation](https://pelagolang.github.io/website/en-US/docs/) has a page for every type, module and feature; this repository is the "show me the code" companion to it.

## Run the examples

You need the `pelago` tool. There are no binary releases yet, so build it from source (this needs a [Rust toolchain](https://rustup.rs)); see [Install](https://pelagolang.github.io/website/en-US/docs/getting-started/install):

```
cargo install --git https://github.com/pelagolang/pelago --locked pelago
```

Then, from the root of this repository (the commands are the same in PowerShell and bash):

```
pelago run basics/hello.pel            # build machine code and run `main` (the default)
pelago run --interp basics/hello.pel   # the IR interpreter instead of native code
pelago run --interp --opt --stats basics/hello.pel   # optimise the IR first and print statistics
pelago run --native basics/hello.pel   # the native route, spelled out
pelago build -o hello basics/hello.pel # write an executable (hello.exe on Windows); run it with ./hello
pelago check basics/hello.pel          # parse, resolve names and check types only
pelago fmt --check .                   # exit 1 if a file would be reformatted; drop --check to format in place
```

`pelago run` compiles to native code in memory and runs it; the interpreter is the fallback (`--interp`) and a second opinion: every example here must print the same thing on both. For all options see [Command line](https://pelagolang.github.io/website/en-US/docs/tools/cli).

A few examples are folders (`modules/imports`, `projects/rpn`): run the folder, for example `pelago run modules/imports`, so the files in it can import each other.

### Run all of them

```
python3 tools/run-examples.py          # check, run natively and in the interpreter, compare with the header
python3 tools/run-examples.py strings  # only the examples whose path matches
python3 tools/run-examples.py --pelago path/to/pelago --quick
```

On Windows use `python tools\run-examples.py`. The script needs only Python 3.

## How an example is written

```pelago
/// Shows: the smallest program. `print` writes its arguments and a newline.
/// Run:   pelago run basics/hello.pel
/// Output:
/// | Hello, world
fn main() {
    print("Hello, world")
}
```

The `/// |` lines are the exact standard output the program must print; CI compares them. Examples print the same text on every machine, so those that use clocks or system randomness print only what must always hold (for example `true` for "at least 30 ms went by"). An example may add `/// Interp: no` if the interpreter cannot run it. See [CONTRIBUTING.md](CONTRIBUTING.md) to add one.

## What is here

### Basics

Docs: [values](https://pelagolang.github.io/website/en-US/docs/guide/values), [functions](https://pelagolang.github.io/website/en-US/docs/guide/functions)

| Example | Shows |
|---|---|
| [`basics/casts.pel`](basics/casts.pel) | `to` for conversions that cannot lose information, `truncInt`/`roundInt` for float to int, and the checked and wrapping byte helpers. |
| [`basics/closures.pel`](basics/closures.pel) | Closures written with `~>`, one-argument shorthand (`x ~> ...`), capturing a variable to change it (`[total!]`), and passing one to a function (a function cannot return a closure that borrows; that needs `box<fn ...>`). |
| [`basics/control_flow.pel`](basics/control_flow.pel) | `if` as a statement and as an expression, `while`, `for ... of` over ranges, `break` and `continue`. |
| [`basics/defer.pel`](basics/defer.pel) | `defer` runs a statement when the function ends, however it ends, in reverse order: clean-up written next to the code that needs it. |
| [`basics/functions.pel`](basics/functions.pel) | Functions, default arguments, expression bodies (`= expr`), early `return` and the last expression as the value. |
| [`basics/hello.pel`](basics/hello.pel) | The smallest program. `print` writes its arguments and a newline. |
| [`basics/switch.pel`](basics/switch.pel) | `switch` as the one pattern matching form: values, ranges, guards and a default. |
| [`basics/variables.pel`](basics/variables.pel) | `const` (cannot change) and `var` (can), type annotations, inference, and `#name` / `#(expr)` in strings. |

### Types

Docs: [types](https://pelagolang.github.io/website/en-US/docs/guide/types), [types](https://pelagolang.github.io/website/en-US/docs/reference/types)

| Example | Shows |
|---|---|
| [`types/enums.pel`](types/enums.pel) | `enum` with and without data, `switch` over variants with destructuring, and methods on an enum. |
| [`types/floats.pel`](types/floats.pel) | `float`, the sized `float32`/`float64`, and the soft-float types `float16`, `float128` and `float256`. |
| [`types/function_types.pel`](types/function_types.pel) | Function types, closures with `~>`, and the access marks in function types: `fn(int!)` takes `inout`, `fn(string!!)` takes `sink`. `x!` hands over a variable to change, `x!!` hands it over for good. |
| [`types/interfaces_generics.pel`](types/interfaces_generics.pel) | An `interface`, a generic function with a bound, and the `order` bound that `min`/`max` use. |
| [`types/objects.pel`](types/objects.pel) | `obj` with fields, inheritance written `:`, `open` and `override` for methods that subclasses change. |
| [`types/operators.pel`](types/operators.pel) | Operator overloading with `impl add for ...`, and equality derived for structs. |
| [`types/structs.pel`](types/structs.pel) | `struct` with methods, `inout self` to change a value in place (`c.bump!()`), and value semantics (`copy`). |
| [`types/wide_ints.pel`](types/wide_ints.pel) | 128 and 256 bit integers (`int128`, `uint128`, `int256`, `uint256`) with exact arithmetic that traps on overflow like every other integer, and the wrapping operators `+%`, `-%`, `*%`. |

### Braids

Docs: [braids](https://pelagolang.github.io/website/en-US/docs/guide/braids)

| Example | Shows |
|---|---|
| [`braids/basics.pel`](braids/basics.pel) | A braid is a fixed-size sequence of N slots whose types alternate: `(int, string; 4)` is int, string, int, string. The annotation makes a list a braid; the long spelling `braid<int, string; 4>` means the same. |
| [`braids/pairs_and_strands.pel`](braids/pairs_and_strands.pel) | Reading a braid as pairs, its two strands (every other slot), and `split`/`unbraid`/`swap`. |
| [`braids/zip_and_compare.pel`](braids/zip_and_compare.pel) | `braid.zip` weaves two lists into one braid and `unbraid` splits it back; braids compare, order and hash slot by slot, so they work in sets; and `[(A, B); N]` (N pairs) is a different type with the same memory. |

### Collections

Docs: [collections](https://pelagolang.github.io/website/en-US/docs/guide/collections)

| Example | Shows |
|---|---|
| [`collections/builders.pel`](collections/builders.pel) | Builders, the short way to make a list, set or map from another collection, with `of`, `if` and `~>`. |
| [`collections/list_patterns.pel`](collections/list_patterns.pel) | `switch` on the shape of a list: empty, one element, head and tail (`first, ...rest`). |
| [`collections/lists.pel`](collections/lists.pel) | Lists: literals, indexing, `first`/`last`, slicing, `push!`, `sortBy!`, searching and `retain!`. |
| [`collections/maps_sets.pel`](collections/maps_sets.pel) | `map` and `set`: literals (`{:}` is the empty map), `insert!`, `get` with `??`, iteration in insertion order. |

### Strings and regex

Docs: [core](https://pelagolang.github.io/website/en-US/docs/library/core), [regex](https://pelagolang.github.io/website/en-US/docs/library/std/data/regex)

| Example | Shows |
|---|---|
| [`strings/basics.pel`](strings/basics.pel) | Strings are UTF-8: `len` counts bytes, `charCount` counts characters; searching, trimming, case, replacing. |
| [`strings/regex.pel`](strings/regex.pel) | `std.regex`: compile a pattern (a `result`), then `isMatch`, `findAll`, capture groups and `replaceAll`. |
| [`strings/split_join_build.pel`](strings/split_join_build.pel) | `split`, `lines`, `join`, building a string with `pushStr!`, and parsing numbers with `parseInt` / `parseFloat`. |

### Errors, `option` and `result`

Docs: [errors](https://pelagolang.github.io/website/en-US/docs/guide/errors)

| Example | Shows |
|---|---|
| [`errors/custom_errors.pel`](errors/custom_errors.pel) | Your own error type (an `enum`), `?` converting between steps, and `switch` over the error cases. |
| [`errors/option.pel`](errors/option.pel) | No null. `T?` is an `option`: `none` or a value. `??` picks a default, `switch` and `is` take it apart. |
| [`errors/result.pel`](errors/result.pel) | No exceptions. A fallible function returns `T ! E` (a `result`), `ok(..)` / `err(..)` build one, `?` passes an error up, and `switch` takes it apart. |
| [`errors/stops.pel`](errors/stops.pel) | `checkedAdd` and friends return an `option` instead of stopping; an unchecked overflow is a stop, never silent wrap-around. `+%` wraps on purpose and `saturatingAdd` clamps. |

### Iterators

Docs: [core](https://pelagolang.github.io/website/en-US/docs/library/core)

| Example | Shows |
|---|---|
| [`iterators/adapters.pel`](iterators/adapters.pel) | Iterators: `map`, `filter`, `fold`, `zip`, `enumerate`, `take`, `skip`, `chain`, `reversed`, `min`/`max`, `sum`. |
| [`iterators/custom_iterator.pel`](iterators/custom_iterator.pel) | `iter<T>` values you build from a range with `.iter()`, passed to functions that take any iterator. |
| [`iterators/ranges_and_loops.pel`](iterators/ranges_and_loops.pel) | Ranges (`a..b` excludes `b`), `for x of`, `for i, x of` with an index, and iterating a string and a map. |

### Files, input and output

Docs: [io](https://pelagolang.github.io/website/en-US/docs/library/std/io)

| Example | Shows |
|---|---|
| [`files/errors.pel`](files/errors.pel) | A missing file is an `err`, never a crash, and the `io_error` says what went wrong. |
| [`files/read_write.pel`](files/read_write.pel) | `std.fs`: write a file, read it back, append, list a directory, ask about a file, and remove it again. Every call returns a `result` with an `io_error` and `?` passes it up. |
| [`files/streams.pel`](files/streams.pel) | `std.io`: `print` for standard output, `io.eprintln` for standard error, `io.readLine` for standard input (it returns `none` at the end of input), and `std.env` / `std.path` helpers. |

### Time and dates

Docs: [time](https://pelagolang.github.io/website/en-US/docs/library/std/time)

| Example | Shows |
|---|---|
| [`time/calendar_dates.pel`](time/calendar_dates.pel) | `std.calendar`: building dates (a `result`: February 30th is an error), weekday, ordinal day, adding months and days, leap years, and ISO weeks. |
| [`time/clocks.pel`](time/clocks.pel) | Clocks and timers: `now`, `sleep`, `stopwatch`. Times differ on every run, so only what must always hold is printed. |
| [`time/durations.pel`](time/durations.pel) | `std.time` durations: constructors, arithmetic, comparison, and the checked variants that return `none` instead of overflowing. |
| [`time/zones_and_formats.pel`](time/zones_and_formats.pel) | `std.zone` and `std.timefmt`: a moment in a fixed-offset zone, RFC 3339 and RFC 2822 text, a custom pattern, parsing it back, and a POSIX rule time zone (daylight saving time without a database). |

### Math and big numbers

Docs: [math](https://pelagolang.github.io/website/en-US/docs/library/core/math), [math](https://pelagolang.github.io/website/en-US/docs/library/std/math)

| Example | Shows |
|---|---|
| [`math/bigint.pel`](math/bigint.pel) | `std.big`: integers of any size. `big.parse` is a `result`; the operators work as on `int`. |
| [`math/functions.pel`](math/functions.pel) | The `math` helpers: `min`, `max`, `clamp`, `sqrt`, `floor`, `pow`, `gcd`, `lcm`, `isqrt`, and float tests. |

### Hashes, keys, ciphers and random numbers

Docs: [hashes](https://pelagolang.github.io/website/en-US/docs/library/std/hashes), [crypto](https://pelagolang.github.io/website/en-US/docs/library/std/crypto), [ciphers](https://pelagolang.github.io/website/en-US/docs/library/std/ciphers), [random](https://pelagolang.github.io/website/en-US/docs/library/std/random)

| Example | Shows |
|---|---|
| [`crypto/aead.pel`](crypto/aead.pel) | `std.aead` (ChaCha20-Poly1305): `seal` encrypts and authenticates, `open` returns `none` if anything, even one bit of the message or the extra data, was changed. |
| [`crypto/hashes.pel`](crypto/hashes.pel) | `std.sha2`, `std.sha3`, `std.blake3` and `std.checksum`: every hash has the same shape, `hash.digest(hasher, bytes)`, and `hash.hex` shows the bytes. Hashing in pieces gives the same answer as hashing at once. |
| [`crypto/mac_and_kdf.pel`](crypto/mac_and_kdf.pel) | `std.mac` (HMAC: sign and verify a message) and `std.kdf` (HKDF and PBKDF2: derive keys). |
| [`crypto/passwords.pel`](crypto/passwords.pel) | `std.password` and `std.bcrypt`: store a password as an encoded hash string and `verify` it later. The cost settings here are small so the example is quick; use larger ones for real passwords. |
| [`crypto/random_numbers.pel`](crypto/random_numbers.pel) | `std.random` (a seeded generator: the same seed gives the same numbers) and `std.csprng` (a secure generator that you can seed from the system, or from a key for tests). |

### JSON

Docs: [json](https://pelagolang.github.io/website/en-US/docs/library/std/data/json)

| Example | Shows |
|---|---|
| [`json/bignum_and_maps.pel`](json/bignum_and_maps.pel) | Derived JSON for `map<string, V>` fields, braid fields and the 128/256 bit integers, which keep every digit. |
| [`json/derive.pel`](json/derive.pel) | `@derive(toJson, fromJson)` writes the encoder and decoder for a struct or enum for you (`pointEncode`, `pointDecode`). Nested structs, lists, options, defaults and enums all work, and a decode error says where it went wrong. |
| [`json/parse_and_print.pel`](json/parse_and_print.pel) | `std.json`: parse text into a `json.value`, look inside with `get`, `at` and `size`, and write it back out compactly (`encode`) or indented (`pretty`). Bad input is an `err` with a position. |

### Concurrency

Docs: [concurrency](https://pelagolang.github.io/website/en-US/docs/guide/concurrency)

| Example | Shows |
|---|---|
| [`concurrency/channels.pel`](concurrency/channels.pel) | `chan<T>()` makes a sender and a receiver. One task sends, the main task calls `recv()` until it returns `none`, which happens when every sender is gone. |
| [`concurrency/lock.pel`](concurrency/lock.pel) | `lock<T>` is shared state that changes from several tasks one at a time: reach inside with `with`. Each task gets its own handle with `copy`. |
| [`concurrency/scope.pel`](concurrency/scope.pel) | `scope` runs tasks that borrow local variables and waits for all of them before the block ends, so two halves of a list can be summed in parallel. |
| [`concurrency/select.pel`](concurrency/select.pel) | `select` waits on several channels at once and runs the first case that is ready (`v` is what `recv()` returns, an `option`); `default` runs when nothing is ready. |
| [`concurrency/spawn_join.pel`](concurrency/spawn_join.pel) | `spawn` starts a task and returns a `task<T>`; `join!!()` waits for its result. A closure that outlives the function that made it gets what it uses moved in with `[sink x]`. |

### Modules

Docs: [modules](https://pelagolang.github.io/website/en-US/docs/guide/modules)

| Example | Shows |
|---|---|
| [`modules/imports/`](modules/imports/) | A file is a module and its file name is the module name. `import { a, b } = .name` brings names from a sibling file in. Run the directory: `pelago run modules/imports`, so the other files are found. |

### Small programs

Docs: [examples](https://pelagolang.github.io/website/en-US/docs/examples)

| Example | Shows |
|---|---|
| [`programs/bank.pel`](programs/bank.pel) | A small domain model: a struct with methods that change it (`inout self`), `result` errors from an enum, and `?` chaining the steps of a transfer. |
| [`programs/fizzbuzz.pel`](programs/fizzbuzz.pel) | The classic exercise with `switch` on a pair of remainders. |
| [`programs/primes.pel`](programs/primes.pel) | The sieve of Eratosthenes with a list of `bool`, `while` loops and a result that is easy to check. |
| [`programs/word_count.pel`](programs/word_count.pel) | A small program: split text into words, count them in a `map`, sort the entries and print the top ones. |

### A whole project

[`projects/rpn`](projects/rpn) is a complete little project on disk: a `pelago.yaml`, two modules, an `enum` with data, `result` errors passed up with `?`, and its own expected output. Run it with `pelago run projects/rpn`; see its [README](projects/rpn/README.md).

## Where the language is described

| | |
|---|---|
| [Guide](https://pelagolang.github.io/website/en-US/docs/guide/values) | Values, functions, types, collections, errors, modules, concurrency, ownership |
| [Library](https://pelagolang.github.io/website/en-US/docs/library) | `core` (always available) and `std` (import it), one page per type and module |
| [Reference](https://pelagolang.github.io/website/en-US/docs/reference/lexical) | Lexical rules, keywords, operators, declarations, semantics |
| [Tools](https://pelagolang.github.io/website/en-US/docs/tools/cli) | The command line, formatter, language server, `pelago.yaml`, targets |
| [`examples/tour.pel`](https://github.com/pelagolang/pelago/blob/main/examples/tour.pel) | One big file that shows the whole syntax; it is only parsed, not run |

## Editor setup

| Editor | How |
|---|---|
| VS Code | Install **Pelago** from the Visual Studio Marketplace: highlighting, snippets and the language server. The language server runs the `pelago` tool, so install it first and make sure it is on your `PATH` (or set `pelago.serverPath`). Source: [vscode-pelago](https://github.com/pelagolang/vscode-pelago). |
| Zed | [zed-pelago](https://github.com/pelagolang/zed-pelago) is not published yet; install it as a dev extension from a checkout. It needs `pelago` on your `PATH`. |
| Neovim, Helix | No extension yet. [tree-sitter-pelago](https://github.com/pelagolang/tree-sitter-pelago) has the grammar and `pelago lsp` speaks the language server protocol over stdio. |

See [Editors](https://pelagolang.github.io/website/en-US/docs/getting-started/editors) in the docs.

## A note on what the examples do not show yet

- `spawn`, channels, `scope`, `lock` and `select` run as tasks on one worker; the operating-system thread layer exists in the runtime but the scheduler does not spread tasks over several threads yet.
- A list is indexed from 0 upwards; indexing and slicing with negative numbers is for braids only (`o.first(-1)`).
- A function cannot return a closure that uses its surroundings; return a `box<fn ...>` instead.

## Licence

MIT OR Apache-2.0, at your option: see `LICENSE-MIT` and `LICENSE-APACHE`.
