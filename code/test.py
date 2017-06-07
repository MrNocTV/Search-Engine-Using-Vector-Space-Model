import tkinter as tk


# def demo(master):
#     listbox = tk.Listbox(master)
#     listbox.pack(expand=1, fill="both")

#     # inserting some items
#     listbox.insert("end", "A list item")

#     for item in ["one", "two", "three", "four"]:
#         listbox.insert("end", item)

#     # this changes the background colour of the 2nd item
#     listbox.itemconfig(1, {'bg':'red'})

#     # this changes the font color of the 4th item
#     listbox.itemconfig(3, {'fg': 'blue'})

#     # another way to pass the colour
#     listbox.itemconfig(2, bg='green')
#     listbox.itemconfig(0, foreground="purple")

# if __name__ == "__main__":
#     root = tk.Tk()
#     demo(root)
#     root.mainloop()

from tkinter import *

def onclick():
   pass

root = Tk()
text = Text(root)
text.insert(INSERT, "Hello.....")
text.insert(END, "Bye Bye.....")
text.pack()

text.tag_add("here", "1.0", "1.4")
text.tag_add("start", "1.8", "1.13")
text.tag_config("here", background="yellow", foreground="blue")
text.tag_config("start", background="black", foreground="green")
root.mainloop()


from tkinter import *
import tkinter.filedialog
import tkinter.messagebox as tmb
import os

PROGRAM_NAME = "Footprint Editor"
file_name = None

root = Tk()
root.geometry('350x350')
root.title(PROGRAM_NAME)

def cut():
    content_text.event_generate('<<Cut>>')
    on_content_changed()
    return 'break'

def copy():
    content_text.event_generate('<<Copy>>')
    return 'break' # job's done, no more propagation

def paste():
    content_text.event_generate('<<Paste>>')
    on_content_changed()
    return 'break'

def undo():
    content_text.event_generate('<<Undo>>')
    on_content_changed()
    return 'break'

def redo(event=None):
    content_text.event_generate('<<Redo>>')
    on_content_changed()
    return 'break'

def select_all(event=None):
    content_text.tag_add('sel', 1.0, 'end')
    return 'break'

def find_text(event=None):
    search_toplevel = Toplevel(root)    # create a pop up window
    search_toplevel.title('Find Text')   # name the window 'Find Text'
    search_toplevel.transient(root) # make the search window appear on top of root
    search_toplevel.resizable(False, False)  # disable resize
    Label(search_toplevel, text='Find All:').grid(row=0, column=0, sticky='e')
    search_entry_widget = Entry(search_toplevel, width=25)
    search_entry_widget.grid(row=0, column = 1, sticky='we')
    search_entry_widget.focus_set() # set focus to this entry
    ignore_case_value = IntVar() # keep track of status of ignore_case
    Checkbutton(search_toplevel, text='Ignore Case', variable=ignore_case_value).grid(row=1, column=1, sticky='e')
    b = Button(search_toplevel, text='Find All', command=lambda: search_output(search_entry_widget.get(),
                                    ignore_case_value.get(), content_text, search_toplevel, search_entry_widget))
    b.grid(row=0, column=2, sticky='w'+'e')
    def close_search_window():
        content_text.tag_remove('match','1.0', END) # remove all the tags before closing the search window
        search_toplevel.destroy()  # explicitly close the search window
    search_toplevel.protocol('WM_DELETE_WINDOW', close_search_window) # override default close operation of search windows
    return 'break'

def search_output(pattern, if_ignore_case, content_text, search_toplevel, search_box):
    content_text.tag_remove('match', '1.0', END) # remove tag results of previous search
    matches_found = 0
    if pattern:  # if pattern is not empty
        start_pos = '1.0'
        while True:
            start_pos = content_text.search(pattern, start_pos, nocase=if_ignore_case, stopindex=END)
            if not start_pos: # if start_pos == None
                break
            end_pos = '{}+{}c'.format(start_pos, len(pattern)) # endpos = startpos + length of pattern
            content_text.tag_add('match', start_pos, end_pos) # add tag into content_text
            matches_found += 1
            start_pos = end_pos        # update start_pos
        content_text.tag_config('match', foreground='red', background='yellow') # change foreground & background color of match tag
    search_box.focus_set()   # set focus on search_box_entry again
    search_toplevel.title('{} matches found'.format(matches_found))  # print out result

