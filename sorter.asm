#run in linux terminal by java -jar Mars4_5.jar nc filename.asm(take inputs from console)

#system calls by MARS simulator:
#http://courses.missouristate.edu/kenvollmar/mars/help/syscallhelp.html
.data
	next_line: .asciiz "\n"
	inp_statement: .asciiz "Enter No. of integers to be taken as input: "
	inp_int_statement: .asciiz "Enter starting address of inputs(in decimal format): "
	out_int_statement: .asciiz "Enter starting address of outputs (in decimal format): "
	enter_int: .asciiz "Enter the integer: "
	.eqv bytespace 4
.text
#input: N= how many numbers to sort should be entered from terminal. 
#It is stored in $t1
jal print_inp_statement	
jal input_int 
move $t1,$t4			

#input: X=The Starting address of input numbers (each 32bits) should be entered from
# terminal in decimal format. It is stored in $t2
jal print_inp_int_statement
jal input_int
move $t2,$t4

#input:Y= The Starting address of output numbers(each 32bits) should be entered
# from terminal in decimal. It is stored in $t3
jal print_out_int_statement
jal input_int
move $t3,$t4 

#input: The numbers to be sorted are now entered from terminal.
# They are stored in memory array whose starting address is given by $t2
move $t8,$t2
move $s7,$zero	#i = 0




loop1:  beq $s7,$t1,loop1end
	jal print_enter_int
	jal input_int
	sw $t4,0($t2)
	addi $t2,$t2,4
      	addi $s7,$s7,1
        j loop1      
loop1end: move $t2,$t8       
#############################################################
#Do not change any code above this line
#Occupied registers $t1,$t2,$t3. Don't use them in your sort function.
#############################################################
#function: should be written by students(sorting function)
#The below function adds 10 to the numbers. You have to replace this with
#your code
#move $s7,$zero #i=0
#add $s7, $zero, $zero   # Set $s7 to zero by adding $zero to itself
addu $s7,$0,$0  #i=0
sort: beq $s7,$t1,sortend #ending the sorting when main loop is done
    addu $t4,$0,$t2 #temporarily storing $t2's address
    addiu $s6,$0,1 #$s6 is 1 initially
    sort1: beq $s6,$t1,sort1end
        lw $s1,0($t4) #checking the first integer's value and the one right after that and comparing
        lw $s2,4($t4)
        slt $t5,$s2,$s1 #if first is larger than second, they swap
        beq $t5,$0,skip 
        sw $s2,0($t4)
        sw $s1,4($t4)
        skip: addi $t4,$t4,4
        addi $s6,$s6,1 #doing the swap for one integer until the end of the array
        j sort1
    sort1end: addi $s7,$s7,1 #i=i+1
    j sort    
sortend: addu $s7,$0,$0
addu $t9,$0,$t3
moveloop: beq $s7,$t1,moveend #function to store the input array sorted to output array
    lw $s1,0($t2)
    sw $s1,0($t3)
    addi $t2,$t2,4
    addi $t3,$t3,4
    addi $s7,$s7,1
    j moveloop
moveend: addu $t3,$0,$t9 #going back to start of output array
addu $t2,$0,$t8
#endfunction
#############################################################
#You need not change any code below this line

#print sorted numbers
l: move $s7,$zero	#i = 0
loop: beq $s7,$t1,end
      lw $t4,0($t3)
      jal print_int
      jal print_line
      addi $t3,$t3,4
      addi $s7,$s7,1
      j loop 
#end
end:  li $v0,10
      syscall
#input from command line(takes input and stores it in $t6)
input_int: li $v0,5
	   syscall
	   move $t4,$v0
	   jr $ra
#print integer(prints the value of $t6 )
print_int: li $v0,1	
	   move $a0,$t4
	   syscall
	   jr $ra
#print nextline
print_line:li $v0,4
	   la $a0,next_line
	   syscall
	   jr $ra

#print number of inputs statement
print_inp_statement: li $v0,4
		la $a0,inp_statement
		syscall 
		jr $ra
#print input address statement
print_inp_int_statement: li $v0,4
		la $a0,inp_int_statement
		syscall 
		jr $ra
#print output address statement
print_out_int_statement: li $v0,4
		la $a0,out_int_statement
		syscall 
		jr $ra
#print enter integer statement
print_enter_int: li $v0,4
		la $a0,enter_int
		syscall 
		jr $ra
