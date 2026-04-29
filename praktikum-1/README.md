# Laporan Praktikum 1 Komputasi Numerik

|    NRP     |           Nama             |
| :--------: |       :------------:       |
| 5025251055 |   Aga Nafta Filadelfiano   |
| 5025251061 |     Bayu Setyo Nugroho     |
| 5025251067 |     Azka Fairus Syamsa     |

## Metode Regula Falsi
azka

## Cara Pengerjaan Metode Regula Falsi
azka

## Implementasi Algoritma Metode Regula Falsi (python)
[regulaFalsi.py](regulaFalsi.py)
```py
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
entry_f.insert(0, "x**2 + 5*x -3")

tk.Label(frame_in, text=" x1:").grid(row=0, column=2)
entry_x1 = tk.Entry(frame_in, width=5); 
entry_x1.grid(row=0, column=3); 
entry_x1.insert(0, "0")

tk.Label(frame_in, text=" x2:").grid(row=0, column=4)
entry_x2 = tk.Entry(frame_in, width=5); 
entry_x2.grid(row=0, column=5); 
entry_x2.insert(0, "1")

tk.Label(frame_in, text=" Iterasi:").grid(row=0, column=6)
entry_n = tk.Entry(frame_in, width=5); 
entry_n.grid(row=0, column=7); 
entry_n.insert(0, "10")

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
```

## Penjelasan Kode Program
bayu&aga
### 1. ...
### 2. ...
### 3. ...
### 4. ...
### 5. ...
### 6. ...
### 7. ...
### 8. ...
### 9. ...
### 10. ...

### Inisialisasi Jendela Utama
```py
root = tk.Tk()
root.title("Metode Regula Falsi")
root.geometry("750x500")
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=3)
root.grid_rowconfigure(5, weight=1)
```
- `tk.Tk()`: Membuat jendela utama aplikasi.
- title & geometry: Mengatur judul dan ukuran jendela.
- `grid_columnconfigure`: Mengatur perbandingan lebar kolom saat jendela ditarik atau diperbesar.

### Pengaturan Gaya (Styling)
```py
style = ttk.Style()
style.configure("Treeview", font=("Consolas", 9), rowheight=22)
style.configure("Treeview.Heading", font=("Consolas", 10, "bold"))
```
- `ttk.Style()`: Mengubah tampilan widget standar.
- `font=("Consolas", 9)`: Menggunakan font monospaced (Consolas).

### Panel Input Parameter
```py
tk.Label(root, text="f(x):").grid(row=0, column=0, sticky="w", padx=5)
input_fungsi = tk.Entry(root)
input_fungsi.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
input_fungsi.insert(0, "(1 - 0.6*x)/x")
```
- `tk.Label`: Menampilkan teks sebagai keterangan di sebelah kiri.
- `tk.Entry`: Kotak putih tempat user mengetikkan nilai.
- `.grid(...)`: Menempatkan widget menggunakan sistem koordinat row dan column.
- `sticky="ew"`: Membuat kotak input melebar mengikuti lebar kolom.
- `.insert(0, "...")`: Memberikan nilai default di dalam kotak.
- Kode ini berulang untuk x1, x2, dan Iterasi

### Tombol Eksekusi
```py
tk.Button(root, text="Hitung", command=regula_falsi)\
    .grid(row=4, column=0, columnspan=2, pady=10)
```
- `command=regula_falsi`: Menghubungkan tombol dengan fungsi logika regula_falsi yang sudah ada.
- `columnspan=2`: Membuat tombol berada di tengah-tengah dengan ruang dua kolom sekaligus.

### Tabel Hasil Iterasi (Treeview)
```py
columns = ("Iterasi", "xr", "f(xr)", "Error")
tree = ttk.Treeview(root, columns=columns, show="headings", height=8)
tree.heading("Iterasi", text="Iterasi")
tree.column("Iterasi", anchor="center", width=70)
```
- `ttk.Treeview`: Untuk membuat tabel.
- columns: Menampilkan judul kolom.
- `anchor="center"`: Membuat data angka di dalam tabel berada di posisi tengah.

### Scrollbar dan Label Hasil
```py
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
label_hasil = tk.Label(root, text="Akar ≈ -", font=("Arial", 12, "bold"))
```
- `ttk.Scrollbar`: Membuat fitur scrool bila iterasi yang ditampilkan sangat banyak.
- `label_hasil`: Menampilkan jawaban akhir.

### Penutup (Loop Utama)
```py
root.mainloop()
```
Bertujuan agar program terus berjalan untuk mendengarkan klik/input dari user.


## Screenshot Hasil Program 
### Polinomial
#### `f(x) = x^3 - x - 1`
`x1 = 1` `x2 = 2` `Iterasi = 20`
![Polinomial](screenshot/Polinomial.png)

### Eksponensial
#### `f(x) = e^x - 5x^2`
`x1 = 0` `x2 = 1` `Iterasi = 15`
![Eksponensial](screenshot/Eksponensial.png)

### Trigonometri
#### `f(x) = cos(x) - x`
`x1 = 0` `x2 = 1` `Iterasi = 10`
![Trigonometri](screenshot/Trigonometri.png)

### Logaritma Natural
#### `f(x) = xln(x) - 10`
`x1 = 1` `x2 = 10` `Iterasi = 10`
![LogaritmaNatural](screenshot/LogaritmaNatural.png)

### Kombinasi Akar
#### `f(x) = x^0.5 - cos(x)`
`x1 = 0.2` `x2 = 1` `Iterasi = 10`
![KombinasiAkar](screenshot/KombinasiAkar.png)