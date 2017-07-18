#from tkinter import *
import string
import tkinter as tk



class Top:
    '''
    Custom parent class for top_level child windows to pull funcs from
    '''

    def but_funcs(self, *funcs):
        '''
        Call multiple functions with a single button click,
        1)get rolodex, header and value entry values
        2)destroy toplevel window
        '''
        def commands(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)
        return commands

    def get_all(self, *args):
        '''
        get() toplevel entry field values
        '''
        try:
            self.dex = self.rolodex.get()
            self.head = self.header.get()
            self.val = self.value.get()
            return (self.dex, self.head, self.val)
        except AttributeError:
            pass

    def get_both(self, *args):
        try:
            self.word = self.custom_word.get()
            self.hint = self.custom_hint.get(1.0, tk.END)
            return (self.head, self.val)
        except AttributeError:
            pass

    def get_single(self, *args):
        try:
            self.name = self.name.get()
            return self.name
        except AttributeError:
            pass

    def destroy(self, *args):
        '''
        Destroy toplevel window
        '''
        self.win.destroy()


    
class Single_entry(Top):
    '''
    Toplevel window wtih one button, returns a single entryfield value
    '''
    def __init__(self,
                 title,
                 label,
                 button_label,
                 **kwargs):
    
        for key, value in kwargs.items():
            self.__dict__[key] = value
        self.win = tk.Toplevel()
        self.win.geometry('250x95')
        self.win.title(title)
        self.label = label
        self.button_label = button_label
        self.master = tk.Frame(self.win, bg = self.bg)
        self.master.pack(fill = tk.BOTH, expand = True)
        self.upper = tk.Frame(self.master, bg = self.bg)
        self.upper.pack()
        self.lower = tk.Frame(self.master, bg = self.bg)
        self.lower.pack()
        try:
            self.win.geometry("+%d+%d" % (self.x, self.y))
        except AttributeError:
            pass
        self.create_widgets()
        
    def create_widgets(self):
        self.entry_frame = tk.Frame(self.upper,
                                    bg = self.bg,
                                    pady = 5)
        
        self.name = tk.Entry(self.entry_frame,
                             bg = self.field_bg,
                             width = 30,
                             highlightthickness = 1,)
        self.name.grid(row=6, column = 0)
        self.name.focus()
        self.name_lab = tk.Label(self.entry_frame,
                                 text = self.label,
                                 bg = self.bg,
                                 fg = self.label_color,
                                 font = self.font,
                                 pady = 0)
        self.name_lab.grid(row=7, column = 0)
        self.entry_frame.pack()
        self.button_frame = tk.Frame(self.lower, bg = 'red')
        width = max(10, len(self.button_label))
        self.but = tk.Button(self.button_frame,
                             text = self.button_label,
                             bg = self.button_bg,
                             fg = self.button_fg,
                             font = self.font,
                             width = width,
                             command = self.but_funcs(self.get_single, self.destroy))
        self.but.grid(row=8,column = 1, sticky = 'S')
        self.but.bind("<Return>", self.but_funcs(self.get_single, self.destroy))   
        self.button_frame.pack(side = tk.TOP)
        
        self.win.wait_window()



