addu $s7,$0,$0 
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
addu $t2,$0,$t8
