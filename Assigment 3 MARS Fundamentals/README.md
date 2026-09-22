# Assignment 3: MARS Fundamentals

This repository contains three introductory MIPS assembly programs created and tested using the MARS MIPS simulator.

## Programs

### `HelloWorld.asm`

Prints:

```text
Hello World
```

### `SumOf100.asm`

Calculates the sum of all even integers from 1 through 100.

Expected output:

```text
2550
```

### `CountTo100.asm`

Uses a loop to print every integer from 1 through 100, with each integer on a separate line.

## Assignment Report

`Assignment_3_MARS_Fundamentals.pdf` contains:

* The source code for all three programs
* Verified program output
* A single-step register trace
* Explanations of changed registers
* Pseudo-instruction rewrites
* Normal and edge-case tests
* A reflection
* Sources and collaboration acknowledgments

## Running the Programs

1. Download and open the MARS MIPS simulator.
2. Open one `.asm` file.
3. Select **Run > Assemble**.
4. Check the Messages area for assembly errors.
5. Select **Run > Go** to execute the program.
6. View the result in the **Run I/O** area.

Each program contains its own `main` label, so the files should be assembled and executed individually.

## Register Usage

| Register | Purpose                                                                 |
| -------- | ----------------------------------------------------------------------- |
| `$t0`    | Current integer or loop counter                                         |
| `$t1`    | Running sum in `SumOf100.asm`                                           |
| `$v0`    | MARS syscall service number                                             |
| `$a0`    | Argument passed to a syscall                                            |
| `$at`    | Temporary register used by MARS when expanding some pseudo-instructions |

## Pseudo-Instructions

The programs use MIPS pseudo-instructions such as `li`, `la`, `move`, and `bgt`. Examples of equivalent real MIPS instructions are documented in the assignment PDF.

For example:

```asm
# Pseudo-instruction
li $t0, 1

# Real MIPS instruction
addiu $t0, $zero, 1
```

```asm
# Pseudo-instruction
move $a0, $t0

# Real MIPS instruction
addu $a0, $t0, $zero
```

## Files

```text
HelloWorld.asm
SumOf100.asm
CountTo100.asm
Assignment_3_MARS_Fundamentals.pdf
README.md
```

## Sources

* ZyBooks, Chapter 3
* [MIPS Instruction Set](https://www.dsi.unive.it/~gasparetto/materials/MIPS_Instruction_Set.pdf)
* [Tutorials Point: Assembly Loops](https://www.tutorialspoint.com/assembly_programming/assembly_loops.htm)
* [MARS Pseudo-Instruction Definitions](https://github.com/dpetersanderson/MARS/blob/main/PseudoOps.txt)
* [ChatGPT](https://chatgpt.com/)

## Collaboration Acknowledgment

I used ZyBooks Chapter 3, the MARS simulator, the MIPS instruction reference, and the Tutorials Point discussion of assembly loops while completing this assignment. I used ChatGPT to explain instructions, review loop boundaries, organize the assignment report, construct the register-trace table, and help draft the reflection. All three programs were assembled and executed successfully in MARS.

## Author

Ethan Brothers
