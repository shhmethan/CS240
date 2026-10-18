asmLine = "    	lb $t1, 0($t1)"


registers = {
    "$zero": 0,
    "$t0": 8,
    "$t1": 9,
    "$t2": 10,
    "$s0": 16,
    "$s1": 17,
    "$s2": 18,
    "$s3": 19,
    "$sp": 29
}


opcodes = {
    "addi": 8,
    "andi": 12,
    "ori": 13,
    "lw": 35,
    "sw": 43,
    "beq": 4,
    "bne": 5
}


function_codes = {
    "add": 32,
    "sub": 34,
    "and": 36,
    "or": 37,
    "slt": 42
}


j_formats = {
    "j": 2,
    "jal": 3
}


def main():
    convert_binary(asmLine)


def register_binary(register):
    return format(registers[register], "05b")


def opcode_binary(opcode):
    return format(opcodes[opcode], "06b")


def jopcode_binary(opcode):
    return format(j_formats[opcode], "06b")


def function_binary(function):
    return format(function_codes[function], "06b")


def convert_binary(asm):
    parts = asm.replace(",", "").replace(")", "").replace("(", " ").split()

    instruction = parts[0]

    # R-format
    if instruction in function_codes:
        rd = parts[1]
        rs = parts[2]
        rt = parts[3]

        opcode = "000000"
        rs_binary = register_binary(rs)
        rt_binary = register_binary(rt)
        rd_binary = register_binary(rd)
        shamt = "00000"
        funct = function_binary(instruction)

        binary = opcode + rs_binary + rt_binary + rd_binary + shamt + funct

        print("Instruction:", asm)
        print("Format: R")
        print("Binary:", binary)
        print(f"Grouped: {opcode} {rs_binary} {rt_binary} "
              f"{rd_binary} {shamt} {funct}")

    # lw/sw format: instruction rt, offset(rs)
    elif instruction in ["lw", "sw"]:
        rt = parts[1]
        immediate = int(parts[2])
        rs = parts[3]

        opcode = opcode_binary(instruction)
        rs_binary = register_binary(rs)
        rt_binary = register_binary(rt)
        immediate_binary = format(immediate & 0xFFFF, "016b")

        binary = opcode + rs_binary + rt_binary + immediate_binary

        print("Instruction:", asm)
        print("Format: I")
        print("Binary:", binary)
        print(f"Grouped: {opcode} {rs_binary} {rt_binary} {immediate_binary}")

    # addi, andi, ori format: instruction rt, rs, immediate
    elif instruction in ["addi", "andi", "ori"]:
        rt = parts[1]
        rs = parts[2]
        immediate = int(parts[3])

        opcode = opcode_binary(instruction)
        rs_binary = register_binary(rs)
        rt_binary = register_binary(rt)
        immediate_binary = format(immediate & 0xFFFF, "016b")

        binary = opcode + rs_binary + rt_binary + immediate_binary

        print("Instruction:", asm)
        print("Format: I")
        print("Binary:", binary)
        print(f"Grouped: {opcode} {rs_binary} {rt_binary} {immediate_binary}")

    # J-format
    elif instruction in j_formats:
        opcode = jopcode_binary(instruction)
        address = int(parts[1])
        address_binary = format(address // 4, "026b")

        binary = opcode + address_binary

        print("Instruction:", asm)
        print("Format: J")
        print("Binary:", binary)
        print(f"Grouped: {opcode} {address_binary}")

    else:
        print("Unknown instruction:", instruction)


main()