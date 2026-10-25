import os
import shutil
import struct
import tkinter as tk
from tkinter import filedialog


# ============================================================
# MIPS Assembler
# CS 240 - Assignment 5
#
# Reads a MIPS .asm file and creates:
#
# Output/
#   FizzBuzz.asm
#   FizzBuzz.mhc-ascii
#   FizzBuzz.mhc-bin
#
# The Output folder is created next to THIS Python file.
# ============================================================


TEXT_BASE = 0x00400000
DATA_BASE = 0x10010000


registers = {
    "$zero": 0,
    "$at": 1,

    "$v0": 2,
    "$v1": 3,

    "$a0": 4,
    "$a1": 5,
    "$a2": 6,
    "$a3": 7,

    "$t0": 8,
    "$t1": 9,
    "$t2": 10,
    "$t3": 11,
    "$t4": 12,
    "$t5": 13,
    "$t6": 14,
    "$t7": 15,

    "$s0": 16,
    "$s1": 17,
    "$s2": 18,
    "$s3": 19,
    "$s4": 20,
    "$s5": 21,
    "$s6": 22,
    "$s7": 23,

    "$t8": 24,
    "$t9": 25,

    "$k0": 26,
    "$k1": 27,

    "$gp": 28,
    "$sp": 29,
    "$fp": 30,
    "$ra": 31
}


opcodes = {
    "addi": 8,
    "addiu": 9,
    "andi": 12,
    "ori": 13,
    "lui": 15,

    "lw": 35,
    "sw": 43,

    "beq": 4,
    "bne": 5,

    "j": 2,
    "jal": 3
}


function_codes = {
    "add": 32,
    "addu": 33,
    "sub": 34,
    "and": 36,
    "or": 37,
    "slt": 42,

    "jr": 8,
    "syscall": 12,

    "div": 26,
    "mfhi": 16
}


# ============================================================
# Helper functions
# ============================================================


def register_number(register):
    if register not in registers:
        raise ValueError("Unknown register: " + register)

    return registers[register]


def register_binary(register):
    return format(register_number(register), "05b")


def opcode_binary(opcode):
    return format(opcodes[opcode], "06b")


def function_binary(function):
    return format(function_codes[function], "06b")


def immediate_binary(value):
    if value < -32768 or value > 65535:
        raise ValueError(
            "Immediate value does not fit in 16 bits: "
            + str(value)
        )

    return format(value & 0xFFFF, "016b")


def remove_comment(line):
    if "#" in line:
        line = line[:line.index("#")]

    return line.strip()


def clean_instruction(line):
    return (
        line
        .replace(",", " ")
        .replace("(", " ")
        .replace(")", " ")
        .split()
    )


def parse_number(value):
    value = value.strip()

    # Character constant
    if (
        len(value) >= 3
        and value[0] == "'"
        and value[-1] == "'"
    ):
        character = value[1:-1]

        if character == "\\n":
            return 10
        elif character == "\\t":
            return 9
        elif character == "\\r":
            return 13
        elif character == "\\0":
            return 0

        return ord(character)

    # Hexadecimal
    if value.lower().startswith("0x"):
        return int(value, 16)

    # Normal decimal
    return int(value)


# ============================================================
# Pseudoinstructions
# ============================================================


def instruction_size(line):
    """
    Returns the number of REAL MIPS instructions generated
    by one assembly instruction.
    """

    parts = clean_instruction(line)

    if not parts:
        return 0

    instruction = parts[0].lower()

    # rem becomes:
    #
    # div rs, rt
    # mfhi rd
    #
    if instruction == "rem":
        return 3

    # bgt with an immediate becomes:
    #
    # addiu $at, $zero, immediate
    # slt   $at, $at, rs
    # bne   $at, $zero, label
    #
    if instruction == "bgt":
        return 3

    # la normally requires two instructions because
    # data is stored around 0x10010000
    if instruction == "la":
        return 2

    return 1


# ============================================================
# First pass
#
# Find all label addresses before generating machine code.
# ============================================================


