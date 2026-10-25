import os
import struct
import tkinter as tk
from tkinter import filedialog


# ============================================================
# MIPS Disassembler
# CS 240 - Assignment 5
#
# Reads either:
#   *.mhc-bin
#   *.mhc-ascii
#
# and reconstructs a MIPS assembly file.
#
# Output is written to:
#   Output/<name>_reconstructed.asm
#
# The Output folder is created next to THIS Python file.
# ============================================================


TEXT_BASE = 0x00400000
DATA_BASE = 0x10010000


register_names = {
    0: "$zero",
    1: "$at",
    2: "$v0",
    3: "$v1",
    4: "$a0",
    5: "$a1",
    6: "$a2",
    7: "$a3",
    8: "$t0",
    9: "$t1",
    10: "$t2",
    11: "$t3",
    12: "$t4",
    13: "$t5",
    14: "$t6",
    15: "$t7",
    16: "$s0",
    17: "$s1",
    18: "$s2",
    19: "$s3",
    20: "$s4",
    21: "$s5",
    22: "$s6",
    23: "$s7",
    24: "$t8",
    25: "$t9",
    26: "$k0",
    27: "$k1",
    28: "$gp",
    29: "$sp",
    30: "$fp",
    31: "$ra"
}


opcode_names = {
    8: "addi",
    9: "addiu",
    12: "andi",
    13: "ori",
    15: "lui",
    35: "lw",
    43: "sw",
    4: "beq",
    5: "bne",
    2: "j",
    3: "jal"
}


function_names = {
    32: "add",
    33: "addu",
    34: "sub",
    36: "and",
    37: "or",
    42: "slt",
    8: "jr",
    12: "syscall",
    26: "div",
    16: "mfhi"
}


def signed_16(value):
    if value & 0x8000:
        return value - 0x10000
    return value


def register_name(number):
    if number not in register_names:
        raise ValueError("Unknown register number: " + str(number))
    return register_names[number]


# ============================================================
# Read .mhc-bin
# ============================================================


def read_binary_file(filename):
    with open(filename, "rb") as file:
        raw = file.read()

    if len(raw) < 12:
        raise ValueError("Binary file is too short to contain an MHC1 header.")

    if raw[:4] != b"MHC1":
        raise ValueError("Binary file does not start with the MHC1 header.")

    text_size = struct.unpack(">I", raw[4:8])[0]
    data_size = struct.unpack(">I", raw[8:12])[0]

    if text_size % 4 != 0:
        raise ValueError("Text size is not divisible by 4.")

    expected_size = 12 + text_size + data_size

    if len(raw) != expected_size:
        raise ValueError(
            "File size does not match its header. "
            f"Expected {expected_size} bytes but found {len(raw)}."
        )

    text_bytes = raw[12:12 + text_size]
    data = raw[12 + text_size:]

    instructions = []

    for offset in range(0, len(text_bytes), 4):
        instructions.append(
            struct.unpack(">I", text_bytes[offset:offset + 4])[0]
        )

    return instructions, data


# ============================================================
# Read .mhc-ascii
# ============================================================


def read_ascii_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines()]

    lines = [line for line in lines if line != ""]

    if not lines or lines[0] != "MHC1":
        raise ValueError("ASCII file does not start with the MHC1 header.")

    text_base = TEXT_BASE
    data_base = DATA_BASE
    text_size = None
    data_size = None

    section = None
    instructions = []
    data = bytearray()

    for line in lines[1:]:
        if line.startswith("TEXT_BASE "):
            text_base = int(line.split()[1], 16)
            continue

        if line.startswith("TEXT_SIZE "):
            text_size = int(line.split()[1])
            continue

        if line.startswith("DATA_BASE "):
            data_base = int(line.split()[1], 16)
            continue

        if line.startswith("DATA_SIZE "):
            data_size = int(line.split()[1])
            continue

        if line.startswith("BYTE_ORDER "):
            continue

        if line == ".text":
            section = "text"
            continue

        if line == ".data":
            section = "data"
            continue

        if section == "text":
            if len(line) != 32 or any(bit not in "01" for bit in line):
                raise ValueError("Invalid 32-bit instruction: " + line)

            instructions.append(int(line, 2))

        elif section == "data":
            if len(line) != 8 or any(bit not in "01" for bit in line):
                raise ValueError("Invalid 8-bit data byte: " + line)

            data.append(int(line, 2))

    if text_base != TEXT_BASE:
        raise ValueError(
            f"This disassembler expects TEXT_BASE 0x{TEXT_BASE:08X}, "
            f"but the file uses 0x{text_base:08X}."
        )

    if data_base != DATA_BASE:
        raise ValueError(
            f"This disassembler expects DATA_BASE 0x{DATA_BASE:08X}, "
            f"but the file uses 0x{data_base:08X}."
        )

    if text_size is not None and text_size != len(instructions) * 4:
        raise ValueError("TEXT_SIZE does not match the number of instructions.")

    if data_size is not None and data_size != len(data):
        raise ValueError("DATA_SIZE does not match the number of data bytes.")

    return instructions, bytes(data)