class Double_entry(Top):
    '''
    Toplevel window with one botton, returns two entry values
    '''
    def __init__(self,
                 title,
                 entry1_label,
                 text_label,
                 button_label,
                 **kwargs):
        for key, value in kwargs.items():
            self.__dict__[key] = value
        self.win = tk.Toplevel()
        self.win.title('New Word')
        self.word = None
        self.hint = None
        self.entry1_label = entry1_label
        self.text_label = text_label
        self.button_label = button_label
        self.master = tk.Frame(self.win, bg = self.bg)
        self.master.pack()
        self.upper = tk.Frame(self.master, bg = self.bg)
        self.upper.pack()
        self.lower = tk.Frame(self.master, bg = self.bg)
        self.lower.pack()
        self.win.geometry("+%d+%d" % (self.x, self.y))
         
        self.create_widgets()
        
    def create_widgets(self):
        #Entry field
        self.word_frame = tk.Frame(self.upper, bg = self.bg)
        self.word_frame.grid(row = 0, column = 0, sticky  = 'W')
        self.word_label = tk.Label(self.word_frame,
                                   bg = self.bg,
                                   fg = self.label_color,
                                   font = self.font,
                                   text = self.entry1_label)
        self.word_label.grid(row=0, column = 0, sticky = 'W')
        self.custom_word = tk.Entry(self.word_frame,
                                    bg = self.field_bg,
                                    highlightthickness = 1,
                                    highlightbackground = self.bg)
        self.custom_word.grid(row=1, column = 0, sticky = 'W')
        self.custom_word.focus()


        #Text field
        self.text_frame = tk.Frame(self.upper, bg = self.bg)
        self.text_frame.grid(row = 1, column = 0)
        self.custom_hint_lab = tk.Label(self.text_frame,
                                        bg = self.bg,
                                        fg = self.label_color,
                                        text = self.text_label)
        self.custom_hint_lab.grid(row= 0, column = 0, sticky = 'W')
        self.custom_hint = tk.Text(self.text_frame,
                                   bg = self.field_bg,
                                   bd = 2,
                                   width = 25,
                                   height = 5,
                                   padx = 2,
                                   pady = 2,
                                   highlightthickness = 1,
                                   highlightbackground = self.bg)
        self.custom_hint.grid(row = 1, column = 0)


        #Button Frame        
        self.button_frame = tk.Frame(self.lower, bg = self.bg)
        self.button_frame.grid(row = 2, column = 0)
        width = max(10, len(self.button_label))
        self.but = tk.Button(self.button_frame,
                             bg = self.button_bg,
                             fg = self.button_fg,
                             bd = 2,
                             text = self.button_label,
                             width = width,
                             command = self.but_funcs(self.get_both, self.destroy))
        self.but.pack()
        self.but.bind("<Return>", self.but_funcs(self.get_both, self.destroy))   

        #Key Bindings
        self.custom_hint.bind("<Tab>", self.focus_next_)
        self.custom_word.bind("<Return>", self.return_)
        self.but.bind("<Return>", self.return_)
        
        self.win.wait_window()
    
    def focus_next_(self, event = None):
        '''
        Prevent textbox from indenting with 'Tab', pass focus to button instead
        '''
        focus = self.win.focus_get()
        if focus == self.custom_hint:
            event.widget.tk_focusNext().focus()
            return("break")

    def return_(self, event = None):
        '''
        Return custom word, custom hint and destroy Toplevel window
        '''
        self.get_both()
        self.destroy()
        

class Triple_entry(Top):
    '''
    Top level window returns three entry field values
    '''

    def __init__(self,
                 title,
                 entry1_label,
                 entry2_label,
                 entry3_label,
                 button_label):
        self.win = tk.Toplevel()
        self.win.geometry('175x200')
        self.win.title(title)
        self.entry1_label = entry1_label
        self.entry2_label = entry2_label
        self.entry3_label = entry3_label
        self.button_label = button_label
        self.master = tk.Frame(self.win)
        self.master.pack()
        self.upper = tk.Frame(self.master)
        self.upper.pack()
        self.lower = tk.Frame(self.master)
        self.lower.pack()
        self.border = 'grey'
        self.create_widgets()
    
        
    def create_widgets(self):
        PADX = 10
        PADY = 10
        
        self.entry_frame = tk.Frame(self.upper)
        self.rolodex = tk.Entry(self.entry_frame,
                             highlightthickness = 1,
                             highlightbackground = self.border)
        self.rolodex.grid(row=6, column = 0, padx = PADX )
        self.rolodex.focus()
        self.rolodex_lab = tk.Label(self.entry_frame,
                                 text = self.entry1_label + '\n')
        self.rolodex_lab.grid(row=7, column = 0, sticky = tk.W, padx = PADX)

        self.header = tk.Entry(self.entry_frame,
                            highlightthickness = 1,
                            highlightbackground = self.border)
        self.header.grid(row=9, column = 0, padx = PADX)
        self.head_lab = tk.Label(self.entry_frame,
                              text = self.entry2_label + '\n')
        self.head_lab.grid(row=10, column = 0, sticky = tk.W, padx = PADX)
        self.value = tk.Entry(self.entry_frame,
                           highlightthickness = 1,
                           highlightbackground = self.border)
        self.value.grid(row=12, column=0, padx = PADX)
        self.val_lab = tk.Label(self.entry_frame,
                             text = self.entry3_label + '\n')
        self.val_lab.grid(row=13, column=0, sticky = tk.W, padx = PADX)
        self.entry_frame.pack()
        self.button_frame = tk.Frame(self.lower)
        width = max(10, len(self.button_label))
        self.but = tk.Button(self.button_frame,
                          text = self.button_label,
                          width = width,
                          command = self.but_funcs(self.get_all, self.destroy))
        self.but.grid(row=15,column = 0, sticky = tk.W)
        self.but.bind("<Return>", self.but_funcs(self.get_all, self.destroy))   
        self.button_frame.pack(side = tk.LEFT)
        self.win.wait_window()
        
