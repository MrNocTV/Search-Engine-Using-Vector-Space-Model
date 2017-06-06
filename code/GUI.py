import tkinter as tk
import random

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # configuration
        self.title("Text Retrieval")
        self.geometry("900x675")
        self.resizable(False, False)

        # this container contains all the pages
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        # set this container to be a 1-cell table 
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        # these are pages that we want to navigate to
        self.frames = {}

        for F in (SearchPage, ResultPage, QueryPage): 
            # create page 
            frame = F(container, self)
            # append to frame list 
            self.frames[F] = frame 
            # put it into container
            # sticky to make it grow and fill the entire 'cell'
            frame.grid(row=0, column=0, sticky="news")
        
        # by default, move to search page
        self.show_frame(SearchPage)
    
    def show_frame(self, name):
        frame = self.frames[name]
        if name == SearchPage:
            frame.bind_again(self)
        frame.tkraise()

class SearchPage(tk.Frame):
    LARGE_FONT = ('Verdana', 23)

    def move_to_query_page(self, event, controller):
        self.search_entry.unbind('<Key>')
        controller.show_frame(QueryPage)

    def bind_again(self, controller, event=None):
        self.search_entry.icursor(0)
        self.search_entry.delete(0, tk.END)
        self.search_entry.bind("<Key>", lambda event, controller=controller: self.move_to_query_page(event, controller))


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background='#FAFAFA')
        self.search_entry = tk.Entry(self, width=30, font=SearchPage.LARGE_FONT)
        self.search_entry.configure(highlightbackground='gray')
        self.search_entry.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        
        self.search_entry.bind("<Key>", lambda event, controller=controller: self.move_to_query_page(event, controller))
        # button frame
        button_frame = tk.Frame(self, background='#FAFAFA')
        button_frame.place(relx=0.5, rely=0.49, anchor=tk.CENTER)
        search_button = tk.Button(button_frame, text='Text Search', width=15, pady=8, highlightthickness=0, bd=0)
        search_button.grid(row=0, column=0, padx=10)
        lucky_button = tk.Button(button_frame, text="I'm Feeling Lucky", width=15, pady=8,highlightthickness=0, bd=0)
        lucky_button.grid(row=0, column=1, padx=10)

        # footer frame 
        footer_frame = tk.Frame(self, height=33, width=900, background='#E0E0E0')
        footer_frame.place(relx=.0, rely=0.95)
        about_label = tk.Label(footer_frame, text='About', width=81, height=2, anchor='w', background='#E0E0E0')
        about_label.grid(row=0, column=0, columnspan=5)
        privacy_label = tk.Label(footer_frame, text='Privacy', width=10, background='#E0E0E0')
        privacy_label.grid(row=0, column=5)
        terms_label = tk.Label(footer_frame, text='Terms', width=10, background='#E0E0E0')
        terms_label.grid(row=0, column=6)
        settings_label = tk.Label(footer_frame, text='Settings', width=10, background='#E0E0E0')
        settings_label.grid(row=0, column=7)

class QueryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(background='#FAFAFA')
        label = tk.Label(self, text='Query Page')
        label.pack(pady=10, padx=10)
        
        back_button = tk.Button(self, text='Back',
                                command=lambda : controller.show_frame(SearchPage))
        back_button.pack()

class ResultPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Result Page')
        label.pack(pady=10, padx=10)

        back_button = tk.Button(self, text='Back',
                                command=lambda : controller.show_frame(SearchPage))
        back_button.pack()
    
if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()