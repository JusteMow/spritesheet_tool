import tkinter as tk
from tkinter import ttk

class ScrollableFrame(ttk.Frame):
    def __init__(self, parent, height=400):
        super().__init__(parent)

        self.canvas = tk.Canvas(self, height=height, highlightthickness=0, bg='#1e1e1e')
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel_global, add='+')

    def _on_mousewheel_global(self, event):
        widget_under_mouse = self.winfo_containing(event.x_root, event.y_root)

        if widget_under_mouse and widget_under_mouse.winfo_toplevel() == self.winfo_toplevel():
            frame = widget_under_mouse
            while frame:
                if isinstance(frame, ScrollableFrame):
                    canvas = frame.canvas
                    if canvas.winfo_height() < canvas.bbox("all")[3]:
                        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
                        return
                frame = frame.master

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('600x600')
    root.title("Nested Scrollable Panels Example")

    main_frame = ScrollableFrame(root, height=600)
    main_frame.pack(fill="both", expand=True)

    # Ajouter 18 boutons au premier niveau
    for i in range(18):
        ttk.Button(main_frame.scrollable_frame, text=f"Bouton niveau 1 - {i}").pack(pady=2)

    # Deuxième niveau imbriqué
    second_frame = ScrollableFrame(main_frame.scrollable_frame, height=300)
    second_frame.pack(fill="x", pady=10)

    for i in range(18):
        ttk.Button(second_frame.scrollable_frame, text=f"Bouton niveau 2 - {i}").pack(pady=2)

    # Troisième niveau imbriqué
    third_frame = ScrollableFrame(second_frame.scrollable_frame, height=300)
    third_frame.pack(fill="x", pady=10)

    for i in range(18):
        ttk.Button(third_frame.scrollable_frame, text=f"Bouton niveau 3 - {i}").pack(pady=2)

    # Quatrième niveau imbriqué
    fourth_frame = ScrollableFrame(third_frame.scrollable_frame, height=300)
    fourth_frame.pack(fill="x", pady=10)

    for i in range(18):
        ttk.Button(fourth_frame.scrollable_frame, text=f"Bouton niveau 4 - {i}").pack(pady=2)

    # Agrandir la hauteur totale pour simuler les 2000 pixels
    main_frame.scrollable_frame.update_idletasks()
    main_frame.canvas.configure(scrollregion=(0, 0, 0, 2000))

    root.mainloop()