def first_pass(lines):
    labels = {}

    section = None

    text_address = TEXT_BASE
    data_address = DATA_BASE

    for original_line in lines:

        line = remove_comment(original_line)

        if not line:
            continue

        # ----------------------------------------
        # Sections
        # ----------------------------------------

        if line == ".text":
            section = "text"
            continue

        if line == ".data":
            section = "data"
            continue

        if line.startswith(".globl"):
            continue

        # ----------------------------------------
        # Label
        # ----------------------------------------

        if ":" in line:
            label, remainder = line.split(":", 1)

            label = label.strip()
            remainder = remainder.strip()

            if section == "text":
                labels[label] = text_address

            elif section == "data":
                labels[label] = data_address

            if not remainder:
                continue

            line = remainder

        # ----------------------------------------
        # Data
        # ----------------------------------------

        if section == "data":

            if ".asciiz" in line:

                string_start = line.find('"')
                string_end = line.rfind('"')

                if string_start == -1 or string_end == -1:
                    raise ValueError(
                        "Invalid .asciiz directive: " + line
                    )

                text = line[string_start + 1:string_end]

                # Decode things like \n
                decoded = bytes(
                    text,
                    "utf-8"
                ).decode("unicode_escape")

                # +1 for null terminator
                data_address += len(
                    decoded.encode("utf-8")
                ) + 1

        # ----------------------------------------
        # Instructions
        # ----------------------------------------

        elif section == "text":

            count = instruction_size(line)

            text_address += count * 4

    return labels


# ============================================================
# Data assembler
# ============================================================


def assemble_data(lines):
    data = bytearray()

    section = None

    for original_line in lines:

        line = remove_comment(original_line)

        if not line:
            continue

        if line == ".data":
            section = "data"
            continue

        if line == ".text":
            section = "text"
            continue

        if section != "data":
            continue

        if ":" in line:
            label, remainder = line.split(":", 1)
            line = remainder.strip()

            if not line:
                continue

        if ".asciiz" in line:

            string_start = line.find('"')
            string_end = line.rfind('"')

            text = line[string_start + 1:string_end]

            decoded = bytes(
                text,
                "utf-8"
            ).decode("unicode_escape")

            data.extend(decoded.encode("utf-8"))

            # Null terminator
            data.append(0)

    return bytes(data)


# ============================================================
# Encode a real MIPS instruction
# ============================================================


def encode_instruction(
    instruction,
    parts,
    current_address,
    labels
):

    # ========================================================
    # R FORMAT
    # add rd, rs, rt
    # ========================================================

    if instruction in [
        "add",
        "addu",
        "sub",
        "and",
        "or",
        "slt"
    ]:

        rd = parts[1]
        rs = parts[2]
        rt = parts[3]

        opcode = 0
        shamt = 0
        funct = function_codes[instruction]

        machine = (
            (opcode << 26)
            | (register_number(rs) << 21)
            | (register_number(rt) << 16)
            | (register_number(rd) << 11)
            | (shamt << 6)
            | funct
        )

        return machine


    # ========================================================
    # DIV
    #
    # div rs, rt
    # ========================================================

    elif instruction == "div":

        rs = parts[1]
        rt = parts[2]

        machine = (
            (register_number(rs) << 21)
            | (register_number(rt) << 16)
            | function_codes["div"]
        )

        return machine


    # ========================================================
    # MFHI
    #
    # mfhi rd
    # ========================================================

    elif instruction == "mfhi":

        rd = parts[1]

        machine = (
            (register_number(rd) << 11)
            | function_codes["mfhi"]
        )

        return machine


    # ========================================================
    # JR
    #
    # jr rs
    # ========================================================

    elif instruction == "jr":

        rs = parts[1]

        machine = (
            (register_number(rs) << 21)
            | function_codes["jr"]
        )

        return machine


    # ========================================================
    # SYSCALL
    # ========================================================

    elif instruction == "syscall":

        return function_codes["syscall"]


    # ========================================================
    # ADDI / ADDIU / ANDI / ORI
    # ========================================================

    elif instruction in [
        "addi",
        "addiu",
        "andi",
        "ori"
    ]:

        rt = parts[1]
        rs = parts[2]

        immediate = parse_number(parts[3])

        machine = (
            (opcodes[instruction] << 26)
            | (register_number(rs) << 21)
            | (register_number(rt) << 16)
            | (immediate & 0xFFFF)
        )

        return machine


    # ========================================================
    # LUI
    #
    # lui rt, immediate
    # ========================================================

    elif instruction == "lui":

        rt = parts[1]

        immediate = parse_number(parts[2])

        machine = (
            (opcodes["lui"] << 26)
            | (register_number(rt) << 16)
            | (immediate & 0xFFFF)
        )

        return machine


    # ========================================================
    # LW / SW
    #
    # lw rt, offset(rs)
    # ========================================================

    elif instruction in ["lw", "sw"]:

        rt = parts[1]

        offset = parse_number(parts[2])

        rs = parts[3]

        machine = (
            (opcodes[instruction] << 26)
            | (register_number(rs) << 21)
            | (register_number(rt) << 16)
            | (offset & 0xFFFF)
        )

        return machine


    # ========================================================
    # BEQ / BNE
    # ========================================================

    elif instruction in ["beq", "bne"]:

        rs = parts[1]
        rt = parts[2]

        target = parts[3]

        if target in labels:

            target_address = labels[target]

            offset = (
                target_address
                - (current_address + 4)
            ) // 4

        else:
            offset = parse_number(target)

        machine = (
            (opcodes[instruction] << 26)
            | (register_number(rs) << 21)
            | (register_number(rt) << 16)
            | (offset & 0xFFFF)
        )

        return machine


    # ========================================================
    # J / JAL
    # ========================================================

    elif instruction in ["j", "jal"]:

        target = parts[1]

        if target in labels:
            address = labels[target]
        else:
            address = parse_number(target)

        if address % 4 != 0:
            raise ValueError(
                "Jump address is not word aligned: "
                + str(address)
            )

        target_field = (
            address >> 2
        ) & 0x03FFFFFF

        machine = (
            (opcodes[instruction] << 26)
            | target_field
        )

        return machine


    else:

        raise ValueError(
            "Unsupported instruction: "
            + instruction
        )


