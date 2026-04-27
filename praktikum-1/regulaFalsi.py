import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox

def hitung_regula_falsi():
    try:
        f_str = entry_f.get()
        x1, x2 = float(entry_x1.get()), float(entry_x2.get())
        n = int(entry_n.get())

        def f(x): return eval(f_str, {"x": x, "np": np})

        if f(x1) * f(x2) >= 0:
            messagebox.showerror("Error", "f(x1) dan f(x2) harus beda tanda!")
            return

        for row in tree.get_children(): tree.delete(row)
        
        x1_awal, x2_awal = x1, x2
        history = []
        xr_old = 0

        for i in range(1, n + 1):
            fx1, fx2 = f(x1), f(x2)
            xr = x2 - (fx2 * (x1 - x2)) / (fx1 - fx2)
            fxr = f(xr)
            history.append((x1, x2, xr))
            err = abs((xr - xr_old) / xr) * 100 if i > 1 else 0
            tree.insert("", "end", values=(i, f"{x1:.4f}", f"{x2:.4f}", f"{xr:.6f}", f"{fxr:.6f}", f"{err:.4f}%"))

            if fx1 * fxr < 0: x2 = xr
            else: x1 = xr
            xr_old = xr

        lbl_hasil.config(text=f"Akar Ditemukan: {xr:.6f}")
        update_grafik(f, x1_awal, x2_awal, xr, history)

    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

def update_grafik(f, a, b, root_val, history):
    ax.clear()
    x_plt = np.linspace(a - 1, b + 1, 100)
    
    ax.plot(x_plt, [f(i) for i in x_plt], label="f(x)")
    ax.axhline(0, color='black', linestyle='--')
    
    for a_i, b_i, c_i in history:
        ax.plot([a_i, b_i], [f(a_i), f(b_i)], ':', color='gray')
        ax.scatter(c_i, 0, color='orange', s=15)

    ax.scatter(root_val, f(root_val), color='red', label="Akar")
    ax.legend()
    canvas.draw()

root = tk.Tk()
root.title("Metode Regula Falsi")

frame_in = tk.Frame(root)
frame_in.pack(pady=10)

tk.Label(frame_in, text="f(x):").grid(row=0, column=0)
entry_f = tk.Entry(frame_in, width=15); 
entry_f.grid(row=0, column=1); 
entry_f.insert(0, "(1 - 0.6*x)/x")

tk.Label(frame_in, text=" x1:").grid(row=0, column=2)
entry_x1 = tk.Entry(frame_in, width=5); 
entry_x1.grid(row=0, column=3); 
entry_x1.insert(0, "1")

tk.Label(frame_in, text=" x2:").grid(row=0, column=4)
entry_x2 = tk.Entry(frame_in, width=5); 
entry_x2.grid(row=0, column=5); 
entry_x2.insert(0, "2")

tk.Label(frame_in, text=" Iterasi:").grid(row=0, column=6)
entry_n = tk.Entry(frame_in, width=5); 
entry_n.grid(row=0, column=7); 
entry_n.insert(0, "5")

tk.Button(frame_in, text="Hitung", command=hitung_regula_falsi).grid(row=0, column=8, padx=10)

lbl_hasil = tk.Label(root, text="Akar: -", font=("Arial", 12, "bold"))
lbl_hasil.pack()

frame_out = tk.Frame(root)
frame_out.pack(fill="both", expand=True, padx=10, pady=10)

cols = ("Iter", "x1", "x2", "xr", "f(xr)", "Error")
tree = ttk.Treeview(frame_out, columns=cols, show="headings", height=10)
for c in cols: 
    tree.heading(c, text=c)
    tree.column(c, width=70, anchor="center")
tree.pack(side="left", fill="y")

fig, ax = plt.subplots(figsize=(5, 4))
canvas = FigureCanvasTkAgg(fig, master=frame_out)
canvas.get_tk_widget().pack(side="right", fill="both", expand=True)

root.mainloop()