def open_file(event=None):
    input_file_name = tkinter.filedialog.askopenfilename(defaultextension='.txt',
                                                     filetypes=[("All Files", "*"), ("Text Documents", "*.txt")])
    if input_file_name: # if input_file_name is not None
        global  file_name
        file_name = input_file_name # keep track of the file_name
        root.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME)) # just displaying the filename - PROGRAM_NAME
        content_text.delete(1.0, END) # remove the current content before inserting the content of new file
        with open(input_file_name) as _file:
            content_text.insert(1.0, _file.read()) # get text from file and insert into content_text
        on_content_changed()
    return 'break'

def save(event=None):
    global file_name
    if file_name:
        write_to_file(file_name)
    else:
        save_as()
    return 'break'

def save_as(event=None):
    input_file_name = tkinter.filedialog.asksaveasfilename(defaultextension='.txt',
                        filetypes=[("All Files", ".*"), ("Text Documents", "*.txt")])
    if input_file_name: # check if input_file_name is not None
        global file_name
        file_name = input_file_name # keep track of the file_name
        write_to_file(file_name)
        root.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME)) # change window title
    return 'break'

def write_to_file(file_name):
    try:
        content = content_text.get(1.0, END) # get text inside content_text
        with open(file_name, 'w') as _file:
            _file.write(content) # write text inside content_text to file
    except IOError:
        pass

def new_file(event=None):
    root.title('{} - {}'.format("Untitled", PROGRAM_NAME)) # set window title
    global file_name
    file_name = None # set file_name to None
    content_text.delete(1.0, END) # remove the content in content_text
    on_content_changed()
    return 'break'

def display_about_messagebox(event=None):
    tmb.showinfo("About", "{}{}".format(PROGRAM_NAME, "\nTkinter GUI Application\n "
                                                      "Development Blueprints"))
    return 'break'

def display_help_messagebox(event=None):
    tmb.showinfo("Help", "Help Book: \nTkinter GUI Application\n Development Blueprints", icon='question')
    return 'break'

def exit_editor(event=None):
    if tmb.askokcancel('Quit?', 'Really Quit?'): # using messagebox to ask user do they really want to quit
        root.destroy()
    return 'break'

def on_content_changed(event=None):
    update_line_numbers()
    update_cursor_info_bar()

def get_line_numbers():
    output = ''
    if show_line_no.get():
        row, col = content_text.index("end").split(".") # calculate the last line and column in the text
                                                        # 1.0 is row 1, column 0
        print(row, col)
        for i in range(1, int(row)):
            output += str(i) + '\n'
    return output

def update_line_numbers(event=None):
    line_numbers = get_line_numbers()
    line_number_bar.config(state='normal') # allow changing content inside line_number_bar
    line_number_bar.delete('1.0', 'end') # remove the old content
    line_number_bar.insert('1.0', line_numbers) # insert new line_numbers
    line_number_bar.config(state='disable') # disallow changing content inside line_number_bar

def show_cursor_info_bar():
    show_curso_info_checked = show_cursor_info.get()
    if show_curso_info_checked:
        cursor_info_bar.pack(expand='no', fill=None, side='right', anchor='se')
    else:
        cursor_info_bar.pack_forget()

def update_cursor_info_bar(event=None):
    row, col = content_text.index(INSERT).split('.') # get current position of row, col
    line_num, col_num = str(int(row)), str(int(col)+1)
    infotext = "Line: {0} | Column: {1}".format(line_num, col_num)
    cursor_info_bar.config(text=infotext)

def highlight_line(interval=100):
    content_text.tag_remove('active_line', 1.0, 'end')
    content_text.tag_add("active_line", "insert linestart",
                         "insert lineend+1c")
    content_text.after(interval, toggle_highlight)

def undo_highlight(event=None):
    content_text.tag_remove('active_line', 1.0, 'end')

def toggle_highlight(event=None):
    if to_highlight_line.get():
        highlight_line()
    else:
        undo_highlight()