# ============================================================
# Expand pseudoinstructions
# ============================================================


def expand_instruction(
    line,
    current_address,
    labels
):

    parts = clean_instruction(line)

    instruction = parts[0].lower()

    results = []


    # ========================================================
    # LI
    #
    # li rt, immediate
    #
    # FizzBuzz only uses small immediate values, so this can
    # become addiu rt, $zero, immediate.
    # ========================================================

    if instruction == "li":

        rt = parts[1]

        immediate = parse_number(parts[2])

        new_parts = [
            "addiu",
            rt,
            "$zero",
            str(immediate)
        ]

        results.append(
            encode_instruction(
                "addiu",
                new_parts,
                current_address,
                labels
            )
        )


    # ========================================================
    # MOVE
    #
    # move rd, rs
    #
    # becomes:
    #
    # addu rd, rs, $zero
    # ========================================================

    elif instruction == "move":

        rd = parts[1]
        rs = parts[2]

        new_parts = [
            "addu",
            rd,
            rs,
            "$zero"
        ]

        results.append(
            encode_instruction(
                "addu",
                new_parts,
                current_address,
                labels
            )
        )


    # ========================================================
    # REM
    #
    # rem rd, rs, immediate
    #
    # For this FizzBuzz program:
    #
    # li   $at, immediate
    # div  rs, $at
    # mfhi rd
    #
    # However, to keep our first-pass size predictable,
    # we use an immediate loaded into $at.
    # ========================================================

    elif instruction == "rem":

        rd = parts[1]
        rs = parts[2]
        divisor = parts[3]

        # Load divisor into $at
        load_parts = [
            "addiu",
            "$at",
            "$zero",
            divisor
        ]

        results.append(
            encode_instruction(
                "addiu",
                load_parts,
                current_address,
                labels
            )
        )

        current_address += 4

        # div rs, $at
        div_parts = [
            "div",
            rs,
            "$at"
        ]

        results.append(
            encode_instruction(
                "div",
                div_parts,
                current_address,
                labels
            )
        )

        current_address += 4

        # mfhi rd
        mfhi_parts = [
            "mfhi",
            rd
        ]

        results.append(
            encode_instruction(
                "mfhi",
                mfhi_parts,
                current_address,
                labels
            )
        )


    # ========================================================
    # BGT
    #
    # bgt rs, immediate, label
    #
    # becomes:
    #
    # addiu $at, $zero, immediate
    # slt   $at, $at, rs
    # bne   $at, $zero, label
    # ========================================================

    elif instruction == "bgt":

        rs = parts[1]
        value = parts[2]
        label = parts[3]

        # Load immediate into $at
        load_parts = [
            "addiu",
            "$at",
            "$zero",
            value
        ]

        results.append(
            encode_instruction(
                "addiu",
                load_parts,
                current_address,
                labels
            )
        )

        current_address += 4

        # slt $at, $at, rs
        slt_parts = [
            "slt",
            "$at",
            "$at",
            rs
        ]

        results.append(
            encode_instruction(
                "slt",
                slt_parts,
                current_address,
                labels
            )
        )

        current_address += 4

        # bne $at, $zero, label
        branch_parts = [
            "bne",
            "$at",
            "$zero",
            label
        ]

        results.append(
            encode_instruction(
                "bne",
                branch_parts,
                current_address,
                labels
            )
        )


    # ========================================================
    # LA
    #
    # la rt, label
    #
    # becomes:
    #
    # lui rt, upper
    # ori rt, rt, lower
    # ========================================================

    elif instruction == "la":

        rt = parts[1]
        label = parts[2]

        if label not in labels:
            raise ValueError(
                "Unknown label: " + label
            )

        address = labels[label]

        upper = (address >> 16) & 0xFFFF
        lower = address & 0xFFFF

        lui_parts = [
            "lui",
            rt,
            str(upper)
        ]

        results.append(
            encode_instruction(
                "lui",
                lui_parts,
                current_address,
                labels
            )
        )

        current_address += 4

        ori_parts = [
            "ori",
            rt,
            rt,
            str(lower)
        ]

        results.append(
            encode_instruction(
                "ori",
                ori_parts,
                current_address,
                labels
            )
        )


    # ========================================================
    # NORMAL INSTRUCTION
    # ========================================================

    else:

        results.append(
            encode_instruction(
                instruction,
                parts,
                current_address,
                labels
            )
        )

    return results


