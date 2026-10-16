# Simple Fortran Compiler

A compiler for a subset of Fortran, written from scratch in Python. It translates Fortran source code into assembly for the **SaM** (Stack Abstract Machine) and runs the result on a bundled SaM virtual machine.

Built for the Compilers course of the B.Sc. in Computer Science at the Instituto Federal de Brasília (IFB).

## Highlights

- **Hand-written lexical analyzer** based on regular expressions, reporting the line of each invalid token.
- **Grammar defined as data** (44 productions). The project computes the **FIRST**, **FOLLOW** and **PREDICT** sets itself and verifies that the grammar is **LL(1)**.
- **Predictive recursive-descent parser**, with one function per nonterminal.
- **Semantic checks:** duplicate declarations, use of undeclared variables, and type tracking between `integer`, `real` and `logical`.
- **Code generation** to SaM assembly, picking integer or floating-point instructions (`ADD`/`ADDF`, `DIV`/`DIVF`, …) based on operand types. `if/else` and `do while` are compiled to labels and conditional jumps.
- **Stack virtual machine** that executes the generated code and writes an execution trace with the stack state after every instruction.

## Pipeline

```
source.f90 ──► Lexer ──► Token stream ──► LL(1) parser + semantic checks ──► SaM assembly (.sam) ──► SaM VM ──► execution trace (_result.txt)
                              ▲
              Grammar ──► FIRST / FOLLOW / PREDICT sets
```

## Supported language

| Feature | Syntax |
|---|---|
| Program | `program <name>` … `end program <name>` |
| Declarations | `integer :: x`, `real :: y`, `logical :: z` |
| Assignment | `x = <expression>` |
| Arithmetic | `+`, `-`, `*`, `/`, parentheses |
| Relational | `==`, `/=`, `>`, `<`, `>=`, `<=` |
| Logical | `.and.`, `.or.`, `.not.`, `.true.`, `.false.` |
| Conditional | `if ( <expr> ) then` … `[else` …`] endif` |
| Loop | `do while ( <expr> )` … `enddo` |
| Output | `print * , <variable>` |

### Grammar (simplified)

```
PROGRAM        → program identifier BODY end
BODY           → STATEMENT BODY | ε
STATEMENT      → DECLARATION | ASSIGNMENT | IF_STATEMENT | DO_LOOP | PRINT_STATEMENT
DECLARATION    → (integer | real | logical) :: identifier
ASSIGNMENT     → identifier = EXPRESSION
IF_STATEMENT   → if ( EXPRESSION ) BODY END_IF
END_IF         → else BODY endif | endif
DO_LOOP        → do while ( EXPRESSION ) BODY enddo
PRINT_STATEMENT→ print * , identifier
EXPRESSION     → TERM END_EXPRESSION
END_EXPRESSION → (+ | - | RELATIONAL_OPERATOR | LOGICAL_OPERATOR) TERM END_EXPRESSION | ε
TERM           → FACTOR END_TERM
END_TERM       → (* | /) FACTOR END_TERM | ε
FACTOR         → ( EXPRESSION ) | identifier | number | .true. | .false. | .not. FACTOR
```

## Usage

Requires Python 3.10+ and no external dependencies.

```bash
python3 fortran_compiler.py examples/math.f90 math.sam
```

This produces:

- `math.sam`: the generated SaM assembly;
- `math_result.txt`: the VM execution trace, including the values written by `print`.

Console messages are in Portuguese.

## Example

Input (`examples/math.f90`):

```fortran
program math
    integer :: a
    integer :: b
    integer :: c
    a = 5
    b = 10
    c = a + ( b / a )
    print * , c
end program math
```

Generated SaM assembly (`math.sam`):

```
PUSHIMM 0
ADDSP 1
// VAR a: integer, address = 1
ADDSP 1
// VAR b: integer, address = 2
ADDSP 1
// VAR c: integer, address = 3
PUSHIMM 5
STOREABS 1
PUSHIMM 10
STOREABS 2
PUSHABS 1
PUSHABS 2
PUSHABS 1
DIV
ADD
STOREABS 3
PUSHABS 3
WRITE
ADDSP -3
STOP
```

Excerpt from the execution trace (`math_result.txt`), where the program prints `7`:

```
WRITE
Escreve valor inteiro ou lógico
7
```

## Examples and error handling

The `examples/` folder includes valid programs and one program for each class of error:

| File | What it shows | Result |
|---|---|---|
| `math.f90` | Integer arithmetic with precedence | prints `7` |
| `mathf.f90` | Floating-point arithmetic (`real`) | prints `55.0` |
| `cond.f90` | `if` / `else` | prints `15`, then `10` |
| `loop.f90` | Two `do while` loops | prints `0` to `9`, then `0` to `10` in steps of 2 |
| `lexical_error.f90` | Invalid character | `Lexical error in line 7 : @` |
| `syntactic_error.f90` | `if` without parentheses | `Syntax error: Expected Token ( / Token Found identifier` |
| `invalid_declaration.f90` | Variable declared twice | `Error: Variable 'x' is already declared` |

## Project structure

| File | Responsibility |
|---|---|
| `fortran_compiler.py` | Entry point: runs the whole pipeline |
| `lexical_analyzer.py` | Tokenization with regular expressions |
| `grammar.py` | Grammar data structure (terminals, nonterminals, productions) |
| `derives_empty_string.py`, `first_operation.py`, `follow_operation.py`, `predict.py` | Computation of nullable, FIRST, FOLLOW and PREDICT sets |
| `ll1_check.py` | Checks that the grammar is LL(1) |
| `token_sequence.py` | Token stream with `peek` / `match` |
| `fortran.py` | Grammar definition, recursive-descent parser, semantic checks and code generation |
| `var_control.py` | Symbol table (names, types, addresses) |
| `file_control.py` | Writing the output assembly file |
| `vm_sam.py` | SaM virtual machine (extended version of [Simulador-SaM](https://github.com/vinyciussousa/Simulador-SaM) with floating-point and output instructions) |

## Known limitations

This is a teaching project and intentionally covers a small subset of Fortran:

- Tokens must be separated by spaces (`a = 5` works, `a=5` does not).
- Relational and logical operators share the precedence level of `+` and `-`, so mixed expressions should use parentheses.
- `print` accepts a single variable.
- No arrays, subroutines, functions or `do` loops with counters.