def change_theme(event=None):
    selected_theme = theme_choice.get()
    fg_bg_colors = color_schemes.get(selected_theme)
    fg_color, bg_color = fg_bg_colors.split(".")
    content_text.config(background=bg_color, foreground=fg_color)

def show_popup_menu(event=None):
    popup_menu.tk_popup(event.x_root, event.y_root)
    return 'break'

# getting icons ready
new_file_icon = PhotoImage(file='new_file.gif')
open_file_icon = PhotoImage(file='open_file.gif')
save_file_icon = PhotoImage(file='save.gif')
cut_icon = PhotoImage(file='cut.gif')
copy_icon = PhotoImage(file='copy.gif')
undo_icon = PhotoImage(file='undo.gif')
paste_icon = PhotoImage(file='paste.gif')
redo_icon = PhotoImage(file='redo.gif')
find_text_icon = PhotoImage(file='find_text.gif')

#create the menu bar
menu_bar = Menu(root)

#create file menu
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='New', accelerator='Ctrl+N', image=new_file_icon, compound='left', command=new_file)
file_menu.add_command(label='Open', accelerator='Ctrl+O', image=open_file_icon, compound='left', command=open_file)
file_menu.add_command(label='Save', accelerator='Ctrl+S', image=save_file_icon, compound='left', command=save)
file_menu.add_command(label='Save as', accelerator='Shift+Ctrl+S', compound='left', command=save_as)
file_menu.add_separator()
file_menu.add_command(label='Exit', accelerator='Alt+F4', compound='left', command=exit_editor)
menu_bar.add_cascade(label='File', menu=file_menu) # add to menu_bar

# create edit menu
edit_menu = Menu(menu_bar, tearoff=1)
edit_menu.add_command(label='Undo', accelerator='Ctrl+Z', image=undo_icon, compound='left', command=undo)
edit_menu.add_command(label='Redo', accelerator='Ctrl+Y', image=redo_icon, compound='left', command=redo)
edit_menu.add_separator()
edit_menu.add_command(label='Cut', accelerator='Ctrl+X', image=cut_icon, compound='left', command=cut)
edit_menu.add_command(label='Copy', accelerator='Ctrl+C', image=copy_icon, compound='left', command=copy)
edit_menu.add_command(label='Paste', accelerator='Ctrl+V', image=paste_icon, compound='left', command=paste)
edit_menu.add_separator()
edit_menu.add_command(label='Find', accelerator='Ctrl+F', image=find_text_icon, compound='left', command=find_text)
edit_menu.add_separator()
edit_menu.add_command(label='Select All', accelerator='Ctrl+A', compound='left', command=select_all)
menu_bar.add_cascade(label='Edit', menu=edit_menu) # add to menu_bar

# create view menu
view_menu = Menu(menu_bar)
show_line_no = IntVar()
show_line_no.set(1)
view_menu.add_checkbutton(label="Show Line Number", variable=show_line_no)
show_cursor_info = IntVar()
show_cursor_info.set(1)
view_menu.add_checkbutton(label='Show Cursor Location at Bottom', variable=show_cursor_info, command=show_cursor_info_bar)
to_highlight_line = IntVar()
view_menu.add_checkbutton(label='Highlight Current Line', onvalue=1, offvalue=0, variable=to_highlight_line, command=toggle_highlight)
themes_menu = Menu(menu_bar, tearoff=0)
view_menu.add_cascade(label='Themes', menu=themes_menu)
menu_bar.add_cascade(label='View', menu=view_menu) # add to menu_bar
"""
color scheme is defined with dictionary elements like theme_name: fg.bg
"""
color_schemes = {
    'Default' : '#000000.#FFFFFF',
    'Greygarious': '#83406A.#D1D4D1',
    'Aquamarine': '#5B8340.#D1E7E0',
    'Bold Beige': '#4B4620.#FFF0E1',
    'Cobalt Blue': '#ffffBB.#3333aa',
    'Olive Green': '#D1E7E0.#5B8340',
    'Night Mode': '#FFFFFF.#000000',
}
theme_choice = StringVar()
theme_choice.set('Default')
for k in sorted(color_schemes):
    themes_menu.add_radiobutton(label=k, variable=theme_choice, command=change_theme)


