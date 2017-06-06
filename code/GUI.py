from time import sleep
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
    LARGE_FONT = ('Verdana', 21)

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
        # top frame: back button, entry, search button
        top_frame = tk.Frame(self, background='#FAFAFA')
        top_frame.place(relx=.01, rely=.01)
        back_button = tk.Button(top_frame, text='Back',
                                command=lambda : controller.show_frame(SearchPage))
        back_button.pack(side=tk.LEFT, padx=(0,10))
        back_button.configure(background='#FAFAFA', height=2)

        self.search_string = tk.StringVar()
        self.search_entry = tk.Entry(top_frame, width=40, textvariable=self.search_string, font=SearchPage.LARGE_FONT)
        self.search_entry.configure(highlightbackground='gray')
        self.search_entry.pack(side=tk.LEFT)
        search_button = tk.Button(top_frame, text='Search', command=None)
        search_button.configure(background='#FAFAFA', height=2)
        search_button.pack(side=tk.LEFT, padx=10)

        # result label 
        # invisible when there is no search yet 
        result_label = tk.Label(self, background='#FAFAFA', width=85, anchor='w', font=('Verdana', 13))
        result_label['text'] = 'About xxx results in xxx seconds'
        result_label.place(x=10, y=55)

        # create canvas with scrollbar
        canvas = tk.Canvas(self, width=880, height=550, background='#FAFAFA')
        canvas.place(x=10, y=90)
        scrollbar = tk.Scrollbar(self, command=canvas.yview)
        scrollbar.place(x=880, y=90, height=552)
        canvas.configure(yscrollcommand=scrollbar.set)
        frame = tk.Frame(canvas, background='#FAFAFA')
        canvas.create_window((0,0), window=frame, anchor='nw')
        def add_label(event):
            for i in range(5):
                label = tk.Label(frame, text='ASD', font=SearchPage.LARGE_FONT, background='#FAFAFA')
                label.pack()
            canvas.configure(scrollregion=canvas.bbox('all'))

        canvas.bind('<Button-1>', add_label)
        canvas.bind('<4>', lambda event: canvas.yview('scroll', -1, 'units'))
        canvas.bind('<5>', lambda event: canvas.yview('scroll', 1, 'units'))

        # change result page frame 
        self.change_page_frame = tk.Frame(self, background='#FAFAFA', width=700, height=20)
        self.change_page_frame.place(x=200, y=645)
        prev_page_button = tk.Button(self.change_page_frame, text='Back')
        prev_page_button.grid(row=0, column=0)
        for i in range(1,11):
            label = tk.Label(self.change_page_frame, text=str(i), anchor=tk.CENTER, width=1)
            if i == 1:
                label.configure(fg='red')
            label.configure(background='#FAFAFA', cursor='fleur')
            label.grid(row=0, column=i, padx=10)
        next_page_button = tk.Button(self.change_page_frame, text='Next')
        next_page_button.grid(row=0, column=11, padx=5)

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