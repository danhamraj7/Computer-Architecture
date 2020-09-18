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
JMP = 0b01010100    # Jump
JEQ = 0b01010101    # Jump - Equal
JNE = 0b01010110    # Jump - Not equal


"""ALU"""
ADD = 0b10100000    # Add
SUB = 0b10100001    # Subtract
MUL = 0b10100010    # Multiply
CMP = 0b10100111    # Compare

""" Bitwise"""
AND = 0b10101000    # AND
OR = 0b10101010     # OR
XOR = 0b10101011    # XOR
NOT = 0b01101001    # NOT
SHL = 0b10101100    # SHL -Shift bits left


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
        # flags: holds current flags status, change on operands given to the CMP,
        # 8 bits register, If a particular bit is set, that flag is "true".
        self.FL = [0] * 8
        # program counter
        # starts with 0
        # keeps track of where we are in memory  Stp #1
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
        self.branchtable[JMP] = self.JMP        # Jump
        self.branchtable[JEQ] = self.JEQ        # Jump - Equal
        self.branchtable[JNE] = self.JNE        # Jump - not equal

        self.branchtable[ADD] = self.ADD        # Add
        self.branchtable[SUB] = self.SUB        # Subtract
        self.branchtable[MUL] = self.MUL        # Multiply
        self.branchtable[CMP] = self.CMP        # Compare

        #                                       # bitwise
        self.branchtable[AND] = self.AND        # AND
        self.branchtable[OR] = self.OR          # OR
        self.branchtable[XOR] = self.XOR        # XOR
        self.branchtable[NOT] = self.NOT        # NOT
        self.branchtable[SHL] = self.SHL        # SHL - shift bits left

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

        # Compare the values in two registers.
        elif op == "CMP":
            # If equal, set E to true (1)
            if self.reg[reg_a] == self.reg[reg_b]:
                self.FL[-1] = 1
            # If a > b, set G to true (1)
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.FL[-2] = 1
            # If a < b, set L to true (1)
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.FL[-3] = 1
            # ********************************************
            elif op == "AND":
                self.reg[reg_a] &= self.reg[reg_b]
            elif op == "OR":
                self.reg[reg_a] |= self.reg[reg_b]
            elif op == "XOR":
                self.reg[reg_a] ^= self.reg[reg_b]
            elif op == "NOT":
                self.reg[reg_a] = ~(self.reg[reg_a])
            elif op == "SHL":
                self.reg[reg_a] = (self.reg[reg_a] << self.reg[reg_b])

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
        # Push return address on the stack
        ret_address = self.pc + 2
        # Decrement the stack pointer
        self.reg[7] -= 1
        self.ram[self.reg[7]] = ret_address
        # call the subroutine
        # Set the PC to the address stored in the given register
        reg_num = self.ram[self.pc + 1]
        subroutine_address = self.reg[reg_num]
        self.pc = subroutine_address

    # Pop the value from the top of the stack and store it in the PC
    def RET(self):
        # Pop the return addr off the stack
        ret_address = self.ram[self.reg[7]]
        # increment the stack pointer
        self.reg[7] += 1
        # Set the PC to the return address
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

    # Compare the values in two registers
    def CMP(self):
        # Set and store the  parameters in the  ram
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]
        # call the alu fn and pass in the parameters
        self.alu("CMP", reg_a, reg_b)
        # Increment the pc
        self.pc += 3

    # Set the PC to the address stored in the given register
    # Jump to the address stored in the given register.
    def JMP(self):
        # get the address from the memory
        memory_address = self.ram[self.pc + 1]
        # set the pc to the address
        self.pc = self.reg[memory_address]

    # If equal flag is set (true), jump to the address stored in the given register.
    def JEQ(self):
        # From the ALU if the flag is true
        if self.FL[-1] == 1:
            # Set the address to jump to
            address = self.ram[self.pc + 1]
            # set that address to that new address
            new_address = self.reg[address]
            # Now set the PC to the new address
            self.pc = new_address
        # If false, continue by incrementing the PC counter
        else:
            self.pc += 2

    # If E flag is clear (false, 0), jump to the address stored in the given register.
    def JNE(self):
        # From the ALU if the flag is False
        if self.FL[-1] == 0:
            # Set the address to jump to
            address = self.ram[self.pc + 1]
            # set that address to that new address
            new_address = self.reg[address]
            # Now set the PC to the new address
            self.pc = new_address
         # If false, continue by incrementing the PC counter
        else:
            self.pc += 2

        # ***********************************************
    # Bitwise-AND the values in registerA and registerB,
    # then store the result in registerA.
    def AND(self):
        # Set and store the parameters  in ram
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]
        # Call the ALU method and pass in the parameters
        self.alu("AND", reg_a, reg_b)
        # Increment the pc
        self.pc += 3

    # Perform a bitwise-OR between the values in registerA and registerB,
    # storing the result in registerA.
    def OR(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]
        self.alu("OR", reg_a, reg_b)
        self.pc += 3

    # Perform a bitwise-XOR between the values in registerA and registerB,
    # storing the result in registerA.
    def XOR(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]
        self.alu("XOR", reg_a, reg_b)
        self.pc += 3

    # Perform a bitwise-NOT on the value in a register,
    # storing the result in the register.
    def NOT(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]
        self.alu("NOT", reg_a, reg_b)
        self.pc += 3

    # Shift the value in registerA left by the number of bits specified in registerB
    # filling the low bits with 0
    def SHL(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]
        self.alu("SHL", reg_a, reg_b)
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
