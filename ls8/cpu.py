"""CPU functionality."""

import sys

# optcode
LDI = 0b10000010    # Set value of a reg to an int
PRN = 0b01000111    # Print
HLT = 0b00000001    # Halt


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # 256 bytes memory
        self.ram = [0] * 256
        # 8 registers
        self.reg = [0] * 8
        # program counter
        # starts with 0
        # # keeps track of where we are in memory  Stp #1
        self.pc = 0
        self.running = True

        # set up branch table
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[HLT] = self.handle_HLT

        # stp 2 add RAM functions
     # takes the given address and reads and returns the value at that address.

    def ram_read(self, mar):
        return self.ram[mar]

    # takes the given address and writes the value at that given address
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def load(self):
        """Load a program into memory."""

        address = 0

        # If there are less than 2 arguments entered, return error
        if len(sys.argv) != 2:
            print("Usage: comp.py program_name")
            sys.exit(1)

        # Otherwise, go on with the load method
        try:
            with open(sys.argv[1]) as file:
                for line in file:
                    split_line = line.split("#")[0]
                    command = split_line.strip()
                    if command == "":
                        continue
                    instruction = int(command, 2)
                    self.ram[address] = instruction
                    address += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} file was not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    # Set the value of a register to an integer.
    def handle_LDI(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.reg[operand_a] = operand_b

    # Print to the console the decimal integer
    # value that is stored in the given register.
    def handle_PRN(self):
        reg_num = self.ram_read(self.pc + 1)
        print(self.reg[reg_num])

    # Halt the CPU (and exit the emulator).

    def handle_HLT(self):
        self.running = False

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while self.running:
            ir = self.ram_read(self.pc)
            self.branchtable[ir]()
            if ir == 0 or None:
                print(f"Unknown Instruction: {ir}")
                sys.exit()