# ============================================================
# Assemble text section
# ============================================================


def assemble_text(lines, labels):

    machine_code = []

    section = None

    current_address = TEXT_BASE

    for line_number, original_line in enumerate(
        lines,
        start=1
    ):

        line = remove_comment(original_line)

        if not line:
            continue

        if line == ".text":
            section = "text"
            continue

        if line == ".data":
            section = "data"
            continue

        if line.startswith(".globl"):
            continue

        if section != "text":
            continue

        # Remove label
        if ":" in line:

            label, remainder = line.split(":", 1)

            line = remainder.strip()

            if not line:
                continue

        try:

            instructions = expand_instruction(
                line,
                current_address,
                labels
            )

            for machine in instructions:

                machine_code.append(machine)

                current_address += 4

        except Exception as error:

            raise ValueError(
                "Error on line "
                + str(line_number)
                + ":\n"
                + original_line.strip()
                + "\n\n"
                + str(error)
            )

    return machine_code


# ============================================================
# Create ASCII output
# ============================================================


def create_ascii_output(
    machine_code,
    data
):

    lines = []

    lines.append("MHC1")
    lines.append(
        "TEXT_BASE 0x{:08X}".format(TEXT_BASE)
    )
    lines.append(
        "TEXT_SIZE {}".format(
            len(machine_code) * 4
        )
    )

    lines.append(
        "DATA_BASE 0x{:08X}".format(DATA_BASE)
    )

    lines.append(
        "DATA_SIZE {}".format(len(data))
    )

    lines.append("BYTE_ORDER BIG_ENDIAN")

    lines.append(".text")

    for instruction in machine_code:

        lines.append(
            format(instruction, "032b")
        )

    lines.append(".data")

    # Data is shown as groups of 8-bit binary bytes
    for byte in data:

        lines.append(
            format(byte, "08b")
        )

    return "\n".join(lines) + "\n"


# ============================================================
# Create binary output
# ============================================================


