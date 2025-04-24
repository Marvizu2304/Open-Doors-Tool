from tkinter import Tk
from tkinter.filedialog import askopenfilename

def get_excel_file():
    Tk().withdraw()  # Oculta la ventana principal de Tk
    file_path = askopenfilename(
        title="Select the Excel file",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    return file_path