# ============================================================
# Find addresses that need labels
# ============================================================


def find_code_labels(instructions):
    targets = set()

    for index, machine in enumerate(instructions):
        address = TEXT_BASE + index * 4

        opcode = (machine >> 26) & 0x3F

        if opcode in (4, 5):
            immediate = signed_16(machine & 0xFFFF)
            target = address + 4 + immediate * 4
            targets.add(target)

        elif opcode in (2, 3):
            field = machine & 0x03FFFFFF
            target = ((address + 4) & 0xF0000000) | (field << 2)
            targets.add(target)

    valid_addresses = {
        TEXT_BASE + index * 4
        for index in range(len(instructions))
    }

    labels = {}

    for target in sorted(targets):
        if target in valid_addresses:
            labels[target] = f"label_{target:08X}"

    return labels


# ============================================================
# Decode one instruction
# ============================================================


def decode_instruction(machine, address, code_labels, data_labels):
    opcode = (machine >> 26) & 0x3F

    rs_number = (machine >> 21) & 0x1F
    rt_number = (machine >> 16) & 0x1F
    rd_number = (machine >> 11) & 0x1F
    shamt = (machine >> 6) & 0x1F
    funct = machine & 0x3F
    immediate = machine & 0xFFFF

    rs = register_name(rs_number)
    rt = register_name(rt_number)
    rd = register_name(rd_number)

    # --------------------------------------------------------
    # R format
    # --------------------------------------------------------

    if opcode == 0:
        if machine == 0x0000000C:
            return "syscall"

        if funct in (32, 33, 34, 36, 37, 42):
            instruction = function_names[funct]
            return f"{instruction} {rd}, {rs}, {rt}"

        if funct == 26:
            return f"div {rs}, {rt}"

        if funct == 16:
            return f"mfhi {rd}"

        if funct == 8:
            return f"jr {rs}"

        raise ValueError(
            f"Unsupported R-format instruction 0x{machine:08X} "
            f"at 0x{address:08X}"
        )

    # --------------------------------------------------------
    # Immediate arithmetic
    # --------------------------------------------------------

    if opcode in (8, 9):
        instruction = opcode_names[opcode]
        value = signed_16(immediate)
        return f"{instruction} {rt}, {rs}, {value}"

    if opcode in (12, 13):
        instruction = opcode_names[opcode]
        return f"{instruction} {rt}, {rs}, {immediate}"

    if opcode == 15:
        return f"lui {rt}, {immediate}"

    # --------------------------------------------------------
    # Memory
    # --------------------------------------------------------

    if opcode in (35, 43):
        instruction = opcode_names[opcode]
        offset = signed_16(immediate)
        return f"{instruction} {rt}, {offset}({rs})"

    # --------------------------------------------------------
    # Branch
    # --------------------------------------------------------

    if opcode in (4, 5):
        instruction = opcode_names[opcode]
        offset = signed_16(immediate)

        target = address + 4 + offset * 4

        target_text = code_labels.get(
            target,
            str(offset)
        )

        return f"{instruction} {rs}, {rt}, {target_text}"

    # --------------------------------------------------------
    # Jump
    # --------------------------------------------------------

    if opcode in (2, 3):
        instruction = opcode_names[opcode]

        field = machine & 0x03FFFFFF

        target = (
            ((address + 4) & 0xF0000000)
            | (field << 2)
        )

        target_text = code_labels.get(
            target,
            f"0x{target:08X}"
        )

        return f"{instruction} {target_text}"

    raise ValueError(
        f"Unsupported opcode {opcode} in 0x{machine:08X} "
        f"at 0x{address:08X}"
    )


# ============================================================
# Reconstruct strings in the data section
# ============================================================


def reconstruct_data(data):
    entries = []
    labels = {}

    offset = 0
    string_number = 0

    while offset < len(data):
        end = data.find(b"\x00", offset)

        if end == -1:
            # If raw bytes remain that are not a null-terminated
            # string, preserve them as .byte values.
            raw = data[offset:]

            label = f"data_{string_number}"
            address = DATA_BASE + offset

            labels[address] = label

            byte_values = ", ".join(str(value) for value in raw)

            entries.append(
                (label, f".byte {byte_values}")
            )

            break

        raw_string = data[offset:end]

        label = f"data_{string_number}"
        address = DATA_BASE + offset

        labels[address] = label

        try:
            text = raw_string.decode("utf-8")
        except UnicodeDecodeError:
            byte_values = ", ".join(
                str(value)
                for value in data[offset:end + 1]
            )

            entries.append(
                (label, f".byte {byte_values}")
            )

            offset = end + 1
            string_number += 1
            continue

        escaped = (
            text
            .replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\n", "\\n")
            .replace("\t", "\\t")
            .replace("\r", "\\r")
        )

        entries.append(
            (label, f'.asciiz "{escaped}"')
        )

        offset = end + 1
        string_number += 1

    return entries, labels


