import tkinter as tk

class EntryWithPrompt(tk.Entry):
    def __init__(self, master=None, prompt="", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.prompt = prompt
        self.default_fg = self['fg']  # Save default foreground color
        self.bind("<FocusIn>", self.handle_focus_in)
        self.bind("<FocusOut>", self.handle_focus_out)
        self.insert_prompt()

    def insert_prompt(self):
        self.insert(0, self.prompt)
        self['fg'] = 'grey'

    def handle_focus_in(self, event):
        if self.get() == self.prompt:
            self.delete(0, tk.END)
            self['fg'] = self.default_fg

    def handle_focus_out(self, event):
        if not self.get():
            self.insert_prompt()
            self['fg'] = 'grey'

# Example usage
root = tk.Tk()
root.geometry("300x200")

# Create an Entry with prompt text
entry = EntryWithPrompt(root, prompt="Enter text here...")
entry.pack(pady=20)

root.mainloop()
