"""CPU functionality."""

import sys


# optcode
LDI = 0b10000010    # Set value of a reg to an int
PRN = 0b01000111    # Print
HLT = 0b00000001    # Halt

PUSH = 0b01000101   # Push
POP = 0b01000110    # Pop

CALL = 0b01010000   # Call
RET = 0b00010001    # Return


"""ALU"""
ADD = 0b10100000    # Add
SUB = 0b10100001    # Subtract
MUL = 0b10100010    # Multiply


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # 256 bytes memory
        self.ram = [0] * 256
        # 8 registers
        self.reg = [0] * 8
        # Stack pointer
        self.reg[7] = 0xF4
        # program counter
        # starts with 0
        # # keeps track of where we are in memory  Stp #1
        self.pc = 0
        # start/stop the program
        self.running = False

        # Branch table
        self.branchtable = {}
        # Instruction branches
        self.branchtable[HLT] = self.HLT        # Halt
        self.branchtable[LDI] = self.LDI        # Set value of a reg to an int
        self.branchtable[PRN] = self.PRN        # Print
        self.branchtable[PUSH] = self.PUSH      # Push
        self.branchtable[POP] = self.POP        # Pop

        self.branchtable[CALL] = self.CALL      # Call
        self.branchtable[RET] = self.RET        # Return

        self.branchtable[ADD] = self.ADD        # Add
        self.branchtable[SUB] = self.SUB        # Subtract
        self.branchtable[MUL] = self.MUL        # Multiply

    def load(self):
        """Load a program into memory."""

        address = 0

        # If there are less than 2 arguments entered, return error
        if len(sys.argv) < 2:
            print("In correct amount of arguments")
            sys.exit(1)

        # load method
        try:
            # Open  file
            with open(sys.argv[1]) as file:
                # Loop through the file
                for line in file:
                    # Remove all white space
                    line = line.strip()
                    # Split into a temp file
                    temp = line.split()

                    # handle blank lines
                    if len(temp) == 0:
                        continue

                    # handle comments
                    if temp[0][0] == '#':
                        continue

                    # files are cleaned continue
                    try:
                        # Set the address of the ram
                        self.ram[address] = int(temp[0], 2)

                    # error handler
                    except ValueError:
                        print(f"Invalid number: {temp[0]}")
                        sys.exit(1)

                    # Increment the address by 1
                    address += 1

        # catch invalid file
        except FileNotFoundError:
            print(f"Could not open {sys.argv[1]}")
            sys.exit(2)

        # If the address is 0, return error and exit
        if address == 0:
            print("Program was not found")
            sys.exit(3)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        # Add the registers
        # store the result in registerA.
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        # Sub the registers
        # store the result in registerA.
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]

        # Multiply the registers
        # store the result in registerA.
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

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

    # takes the given address and reads and returns the value at that address.

    def ram_read(self, MAR):
        return self.reg[MAR]

    # takes the given address and writes the value at that given address
    def ram_write(self, MDR, MAR):
        self.reg[MAR] = MDR

    # Halt the CPU (and exit the emulator)

    def HLT(self):
        self.running = False

    # Set the value of a register to an integer
    def LDI(self):
        address = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2]
        self.ram_write(value, address)
        self.pc += 3

    # Print to the console the decimal integer
    # value that is stored in the given register.
    def PRN(self):
        address = self.ram[self.pc + 1]
        print(self.ram_read(address))
        self.pc += 2

    def PUSH(self):
        # Decrement the stack pointer
        self.reg[7] -= 1
        # Get the register num to push
        reg_num = self.ram[self.pc + 1]
        # get the value to push
        value = self.reg[reg_num]
        # copy the value to the sp addtess
        top_of_stack_address = self.reg[7]
        # Push the value from the register to the RAM
        self.ram[top_of_stack_address] = value
        # Increment the pc by 2 (2-bit operation)
        self.pc += 2

    def POP(self):
        # Point to the top of the stack
        top_of_stack_address = self.reg[7]
        # get the top of the stack address
        value = self.ram[top_of_stack_address]
        # get the reg to pop into
        reg_num = self.ram[self.pc + 1]
        # store the value at that register
        self.reg[reg_num] = value
        # Increment the stack pointer
        self.reg[7] += 1
        # Increment the pc
        self.pc += 2

    # Calls a subroutine (function) at the address stored in the register

    def CALL(self):
        # Push return address
        ret_address = self.pc + 2
        # Decrement the stack pointer
        self.reg[7] -= 1
        self.ram[self.reg[7]] = ret_address
        # Set the PC to the address stored in the given register
        reg_num = self.ram[self.pc + 1]
        subroutine_address = self.reg[reg_num]
        self.pc = subroutine_address

    # Pop the value from the top of the stack and store it in the PC

    def RET(self):
        # Pop the return addr off the stack
        ret_address = self.ram[self.reg[7]]
        self.reg[7] += 1
        # Set the PC to it
        self.pc = ret_address

    def ADD(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]
        self.alu("ADD", reg_a, reg_b)
        self.pc += 3

    def SUB(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]
        self.alu("SUB", reg_a, reg_b)
        self.pc += 3

    def MUL(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]
        self.alu("MUL", reg_a, reg_b)
        self.pc += 3

    def run(self):
        # program started
        self.running = True

        while self.running:
            # Read the memory address from the register's PC
            # store what is read in the ir (instruction register)
            ir = self.ram[self.pc]

            if ir and 0b00010000 == 0:
                self.pc += (ir >> 6) + 1
            else:
                # locate the ir methods from branchtable
                # run the method
                self.branchtable[ir]()
