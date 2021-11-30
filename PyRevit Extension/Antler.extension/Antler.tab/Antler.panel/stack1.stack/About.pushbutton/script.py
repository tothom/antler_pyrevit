from pyrevit import script

output = script.get_output()

print("Made by Thomas Holth, 2021")

output.print_html('''Source code on <a href="github.com/tothom/Antler">GitHub</a>''')

# print("\r\n")

output.print_html('''Icons by <a target="_blank" href="https://icons8.com">Icons8</a>''')
