import json
import csv
import os
import tkinter as tk
from tkinter import filedialog

import datetime

root = tk.Tk()
root.withdraw()


file_path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])

print(file_path)

with open(file_path, mode='r') as file:
    json = json.load(file)

time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H-%M")
path, ext = os.path.splitext(file_path)
# file_path_new = "{} {}.{}".format(path, time_stamp, 'csv')
file_path_new = "{}.{}".format(path, 'csv')

# print(file_path_new)

with open(file_path_new, mode='w') as file:
    # fieldnames = next(iter(json.values())).keys()
    fieldnames = (json[0].keys())

    writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    writer.writerows(json)
