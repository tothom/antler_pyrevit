from rpw import revit
import os

def open_folder_in_explorer(path):
    print(path)
    folder = os.path.dirname(path)

    os.startfile(folder)


document_folder = revit.doc.PathName

open_folder_in_explorer(document_folder)