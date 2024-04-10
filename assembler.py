# Define a dictionary for MIPS opcodes and registers
mips_functions = { #function binary values for these instructions
    "add": "100000",
    "addi": "001000",
    "addu": "100001"
}
mips_opcodes = { #opcode binary values for these instructions
    "add": "100000",
    "addi": "001000",
    "addu": "100001",
    "lw": "100011",
    "sw": "101011",
    "j": "000010",
    "jal": "000011",
    "beq": "000100",
    "addiu": "001001",
    "slt":"101010",
}

mips_registers = { #binary register numbers
    "$0" : "00000",
    "$zero":"00000",
    "$t0": "01000",
    "$t1": "01001",
    "$t2":"01010",
    "$t3":"01011",
    "$t4":"01100",
    "$t5":"01101",
    "$t6":"01110",
    "$t7":"01111",
    "$t8":"11000",
    "$t9":"11001",
    "$s0":"10000",
    "$s1":"10001",
    "$s2":"10010",
    "$s3":"10011",
    "$s4":"10100",
    "$s5":"10101",
    "$s6":"10110",
    "$s7":"10111",
}

mips_labels={ #binary values for the labels' addresses
    "sort":"00000100000000000000010100",
    "sort1":"00000100000000000000010111",
    "skip":"00010000000000000001111000",
    "sort1end":"00010000000000000010000100",
    "sortend":"00010000000000000010001100",
    "moveloop":"00010000000000000010010100",
    "moveend":"00010000000000000010110000",
}

ropcodes = ["slt", "add", "addu"] #list of r, i and j instructions
jopcodes = ["j","jal"]
iopcodes = ["beq","sw","lw","addiu","addi"]

def bino(wording,x): #function to convert integer to binary of x bits length
    if wording[0]=="$":
        wording=wording[1]
    wording2= bin(int((wording))).replace("0b",'')
    padded_num = str(wording2).rjust(x, '0')
    return padded_num
    
def functionj(word): #computing the binary equivalent instruction for a j format instruction
    if word[0] == "j" or word[0] == "jal":
        toprint = mips_opcodes[word[0]]     #opcode
        toprint+=mips_labels[word[1]]       #address of label
        #print(hex(int(toprint,2)),end='')
        print(toprint,end='')
        #print(mips_opcodes[word[0]],mips_labels[word[1]],sep='',end='')
        print()

def functioni(word): #computing the binary equivalent instruction for an i format instruction
    if word[0] == "beq":
        toprint = mips_opcodes[word[0]]     #opcode
        toprint+=(mips_registers[word[1]])     #rs
        toprint+=(mips_registers[word[2]])     #rt
        toprint+=(bino(str(label_line[word[3]]-i-1),16))
        #print(hex(int(toprint,2)),end='')
        print(toprint,end='')
    elif(word[0]=="addiu" or word[0] =="addi"):
        toprint = mips_opcodes[word[0]]     #opcode
        toprint+=(mips_registers[word[2]])  #rs
        toprint+=mips_registers[word[1]]    #rt
        toprint+=(bino(word[3],16))         #imm  
        #print(hex(int(toprint,2)),end='')
        print(toprint,end='')
    elif(word[0]=="lw" or word[0] =="sw"):
        toprint=mips_opcodes[word[0]]          #opcode
        toprint+=(mips_registers[word[3]])     #rs
        toprint+=(mips_registers[word[1]])     #rt
        toprint+=(bino(word[2],16))            #imm
        #print(hex(int(toprint,2)),end='')
        print(toprint,end='')
    print()
        
 
def functionr(word): #computing the binary equivalent instruction for a r format instruction
    if word[0] == "add" or word[0] == "addu":
        toprint="000000"                        #opcode
        toprint+=(mips_registers[word[2]])      #rt
        toprint+=(mips_registers[word[3]])      #rs
        toprint+=(mips_registers[word[1]])      #rd
        toprint+="00000"                        #shamt
        toprint+= mips_opcodes[word[0]]         #function
        #print(hex(int(toprint,2)),end='')
        print(toprint,end='')
    elif(word[0]=="slt"):
        toprint="000000"                        #function
        toprint+=(mips_registers[word[2]])      #rs
        toprint+=(mips_registers[word[3]])      #rt
        toprint+=(mips_registers[word[1]])      #rd
        toprint+="00000"                        #shamt
        toprint+= mips_opcodes[word[0]]         #opcode
        #print(hex(int(toprint,2)),end='')
        print(toprint,end='')
    print()



def rij(words): #function to determine whether an instruction is r, i or j format instruction
    #print(words)
    if(words[0] in ropcodes):
        functionr(words)
    elif(words[0] in iopcodes):
        functioni(words)
    elif(words[0] in jopcodes):
        functionj(words)

#mips code
code = '''addu $s7,$0,$0 
sort: beq $s7,$t1,sortend
    addu $t4,$0,$t2
    addiu $s6,$0,1
    sort1: beq $s6,$t1,sort1end
        lw $s1,0($t4)
        lw $s2,4($t4)
        slt $t5,$s2,$s1
        beq $t5,$0,skip
        sw $s2,0($t4)
        sw $s1,4($t4)
        skip: addi $t4,$t4,4
        addi $s6,$s6,1
        j sort1
    sort1end: addi $s7,$s7,1
    j sort    
sortend: addu $s7,$0,$0
addu $t9,$0,$t3
moveloop: beq $s7,$t1,moveend
    lw $s1,0($t2)
    sw $s1,0($t3)
    addi $t2,$t2,4
    addi $t3,$t3,4
    addi $s7,$s7,1
    j moveloop
moveend: addu $t3,$0,$t9
addu $t2,$0,$t8'''

code_lines = code.split('\n') #making lines out of the full code
code_spaces=[]
for i in code_lines:
    i=i.strip()
    i=i.strip("\t")
    i=i.replace(", ",",")
    i=i.replace(" ",",")
    i=i.replace("(",",")
    i=i.replace(")","")
    code_spaces.append(i.split(",")) #splitting each line into simpler elements to interpret

label_line={} #saving the line at which each label is in so that we can use it for the offset in beq instruction
for i in range(len(code_spaces)):
    if code_spaces[i][0][-1]==":":
        label_line[code_spaces[i][0].rstrip(":")]=i
        code_spaces[i].pop(0) #popping the label out of the instruction as we don't need it

for i in range(len(code_spaces)):
    first = code_spaces[i] #reading each line and starting to convert them to machine language
    rij (first)
#print(bino("$4"))