# ============================================================
# Recognize assembler-generated LA pairs
#
# lui rt, upper
# ori rt, rt, lower
#
# and replace them with:
#
# la rt, data_N
#
# This is optional prettification. The machine instructions
# remain equivalent.
# ============================================================


def decode_program(instructions, data):
    code_labels = find_code_labels(instructions)
    data_entries, data_labels = reconstruct_data(data)

    decoded = []

    index = 0

    while index < len(instructions):
        address = TEXT_BASE + index * 4
        machine = instructions[index]

        # Check for the exact LUI/ORI sequence our assembler
        # generates for "la".
        opcode = (machine >> 26) & 0x3F

        if opcode == 15 and index + 1 < len(instructions):
            rt = (machine >> 16) & 0x1F
            upper = machine & 0xFFFF

            next_machine = instructions[index + 1]
            next_opcode = (next_machine >> 26) & 0x3F
            next_rs = (next_machine >> 21) & 0x1F
            next_rt = (next_machine >> 16) & 0x1F
            lower = next_machine & 0xFFFF

            if (
                next_opcode == 13
                and next_rs == rt
                and next_rt == rt
            ):
                full_address = (upper << 16) | lower

                if full_address in data_labels:
                    decoded.append(
                        (
                            address,
                            f"la {register_name(rt)}, "
                            f"{data_labels[full_address]}"
                        )
                    )

                    index += 2
                    continue

        decoded.append(
            (
                address,
                decode_instruction(
                    machine,
                    address,
                    code_labels,
                    data_labels
                )
            )
        )

        index += 1

    return decoded, code_labels, data_entries


# ============================================================
# Build reconstructed ASM file
# ============================================================


def build_assembly(instructions, data):
    decoded, code_labels, data_entries = decode_program(
        instructions,
        data
    )

    lines = []

    if data_entries:
        lines.append(".data")

        for label, directive in data_entries:
            lines.append(
                f"{label}: {directive}"
            )

        lines.append("")

    lines.append(".text")
    lines.append(".globl main")
    lines.append("")

    # The original label names are not stored in machine code.
    # Give the first instruction the conventional main label.
    if instructions:
        lines.append("main:")

    for address, instruction in decoded:
        if address != TEXT_BASE and address in code_labels:
            lines.append("")
            lines.append(code_labels[address] + ":")

        lines.append("    " + instruction)

    lines.append("")

    return "\n".join(lines)


# ============================================================
# Disassemble a file
# ============================================================


def disassemble_file(input_file):
    lower_name = input_file.lower()

    if lower_name.endswith(".mhc-bin"):
        instructions, data = read_binary_file(input_file)

    elif lower_name.endswith(".mhc-ascii"):
        instructions, data = read_ascii_file(input_file)

    else:
        raise ValueError(
            "Please select a .mhc-bin or .mhc-ascii file."
        )

    reconstructed = build_assembly(
        instructions,
        data
    )

    script_directory = os.path.dirname(
        os.path.abspath(__file__)
    )

    output_folder = os.path.join(
        script_directory,
        "Output"
    )

    os.makedirs(
        output_folder,
        exist_ok=True
    )

    filename = os.path.basename(input_file)

    if filename.lower().endswith(".mhc-ascii"):
        base_name = filename[:-10]
    elif filename.lower().endswith(".mhc-bin"):
        base_name = filename[:-8]
    else:
        base_name = os.path.splitext(filename)[0]

    output_file = os.path.join(
        output_folder,
        base_name + "_reconstructed.asm"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(reconstructed)

    print()
    print("Disassembly successful!")
    print()
    print("Input:", input_file)
    print("Output:", output_file)
    print()
    print("Instructions:", len(instructions))
    print("Text bytes:", len(instructions) * 4)
    print("Data bytes:", len(data))
    print()
    print(
        "Note: Original comments, label names, and "
        "pseudoinstruction spellings cannot be recovered "
        "from machine code."
    )

    return output_file


# ============================================================
# File picker
# ============================================================


def select_file():
    root = tk.Tk()
    root.withdraw()

    filename = filedialog.askopenfilename(
        title="Select MHC Machine-Code File",
        filetypes=[
            (
                "MHC Machine Code",
                "*.mhc-bin *.mhc-ascii"
            ),
            (
                "MHC Binary",
                "*.mhc-bin"
            ),
            (
                "MHC ASCII",
                "*.mhc-ascii"
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
# Main
# ============================================================


def main():
    print(
        "MIPS Disassembler - CS 240 Assignment 5"
    )

    print(
        "Select a .mhc-bin or .mhc-ascii file to disassemble."
    )

    input_file = select_file()

    if not input_file:
        print("No file selected.")
        return

    try:
        disassemble_file(input_file)

    except Exception as error:
        print()
        print("DISASSEMBLY ERROR")
        print("-----------------")
        print(error)


if __name__ == "__main__":
    main()
