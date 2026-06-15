import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox

def hitung_romberg():
    try:
        f_str = entry_f.get()
        calc_dict = {"np": np, "sin": np.sin, "cos": np.cos, "tan": np.tan, "exp": np.exp, "pi": np.pi, "log": np.log, "ln": np.log}
        a = float(eval(entry_a.get(), calc_dict))
        b = float(eval(entry_b.get(), calc_dict))
        n = int(entry_n.get())

        if n < 1 or n > 15:
            messagebox.showwarning("Peringatan", "Nilai n maksimal adalah 15 agar komputasi tetap stabil.")
            return
        
        def f(x): 
            return eval(f_str, {"x": x, "np": np, "sin": np.sin, "cos": np.cos, "tan": np.tan, "exp": np.exp, "pi": np.pi, "log": np.log, "ln": np.log})

        R = np.zeros((n, n))

        h = b - a
        R[0, 0] = (h / 2.0) * (f(a) + f(b))

        for k in range(1, n):
            h = (b - a) / (2**k)
            sum_f = sum(f(a + i * h) for i in range(1, 2**k, 2))
            R[k, 0] = 0.5 * R[k-1, 0] + sum_f * h

            for j in range(1, k + 1):
                R[k, j] = R[k, j-1] + (R[k, j-1] - R[k-1, j-1]) / ((4**j) - 1)

        for row in tree.get_children():
            tree.delete(row)
        
        cols = ["Iterasi"] + [f"O(h^{2*(i+1)})" for i in range(n)]
        tree["columns"] = cols
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=60 if c == "Iterasi" else 100, anchor="center")

        for k in range(n):
            row_data = [k + 1] + [f"{R[k, j]:.7f}" if j <= k else "" for j in range(n)]
            tree.insert("", "end", values=row_data)

        hasil_akhir = R[n-1, n-1]
        lbl_hasil.config(text=f"Hasil Integrasi: {hasil_akhir:.7f}")
        
        update_grafik(f, a, b, hasil_akhir)

    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan penulisan fungsi atau perhitungan:\n{e}")

def update_grafik(f, a, b, luas_area):
    ax.clear()
    
    margin = abs(b - a) * 0.2 if a != b else 1
    x_plt = np.linspace(a - margin, b + margin, 200)
    y_plt = [f(i) for i in x_plt]
    
    ax.plot(x_plt, y_plt, label="f(x)", color="royalblue", linewidth=2)
    ax.axhline(0, color='black', linestyle='--', linewidth=1)

    x_fill = np.linspace(a, b, 100)
    y_fill = [f(i) for i in x_fill]
    ax.fill_between(x_fill, y_fill, alpha=0.3, color="orange", label=f"Area ≈ {luas_area:.5f}")
    
    ax.axvline(a, color='red', linestyle=':', label=f"Batas a = {a}")
    ax.axvline(b, color='green', linestyle=':', label=f"Batas b = {b}")

    ax.set_title("Visualisasi Area Integrasi")
    ax.legend(loc="best", fontsize=9)
    canvas.draw()

root = tk.Tk()
root.title("Metode Integrasi Romberg")
root.geometry("1920x1080") 

frame_in = tk.Frame(root)
frame_in.pack(pady=10)

tk.Label(frame_in, text="f(x):").grid(row=0, column=0, padx=5)
entry_f = tk.Entry(frame_in, width=20) 
entry_f.grid(row=0, column=1) 
entry_f.insert(0, "4 / (1 + x**2)") 

tk.Label(frame_in, text="Batas a:").grid(row=0, column=2, padx=(15, 5))
entry_a = tk.Entry(frame_in, width=5) 
entry_a.grid(row=0, column=3) 
entry_a.insert(0, "0")

tk.Label(frame_in, text="Batas b:").grid(row=0, column=4, padx=(15, 5))
entry_b = tk.Entry(frame_in, width=5) 
entry_b.grid(row=0, column=5) 
entry_b.insert(0, "1")

tk.Label(frame_in, text="Orde (n):").grid(row=0, column=6, padx=(15, 5))
entry_n = tk.Entry(frame_in, width=5) 
entry_n.grid(row=0, column=7) 
entry_n.insert(0, "5")

tk.Button(frame_in, text="Hitung Integrasi", command=hitung_romberg, bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=8, padx=20)

lbl_hasil = tk.Label(root, text="Hasil Integrasi Terbaik: -", font=("Arial", 12, "bold"), fg="darkblue")
lbl_hasil.pack(pady=5)

frame_out = tk.Frame(root)
frame_out.pack(fill="both", expand=True, padx=10, pady=5)

frame_tabel_container = tk.LabelFrame(frame_out, text=" Tabel Ekstrapolasi Romberg ", width=1100)
frame_tabel_container.pack(side="left", fill="both", expand=False)
frame_tabel_container.grid_propagate(False)

tree_scroll = ttk.Scrollbar(frame_tabel_container, orient="horizontal")
tree = ttk.Treeview(frame_tabel_container, show="headings", xscrollcommand=tree_scroll.set)
tree_scroll.config(command=tree.xview)

tree.grid(row=0, column=0, sticky="nsew")
tree_scroll.grid(row=1, column=0, sticky="ew")

frame_tabel_container.grid_rowconfigure(0, weight=1)
frame_tabel_container.grid_columnconfigure(0, weight=1)

fig, ax = plt.subplots(figsize=(5, 4))
fig.tight_layout(pad=2.0)
canvas = FigureCanvasTkAgg(fig, master=frame_out)
canvas.get_tk_widget().pack(side="right", fill="both", expand=True, padx=(15, 0))

hitung_romberg()

root.mainloop()