class Single_comboBox(Top):
    '''
    Single Combobox widget, with a single button
    '''
    def __init(self, title, box_values, button_label, box_label = None):
        self.win = tk.Toplevel()
        self.win.geometry('175x200')
        self.win.title(title)
        self.box_values = box_values
        self.button_label = button_label
        self.box_label = box_label
        self.master = Frame(self.win)
        self.master.pacl()
        self.creat_widgets()

    def create_widgets(self):
        box = Combobox(self.master)

class Custom_dialogue(Top):
    '''
    1x1 toplevel window with a Diaplogue box, two buttons, and a checkbox
    '''

    def __init__(self, title, dialogue, **kwargs):
        self.win = tk.Toplevel(takefocus = True)
        self.win.title(title)
        self.win.focus_set()
        self.msg = dialogue
        
        for key, value in kwargs.items():
            self.__dict__[key] = value 
        self.confirm = ''
        self.for_all = ''
        self.master = tk.Frame(self.win, bg = self.bg)
        self.master.pack()
        self.upper = tk.Frame(self.master)
        self.upper.pack()
        self.lower = tk.Frame(self.master)
        self.lower.pack()
        try:
            self.win.geometry("+%d+%d" % (self.x, self.y))
        except AttributeError:
            pass
        
        #Key Binding
        self.win.bind('<Return>', self.bound_option)
        self.win.bind('<Escape>', self.decline)
        
        self.create_widgets()

        
        

    def create_widgets(self):
        self.msg_frame = tk.Frame(self.upper, bg = self.bg)
        self.msg_label = tk.Label(self.msg_frame,
                                  font = self.font,
                                  fg = self.label_color,
                                  bg = self.bg,
                                  text = self.msg)
        self.msg_label.grid(row = 0,
                            column = 0,
                            columnspan = 2,
                            sticky = 'ew') 
        self.msg_frame.pack(fill = tk.BOTH, expand = True)
        self.button_frame = tk.Frame(self.lower)
        
        self.yes = tk.Button(self.button_frame,
                             text = 'Yes',
                             bd = 2,
                             font = self.font,
                             bg = self.button_bg,
                             fg = self.button_fg,
                             command = self.but_funcs(self.yes,self.destroy),
                             width = 10)
        
        self.no = tk.Button(self.button_frame,
                            text = 'No',
                            bd = 2,
                            font = self.font,
                            bg = self.button_bg,
                            fg = self.button_fg,
                            command = self.but_funcs(self.no,self.destroy),
                            width = 10)
  

        self.yes.pack(side = tk.LEFT)
        self.yes.focus()
        self.no.pack(side = tk.LEFT)

        self.button_frame.pack()
        self.win.wait_window()


    def yes(self):
        self.confirm = 'yes'
    def no(self):
        self.confirm = 'no'
        
    def bound_option(self, event = None):
        '''
        Key Binding for self.yes and self.no
        '''
        focus = self.win.focus_get()
        if focus == self.yes:
            self.confirm = 'yes'
            self.destroy()
        elif focus == self.no:
            self.confirm = 'no'
            self.destroy()
        else:
            pass

    def decline(self, event = None):
        '''
        Use Escape key to decline to play again
        '''
        self.confirm = 'no'
        self.destroy()
        
        



        