# create about menu
about_menu = Menu(menu_bar)
about_menu.add_command(label='About', compound='left', command=display_about_messagebox)
about_menu.add_command(label='Help', compound='left', command=display_help_messagebox)
menu_bar.add_cascade(label='About', menu=about_menu)
root.config(menu=menu_bar)


# add the shorcut bar
shortcut_bar = Frame(root, height=25, bg='light sea green')
shortcut_bar.pack(expand='no', fill='x')
# add icons to shortcut bar
new_shortcut = Button(shortcut_bar, image=new_file_icon, command=new_file)
new_shortcut.pack(side='left')
open_shortcut = Button(shortcut_bar, image=open_file_icon, command=open_file)
open_shortcut.pack(side='left')
save_shortcut = Button(shortcut_bar, image=save_file_icon, command=save)
save_shortcut.pack(side='left')
cut_shortcut = Button(shortcut_bar, image=cut_icon, command=cut)
cut_shortcut.pack(side='left')
copy_shortcut = Button(shortcut_bar, image=copy_icon, command=copy)
copy_shortcut.pack(side='left')
paste_shortcut = Button(shortcut_bar, image=paste_icon, command=paste)
paste_shortcut.pack(side='left')
undo_shortcut = Button(shortcut_bar, image=undo_icon, command=undo)
undo_shortcut.pack(side='left')
redo_shortcut = Button(shortcut_bar, image=redo_icon, command=redo)
redo_shortcut.pack(side='left')
find_shortcut = Button(shortcut_bar, image=find_text_icon, command=find_text)
find_shortcut.pack(side='left')


# add line number text field
line_number_bar = Text(root, width=4, pady=-3, takefocus=0, border=0,
                       bg='khaki', state='disabled', wrap='none')
line_number_bar.pack(side='left', fill='y')

# add the content text field
content_text = Text(root, wrap='word', undo=1)
content_text.pack(expand='yes', fill='both')
# add the scroll bar next to content text field
scroll_bar = Scrollbar(content_text)
content_text.configure(yscrollcommand=scroll_bar.set) # ?
scroll_bar.config(command=content_text.yview) # ?
scroll_bar.pack(side='right', fill='y')

# adding popup menu
popup_menu = Menu(content_text)
for i in ('cut', 'copy', 'paste', 'undo', 'redo'):
    cmd = eval(i)
    popup_menu.add_command(label=i, compound='left', command=cmd)
popup_menu.add_separator()
popup_menu.add_command(label='Select All', command=select_all)

# handling redo quirk
# note: on mac, Control == Command
content_text.bind('<Control-y>', redo)
content_text.bind('<Control-Y>', redo)

# bind select all as Control-A / Control-a to content_text
content_text.bind('<Control-a>', select_all)
content_text.bind('<Control-A>', select_all)

# bind find all feature to Ctrl+f shortcut
content_text.bind('<Control-f>', find_text)
content_text.bind('<Control-F>', find_text)

# bind open file feature to Ctrl+o shortcut
content_text.bind('<Control-o>', open_file)
content_text.bind('<Control-O>', open_file)

# bind save and save_as feature to Ctrl+S and Shift+Ctrl+S shortcuts
content_text.bind('<Control-s>', save)
content_text.bind('<Control-S>', save)
content_text.bind('<Shift-Control-s>', save_as)
content_text.bind('<Shift-Control-S>', save_as)

# bind new file feature to Ctrl+N shorcut
content_text.bind('<Control-n>', new_file)
content_text.bind('<Control-N>', new_file)

content_text.bind('<KeyPress-F1>', display_help_messagebox)
content_text.bind('<Any-KeyPress>', on_content_changed)

# bind right mouse to popup menu
content_text.bind('<Button-2>', show_popup_menu)

content_text.tag_configure('active_line', background='ivory2')
cursor_info_bar = Label(content_text, text='Line:1 | Column:1')
cursor_info_bar.pack(expand='NO', fill=None, side='right', anchor='se')

root.protocol('WM_DELETE_WINDOW', exit_editor) # override destroy handler
root.mainloop()