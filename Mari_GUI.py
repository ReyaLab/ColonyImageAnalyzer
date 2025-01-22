# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 15:26:47 2025

@author: mchva


This is the Tkinter GUI for Mari's image analysis program

"""

import tkinter as tk
import os
import sys


file_list = ["",""]

max_colony_size = 0
min_colony_size = 0
circularity = 0
filename = ""
LQP_cutoff = 0
necrotic_px_std_cutoff = 0
necrotic_circ_min = 0
live_px_std_cutoff = 0
lowest_pix_max = 0

root = tk.Tk()
root.title("Reya Lab Image Analysis Software")
root.geometry("1250x200")  # Set the window size

try:
    root.iconbitmap("C:/Users/mchva/Desktop/Reya Lab/Data/Mari_image_Analysis_Jan2025/cell_icon.ico")
except:
    pass

label_size_min = tk.Label(root, text="Colony size minimum cutoff:")
label_size_min.grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_size_min = tk.Entry(root, width=30)
entry_size_min.grid(row=0, column=1, padx=10, pady=5)
entry_size_min.insert(0, "4000")

label_size_max = tk.Label(root, text="Colony size maximum cutoff:")
label_size_max.grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_size_max = tk.Entry(root, width=30)
entry_size_max.grid(row=1, column=1, padx=10, pady=5)
entry_size_max.insert(0, "60000")

label_circularity = tk.Label(root, text="Colony circularity cutoff:")
label_circularity.grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_circularity = tk.Entry(root, width=30)
entry_circularity.grid(row=2, column=1, padx=10, pady=5)
entry_circularity.insert(0, ".5")

label_nec_circ = tk.Label(root, text="Necrosis circularity cutoff:")
label_nec_circ.grid(row=0, column=2, padx=10, pady=5, sticky="w")
entry_nec_circ = tk.Entry(root, width=30)
entry_nec_circ.grid(row=0, column=3, padx=10, pady=5)
entry_nec_circ.insert(0, ".45")

label_col_LQP = tk.Label(root, text="Colony lowest quartile pixel cutoff:")
label_col_LQP.grid(row=1, column=2, padx=10, pady=5, sticky="w")
entry_col_LQP = tk.Entry(root, width=30)
entry_col_LQP.grid(row=1, column=3, padx=10, pady=5)
entry_col_LQP.insert(0, "125")

label_col_low_pix = tk.Label(root, text="Colony lowest pixel maximum:")
label_col_low_pix.grid(row=2, column=2, padx=10, pady=5, sticky="w")
entry_col_low_pix = tk.Entry(root, width=30)
entry_col_low_pix.grid(row=2, column=3, padx=10, pady=5)
entry_col_low_pix.insert(0, "65")

label_nec_std = tk.Label(root, text="Necrosis pixel standard dev > cutoff:")
label_nec_std.grid(row=0, column=4, padx=10, pady=5, sticky="w")
entry_nec_std = tk.Entry(root, width=30)
entry_nec_std.grid(row=0, column=5, padx=10, pady=5)
entry_nec_std.insert(0, "35")

label_live_std = tk.Label(root, text=" Colony pixel standard dev < cutoff:")
label_live_std.grid(row=1, column=4, padx=10, pady=5, sticky="w")
entry_live_std = tk.Entry(root, width=30)
entry_live_std.grid(row=1, column=5, padx=10, pady=5)
entry_live_std.insert(0, "14")

file_chosen = tk.StringVar(root) 
# Set the default value of the variable 
file_chosen.set("Select an Option") 

def checkbox_change():
    if (checkbox_var.get()):
        dropdown.config(state="disabled")
    else:
        dropdown.config(state="normal")
        
def on_entry_change(*args):
    if (entry_path.get() == "") or (entry_path.get() == "Enter image path"):  # Check if the entry box is filled
        label_hidden.config(text="Enter valid path.")
    else:
        try:
            global file_list
            file_list = os.listdir(entry_path.get())
            file_list = [x for x in file_list if x[-4::]==".tif"]
            if len(file_list) == 0:
                label_hidden.config(text="There are no .tif files in that folder.")
                return(0)
            else:
                label_hidden.config(text="")
            label_drop = tk.Label(root, text="Choose file:")
            label_drop.grid(row=4, column=0, padx=10, pady=5, sticky="w")
            frame = tk.Frame(root)
            global dropdown
            dropdown = tk.OptionMenu(frame, file_chosen, *file_list) 
            dropdown.pack(side="left", padx=5)
            global checkbox_var
            checkbox_var = tk.IntVar()
            global checkbox_all
            checkbox_all= tk.Checkbutton(frame, text='Do all',variable=checkbox_var, onvalue=True, offvalue=False, command=checkbox_change)
            checkbox_all.pack(side="right", padx=5)
            frame.grid(row=4, column=1, padx=5, pady=5)
        except:
            label_hidden.config(text="Enter valid path.")
        
entry_path_txt = tk.StringVar(value="Enter image path")
entry_path = tk.Entry(root, width=30, textvariable=entry_path_txt)
entry_path.grid(row=3, column=1, padx=10, pady=5)
entry_path_txt.trace_add("write", on_entry_change)



label_hidden = tk.Label(root, text="")
label_hidden.grid(row=5, column=0, padx=10, pady=5, sticky="w")

def run_analysis(maxc, minc, circ, filn, path, LQP_cut, nec_px_std_cut, nec_circ_min, live_px_std_cut, low_pix_max, do_all = False):
    sys.path.append(path)
    label_hidden.config(text="Initiated analysis.")
    import Mari_image_analyzer5 as MA
    if do_all == False:
        MA.main([maxc, minc, circ, path, filn, LQP_cut, nec_px_std_cut, nec_circ_min, live_px_std_cut, low_pix_max])
    else:
        for x in file_list:
            MA.main([maxc, minc, circ, path, x, LQP_cut, nec_px_std_cut, nec_circ_min, live_px_std_cut, low_pix_max])
       
def click_conf():
    if (entry_size_min.get() == "") or (entry_size_max.get() == "") or (entry_circularity.get() == ""):
        label_hidden.config(text="Please fix input.")
    elif (0<=int(entry_size_min.get())) and (int(entry_size_min.get())<int(entry_size_max.get())<1000000) and (0<= float(entry_circularity.get())<1.0) and ((file_chosen.get() in file_list) or (checkbox_var.get())):
        label_hidden.config(text="")
        max_colony_size = int(entry_size_max.get())
        min_colony_size = int(entry_size_min.get())
        circularity = float(entry_circularity.get())
        LQP_cutoff = int(entry_col_LQP.get())
        necrotic_px_std_cutoff = int(entry_nec_std.get())
        necrotic_circ_min = float(entry_nec_circ.get())
        live_px_std_cutoff = int(entry_live_std.get())
        lowest_pix_max = int(entry_col_low_pix.get())
        filename = file_chosen.get()
        run_analysis(max_colony_size, min_colony_size, circularity, filename, entry_path.get(), LQP_cutoff, necrotic_px_std_cutoff, necrotic_circ_min, live_px_std_cutoff, lowest_pix_max, do_all = checkbox_var.get())
        label_hidden.config(text="Finished analysis.")       
    else:
        label_hidden.config(text="Please fix input.")

btn_confirm = tk.Button(root, text = "Confirm parameters and analyze" , fg = "black", command=click_conf)
# Set Button Grid
btn_confirm.grid(row=5, column=1, padx=10, pady=5)

root.mainloop()