def create_binary_output(
    machine_code,
    data
):

    output = bytearray()

    # --------------------------------------------------------
    # Header
    #
    # MHC1
    # text size
    # data size
    #
    # This lets the disassembler know where text stops
    # and data begins.
    # --------------------------------------------------------

    output.extend(b"MHC1")

    output.extend(
        struct.pack(
            ">I",
            len(machine_code) * 4
        )
    )

    output.extend(
        struct.pack(
            ">I",
            len(data)
        )
    )

    # --------------------------------------------------------
    # Machine instructions
    # --------------------------------------------------------

    for instruction in machine_code:

        output.extend(
            struct.pack(
                ">I",
                instruction
            )
        )

    # --------------------------------------------------------
    # Data
    # --------------------------------------------------------

    output.extend(data)

    return bytes(output)


# ============================================================
# Main assembler
# ============================================================


def assemble_file(input_file):

    # --------------------------------------------------------
    # Read source file
    # --------------------------------------------------------

    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as file:

        lines = file.readlines()


    # --------------------------------------------------------
    # Assemble
    # --------------------------------------------------------

    labels = first_pass(lines)

    machine_code = assemble_text(
        lines,
        labels
    )

    data = assemble_data(lines)


    # --------------------------------------------------------
    # OUTPUT LOCATION
    #
    # Get the directory containing THIS Python file.
    # --------------------------------------------------------

    script_directory = os.path.dirname(
        os.path.abspath(__file__)
    )


    # --------------------------------------------------------
    # Create:
    #
    # Assignment 5 Assembler Project/
    #     mips_assembler.py
    #     Output/
    # --------------------------------------------------------

    output_folder = os.path.join(
        script_directory,
        "Output"
    )

    os.makedirs(
        output_folder,
        exist_ok=True
    )


    # --------------------------------------------------------
    # Get original filename
    # --------------------------------------------------------

    original_filename = os.path.basename(
        input_file
    )

    base_name = os.path.splitext(
        original_filename
    )[0]


    # --------------------------------------------------------
    # Output filenames
    # --------------------------------------------------------

    copied_source = os.path.join(
        output_folder,
        original_filename
    )

    ascii_file = os.path.join(
        output_folder,
        base_name + ".mhc-ascii"
    )

    binary_file = os.path.join(
        output_folder,
        base_name + ".mhc-bin"
    )


    # --------------------------------------------------------
    # Copy original ASM file
    # --------------------------------------------------------

    shutil.copy2(
        input_file,
        copied_source
    )


    # --------------------------------------------------------
    # Write ASCII machine-code file
    # --------------------------------------------------------

    ascii_contents = create_ascii_output(
        machine_code,
        data
    )

    with open(
        ascii_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            ascii_contents
        )


    # --------------------------------------------------------
    # Write binary machine-code file
    # --------------------------------------------------------

    binary_contents = create_binary_output(
        machine_code,
        data
    )

    with open(
        binary_file,
        "wb"
    ) as file:

        file.write(
            binary_contents
        )


    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    print()
    print("Assembly successful!")
    print()

    print(
        "Source:",
        input_file
    )

    print(
        "Output folder:",
        output_folder
    )

    print()

    print(
        "Instructions:",
        len(machine_code)
    )

    print(
        "Text bytes:",
        len(machine_code) * 4
    )

    print(
        "Data bytes:",
        len(data)
    )

    print(
        "Labels:",
        len(labels)
    )

    print()

    print("Created:")

    print(
        " ",
        copied_source
    )

    print(
        " ",
        ascii_file
    )

    print(
        " ",
        binary_file
    )


# ============================================================
# Select ASM file
# ============================================================


def select_file():

    root = tk.Tk()

    root.withdraw()

    filename = filedialog.askopenfilename(
        title="Select MIPS Assembly File",
        filetypes=[
            (
                "MIPS Assembly Files",
                "*.asm"
            ),
            (
                "All Files",
                "*.*"
            )
        ]
    )

    root.destroy()

    return filename


# ============================================================
# Program entry point
# ============================================================


def main():

    print(
        "MIPS Assembler - CS 240 Assignment 5"
    )

    print(
        "Select the MIPS .asm file to assemble."
    )

    input_file = select_file()

    if not input_file:

        print(
            "No file selected."
        )

        return

    try:

        assemble_file(
            input_file
        )

    except Exception as error:

        print()
        print("ASSEMBLY ERROR")
        print("--------------")
        print(error)


if __name__ == "__main__":
    main()