import tkinter as tk

# CPU State
state_history = []

def init_state():
    return {
        'AX': 0x0000,
        'BX': 0x0000,
        'CX': 0x0004,
        'SI': 0x0000,
        'PC': 'FETCH',
        'step': 0,
        'instr': 'Press Next Step to begin',
        'active_signal': ''
    }

state = init_state()

instructions = ['DO_MEM_READ', 'DO_ALU_ADD', 'DO_ALU_SUB', 'DO_HALT']

# Save / Restore
def save_state():
    import copy
    state_history.append(copy.deepcopy(state))

def restore_state():
    global state
    if state_history:
        state = state_history.pop()
        update_ui()

# Next Step
def next_step():
    global state

    if state['PC'] == 'DONE':
        state['instr'] = 'Program Finished - INT 21h called'
        update_ui()
        return

    save_state()

    si = state['SI']
    cx = state['CX']

    # FETCH: cmp cx, 0 -> je DONE
    if cx == 0:
        state['PC'] = 'DONE'
        state['instr'] = 'FETCH: CX=0 -> JE DONE'
        state['active_signal'] = ''
        state['step'] += 1
        update_ui()
        return

    current = instructions[si]

    if current == 'DO_MEM_READ':
        state['BX'] = 0x1234
        state['instr'] = 'DO_MEM_READ: MOV BX, 1234h'
        state['active_signal'] = 'MEM_READ'

    elif current == 'DO_ALU_ADD':
        state['AX'] = 0x0005
        state['BX'] = 0x0003
        state['AX'] = state['AX'] + state['BX']
        state['instr'] = 'DO_ALU_ADD: MOV AX,0005h | MOV BX,0003h | ADD AX,BX -> AX=' + hex(state['AX'])
        state['active_signal'] = 'ALU_ADD'

    elif current == 'DO_ALU_SUB':
        state['AX'] = 0x0009
        state['BX'] = 0x0004
        state['AX'] = state['AX'] - state['BX']
        state['instr'] = 'DO_ALU_SUB: MOV AX,0009h | MOV BX,0004h | SUB AX,BX -> AX=' + hex(state['AX'])
        state['active_signal'] = 'ALU_SUB'

    elif current == 'DO_HALT':
        state['instr'] = 'DO_HALT: MOV AH,4Ch | INT 21h -> Program Halted'
        state['active_signal'] = 'HALT'
        state['PC'] = 'DONE'
        state['step'] += 1
        update_ui()
        return

    # NEXT: inc si, dec cx
    state['SI'] += 1
    state['CX'] -= 1
    state['step'] += 1
    update_ui()

# Update UI
def update_ui():
    s = state

    ax_label.config(text=f"AX = {hex(s['AX'])}")
    bx_label.config(text=f"BX = {hex(s['BX'])}")
    si_label.config(text=f"SI = {hex(s['SI'])}")
    cx_label.config(text=f"CX = {hex(s['CX'])}")
    pc_label.config(text=f"PC: {s['PC']}")
    instr_label.config(text=f"Step {s['step']}: {s['instr']}")

    for sig, lbl in signal_labels.items():
        if sig == s['active_signal']:
            lbl.config(bg='#00adb5', fg='white')
        else:
            lbl.config(bg='#2b2b3d', fg='#aaaaaa')

    log_box.insert(tk.END, f"Step {s['step']}: {s['instr']}\n")
    log_box.see(tk.END)

# Reset
def reset_sim():
    global state, state_history
    state = init_state()
    state_history = []
    log_box.delete('1.0', tk.END)
    for lbl in signal_labels.values():
        lbl.config(bg='#2b2b3d', fg='#aaaaaa')
    instr_label.config(text='Step 0: Press Next Step to begin')
    ax_label.config(text='AX = 0x0000')
    bx_label.config(text='BX = 0x0000')
    si_label.config(text='SI = 0x0000')
    cx_label.config(text='CX = 0x0004')
    pc_label.config(text='PC: FETCH')

# GUI

root = tk.Tk()
root.title('Microprogrammed Control Unit Simulator')
root.geometry('700x580')
root.configure(bg='#1e1e2f')

tk.Label(root, text='Microprogrammed Control Unit Simulator',
         font=('Arial', 15, 'bold'), bg='#1e1e2f', fg='white').pack(pady=8)
tk.Label(root, text=' Moez Ali [528915]  |  Haseeb Ahmed [512009]',
         font=('Arial', 10), bg='#1e1e2f', fg='#aaaaaa').pack()
tk.Label(root, text='org 100h  (COM file format)',
         font=('Consolas', 9), bg='#1e1e2f', fg='#555577').pack(pady=2)

pc_label = tk.Label(root, text='PC: FETCH', font=('Consolas', 11),
                    bg='#1e1e2f', fg='#ffcc00')
pc_label.pack(pady=4)

reg_frame = tk.Frame(root, bg='#1e1e2f')
reg_frame.pack(pady=6)

ax_label = tk.Label(reg_frame, text='AX = 0x0000', font=('Consolas', 12),
                    bg='#2b2b3d', fg='#00ffcc', width=16)
ax_label.grid(row=0, column=0, padx=5)

bx_label = tk.Label(reg_frame, text='BX = 0x0000', font=('Consolas', 12),
                    bg='#2b2b3d', fg='#00ffcc', width=16)
bx_label.grid(row=0, column=1, padx=5)

si_label = tk.Label(reg_frame, text='SI = 0x0000', font=('Consolas', 12),
                    bg='#2b2b3d', fg='#00ffcc', width=16)
si_label.grid(row=0, column=2, padx=5)

cx_label = tk.Label(reg_frame, text='CX = 0x0004', font=('Consolas', 12),
                    bg='#2b2b3d', fg='#00ffcc', width=16)
cx_label.grid(row=0, column=3, padx=5)

instr_label = tk.Label(root, text='Step 0: Press Next Step to begin',
                       font=('Consolas', 11), bg='#2b2b3d', fg='white',
                       width=70, height=2)
instr_label.pack(pady=8)

tk.Label(root, text='Control Signals', font=('Arial', 11, 'bold'),
         bg='#1e1e2f', fg='white').pack()

sig_frame = tk.Frame(root, bg='#1e1e2f')
sig_frame.pack(pady=6)

signal_labels = {}
for i, sig in enumerate(['MEM_READ', 'ALU_ADD', 'ALU_SUB', 'HALT']):
    lbl = tk.Label(sig_frame, text=sig, font=('Consolas', 11),
                   bg='#2b2b3d', fg='#aaaaaa', width=14, height=2)
    lbl.grid(row=0, column=i, padx=5)
    signal_labels[sig] = lbl

log_box = tk.Text(root, height=8, width=80, bg='#2b2b3d', fg='white',
                  font=('Consolas', 10))
log_box.pack(pady=8)

btn_frame = tk.Frame(root, bg='#1e1e2f')
btn_frame.pack()

tk.Button(btn_frame, text='Next Step', command=next_step,
          width=14, bg='#00adb5', fg='white').grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text='Prev Step', command=restore_state,
          width=14, bg='#ff5722', fg='white').grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text='Reset', command=reset_sim,
          width=14, bg='#4caf50', fg='white').grid(row=0, column=2, padx=5)

root.mainloop()