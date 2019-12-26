from classes.app import App

if __name__ == "__main__":

    try:
        app = App()
        app.run()
        
    except FileNotFoundError as error:

        from tkinter import Tk, messagebox

        Tk().withdraw()
        messagebox.showerror("FileNotFoundError", str(error))