class Help_window(Top):
    '''
    A toplevel window, with a listbox on the left and a text display on the
    right.
    '''
    
    def __init__(self, entries, definitions):
        self.entries = entries
        self.definitions = definitions
        self.win = tk.Toplevel()
        self.win.title('Help...')
        self.master = tk.Frame(self.win)
        self.master.rowconfigure(1, weight = 1)
        self.master.columnconfigure(0, weight = 1)
        self.master.columnconfigure(1, weight = 1)
        self.master.pack(fill =tk.BOTH, expand = 1)
        self.text_bar = False
        self.create_widgets()

    def create_widgets(self):
        #list box
        #Frames
        self.label_frame = tk.Frame(self.master)
        self.label_frame.grid(row = 0, column = 0)
        self.label = tk.Label(self.label_frame, text = 'Help with...')
        self.label.pack()
        self.option_frame = tk.Frame(self.master)
        self.option_frame.grid(row = 1, column = 0, sticky = tk.N+tk.E+tk.S+tk.W )
        #Listbox
        self.options = tk.Listbox(self.option_frame)
        for index, option in enumerate(self.entries):
            self.options.insert(index, option)
        self.options.pack(side = tk.LEFT,
                          anchor = tk.NW,
                          fill =tk.BOTH,
                          expand = 1)
        #List Scrollbar
        if len(self.entries) > 10:
            self.list_bar = Scrollbar(self.option_frame,
                                      command = self.options.yview)
            self.options.config(yscrollcommand = self.list_bar.set)
            self.list_bar.pack(side = LEFT,
                               fill = Y)
        #Button
        self.button_frame = tk.Frame(self.master)
        self.button_frame.grid(row = 2, column = 0)
        self.button = tk.Button(self.button_frame,
                             text = 'OK',
                             width = 10,
                             command = self.win.destroy)
        self.button.pack(side = tk.TOP, anchor = tk.N)
        #Keybinding
        self.options.bind('<Double-Button-1>', self.on_double)
        
        
        #Display
        self.display_frame = tk.Frame(self.master)
        self.display_frame.columnconfigure(0, weight = 1)
        self.display_frame.rowconfigure(0, weight = 1)
        self.display_frame.grid(row = 0,
                                rowspan = 3,
                                column = 1,
                                sticky = tk.N+tk.S+tk.E+tk.W)
        self.display = tk.Text(self.display_frame,
                            bg='grey94',
                            wrap = tk.WORD,
                            height = 15,
                            width = 50)
        self.display.pack(side = tk.LEFT, fill= tk.BOTH, expand =1)
        
        

    def on_double(self, event):
        '''
        Return the value selected by user with a double click from listbox
        Display cooresponding Help_text dict entry in text box
        '''
        
        index = self.options.curselection()[0]
        category = self.entries[index]
        text = help_text.display[category]
        self.display.config(state = tk.NORMAL)
        #Clear Text Box of existing text if any
        self.display.delete(1.0,tk.END)
        #Insert desired Help text
        self.display.insert(tk.INSERT,text)
        self.display.config(state = tk.DISABLED)
        lines = int(self.display.index('end-1c').split('.')[0])
        #Vertical scroll bar IF text exceeds n lines
        if lines > 13 and self.text_bar == False:
            self.text_bar = True
            self.bar_frame = tk.Frame(self.display_frame)
            self.bar_frame.pack(side = tk.LEFT, fill = tk.Y)
            self.scrollbar = tk.Scrollbar(self.bar_frame)
            self.scrollbar.pack(side = tk.LEFT, fill =tk.Y)
            self.scrollbar.config(command = self.display.yview)
            self.display.config(yscrollcommand = self.scrollbar.set)
        
        

class Basic_display(Top):
    '''
    1x1 grid, simple canvas to display message with a single button
    '''
    def __init__(self,title, msg):
        self.win = tk.Toplevel()
        self.win.title(title)
        self.master = tk.Frame(self.win)
        self.master.pack()
        self.canvas = tk.Canvas(self.master,
                             borderwidth = 5)
        self.label = tk.Label(self.canvas,
                           text = msg)
        self.button = tk.Button(self.canvas,
                             text = 'Ok',
                             width = 10,
                             borderwidth = 3,
                             command = self.but_funcs(self.destroy))
        self.label.pack()
        self.button.pack()
        self.canvas.pack()
if __name__ == "__main__":
    msg = 'TEST MESSAGE'
    bg = 'Slate Blue'
    fg = 'pink'
    field_bg = 'orange'
    font = ('Comic Sans MS', 12)
    label_color = 'red'
    button_bg = 'green'
    button_fg = 'yellow'
    x = 100
    y = 100
    '''
    delete = Custom_dialogue('Delete Confirm',msg,
                             font = ('Courier', 12),
                             bg = 'sky blue',
                             label_bg = 'dark slate blue',
                             label_color = 'dark green',
                             button_bg = 'slate blue',
                             button_fg = 'light green')

    '''
    name = Single_entry("NEW RECORD", "Your Name", 'Ok',
                        font = font,
                        bg = bg,
                        label_color = label_color,
                        field_bg = field_bg,
                        button_bg = button_bg,
                        button_fg = button_fg,
                        x = x,
                        y = y)
    '''
    custom_word = Double_entry("NEW RECORD", "Custom Word", 'Hint', 'Play Game',
                                 font = font,
                                 bg = bg,
                                 label_color = label_color,
                                 field_bg = field_bg,
                                 button_bg = button_bg,
                                 button_fg = button_fg
                                 )
    '''
  
