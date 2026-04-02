import tkinter as tk

def main():
    # Create the main window
    root = tk.Tk()
    root.title("Hello World App")
    root.geometry("300x150")
    
    # Create a label with "Hello World"
    label = tk.Label(
        root,
        text="Hello World",
        font=("Arial", 24),
        fg="blue"
    )
    label.pack(expand=True)
    
    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    main()
