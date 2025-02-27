import tkinter as tk
from tkinter import ttk, messagebox
import random
from itertools import combinations

def generate_random_data():
    num_transactions = int(entry_num_rows.get())
    items = entry_custom_items.get().split(',') if entry_custom_items.get() else ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    transactions.clear()
    for i in range(1, num_transactions + 1):
        random_items = random.sample(items, random.randint(2, min(4, len(items))))
        transactions.append((i, set(random_items)))
    display_transactions()

def load_default_data():
    global transactions
    transactions = [(1, {'A', 'C', 'D'}),
                    (2, {'B', 'C', 'E'}),
                    (3, {'A', 'B', 'C', 'E'}),
                    (4, {'B', 'E'})]
    display_transactions()

def display_transactions():
    text_data.delete("1.0", tk.END)
    text_data.insert(tk.END, "Tid\tItems\n")
    for tid, items in transactions:
        text_data.insert(tk.END, f"{tid}\t{','.join(items)}\n")

def apriori_algorithm():
    if not transactions:
        messagebox.showerror("Lỗi", "Vui lòng nhập hoặc tạo dữ liệu trước!")
        return
    try:
        min_support = float(entry_minsup.get())
    except ValueError:
        messagebox.showerror("Lỗi", "Giá trị minsup không hợp lệ!")
        return
    
    min_count = min_support * len(transactions)
    
    def count_support(itemset):
        return sum(1 for _, t in transactions if itemset.issubset(t))
    
    item_counts = {}
    for _, transaction in transactions:
        for item in transaction:
            item_counts[item] = item_counts.get(item, 0) + 1
    
    L1 = {frozenset([item]) for item, count in item_counts.items() if count >= min_count}
    
    all_frequent_itemsets = L1.copy()
    Lk = L1
    k = 1
    
    while Lk:
        k += 1
        Ck_plus_1 = {a.union(b) for a in Lk for b in Lk if len(a.union(b)) == k}
        Lk_plus_1 = {itemset for itemset in Ck_plus_1 if count_support(itemset) >= min_count}
        if not Lk_plus_1:
            break
        all_frequent_itemsets.update(Lk_plus_1)
        Lk = Lk_plus_1
    
    text_result.delete("1.0", tk.END)
    text_result.insert(tk.END, "Tập phổ biến:\n")
    for itemset in sorted(all_frequent_itemsets, key=len):
        text_result.insert(tk.END, f"{set(itemset)} (support = {count_support(itemset) / len(transactions):.2f})\n")

def reset_data():
    transactions.clear()
    text_data.delete("1.0", tk.END)
    text_result.delete("1.0", tk.END)

root = tk.Tk()
root.title("Apriori Algorithm GUI")
transactions = []

frame_controls = tk.Frame(root)
frame_controls.pack(pady=10)

tk.Label(frame_controls, text="Số dòng:").grid(row=0, column=0)
entry_num_rows = tk.Entry(frame_controls, width=5)
entry_num_rows.grid(row=0, column=1)
entry_num_rows.insert(0, "4")

tk.Label(frame_controls, text="MinSup:").grid(row=0, column=2)
entry_minsup = tk.Entry(frame_controls, width=5)
entry_minsup.grid(row=0, column=3)
entry_minsup.insert(0, "0.5")

tk.Label(frame_controls, text="Dữ liệu tùy chỉnh:").grid(row=1, column=0, columnspan=2)
entry_custom_items = tk.Entry(frame_controls, width=30)
entry_custom_items.grid(row=1, column=2, columnspan=3)

btn_generate = tk.Button(frame_controls, text="Random", command=generate_random_data)
btn_generate.grid(row=0, column=4, padx=5)

btn_load_default = tk.Button(frame_controls, text="Dữ liệu gốc", command=load_default_data)
btn_load_default.grid(row=0, column=5, padx=5)

btn_solve = tk.Button(frame_controls, text="Bắt đầu giải", command=apriori_algorithm)
btn_solve.grid(row=0, column=6, padx=5)

btn_reset = tk.Button(frame_controls, text="Reset", command=reset_data)
btn_reset.grid(row=0, column=7, padx=5)

frame_data = tk.Frame(root)
frame_data.pack()

text_data = tk.Text(frame_data, height=8, width=40)
text_data.pack()

frame_result = tk.Frame(root)
frame_result.pack()

tk.Label(frame_result, text="Kết quả:").pack()
text_result = tk.Text(frame_result, height=10, width=40)
text_result.pack()

root.mainloop()
