import tkinter as tk

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
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

        for F in (SearchPage, ResultPage): 
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
        frame.tkraise()

class SearchPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Search Page')
        label.pack(pady=10, padx=10)

        search_button = tk.Button(self, text='Search', 
                                command=lambda : controller.show_frame(ResultPage))
        search_button.pack()

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