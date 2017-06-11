# -*- coding: utf-8 -*-

from time import sleep
from VSM import connect_server, querying_and_ranking
from itertools import combinations
import tkinter as tk
import random
import time 
import string

db = connect_server()
cur = db.cursor()

def get_title_of_doc(doc):
    cur.execute('SELECT content from doc where title=%s', [doc])
    link_content = cur.fetchall()[0][0]
    title = open(link_content, encoding='utf16').readlines()[0].strip()
    return title

def get_link_of_doc(doc):
    cur.execute('SELECT content from doc where title=%s', [doc])
    link_content = cur.fetchall()[0][0]
    return link_content

def get_first_content_line(doc):
    cur.execute('SELECT content from doc where title=%s', [doc])
    link_content = cur.fetchall()[0][0]
    first_content_line = open(link_content, encoding='utf16').readlines()[2].strip()
    return first_content_line

def get_doc_content(doc):
    cur.execute('SELECT content from doc where title=%s', [doc])
    link_content = cur.fetchall()[0][0]
    return open(link_content, encoding='utf16').read().strip()

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
        controller.frames[QueryPage].reset()
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
        self.result_label = tk.Label(self, background='#FAFAFA', width=85, anchor='w', font=('Verdana', 13))
        self.result_label['text'] = ''
        self.result_label.place(x=10, y=55)

        # doc list result
        frame = tk.Frame(self,  background='#FAFAFA', bd=20)
        frame.place(x=-5, y=80)
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.doc_list = tk.Listbox(frame, width=66, height=21, font=('Verdana', 15))
        self.doc_list.pack()

        self.doc_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.doc_list.yview)

        # change/switch result page frame 
        change_page_frame = tk.Frame(self, background='#FAFAFA', width=700, height=20)
        change_page_frame.place(x=200, y=645)
        prev_page_button = tk.Button(change_page_frame, text='Back')
        prev_page_button.grid(row=0, column=0)
        labels = [None]
        for i in range(1,11):
            label = tk.Label(change_page_frame, text=str(i), anchor=tk.CENTER, width=1)
            labels.append(label)
            if i == 1:
                label.configure(fg='red')
            label.configure(background='#FAFAFA', cursor='fleur')
            label.grid(row=0, column=i, padx=10)
        next_page_button = tk.Button(change_page_frame, text='Next')
        next_page_button.grid(row=0, column=11, padx=5)

        # displaying logic code
        # after getting result from server 
        # we display the list of docs 10 item each time 
        # allow user to navigate between pages by clicking on 
        # prev and next button 
        # or directly on page's label  
        self.current_page = 1
        def move_to_page(page_num, event=None):
            if page_num < 1:
                page_num = 1
            elif page_num > 10:
                page_num = 10
            self.current_page = page_num
            self.doc_list.delete(0, tk.END)
            
            # add doc to list 
            for i in range((self.current_page-1)*10, (self.current_page-1)*10 + 10):
                if i >= len(self.results):
                    break
                self.doc_list.insert(tk.END, self.results[i][0] + " - " + get_title_of_doc(self.results[i][0]))
                self.doc_list.insert(tk.END, 'Link: ' + get_link_of_doc(self.results[i][0]))
                self.doc_list.insert(tk.END, get_first_content_line(self.results[i][0]))
                self.doc_list.insert(tk.END, '')
            
            # change font color to make it more readable 
            for i in range(40):
                if i % 4 == 0:
                    self.doc_list.itemconfig(i, fg="blue")
            # change label color of other pages to black and this page to red 
            for i in range(1, len(labels)):
                labels[i].config(fg='black')
            labels[page_num].config(fg='red')
            print(self.current_page)
            
        def move_next(event=None):
            move_to_page(self.current_page+1)
        next_page_button.configure(command=move_next)

        def move_back(event=None):
            move_to_page(self.current_page-1)
        prev_page_button.configure(command=move_back)
        
        # changing list content when clicking on page labels 
        for i in range(1, len(labels)):
            labels[i].bind('<Button-1>', lambda event, page=i: move_to_page(page))
        
        # after displaying all docs on the list 
        # we need to display content of the doc
        # when user click on doc's title
        def onselect(event=None):
            w = event.widget
            index = int(w.curselection()[0])
            if index % 4 == 0:
                print("Move to doc {}".format(index//4))
                real_index = ((self.current_page-1)*10 + index//4) 
                controller.frames[ResultPage].set_title(get_title_of_doc(self.results[real_index][0]))
                controller.frames[ResultPage].author = str(w.get(index+1))
                controller.frames[ResultPage].set_content(get_doc_content(self.results[real_index][0]), self.query)
                controller.frames[ResultPage].set_query(self.query)
                controller.frames[ResultPage].set_score(self.results[real_index][1])
                controller.frames[ResultPage].set_word_match(self.results[real_index][2])
                controller.show_frame(ResultPage)

        self.doc_list.bind('<<ListboxSelect>>', onselect)

        def querying(event=None):
            start = time.time()
            print(self.search_string.get())
            query = self.search_string.get()
            # get results as a list of doc 
            self.results, self.query = querying_and_ranking(query, cur)
            if self.results is None:
                return
            # calculate time taken 
            timestamp = time.time() - start 
            self.result_label['text'] = 'About {} results in {} seconds'.format(len(self.results), timestamp)
            # remove all results from the last query
            self.doc_list.delete(0, tk.END)
            # move to first page 
            move_to_page(1)

        self.search_entry.bind('<Return>', querying)
    
    def reset(self):
        self.search_string.set('')
        self.current_page = 1
        self.doc_list.delete(0, tk.END)
        self.result_label['text'] = ''     
        self.results = []   

class ResultPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background='#FAFAFA')
        back_button = tk.Button(self, text='Back',
                                command=lambda : controller.show_frame(QueryPage))
        back_button.config(bg='#FAFAFA')
        back_button.place(x=10, y=10)
        # title label 
        self.title_label = tk.Label(self, font=('Verdana', 15, 'bold'), text='Trương Văn Lộc', fg='blue')
        self.title_label.configure(background='#FAFAFA')
        self.title_label.place(x=70, y=10)

        # content frame 
        frame = tk.Frame(self, background='red')
        frame.place(x=10,y=55)
        self.content_string = ''
        self.content_text = tk.Text(frame, font=('Verdana', 12), wrap=tk.WORD, width=86, height=30)
        scrollbar = tk.Scrollbar(frame, width=10)
        self.content_text.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.content_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.content_text.pack()

        # information about result 
        self.word_match_label = tk.Label(self, text='word(s) match: ', background='#FAFAFA')
        self.word_match_label.place(x=10, y=650)
        self.score_label = tk.Label(self, text='score: ', background='#FAFAFA')
        self.score_label.place(x=200, y=650)

    def set_title(self, val):
        self.title_label['text'] = val 
    
    def set_content(self, val, query):
        self.content_text.delete(1.0, tk.END)
        self.content_text.insert(1.0, val)
        self.content_string = val 
        self.content_text.tag_remove('match', '1.0', tk.END)
        punctuation = string.punctuation + '”“… '
        pairs = list(combinations(punctuation, 2)) + [(' ', ' ')]
        punctuation = punctuation[::-1]
        pairs += list(combinations(punctuation, 2))
        for word in query:
            for x1, x2 in pairs:
                temp = x1 + word + x2
                start_pos = '1.0'
                while True:
                    start_pos = self.content_text.search(temp, start_pos, nocase=True, stopindex=tk.END)
                    if not start_pos:
                        break
                    end_pos = '{}+{}c'.format(start_pos, len(temp))
                    self.content_text.tag_add('match', start_pos, end_pos)
                    start_pos = end_pos
            self.content_text.tag_config('match', foreground='red', background='yellow')
            
    
    def set_query(self, val):
        self.query = val
    
    def set_word_match(self, val):
        self.word_match_label['text'] = 'word(s) match: {}'.format(val)
    
    def set_score(self, val):
        self.score_label['text'] = 'score: {}'.format(val)

if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()