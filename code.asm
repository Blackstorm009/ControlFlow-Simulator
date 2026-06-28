;Microprogrammed Control Unit Simulation

org 100h

start:
    mov ax, 0000h
    mov bx, 0000h
    mov cx, 0004h    
    mov si, 0000h      ; si = current instruction number

FETCH:
    cmp cx, 0
    je DONE

    ; check which instruction we are on and jump to it
    cmp si, 0
    je DO_MEM_READ
    cmp si, 1
    je DO_ALU_ADD
    cmp si, 2
    je DO_ALU_SUB
    cmp si, 3
    je DO_HALT

NEXT:
    inc si             ; move to next instruction
    dec cx             ; one less instruction remaining
    jmp FETCH

; CONTROL SIGNALS

DO_MEM_READ:
    mov bx, 1234h
    jmp NEXT

DO_ALU_ADD:
    mov ax, 0005h
    mov bx, 0003h
    add ax, bx
    jmp NEXT

DO_ALU_SUB:
    mov ax, 0009h
    mov bx, 0004h
    sub ax, bx
    jmp NEXT

DO_HALT:
    mov ah, 4Ch
    int 21h

DONE:
    mov ah, 4Ch
    int 21h