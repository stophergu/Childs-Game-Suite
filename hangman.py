import tkinter as tk
from tkinter import Frame
import top_wins
from operator import itemgetter
import json, random, os, string, datetime


class Hangman_shell(tk.Frame):
    '''
    A GUI shell for a game of hangman, multiple frames exist on top of
    each other,
    '''
    
    def __init__(self, parent,*args, **kwargs):
        tk.Frame.__init__(self, parent)
        for key, value in kwargs.items():
            self.__dict__[key] = value
        self.shell = tk.Frame(self)
        self.shell.pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        self.shell.grid_rowconfigure(0, weight = 1)
        self.shell.grid_columnconfigure(0, weight = 1)
        self.dic_fn = r'json\dictionary.jsn'
        self.vocab_fn = r'json\hangman_vocab.jsn'
        self.scores_fn = r'json\hangman_scores.jsn'
        self.level = None
        self.word = None
        self.custom_hint = None
        #self.clear_scores()
        self.high_scores = self.load_scores()
        self.all_vocab = self.load_vocab()
        self.all_defs = self.load_defs()
        
        #Game Title
        self.header = tk.Label(self.shell,
                               text = '{}\n{}\n{}'.format(
                                   '_'*122,
                                   ' '*36 + '\nHANGMAN\n' + ' '*36,
                                   '_'*122))
        self.header.grid(row = 0, column = 0, sticky = 'news')

        #The stacked frames
        self.frames = {}
        for F in (Main, Level, View, List_editor, Game):
            page_name = F.__name__
            frame = F(parent=self.shell, controller=self)
            self.frames[page_name] = frame

            frame.grid(row = 1, column = 0, sticky = 'news')
        self.show_frame('Main')

    def load_vocab(self, event = None):
        """
        Return a dict of all known Lists of vocab words
        """
        pulled_dic = {}
        with open(self.vocab_fn) as infile:
            words = json.load(infile)

        for key in words.keys():
            if key == 'custom':
                for custom_key in words[key].keys():
                    pulled_dic[custom_key] = words[key][custom_key]
            else:
                pulled_dic[key] = words[key]
        
        return pulled_dic

    def dump_vocab(self, vocab = None):
        '''
        Save all vocab lists to json file
        '''
        if vocab == None:
            vocab = self.all_vocab
        with open(self.vocab_fn, 'w') as words_to_write:
            words = json.dump(vocab, words_to_write)

    def load_defs(self, event = None):
        """
        Return a dict of all known defs of vocab words
        """
        pulled_dic = {}
        with open(self.dic_fn) as infile:
            pulled_dic = json.load(infile)
        return pulled_dic

    def dump_defs(self, event = None):
        '''
        Save all known defs to json file
        '''
        with open(self.dic_fn, 'w') as defs_to_write:
            json.dump(self.all_defs, defs_to_write)

    def load_scores(self):
        '''
        Return list of scores stored in self.scores_fn, return a list  of tuples
        for tuple in scores: name, score = scores
        '''
        with open(self.scores_fn) as infile:
            scores = json.load(infile)

            return scores
        
    def dump_scores(self):
        '''
        Store top ten high scores in json file, scores is a list of tuples
        '''
        scores = sorted(self.high_scores, key=itemgetter(1))
        while len(scores) > 10:
            scores.pop(0)
        with open(self.scores_fn, 'w') as scores_to_write:
            json.dump(scores, scores_to_write)

    def clear_scores(self):
        '''
        Use to clear all HighScores
        '''
        self.high_scores = []
        self.dump_scores()

    def override_bind(self, event = None):
        pass

    def show_frame(self, page_name):
        '''
        Show frame of given page_name, set potentially overlapping keybindings
        as frame is raised and adjust appearance of contoller.header to fit page
        theme
        '''
        frame = self.frames[page_name]
          
        if page_name == "Main":
            ####################################################################
            #                          Header Config                           #
            ####################################################################
            self.shell.config(bg = frame.header_bg)
            text = '{}\n{}\n{}'.format('_'*56,
                                       ' '*36 + '\nHANGMAN\n' + ' '*36,
                                       '_'*56)
            self.header.config(font = frame.header_font,
                               text = text,
                               fg = frame.header_fg,
                               bg = frame.header_bg)
            frame.populate_scorecard()
            
            ####################################################################
            #                           Key Bindings                           # 
            ####################################################################
            self.controller.bind("<Escape>", lambda x: frame.controller.controller.show_frame("Main_game_master"))
            self.controller.bind("<Return>", frame.menu_choice)
            self.controller.bind("<Down>", frame.next_option)
            self.controller.bind("<Up>", frame.prev_option)
            
        
        if page_name == "Level":
            ####################################################################
            #                          Header Config                           #
            ####################################################################
            self.shell.config(bg = frame.header_bg)
            text = '{}\n{}\n{}'.format('_'*56,
                                       ' '*36 + '\nHANGMAN\n' + ' '*36,
                                       '_'*56)
            self.header.config(font = frame.header_font,
                               text = text,
                               fg = frame.header_fg,
                               bg = frame.header_bg)
            #Reset Menus
            frame.radio_indx = 0
            frame.list_indx = 0
            frame.level_options.set(frame.radio_indx)
            #Update custom list
            frame.update_other_lists()
            
            ####################################################################
            #                           Key Bindings                           # 
            ####################################################################
            self.controller.bind("<Return>", frame.play_game)
            self.controller.bind("<Escape>", frame.to_main)
            self.controller.bind("<Down>", frame.next_what)
            self.controller.bind("<Up>", frame.prev_what)
            self.controller.bind("<Button-1>",frame.on_single)
            

        if page_name == "View":
            ####################################################################
            #                          Header Config                           #
            ####################################################################
            #Update Custom list Listbox
            #frame.update_option_menu()
            self.shell.config(bg = frame.header_bg)
            text = '{}\n{}\n{}'.format('_'*56,
                                       ' '*36 + '\nHANGMAN\n' + ' '*36,
                                       '_'*56)
            self.header.config(font = frame.header_font,
                               text = text,
                               fg = frame.header_fg,
                               bg = frame.header_bg)

            ####################################################################
            #                           Key Bindings                           # 
            ####################################################################
            self.controller.bind("<Return>", frame.define)
            self.controller.bind('<Double-Button-1>', frame.define)
            self.controller.bind("<Escape>", frame.to_main)
            self.controller.bind("<Right>", frame.next_list_option)
            self.controller.bind("<Left>", frame.prev_list_option)
            self.controller.bind("<Down>", frame.next_vocab_option)
            self.controller.bind("<Up>", frame.prev_vocab_option)
            self.controller.bind("<Control_L><e>", frame.edit)
            self.controller.bind("<Control_L><E>", frame.edit)
            self.controller.bind('<Control_L><s>', frame.commit)
            self.controller.bind("<Control_L><S>", frame.commit)
            self.controller.bind("<Button-1>",None)

        if page_name == "Game":
            ####################################################################
            #                           Key Bindings                           # 
            ####################################################################
            self.controller.bind("<Return>", frame.guess)
            self.controller.bind("<Escape>", frame.quit_game)
            self.controller.bind("<Button-1>", frame.on_single)
            #Set a new game every time Game frame is raised to top
            frame.setup()

        if page_name == "List_editor":
            ####################################################################
            #                          Header Config                           #
            ####################################################################
            self.shell.config(bg = frame.header_bg)
            text = '{}\n{}\n{}'.format('_'*56,
                                       ' '*36 + '\nHANGMAN\n' + ' '*36,
                                       '_'*56)
            self.header.config(font = frame.header_font,
                               text = text,
                               fg = frame.header_fg,
                               bg = frame.header_bg)

            ####################################################################
            #                           Key Bindings                           # 
            ####################################################################
            self.controller.bind("<Escape>", frame.to_main)
            self.controller.bind("<Return>", frame.return_what)
            self.controller.bind("<Control_L><E>", frame.edit_what)
            self.controller.bind("<Control_L><e>", frame.edit_what)
            self.controller.bind("<Control_R><E>", frame.edit_what)
            self.controller.bind("<Control_R><e>", frame.edit_what)
            self.controller.bind("<Control_L><D>", frame.delete_what)
            self.controller.bind("<Control_L><d>", frame.delete_what)
            self.controller.bind("<Control_R><D>", frame.delete_what)
            self.controller.bind("<Control_R><d>", frame.delete_what)
            self.controller.bind("<Control_L><r>", frame.create_list)
            self.controller.bind("<Control_L><R>", frame.create_list)
            self.controller.bind("<Control_R><r>", frame.create_list)
            self.controller.bind("<Control_R><R>", frame.create_list)
            self.controller.bind("<Control_L><O>", frame.add_word)
            self.controller.bind("<Control_L><o>", frame.add_word)
            self.controller.bind("<Control_R><O>", frame.add_word)
            self.controller.bind("<Control_R><o>", frame.add_word)
            self.controller.bind("<Tab>", frame.focus_next_)
            self.controller.bind("<Button-1>",None)
        frame.tkraise()




class Main(tk.Frame):
    '''
    Main Page of Hangman, Contain a set of radiobuttons to allow user to navigate to
    the other pages of game and a display of Top Ten High Scores
    '''
    def __init__(self, parent, controller):
        self.controller = controller
        #GUI style constants
        self.bg = 'cornflower blue'
        self.title_font = ('Courier', 14)
        self.header_font = ('Courier', 13)
        self.header_bg = 'cornflower blue'
        self.header_fg = 'misty rose'
        self.category_font = ('Courier', 10)
        #Button colors
        self.selector_color = 'steel blue'
        self.button_bg = 'slate blue'
        self.button_fg = 'orchid1'
        #label fg and Font
        self.label_color = 'misty rose'
        self.label_font = ('Courier', 12)
        self.field_bg = 'bisque'
        #Score Card
        self.score_label_font = ('Courier', 15)
        self.score_font = ('Courier', 8)
        self.score_color = 'maroon'
        self.score_bg = 'steel blue'

        #Master Frame
        tk.Frame.__init__(self, parent, bg  = self.bg)
        self.create_widgets()

    def __str__(self):
        return 'Match Game Main Page'
        

    def create_widgets(self):
        #Decorative panels
        img_path = os.getcwd() + r"\images"
        left_flower = img_path + r'\Decor\left_turret1.gif'
        left_flower_img = tk.PhotoImage(master = self,
                               file = left_flower)
        
        right_flower = img_path + r'\Decor\right_turret1.gif'
        right_flower_img = tk.PhotoImage(master = self,
                                         file = right_flower)
        
        #Left Flower
        self.flower_left = tk.Frame(self, bg = self.bg)
        self.flower_left.grid(row = 0, column = 0, rowspan = 2, sticky = 'news')
        self.flower_L_label = tk.Label(self.flower_left, bg = self.bg)
        self.flower_L_label.config(image = left_flower_img)
        self.flower_L_label.img = left_flower_img
        self.flower_L_label.pack()

        #Right Flower
        self.flower_right = tk.Frame(self, bg = self.bg)
        self.flower_right.grid(row = 0, column = 2, rowspan = 2, sticky = 'news')
        self.flower_R_label = tk.Label(self.flower_right,bg = self.bg)
        self.flower_R_label.config(image = right_flower_img)
        self.flower_R_label.img = right_flower_img        
        self.flower_R_label.pack()
       
        #Menu Frame
        self.main_menu = tk.Frame(self,
                                  highlightthickness = 0,
                                  bg = self.bg,
                                  pady = 20,
                                  relief = 'raised')
        self.main_menu.grid(row = 0, column = 1)
        self.main_menu.grid_rowconfigure(0, weight = 1)
        self.main_menu.grid_columnconfigure(0, weight = 1)

        self.menu_title = tk.Label(self.main_menu,
                                   font = self.header_font,
                                   fg = self.label_color,
                                   bg = self.bg,
                                   text = '{}\n{}{}{}'.format(
                                       'Main Menu',' '*5, '_'*15, ' '*5))
        self.menu_title.pack()

        #Menu Radio's
        self.menu_options = tk.IntVar()
        self.menu_options.set(1)
                                                
        #Radio: Easy
        self.easy = tk.Radiobutton(self.main_menu,
                                   font = self.label_font,
                                   fg = self.label_color,
                                   bg = self.bg,
                                   selectcolor = self.selector_color,
                                   text = 'Play       ',
                                   variable = self.menu_options,
                                   value = 1)
        self.easy.pack(anchor = tk.N)
        
        #Radio: normal
        self.normal = tk.Radiobutton(self.main_menu,
                                   font = self.label_font,
                                   fg = self.label_color,
                                   bg = self.bg,
                                   selectcolor = self.selector_color,
                                   text = 'View       ',
                                   variable = self.menu_options,
                                   value = 2)
        self.normal.pack(anchor = tk.N)
        
        #Radio:Hard
        self.hard = tk.Radiobutton(self.main_menu,
                                   font = self.label_font,
                                   fg = self.label_color,
                                   bg = self.bg,
                                   selectcolor = self.selector_color,
                                   text = 'List Editor',
                                   variable = self.menu_options,
                                   value = 3)
        self.hard.pack(anchor = tk.N)
        
        #Exit
        self.exit = tk.Radiobutton(self.main_menu,
                                   font = self.label_font,
                                   fg = self.label_color,
                                   bg = self.bg,
                                   selectcolor = self.selector_color,
                                   text = 'Exit       ',
                                   variable = self.menu_options,
                                   value = 4)
        self.exit.pack(anchor = tk.N)
        self.spacer = tk.Label(self.main_menu,
                               bg = self.bg,
                               text = '')
        self.spacer.pack(anchor = tk.NW)
        
        #Menu submit Button
        self.submit = tk.Button(self.main_menu,
                                font = self.label_font,
                                fg = self.button_fg,
                                bg = self.button_bg,
                                text = 'Ok',
                                width = 8,
                                border = 4,
                                padx = 2,
                                pady = 2,
                                command = self.menu_choice)
        self.submit.pack(side = tk.BOTTOM)

        #Display Highscores
        #Scorecard Frame
        self.scores = tk.Frame(self)
        self.scores.grid(row = 2, column = 0, columnspan = 4)

        #Scorecard Header
        self.score_header = tk.Label(self,
                                     bg = self.bg,
                                     fg = self.score_color,
                                     font = self.score_label_font,
                                     text = '\n\n\nHIGH SCORES')
        
        self.score_header.grid(row = 1,
                               column = 1,
                               sticky = 'EW')

        #Scorecard column labels
        #"Name"
        self.name_label = tk.Label(self.scores,
                                   relief = tk.RAISED,
                                   width = 20,
                                   font = self.header_font,
                                   bg = self.bg,
                                   fg = self.label_color,
                                   text = 'Name')
        self.name_label.grid(row = 3,
                             column = 0,
                             sticky = "NEWS")
        #"Score"
        self.score_label = tk.Label(self.scores,
                                    relief = tk.RAISED,
                                    width = 12,
                                    font = self.header_font,
                                    bg = self.bg,
                                    fg = self.label_color,
                                    text = 'Score')
        self.score_label.grid(row = 3, column = 1, sticky = "NEWS")
        #"List"
        self.list_label = tk.Label(self.scores,
                                   relief = tk.RAISED,
                                   width = 18,
                                   font = self.header_font,
                                   bg = self.bg,
                                   fg = self.label_color,
                                   text = 'List')
        self.list_label.grid(row = 3, column = 2, sticky = 'NEWS')
        #"Date"
        self.date_label = tk.Label(self.scores,
                                   relief = tk.RAISED,
                                   width = 12,
                                   font = self.header_font,
                                   bg = self.bg,
                                   fg = self.label_color,
                                   text = 'Date')
        self.date_label.grid(row = 3, column = 3, sticky = 'NEWS')
        
        self.scorecard = tk.Frame(self.scores, bg = self.field_bg,)
        for c in range(4):
            self.scorecard.grid_rowconfigure(c, weight = 1)
            self.scorecard.grid_columnconfigure(c, weight = 1)
        self.scorecard.grid(row = 4,
                            column = 0,
                            columnspan = 4,
                            sticky = 'NEWS')

    def populate_scorecard(self):
        #Populate Top 10 scores, highest score at top, lowest at bottom
        self.controller.high_scores = self.controller.load_scores()
        while len(self.controller.high_scores) < 10:
            self.controller.high_scores.insert(0, ('',0,'',''))
        for indx, record in enumerate(self.controller.high_scores):
            #list scores in highest --> lowest
            line = 14 - indx
            name, score, level, date = record
            if name == '':
                score = ''
            
            #Clear entry and replace with updated values
            self.name = tk.Label(self.scorecard,
                                 font = self.score_font,
                                 bg = self.field_bg,
                                 anchor = 'center',
                                 relief = 'groove',
                                 width = 23)                
            
            self.score = tk.Label(self.scorecard,
                                  font = self.score_font,
                                  bg = self.field_bg,
                                  anchor = 'center',
                                  relief = 'groove',
                                  width = 12)

            self.level = tk.Label(self.scorecard,
                                  font = self.score_font,
                                  bg = self.field_bg,
                                  anchor = 'center',
                                  relief = 'groove',
                                  width = 20)
            self.date = tk.Label(self.scorecard,
                                  font = self.score_font,
                                  bg = self.field_bg,
                                  anchor = 'center',
                                 relief = 'groove',
                                  width = 12)
            self.name.config(text = name)
            self.score.config(text = score)
            self.level.config(text = level)
            self.date.config(text = date)
            
            self.name.grid(row = line, column = 0, sticky = 'EWS')
            self.score.grid(row = line, column = 1, sticky = 'EWS')
            self.level.grid(row = line, column = 2, sticky = 'EWS')
            self.date.grid(row = line, column = 3, sticky = 'EWS')
            
    def menu_choice(self, event = None):
        '''
        Return Value of Main Menu Radio Button Option
        '''
        choice = self.menu_options.get()
        if choice == 1:
            self.controller.show_frame("Level")
        elif choice == 2:
            self.controller.show_frame("View")
        elif choice == 3:
            self.controller.show_frame("List_editor")
        elif choice == 4:
            self.menu_options.set(1)
            self.controller.controller.show_frame("Main_game_master")
            
    ###########################################################################
    #KEY BINDINGS                                                             #
    ###########################################################################
    def next_option(self, event = None):
        '''
        Select Next Radio Button
        '''
        option = self.menu_options.get()
        option += 1
        if option > 4:
            option = 1
        self.menu_options.set(option)

    def prev_option(self, event = None):
        '''
        Select Previous Radio Button
        '''
        option = self.menu_options.get()
        option -= 1
        if option < 1:
            option = 4
        self.menu_options.set(option)

    def quit(self, event = None):
        self.controller.controller.show_frame('Main_game_master')
            
class Level(tk.Frame):
    '''
    Frame that allows user to pick what list of words game will choose from, or
    create a custom game via Toplevel window prompting user for a word/hint.
    Total Score of custom games are tallied and displayed but not pushed to
    Highscore list.
    '''
    def __init__(self, parent, controller):
        #GUI style constants
        self.bg = 'cornflower blue'
        self.header_font = ('Courier', 14)
        self.header_bg = 'cornflower blue'
        self.header_fg = 'misty rose'
        #Button colors
        self.selector_color = 'steel blue'
        self.button_bg = 'slate blue'
        self.button_fg = 'orchid1'
        #label fg and Font
        self.label_color = 'misty rose'
        self.label_font = ('Courier', 12)
        self.field_bg = 'bisque'
        self.disabled_bg = 'green'
        self.disabled_fg = 'light green'
        #Toplevel window styling
        self.top_bg = 'royal blue'
        self.top_label_color = 'khaki1'
        self.top_button_bg = 'cornflower blue'
        self.top_button_fg = 'black'
        self.top_field_bg = 'pink'
        self.top_font = ('Courier', 12)
     
        #Reference of built in vocab lists
        self.built_ins = ('easy', 'normal', 'hard', 'extreme')
        #Record of last few words used
        self.past_words = []
        #Master Frame
        tk.Frame.__init__(self, parent, bg = self.bg)
        self.controller = controller
        self.level_frame = tk.Frame(self, bg = self.bg)

        self.create_widgets()
        self.update_other_lists()
        self.list_indx = 0
        self.topLevel = False
              
        
    def create_widgets(self):
        self.level_frame.pack()
        #Menu Title
        self.level_title = tk.Label(self.level_frame,
                                    font = self.label_font,
                                    fg = self.label_color,
                                    bg = self.bg,
                                    text = '_'*30 + '\n\nDIFICULTY\n' + '_'*30)
        self.level_title.pack(anchor = tk.W)
        #Set Difficulty level
        #Level Radio's
        self.level_options = tk.IntVar()
        self.level_options.set(0)
        #Easy
        self.easy = tk.Radiobutton(self.level_frame,
                                   text = '  Easy  ',
                                   font = self.label_font,
                                   fg = self.label_color,
                                   bg = self.bg,
                                   selectcolor = self.selector_color,
                                   variable = self.level_options,
                                   value = 0)
        self.easy.pack(anchor = 'n')
        #Normal
        self.normal = tk.Radiobutton(self.level_frame,
                                     text = '  Normal',
                                     font = self.label_font,
                                     fg = self.label_color,
                                     bg = self.bg,
                                     justify = 'left',
                                     selectcolor = self.selector_color,
                                     variable = self.level_options,
                                     value = 1)
        self.normal.pack(anchor = 'n')
        #Hard
        self.hard = tk.Radiobutton(self.level_frame,
                                   text = '  Hard  ',
                                   font = self.label_font,
                                   fg = self.label_color,
                                   bg = self.bg,
                                   justify = 'left',
                                   selectcolor = self.selector_color,
                                   value = 2,
                                   variable = self.level_options)
        self.hard.pack(anchor = 'n')
        #Extreme
        self.extreme = tk.Radiobutton(self.level_frame,
                                      text = ' Extreme',
                                      font = self.label_font,
                                      fg = self.label_color,
                                      bg = self.bg,
                                      justify = 'left',
                                      selectcolor = self.selector_color,
                                      value = 3,
                                      variable = self.level_options)
        self.extreme.pack(anchor = 'n')
        #Other
        self.other = tk.Radiobutton(self.level_frame,
                                      text = '  Other ',
                                      font = self.label_font,
                                      fg = self.label_color,
                                      bg = self.bg,
                                      justify = 'left',
                                      selectcolor = self.selector_color,
                                      value = 4,
                                      variable = self.level_options)
        self.other.pack(anchor = 'n')


        #Decorative line
        self.spacer_line = tk.Label(self.level_frame,
                                    text = '_'*60,
                                    bg = self.bg,
                                    fg = self.label_color)
        self.spacer_line.pack(side = tk.TOP,
                              anchor = 'n')

        #'other' vocab list, Listbox
        self.list_frame = tk.Frame(self.level_frame, bd = 5, bg = self.bg)
        self.list_frame.pack(anchor = 'n')

        self.other_list = tk.Listbox(self.list_frame,
                                     height = 12,
                                     font = self.label_font,
                                     bg = self.field_bg,
                                     selectbackground = self.field_bg,
                                     selectforeground = 'black')

        self.other_list.pack(side = tk.LEFT,
                             anchor = tk.NW,
                             fill = tk.BOTH,
                             expand = 1)

        #'other' list Listbox Scrollbar
        self.list_bar = tk.Scrollbar(self.list_frame,
                                      command = self.other_list.yview,
                                      bg = self.field_bg)
        self.other_list.config(yscrollcommand = self.list_bar.set)
        self.list_bar.pack(side = tk.LEFT,
                           fill = tk.Y)

        #Level Menu back button
        self.button_frame = tk.Frame(self.level_frame)
        self.button_frame.pack()
        self.back = tk.Button(self.button_frame,
                              font = self.label_font,
                              fg = self.button_fg,
                              bg = self.button_bg,
                              text = '<< Back',
                              width = 8,
                              border = 4,
                              padx = 2,
                              pady = 2,
                              command = self.to_main)
                              
        self.back.grid(row = 0, column =0)
        #Level Menu submit Button
        self.submit = tk.Button(self.button_frame,
                                font = self.label_font,
                                fg = self.button_fg,
                                bg = self.button_bg,
                                text = 'Play',
                                width = 8,
                                border = 4,
                                padx = 2,
                                pady = 2,
                                command = self.play_game)
        self.submit.grid(row = 0, column = 1)
     
    def play_game(self, event = None):
        '''
        Raise "Game" frame, start Hangman game
        '''
        self.level_menu_choice()
        self.controller.word = self.get_word()
        #Prevent Game from starting if User entered invalid word for custom
        #game
        if self.controller.word != None and len(self.controller.word) > 0:
            self.controller.show_frame("Game")

    ############################################################################
    #Level Frame PRIVATE FUNCS                                                 #
    ############################################################################

    def to_main(self, event = None):
        '''
        Raise "Main" Frame
        '''
        self.controller.show_frame("Main")
    def level_menu_choice(self):
        '''
        Set controller dificulty level, and sets word
        '''
        choice  = self.level_options.get()
        if choice == 0:
            level = 'easy'
        elif choice == 1:
            level = 'normal'
        elif choice == 2:
            level = 'hard'
        elif choice == 3:
            level = 'extreme'
        elif choice == 4:
            level = 'other'
        else:
            level = self.get_custom_list()
        
        self.controller.level = level
        
    def get_word(self):
        '''
        Return a random word from given list, if 'other', topwindow prompts
        user for a word and hint
        '''        
        if self.controller.level == 'other':
            try:
                if self.topLevel == False:
                    word, hint = self.custom_game()
                    if len(word) == 0:
                        self.controller.word = None
                    
                    self.controller.custom_hint = hint

                #Add Custom words and hints to built in Lists
                try:                        
                    level = None
                    if 2 < len(word) < 6:
                        level = 'easy'
                    elif len(word) < 10:
                        level = 'normal'
                    elif len(word) < 13:
                        level = 'hard'
                    else:
                        level = 'extreme'  
                    #if level and word ot in self.controller.all_vocab[level]:
                    self.controller.all_vocab[level].append(word.upper())
                    self.controller.all_defs[word.upper()] = hint
                    self.controller.dump_vocab()
                    self.controller.dump_defs()
                except AttributeError:
                    self.controller.show_frame("Level")
            except TypeError:
                if word == None:
                    self.controller.show_frame('Level')
        else:
            words = self.controller.all_vocab
            #Take a random word from appropriate list
            word = random.choice(words[self.controller.level])
            #prevent random word from repeating consecutive words from same list in
            #consecutive games
            min_length = len(words[self.controller.level]) //2
            if len(words[self.controller.level]) > min_length:
                while word in self.past_words[-min_length:]:
                    word  = random.choice(words[self.controller.level])
            else:
                word = random.choice(words[self.controller.level])
            self.past_words.append(word)
        if word != None:
            return word.upper()

    def get_custom_list(self):
        '''
        Radio Button is deselcted, listbox selection is returned
        '''
        self.level_options.set(5)
        list_name = self.other_list.get(self.list_indx)
        return list_name

    def custom_game(self):
        '''
        Open a Toplevel window prompting user for custom word and custom hint
        '''
        self.topLevel = True
        #Calculate coords to place toplevel window 
        x = self.controller.winfo_rootx() + (self.controller.winfo_width() / 3)
        y = self.controller.winfo_rooty() + (self.controller.winfo_height() /3)
        custom = top_wins.Double_entry('title', 'Word:', 'Hint:', 'Play Game!',
                                       font = self.top_font,
                                       bg = self.top_bg,
                                       label_color = self.top_label_color,
                                       field_bg = self.top_field_bg,
                                       button_bg = self.top_button_bg,
                                       button_fg = self.top_button_fg,
                                       x = x,
                                       y = y
                                       )
      
        word = custom.word
        for char in word:
            if char in '1234567890':
                word, hint = self.custom_game()
        hint = custom.hint
        self.topLevel = False
        return word, hint
    
    def update_other_lists(self):
        '''
        Check for new lists, update custom lists option menu
        '''
        self.other_list.delete(0, tk.END)
        for indx, list_name in enumerate(sorted(self.controller.all_vocab.keys())):
            if list_name not in self.built_ins:
                self.other_list.insert(indx, list_name)
        self.other_list.config(state = tk.NORMAL)
        


    ###########################################################################
    #Level Frame KEY BINDINGS                                                 #
    ###########################################################################    
    def next_radio(self, event = None):
        option = self.level_options.get()
        option += 1
        if option > 4:
            self.other_list.focus()
        self.level_options.set(option)

    def prev_radio(self, event = None):
        option = self.level_options.get()
        if option == 0:
            pass
        else:
            option -= 1
        self.level_options.set(option)
        
    def next_list(self, event = None):
        line = self.other_list.curselection()[0]
        self.list_indx = line
        self.other_list.selection_clear(0, tk.END)
        line += 1
        self.other_list.select_set(line)
    
    def prev_list(self, event = None):
        if self.list_indx == 0:
            self.focus()
            self.level_options.set(4)
        line = self.other_list.curselection()[0]
        self.list_indx = line
        self.other_list.selection_clear(0, tk.END)
 
    def next_what(self, event = None):
        focus = self.focus_get()
        if focus != self.other_list:
            self.next_radio()
        elif focus == self.other_list:
            self.next_list()

    def prev_what(self, event = None):
        focus = self.focus_get()
        if focus == self.other_list:
            self.prev_list()
        else:
            self.prev_radio()

    def on_single(self,event = None):
        '''
        Determine which custom list is selected by mouse click
        '''
        try:
            self.list_indx = self.other_list.curselection()[0]
            self.other_list.selection_clear(0, tk.END)
            self.level_options.set(5)
            self.level_menu_choice()
            
        except IndexError:
            self.focus()
            self.level_menu_choice()

         
class Game(tk.Frame):
    '''
    The Actual Game, allow user to 'replay' if word is correctly guessed
    before guesses run out, keep score tallied for each contiguous game played.  Allow User to 'replay'
    If custom word being used despite win/loose condition.
    '''
    def __init__(self, parent, controller, level = None):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.score = 100
        self.score_bank = 0
        self.guesses = 6
        self.mask = None
        self.path = os.getcwd()
        self.pic_fn = self.path + r'\images\gallows\stage_{}.gif'
        self.used = []
        #GUI style constants
        self.masked_font = ("Comic Sans MS", 18)
        self.score_font = ("Comic Sans MS", 18)
        self.bg = 'cornflower blue'
        self.header_font = ('Courier', 14)
        self.header_bg = 'cornflower blue'
        self.header_fg = 'misty rose'
        #Button colors
        self.selector_color = 'steel blue'
        self.button_bg = 'slate blue'
        self.button_fg = 'orchid1'
        #label fg and Font
        self.label_color = 'misty rose'
        self.label_font = ("Comic Sans MS", 10)
        #Hint Field Colors
        self.field_fg = 'black'
        self.field_bg = 'bisque'
        self.disabled_bg = 'green'
        self.disabled_fg = 'light green'
        #Toplevel window styling
        self.top_bg = 'Aquamarine'
        self.top_label_color = 'black'
        self.top_button_bg = 'DarkTurquoise'
        self.top_button_fg = 'black'
        self.top_field_bg = 'pink'
        self.top_font = ('Courier', 12)

        #Frames
        self.container = tk.Frame(self, bg = self.bg)
        self.container.pack(fill = tk.BOTH, expand = tk.YES)
        self.container.rowconfigure(0, weight = 1)
        self.container.columnconfigure(0, weight = 1)
        self.create_widgets()
        
        
    def create_widgets(self):
        #The Canvas
        #The picture progression
        self.canvas_frame = tk.Frame(self.container,bg = self.bg)
        self.hash(self.canvas_frame)
        self.canvas_frame.grid(row = 0,
                               column = 0,
                               columnspan = 2)
        self.canvas = tk.Canvas(self.canvas_frame,
                                bg = self.bg,
                                width = 630,
                                height = 400)
        self.canvas.grid(row = 0, column = 0, columnspan = 3)
        #Gallows
        self.img = tk.PhotoImage(master = self.canvas,
                                 file = self.pic_fn.format(len(self.used)))
        fn = self.pic_fn.format(len(self.used))
        self.canvas.create_image(0,0, image = self.img, anchor = tk.NW)

        #Masked Word
        self.word_frame = tk.Frame(self.container, bg = self.bg)
        self.hash(self.word_frame)
        self.word_frame.grid(row = 1, column = 0,
                             columnspan = 2)
        self.masked_word = tk.Label(self.word_frame,
                                    text = None,
                                    font = self.masked_font,
                                    bg = self.bg)
        self.masked_word.grid(row = 0,
                              column = 2,
                              sticky = 'e')

        #Read Out
        #Read out display (Guessed letters, remaining guesses)
        self.read_out = tk.Frame(self.container, bg = self.bg)
        self.hash(self.read_out)
        self.read_out.grid(row = 2,
                           column = 0,
                           sticky = tk.W + tk.E)
        
        #List of wrong guesses
        self.guessed_label = tk.Label(self.read_out,
                                      font = self.label_font,
                                      bg = self.bg,
                                      fg = self.label_color,
                                      text = 'Guessed :')
        self.guessed_label.grid(row = 2,
                                column = 1,
                                sticky = tk.W)
        self.guessed = tk.Label(self.read_out,
                                text = self.used,
                                bg = self.bg,
                                font = self.label_font)
        self.guessed.grid(row = 3,
                          column = 1,
                          sticky = tk.W)
        #Remaining guesses counter
        self.remaining = tk.Label(self.read_out,
                                  bg = self.bg,
                                  fg = self.label_color,
                                  text = 'Guesses : {}'.format(self.guesses))
        self.remaining.grid(row = 4,
                            column = 1,
                            sticky = tk.W)
        #User input
        #Take user guess
        self.guess_frame = tk.Frame(self.container, bg = self.bg)
        self.hash(self.guess_frame)
        self.guess_frame.grid(row = 5,
                              column = 0,
                              sticky = tk.W)
        #User Guess Entry field
        self.entry_label = tk.Label(self.guess_frame,
                                    text = 'Guess a letter: ',
                                    bg = self.bg,
                                    fg = self.label_color,
                                    font = self.label_font)
        self.entry_label.grid(row = 1, column = 1)
        self.input = tk.Entry(self.guess_frame, width = 5, bd = 4)
        self.input.grid(row = 1, column = 2)


        #Word definition
        self.hint_frame = tk.Frame(self.container, bg = self.bg)
        self.hint_frame.grid(row = 2, column = 1,
                             rowspan = 3)
        self.hint = tk.Text(self.hint_frame,
                            font = self.label_font,
                            fg = self.field_fg,
                            bg= self.field_bg,
                            height = 4,
                            width = 55)
        self.hint.pack(side = tk.LEFT)
        #Hint Scrollbar
        self.hint_bar = tk.Scrollbar(self.hint_frame,
                                     command = self.hint.yview)
        self.hint.config(yscrollcommand = self.hint_bar.set)

        self.hint_bar.pack(side = tk.LEFT, fill = tk.Y)        

        #Buttons
        self.button_frame = tk.Frame(self.container, bg = self.bg)
        self.button_frame.grid(row = 6,
                               column = 0,
                               columnspan = 2,
                               sticky = 'ew')
        self.hash(self.button_frame)

        #Guess submit Button
        self.submit = tk.Button(self.button_frame,
                                text = 'Guess',
                                width = 8,
                                font = self.label_font,
                                fg = self.label_color,
                                bg = self.button_bg,
                                border = 4,
                                padx = 2,
                                pady = 2,
                                command = self.guess)
        self.submit.grid(row = 1,
                         column = 1,
                         sticky = tk.W)
        
        
        #Game Quit button
        self.back = tk.Button(self.button_frame,
                              text = 'Quit',
                              width = 8,
                              font = self.label_font,
                              fg = self.label_color,
                              bg = self.button_bg,
                              border = 4,
                              padx = 2,
                              pady = 2,
                              command = self.quit_game)
        self.back.grid(row = 1,
                       column = 3,
                       sticky = tk.E)

        #Game Score Display
        self.score_display = tk.Label(self.button_frame,
                                      text = "Score: {}".format(self.score),
                                      fg = 'yellow',
                                      bg = self.bg,
                                      font = self.score_font)

        self.score_display.grid(row = 1,
                                column = 2,
                                sticky = 'EW')
                                      

    ############################################################################
    #Game Frame PRIVATE FUNCS                                                 #
    ############################################################################
    def quit_game(self, event = None):
        '''
        Clear hint Text box, controller.word and masked word,
        return to Main menu.
        Bound to 'Escape' key
        '''
        self.controller.update_idletasks()
        self.keep_score()
        self.masked_word.config(text = '')
        self.hint.delete(1.0,tk.END)
        self.controller.show_frame("Main")

    def guess(self, event = None):
        '''
        Check for correct/valid guess, update masked word, guess counter,
        and guessed list if guess valid.
        Bound to 'Return' key
        '''
        self.controller.update_idletasks()
        word = self.controller.word.lower()
        try:
            char = self.input.get().strip().lower()
            if self.guesses > 0 and \
            char in string.ascii_lowercase and \
            len(char) == 1:
                self.input.delete(0, tk.END)
                #Check char not already guessed
                if char.upper() in self.used or char.upper() in self.mask:
                    self.input.delete(0, tk.END)
                #Correct Guess
                if char in word:
                    self.unmask_word(char, word)
                    self.masked_word.config(text = ' '.join(self.mask).upper())
                #Wrong Guess
                else:
                    if char.upper() not in self.used:
                        self.guesses -= 1
                        self.score -= 16
                        score = self.score + self.score_bank
                        self.score_display.config(text = "Score: {}".format(
                                                                       score))
                        self.remaining.config(text =  "Guesses: {}".format(
                                              self.guesses))
                        if self.guesses == 0:
                            self.masked_word.config(fg = 'red',
                                                    text = '{}'.format(self.controller.word))
                        self.used.append(char.upper())
                        self.guessed.config(text = (','.join(self.used)))
                        self.img.config(file = self.pic_fn.format(
                                                           len(self.used)))
                self.game_over()
            else:
                self.input.delete(0, tk.END)
        except TypeError:
            self.input.delete(0, tk.END)               
        
            
    def mask_word(self, word):
        '''
        Take word to be guessed and replace ALL letters with underscore
        '''
        letters = ['_' for i in word.strip()]
        for indx, char in enumerate(word):
            if char == '-' or char == ' ':
                letters[indx] = char
        self.mask = letters
        return '  '.join(letters)

    def unmask_word(self, char, word):
        '''
        Reveal all letters of word that == char
        '''
        for indx, letter in enumerate(word):
            if char.lower() == letter.lower():
                self.mask[indx] = char
                

    def word_hint(self, word):
        '''
        Return definition of masked word
        '''
        level = self.controller.level
        if level == 'other':
            hint = self.controller.custom_hint
        else:
            try:
                hint = self.controller.all_defs[self.controller.word.upper()]
            except KeyError:
                pass
            
        return hint
    
    def setup(self):
        '''
        Reset Game, called each time "Game" frame is raised
        '''
        self.img.config(file = self.pic_fn.format('0'))
        self.hint.config(state = tk.NORMAL)
        self.hint.delete(1.0, tk.END)
        self.input.config(state = tk.NORMAL)
        self.input.focus()
        self.used = []
        self.guesses = 6
        self.score = 100
        score = self.score + self.score_bank
        self.score_display.config(text = "Score: {}".format(score))
        self.input.delete(0, tk.END)
        self.remaining.config(font = self.label_font,
                              text =  "Guesses: {}".format(self.guesses))
        self.guessed.config(font = self.label_font,
                            text = self.used)
        masked = self.mask_word(self.controller.word)
        self.masked_word.config(text = masked, fg = 'black')
        self.hint.config(state = tk.NORMAL)
        self.hint.insert(1.0,'HINT :\n{}'.format(
            self.word_hint(self.controller.word)))
        self.hint.config(state = tk.DISABLED)
        self.controller.custom_hint = None
        

    def game_over(self):
        '''
        Check for win condition, prompt user to play again,
        if yes, game restarts with new word from same list and tallys score,
        if no, raise 'Main' frame
        '''
        self.controller.update_idletasks()
        game_over = False
        #If user correctly guesses word
        if '_' not in self.mask and self.guesses > 0:
            image_path = self.path + r'\images\win images'
            fn = random.choice(os.listdir(image_path))
            final_img = '{}\{}'.format(image_path, fn)
            game_over = True
            self.img.config(file = final_img)
            self.input.config(state = tk.DISABLED)
            self.score_bank += self.score
            
        #if user is out of guesses
        elif self.guesses == 0:
            image_path = self.path + r'\images\game over'
            fn = random.choice(os.listdir(image_path))
            final_img = '{}\{}'.format(image_path, fn)
            game_over = True
            self.score = 0
            #self.keep_score()
            self.score_bank = 0
            self.controller.after(2000, self.img.config(file = final_img))
            self.input.config(state = tk.DISABLED)
           
        if game_over:
            self.play_again()

    def play_again(self):
        '''
        Raise a top window to ask if player would like play again
        '''
        
        x = self.controller.winfo_rootx() + (self.controller.winfo_width() / 3)
        y = self.controller.winfo_rooty() + (self.controller.winfo_height() /10)
        again = top_wins.Custom_dialogue('Play Again...', 'Play Again?',
                                         font = self.label_font,
                                         bg = self.top_bg,
                                         label_color = self.top_label_color,
                                         field_bg = self.top_field_bg,
                                         button_bg = self.top_button_bg,
                                         button_fg = self.top_button_fg,
                                         x = x,
                                         y = y
                                         )
        confirm = again.confirm
        if confirm == 'yes':
            self.controller.word = self.controller.frames["Level"].get_word()
            if self.controller.word != None and len(self.controller.word) > 0:
                self.controller.show_frame('Game')
            else:
                self.controller.show_frame("Main")
            #self.score_display.config(text = 'Score: {}'.format(self.score))
        elif confirm == 'no':
            print("no replay")
            self.quit_game()
            
            
    def keep_score(self):
        '''
        Track and update top ten highscores, comparing users current score to
        list of known high scores. High Scores not kept for custom word games.
        '''
        if self.controller.level == "other":
            pass
        else:
            try:
                low_score = min(self.controller.high_scores,
                                key = itemgetter(1))[1]
            except ValueError:
                low_score = 0
            if self.score_bank > low_score or \
               len(self.controller.high_scores) < 10:
                #Get user name and create a tuple of (name, score) for high
                #score ,       cccccccccccccccclog
                x = self.controller.winfo_rootx() + \
                    (self.controller.winfo_width() / 3)

                y = self.controller.winfo_rooty() + \
                    (self.controller.winfo_height() / 7)
        
                new_record = top_wins.Single_entry("NEW RECORD",
                                                   "Your Name",
                                                   'Ok',
                                                   font = self.label_font,
                                                   bg = self.bg,
                                                   label_color = self.label_color,
                                                   field_bg = self.field_bg,
                                                   button_bg = self.button_bg,
                                                   button_fg = self.button_fg,
                                                   x = x,
                                                   y = y
                                                 )
                name = new_record.name
                if name != str(name):
                    name = 'Washington Irving'
                elif name == '':
                    name = 'Irving Washington'
                today = datetime.date.today()
                date = today.strftime("%b %d, %Y")
                record = (name, self.score_bank, self.controller.level, date)
                #Scores get sorted, clipped to top ten with
                #controller.score_dump()
                if self.score_bank > 0:
                    self.controller.high_scores.append(record)
                    self.controller.dump_scores()
        self.score_bank = 0
                

    def hash(self, frame):
        '''
        A 3x3 grid of rows and columns, row=2/col=2 is center of frame,
        soley used to adjust GUI layout
        '''
        for i in range(1,4):
            frame.rowconfigure(i, weight = 1)
            frame.columnconfigure(i, weight = 1)

    def on_single(self, event = None):
        '''
        Override keybinding assigned to "<Button-1>" in different frame
        '''
        pass     
                    
    
class View(tk.Frame):
    '''
    View Built-in vocab lists.  Allow user to see full list of vocab for each level and
    make edits to any definition.
    '''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #GUI Style constants
        self.bg = 'DarkTurquoise'
        self.header_font = ('Courier', 14)
        self.header_bg = self.bg
        self.header_fg = 'MediumBlue'
        #Button colors
        self.button_bg = 'teal'
        self.button_fg = 'white'
        #label fg and Font
        self.label_color = 'black'
        self.label_font = ('Courier', 10)
        self.field_bg = 'bisque'
        self.disabled_bg = 'green'
        self.disabled_fg = 'light green'
        #Toplevel window styling
        self.top_bg = 'royal blue'
        self.top_label_color = 'khaki1'
        self.top_button_bg = 'cornflower blue'
        self.top_button_fg = 'black'
        self.top_field_bg = 'pink'
        self.top_font = ('Courier', 12)

        self.controller = controller
        self.master = tk.Frame(self, bg = self.bg)
        self.master.rowconfigure(1, weight = 1)
        self.master.columnconfigure(0, weight = 1)
        self.master.columnconfigure(1, weight = 1)
        self.master.pack(fill =tk.BOTH, expand = 1)
        self.dic_fn = r'json\dictionary.jsn'
        self.vocab_fn = r'json\vocab.jsn'
        self.index = None
        self.word = ''
        self.entries = []
        self.create_widgets()
        #Fill list  box with vocab, default is 'easy' list
        self.get_list()
        self.display.config(state = tk.DISABLED)
        self.vocab_list.select_set(0)

    def create_widgets(self):
        #Frames
        #Radio Buttons
        self.radio_frame = tk.Frame(self.master,
                                    bg = self.bg)
        self.radio_frame.grid(row = 0,
                              column = 0,
                              columnspan = 2,
                              sticky =tk.W)
        #Vocab Listbox
        self.option_frame = tk.Frame(self.master,
                                     bg = self.bg,
                                     padx = 3)
        self.option_frame.grid(row = 1,
                               column = 0,
                               sticky = "news")
        #'Back', 'Define' buttons
        self.bottom_buttons = tk.Frame(self.master,
                                       bg = self.bg,
                                       padx = 3,
                                       pady = 3)
        self.bottom_buttons.grid(row = 2,
                                 column = 0,
                                 sticky = 'news',
                                 columnspan = 3)

        #Definition Display
        self.display_frame = tk.Frame(self.master,
                                      bg = self.bg)
        self.display_frame.columnconfigure(0, weight = 1)
        self.display_frame.rowconfigure(0, weight = 1)
        self.display_frame.grid(row = 0,
                                rowspan = 3,
                                column = 1)
        self.display_frame_buttons = tk.Frame(self.display_frame,
                                              bg = self.bg,
                                              pady = 3)
        self.display_frame_buttons.columnconfigure(0, weight = 1)
        self.display_frame_buttons.rowconfigure(0, weight = 1)
        self.display_frame_buttons.pack(side = tk.BOTTOM, anchor = 'w')
        
        #Radiobuttons, determine which list to view
        self.view_options = tk.IntVar()
        self.view_options.set(1)
        #Easy List
        self.easy_list = tk.Radiobutton(self.radio_frame,
                                        text = 'Easy',
                                        font = self.label_font,
                                        fg = self.label_color,
                                        bg = self.bg,
                                        variable = self.view_options,
                                        value = 1,
                                        command = self.get_list)
        self.easy_list.pack(side = tk.LEFT, anchor = tk.NW)
        #Normal List
        self.normal_list = tk.Radiobutton(self.radio_frame,
                                          text = 'Normal',
                                          font = self.label_font,
                                          fg = self.label_color,
                                          bg = self.bg,
                                          variable = self.view_options,
                                          value = 2,
                                        command = self.get_list)
        self.normal_list.pack(side = tk.LEFT,anchor = tk.NW)
        #Hard List
        self.hard_list = tk.Radiobutton(self.radio_frame,
                                        text = 'Hard',
                                        font = self.label_font,
                                        fg = self.label_color,
                                        bg = self.bg,
                                        variable = self.view_options,
                                        value = 3,
                                        command = self.get_list)
        self.hard_list.pack(side = tk.LEFT,anchor = tk.NW)
        #Extreme List
        self.extreme_list = tk.Radiobutton(self.radio_frame,
                                           text = 'Extreme',
                                           font = self.label_font,
                                           fg = self.label_color,
                                           bg = self.bg,
                                           variable = self.view_options,
                                           value = 4,
                                           command = self.get_list)
        self.extreme_list.pack(side = tk.LEFT, anchor = tk.NW)
        
        #Listbox
        self.vocab_list = tk.Listbox(self.option_frame,
                                     bg = self.field_bg)
        for index, option in enumerate(self.entries):
            self.options.insert(index, option)
        self.vocab_list.pack(side = tk.LEFT,
                          anchor = tk.NW,
                          fill = tk.BOTH,
                          expand = 1)

        #List Scrollbar
        self.list_bar = tk.Scrollbar(self.option_frame,
                                  command = self.vocab_list.yview)
        self.vocab_list.config(yscrollcommand = self.list_bar.set)
        self.list_bar.pack(side = tk.LEFT,
                           fill = tk.Y)
        #Buttons
        #Level Menu back button
        self.back = tk.Button(self.bottom_buttons,
                              text = '<< Back',
                              font = self.label_font,
                              fg = self.button_fg,
                              bg = self.button_bg,
                              width = 8,
                              border = 4,
                              padx = 2,
                              pady = 2,
                              command = self.to_main)
                              
        self.back.pack(side = tk.LEFT,
                       anchor = tk.SW)
    
        #Vocab Define button
        self.submit = tk.Button(self.bottom_buttons,
                                text = 'Define',
                                font = self.label_font,
                                fg = self.button_fg,
                                bg = self.button_bg,
                                width = 8,
                                border = 4,
                                padx = 2,
                                pady = 2,
                                command = self.define)
        self.submit.pack(side = tk.LEFT,
                         anchor = tk.SW)
        #Vocab Delete button
        self.delete_word = tk.Button(self.bottom_buttons,
                                     text = "Delete",
                                     font = self.label_font,
                                     fg = self.button_fg,
                                     bg = self.button_bg,
                                     width = 8,
                                     border = 4,
                                     padx = 2,
                                     pady = 2,
                                     command = self.delete)
        self.delete_word.pack(side = tk.RIGHT, anchor = tk.SW)

        #Total number of words in list
        self.total = tk.Label(self.bottom_buttons,
                              text = None,
                              font = self.label_font,
                              fg = self.label_color,
                              bg = self.bg)
                              
        self.total.pack()
        
        #Def/Hint Display
        self.display = tk.Text(self.display_frame,
                               bg = self.field_bg,
                               font = self.label_font,
                               wrap = tk.WORD,
                               width =50)
        self.display.pack(side = tk.TOP, fill= tk.BOTH, expand =1)
        #Edit/submit buttons
        self.edit_def = tk.Button(self.display_frame_buttons,
                                  text = 'Edit',
                                  font = self.label_font,
                                  fg = self.button_fg,
                                  bg = self.button_bg,
                                  width = 8,
                                  border = 4,
                                  padx = 2,
                                  pady = 2,
                                  command = self.edit)
        self.edit_def.pack(side = tk.LEFT, anchor = tk.N)
        
        self.submit_edit = tk.Button(self.display_frame_buttons,
                                     text = 'Submit',
                                     font = self.label_font,
                                     fg = self.button_fg,
                                     bg = self.button_bg,
                                     width = 8,
                                     border = 4,
                                     padx = 2,
                                     pady = 2,
                                     command = self.commit)
        self.submit_edit.pack(side = tk.LEFT, anchor = tk.N)


    ############################################################################
    #View Frame Functions                                                     #
    ############################################################################         
    def get_list(self):
        """
        Return voacab list corrosponding to Radio button selection
        """
        vocab_level = self.view_options.get()
        words = self.controller.load_vocab()
  
        #Clear listbox and insert list of words, default is 'easy' list
        self.vocab_list.delete(0, 'end')
        if vocab_level == 1:
            self.list_name = 'easy'
            self.vocab = words['easy']
            for index, word in enumerate(sorted(self.vocab)):
                self.vocab_list.insert(index, word.title())
            
        elif vocab_level == 2:
            self.list_name = 'normal'
            self.vocab = words['normal']
            for index, word in enumerate(sorted(self.vocab)):
                self.vocab_list.insert(index, word.title())
                                
        elif vocab_level == 3:
            self.list_name = 'hard'
            self.vocab = words['hard']
            for index, word in enumerate(sorted(self.vocab)):
                self.vocab_list.insert(index, word.title())
                                
        elif vocab_level == 4:
            self.list_name = 'extreme'
            self.vocab = words['extreme']
            for index, word in enumerate(sorted(self.vocab)):
                self.vocab_list.insert(index, word.title())
        try:
            self.vocab_list.see(self.indx)
        except AttributeError:
            self.vocab_list.select_set(0)
        
    def to_main(self, event = None):
        '''
        Return to Main Menu
        '''
        self.controller.show_frame("Main")
        
    def define(self, event = None):
        '''
        Clear any existing text from Definition Textbox, insert definition/hint of
        selected word.
        '''
        #The word and its definition
        self.indx = self.vocab_list.curselection()[0]
        self.word = sorted(self.vocab)[self.indx].upper()
        definition = self.controller.all_defs[self.word]
        
        #display word x of y
        self.total.config(text = '\n Word: {} of {}'.format(
                         (self.indx + 1), len(self.vocab)))
        
        #Clear Text Box of existing text if any
        self.display.config(state = tk.NORMAL)
        self.display.delete(1.0,tk.END)
        
        #Insert desired Definition
        self.display.insert(tk.INSERT, '"{}"'.format(self.word))
        self.display.insert(tk.INSERT, "\n\nDefinition:\n\n{}".format(definition))
        self.display.config(state = tk.DISABLED)
        lines = int(self.display.index('end-1c').split('.')[0])
            
    def edit(self, event = None):
        '''
        Activate Definition Display Textbox, allow user to edit text
        '''
        self.display.config(bg = 'white')
        self.display.config(state = tk.NORMAL)

    def delete(self, event = None):
        '''
        Allow User to delete individual word from built in list
        '''
        self.display.config(state = tk.NORMAL)
        self.display.delete(1.0, tk.END)
        self.display.config(state = tk.DISABLED)
       
        vocab_list = self.view_options.get()
        self.indx = self.vocab_list.curselection()[0]
        self.word = sorted(self.vocab)[self.indx].upper()
        self.display.delete(1.0, tk.END)
        self.controller.all_vocab[self.list_name].remove(self.word)
        self.controller.all_defs.pop(self.word, None)
        self.controller.dump_defs()
        self.controller.dump_vocab()
        self.get_list()
       

    def commit(self, event = None):
        '''
        Deactivate Definition Display Textbox, push edited Definition/Hint to
        json dictionary
        '''
        try:
            new_def = self.display.get(5.0, tk.END)
            self.display.config(state = tk.DISABLED)
            self.controller.all_defs[self.word] = new_def
            self.controller.dump_defs()

        except TypeError:
            pass  
    
    ###########################################################################
    #KEY BINDINGS                                                             #
    ###########################################################################
    def next_list_option(self, event = None):
        '''
        Select Next Radio Button
        '''
        option = self.view_options.get()
        option += 1
        if option > 4:
            option = 1
        self.view_options.set(option)
        self.indx = 0
        self.get_list()
        
    def prev_list_option(self, event = None):
        '''
        Select Previous Radio Button
        '''
        option = self.view_options.get()
        option -= 1
        if option < 1:
            option = 4
        self.view_options.set(option)
        self.indx = 0
        self.get_list()

    def next_vocab_option(self, event = None):
        '''
        Select next word in List box
        '''
        word_indx = self.vocab_list.curselection()[0]
        self.vocab_list.selection_clear(0, tk.END)
        select = self.vocab_list.select_set(word_indx)
        self.define()
    
    def prev_vocab_option(self, event = None):
        '''
        Select previous word in List Box
        '''
        word_indx = self.vocab_list.curselection()[0]
        self.vocab_list.selection_clear(0, tk.END)
        word_indx -= 1
        self.vocab_list.select_set(word_indx)
        self.define()

class List_editor(tk.Frame):
    '''
    A page to allow user to view, edit and create custom Vocab lists
    '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        #GUI Style constants
        self.bg = 'coral1'
        #Button colors
        self.button_bg = 'orchid3'
        self.button_fg = 'white'
        #label fg and Font
        self.label_color = 'white'
        self.label_font = ('Courier', 12)
        self.field_bg = 'orchid1'
        self.disabled_bg = 'plum4'
        self.disabled_fg = self.button_bg
        #Header
        self.header_font = ('Courier', 14)
        self.header_bg = self.bg
        self.header_fg = self.label_color
        #Toplevel window styling
        self.top_bg = 'light blue'
        self.top_label_color = 'black'
        self.top_button_bg = 'MediumPurple1'
        self.top_button_fg = 'black'
        self.top_font = ('Courier', 12)

        self.controller = controller
        self.master = tk.Frame(self, bg = self.bg)
        self.master.rowconfigure(1, weight = 1)
        self.master.columnconfigure(0, weight = 1)
        self.master.columnconfigure(1, weight = 1)
        self.master.pack(fill =tk.BOTH, expand = 1)
        #Json file names
        self.dic_fn = 'dictionary.json'
        self.vocab_fn = 'vocab.jsn'
        #Vules to track and share between functions
        self.index = None
        self.list_name = None
        self.topLevel = False     
        self.word = None
        self.create_widgets()
        self.input.focus()
        self.populate_custom_lists()
        
    def create_widgets(self):
        #Custom Entry field
        self.entry_frame = tk.Frame(self.master,bd = 5, bg = self.bg)
        self.entry_frame.grid(row = 0,
                              column = 0,
                              columnspan = 3,
                              sticky = 'w')
        for n in range(3):
            self.entry_frame.grid_rowconfigure(n, weight = 1)
            self.entry_frame.grid_columnconfigure(n, weight = 1)

        #New dict name entry box w/ label and submit button
        self.input = tk.Entry(self.entry_frame,
                              bd = 3,
                              bg = self.field_bg)

        self.input.grid(row = 0,
                        column = 0)
        self.input_label = tk.Label(self.entry_frame,
                                    font = self.label_font,
                                    text = 'New List Name',
                                    bg = self.bg,
                                    fg = self.label_color)
        self.input_label.grid(row = 1,
                              column = 0)
        self.input_submit = tk.Button(self.entry_frame,
                                      text = 'Create',
                                      underline = 1,
                                      width = 8,
                                      bg = self.button_bg,
                                      fg = self.button_fg,
                                      bd = 2,
                                      padx = 2,
                                      pady = 2,
                                      command = self.create_list)
        self.input_submit.grid(row = 2,
                               column = 0,
                               columnspan = 2,
                               sticky = tk.W)

        #Cust Dicts Listbox
        self.cust_dicts_frame = tk.Frame(self.master, bd = 5, bg = self.bg)
        self.cust_dicts_frame.grid(row = 2,
                               column = 0,
                               sticky = 'nsw')
        self.spacer_line = tk.Label(self.cust_dicts_frame,
                                    text = '_'*40,
                                    bg = self.bg,
                                    fg = self.label_color)
        self.spacer_line.pack(side = tk.TOP,
                              anchor = 'nw')
        self.dict_list_label = tk.Label(self.cust_dicts_frame,
                                        font = self.label_font,
                                        text = "Custom Lists",
                                        bg = self.bg,
                                        fg = self.label_color)
        self.dict_list_label.pack(side = tk.TOP,
                                  anchor = 'nw')
        #Listbox of Lists Names
        self.list_names = tk.Listbox(self.cust_dicts_frame,
                                    height = 8,
                                    bg = self.field_bg,
                                     selectbackground = self.field_bg,
                                     selectforeground = 'black')
    
        self.list_names.pack(side = tk.LEFT,
                            anchor = tk.W,
                            fill = tk.BOTH,
                            expand = 1)
        #List names buttons, 'Edit', 'Delete'
        self.dicts_frame_butt = tk.Frame(self.master, bd = 5, bg = self.bg)
        self.dicts_frame_butt.grid(row = 3,
                                   column = 0,
                                   sticky = 'w')
        self.delete_dict = tk.Button(self.dicts_frame_butt,
                                     text = "Edit",
                                     underline = 0,
                                     width = 8,
                                     bg = self.button_bg,
                                     fg = self.button_fg,
                                     command = self.edit_list)

        self.delete_dict.pack(side = tk.LEFT,
                              anchor = tk.NW)
        self.delete_dict = tk.Button(self.dicts_frame_butt,
                                     text = "Delete",
                                     underline = 0,
                                     width = 8,
                                     bg = self.button_bg,
                                     fg = self.button_fg,
                                     command = self.delete_list)
        self.delete_dict.pack(side = tk.LEFT,
                              anchor = tk.NW)

        #Dict list Scrollbar
        self.dict_bar = tk.Scrollbar(self.cust_dicts_frame,
                                     command = self.list_names.yview)
        self.list_names.config(yscrollcommand = self.dict_bar.set)
        self.dict_bar.pack(side = tk.LEFT,
                           fill = tk.Y)
        
        #Vocab Listbox
        self.vocab_frame = tk.Frame(self.master, bd = 5, bg = self.bg)
        self.vocab_frame.grid(row = 4,
                               column = 0,
                               sticky = 'nws')
        msg = 'Vocabulary List: {}'.format(self.list_name)
        self.spacer_line = tk.Label(self.vocab_frame,
                                    text = '_'*(2*len(msg)),
                                    bg = self.bg,
                                    fg = self.label_color)
        self.spacer_line.pack(side = tk.TOP,
                              anchor = 'nw')
        self.vocab_list_label = tk.Label(self.vocab_frame,
                                         font = self.label_font,
                                         text = msg,
                                         bg = self.bg,
                                         fg = self.label_color)
        self.vocab_list_label.pack(side = tk.TOP,
                                   anchor = 'nw')
        self.vocab_list = tk.Listbox(self.vocab_frame,
                                     height = 12,
                                     bg = self.field_bg,
                                     selectbackground = self.field_bg,
                                     selectforeground = 'black')

        self.vocab_list.pack(side = tk.LEFT,
                             anchor = tk.NW,
                             fill =tk.BOTH,
                             expand = 1)

        #Vocab list Scrollbar
        self.vocab_bar = tk.Scrollbar(self.vocab_frame,
                                      command = self.vocab_list.yview,
                                      bg = self.field_bg)
        self.vocab_list.config(yscrollcommand = self.vocab_bar.set)
        self.vocab_bar.pack(side = tk.LEFT,
                           fill = tk.Y)

        #Vocab List buttons
        self.vocab_list_buttons = tk.Frame(self.master,
                                           bd = 5,
                                           bg = self.bg)
        self.vocab_list_buttons.columnconfigure(0, weight = 1)
        self.vocab_list_buttons.grid(row = 5,
                                     column = 0,
                                     sticky = 'news')

        #Edit
        self.edit_vocab = tk.Button(self.vocab_list_buttons,
                                    text = 'Edit',
                                    underline = 0,
                                    width = 8,
                                    padx = 2,
                                    pady = 2,
                                    bg = self.button_bg,
                                    fg = self.button_fg,
                                    command = self.edit_word)
                              
        self.edit_vocab.pack(side = tk.LEFT)
       
   
        #Delete
        self.define = tk.Button(self.vocab_list_buttons,
                                text = 'Delete',
                                underline = 0,
                                width = 8,
                                padx = 2,
                                pady = 2,
                                bg = self.button_bg,
                                fg = self.button_fg,
                                command = lambda: self.delete_word(self.word))
        self.define.pack(side = tk.LEFT)
       

        #Mutlit_purpose readout label
        self.readout_frame = tk.Frame(self.master)
        self.readout_frame.grid(row = 5,
                              column = 1)
        self.read_out = tk.Label(self.readout_frame,
                              text = ' '*15,
                              font = self.label_font,
                              bg = self.bg)
                              
       
        self.read_out.grid(row = 0,
                        column = 2,
                        sticky = "E")
        
        #New Word Entry Frame
        self.new_word_frame = tk.Frame(self.master, bd = 5, bg = self.bg)
        self.new_word_frame.columnconfigure(0, weight = 1)
        self.new_word_frame.rowconfigure(0, weight = 1)
        self.new_word_frame.grid(row = 0,
                                 column = 1,
                                 sticky = 'NW')
        #New Word Entry Field w/ label
        self.word_entry = tk.Entry(self.new_word_frame,
                                   state = tk.DISABLED,
                                   bg = self.field_bg,
                                   disabledbackground = self.disabled_bg)
        self.word_entry.grid(row = 0,
                             column = 0,
                             sticky = 'NW')
        self.word_label = tk.Label(self.new_word_frame,
                                   font = self.label_font,
                                   text = 'New Word',
                                   bg = self.bg,
                                   fg = self.label_color)
        self.word_label.grid(row = 1,
                             column = 0,
                             sticky = 'NW',
                             rowspan = 2,
                             columnspan = 3)
        
        #Definition Display
        self.display_frame = tk.Frame(self.master, bd = 5, bg = self.bg)
        self.display_frame.columnconfigure(0, weight = 1)
        self.display_frame.rowconfigure(1, weight = 1)
        self.display_frame.grid(row = 1,
                                rowspan = 4,
                                column = 1,
                                columnspan = 2,
                                sticky = 'NWE')

        #Hint Label
        self.hint_label = tk.Label(self.display_frame,
                                   font = self.label_font,
                                   text = "HINT:",
                                   bg = self.bg,
                                   fg = self.label_color)
        self.hint_label.grid(row = 0,
                             column = 0,
                             sticky = 'NW')
        
        #Def/Hint Display
        self.hint = tk.Text(self.display_frame,
                            bd = 2,
                            bg = self.disabled_bg,   
                            wrap = tk.WORD,
                            padx = 2,
                            pady = 2,
                            width =45,
                            height = 25,
                            state = tk.DISABLED)
        self.hint.grid(row = 1,
                          column = 0,
                          sticky = 'NWE')
        #Edit/submit buttons
        self.submit_button_frame = tk.Frame(self.display_frame, bg = self.bg)
        self.submit_button_frame.grid(row = 2,
                                      column = 0,
                                      pady = 4,
                                      sticky = 'NW')
        self.edit_def = tk.Button(self.submit_button_frame,
                                  text = 'Ok',
                                  underline = 0,
                                  width = 8,
                                  border = 4,
                                  padx = 2,
                                  pady = 2,
                                  disabledforeground = self.disabled_fg,
                                  bg = self.button_bg,
                                  fg = self.button_fg,
                                  command = self.add_word,
                                  state = tk.DISABLED)
        self.edit_def.grid(row = 2,
                           column = 0,
                           sticky = 'NW')

        self.exit_frame = tk.Frame(self.master,
                                   bd = 2,
                                   bg = self.bg)
        self.exit_frame.grid(row = 5,
                             column = 2)
        self.back_button = tk.Button(self.exit_frame,
                                     bd = 2,
                                     bg = self.button_bg,
                                     fg = self.button_fg,
                                     width = 8,
                                     padx = 2,
                                     pady = 2,
                                     text = '<< Back',
                                     command = self.to_main)
        self.back_button.grid(row = 0,
                              column = 0)

    ############################################################################
    #List editor Private Functions                                             #
    ############################################################################
    def populate_custom_lists(self):
        '''
        Populate Custom Dictionary listbox, with any known custom dictionaries,
        '''
        custom_lists = []
        self.list_names.delete(0, tk.END)
        
        for list_name, vocab_list in self.controller.load_vocab().items():
            if list_name not in ('easy', 'normal', 'hard', 'extreme'):
                custom_lists.append(list_name)
            
        for indx, key in enumerate(sorted(custom_lists)):
            self.list_names.insert(indx, key)
            
    def populate_custom_vocab(self, list_name):
        '''
        Populate Custom Vocabulary of selected list
        '''
        self.vocab_list.delete(0, tk.END)
        vocab = self.controller.load_vocab()
        for indx, word in enumerate(sorted(vocab[list_name])):
            self.vocab_list.insert(indx, word)
 
    def create_list(self):
        '''
        Create a new dict and write it to existing json file
        '''
        self.input_label.config(fg = self.label_color)
        list_name = self.input.get()
        if list_name in self.controller.all_vocab.keys():
            self.input_label.config(fg = 'red')
        elif list_name != '':
            self.controller.all_vocab[list_name] = []
            self.input.delete(0, tk.END)
            self.controller.dump_vocab()
            self.populate_custom_lists()
            self.word_entry.config(state = tk.NORMAL)
            self.hint.config(state = tk.NORMAL,
                             bg = self.field_bg)
            self.edit_def.config(state = tk.NORMAL,
                                 fg = self.button_fg)
            self.list_name = list_name
            #Clear fields
            self.word_entry.delete(0, tk.END)
            self.hint.delete(1.0, tk.END)
            #Update Vocab Listbox
            self.populate_custom_vocab(self.list_name)
            self.word_entry.focus()
            #Update readout
            self.read_out.config(text = 'Created List: {}'.format(list_name))
            #Update vocab list box label
            msg = 'Vocabulary List: {}'.format(self.list_name)

            #If len(msg) exceedes header length, extend header
            if len(msg) > 45:
                text = '{}\n{}\n{}'.format('_'*len(msg),
                                           ' '*36 + '\nHANGMAN\n' + ' '*36,
                                           '_'*len(msg))
                self.controller.header.config(text = text)
               
            self.spacer_line.config(text = '_'*(2*len(msg)))
            self.vocab_list_label.config(text = msg)
                
    def edit_list(self):
        '''
        Get selected Vocab list name from custom list Textbox, populate custom
        vocab list box with list's words, activate word entry and hint display
        fields.
        '''
        try:
            list_indx = self.list_names.curselection()[0]
        except IndexError:
            list_indx = 0
        self.list_name = self.list_names.get(list_indx)
        self.word_entry.config(state = tk.NORMAL)
        self.hint.config(state = tk.NORMAL,
                         bg = self.field_bg)
        self.edit_def.config(state = tk.NORMAL,
                             fg = self.button_fg)
        #Clear fields
        self.word_entry.delete(0, tk.END)
        self.hint.delete(1.0, tk.END)
        #Update Vocab Listbox
        self.populate_custom_vocab(self.list_name)
        #Update readout
        self.read_out.config(text = 'Editing List: {}'.format(self.list_name))
        #Update vocab list box label
        msg = 'Vocabulary List: {}'.format(self.list_name)

        #If len(msg) exceedes header length, extend header
        if len(msg) > 45:
            text = '{}\n{}\n{}'.format('_'*len(msg),
                                       ' '*36 + '\nHANGMAN\n' + ' '*36,
                                       '_'*len(msg))
            self.controller.header.config(text = text)
            
        self.spacer_line.config(text = '_'*(2*len(msg)))
        self.vocab_list_label.config(text = msg)
        self.word_entry.focus()
        
    def delete_list(self):
        '''
        Delete a Custom word list, Toplevel window prompts confirmation of delete
        '''
        try:
            list_indx = self.list_names.curselection()[0]
            list_name = self.list_names.get(list_indx)
        except IndexError:
            self.list_names.selection_set(0)
            list_indx = self.list_names.curselection()[0]
            list_name = self.list_names.get(list_indx)
            
        #Top window confirmation of list delete
        msg = "Delete List: {}".format(list_name)
        if  not self.topLevel:
            self.topLevel = True
            x = self.controller.winfo_rootx() + (self.controller.winfo_width() / 3)
            y = self.controller.winfo_rooty() + (self.controller.winfo_height() / 3)
            delete = top_wins.Custom_dialogue("Confirm Delete", msg,
                                              font = self.label_font,
                                              bg = self.top_bg,
                                              label_bg = self.top_bg,
                                              label_color = self.top_label_color,
                                              button_bg = self.top_button_bg,
                                              button_fg = self.top_button_fg,
                                              x = x,
                                              y = y)
            self.topLevel = False
            if delete.confirm == 'yes':
                try:
                    self.controller.all_vocab.pop(list_name)
                    self.controller.dump_vocab()
                    self.populate_custom_lists()
                    #Update readout
                    self.read_out.config(text = 'Deleted List: {}'.format(
                                                                   list_name))
                except KeyError:
                    pass
        else:
            pass
    
    def add_word(self):
        '''
        Get new word from entry field input, and any description provided
        in display textboc, update Vocab listbox
        '''
        new_word = self.word_entry.get().upper()
        hint = self.hint.get(1.0, tk.END).strip()

        if new_word != '':

            if new_word not in self.controller.all_vocab[self.list_name]:
                self.controller.all_vocab[self.list_name].append(new_word)

            #Define/redefine word in dict of defs
            self.controller.all_defs[new_word] = hint
            #Update Vocab and Hints
            self.controller.dump_vocab()
            self.controller.dump_defs()
            #Clear fields
            self.word_entry.delete(0, tk.END)
            self.hint.delete(1.0, tk.END)
            #Update Vocab Listbox
            self.populate_custom_vocab(self.list_name)
            self.word_entry.focus()
            #ALter Read out
            self.read_out.config(text = "Added Word: {}".format(new_word))
            
        
    def edit_word(self):
        '''
        Insert selected word into 'new word' entry field and corrosponding word hint/
        definition into Hint Textbox object, allow user to alter word and/or
        Hint and save changes in place, if word is altered, new entry is created
        '''
        hints = self.controller.load_defs()
        try:
            word_indx = self.vocab_list.curselection()[0]
        except IndexError:
            word_indx = 0
        try:
            word = self.vocab_list.get(word_indx)
        except ValueError:
            pass
        self.word_entry.delete(0, tk.END)
        self.hint.delete(1.0, tk.END)
        hint = hints[word]
        self.word_entry.insert(0,word)
        self.hint.insert(tk.INSERT, hint)
        
        #display word index of total words (formated for users)
        msg = 'List: {}  Word: {} of {}'
        self.read_out.config(font = self.label_font,
                             text = msg.format(
                             self.list_name,
                             (word_indx + 1),
                             len(self.controller.all_vocab[self.list_name])))
        self.hint.focus()
            
     
    def delete_word(self, word = None, event = None):
        '''
        Delete a single word from a populated Listbox object, update listbox entries
        '''
        try:
            word_indx = self.vocab_list.curselection()[0]
        except IndexError:
            word_indx = 0
        word = self.vocab_list.get(word_indx)
        vocab = self.controller.load_vocab()
        if word in vocab[self.list_name]:
            vocab[self.list_name].remove(word)
            self.controller.dump_vocab(vocab = vocab)
        
            self.populate_custom_vocab(self.list_name)
                
    
        
               
    def to_main(self, event = None):
        '''
        Return to Main Menu
        '''
        self.controller.show_frame("Main")
        self.word_entry.delete(0, tk.END)
        self.word_entry.config(state = tk.DISABLED)
        self.hint.delete(1.0, tk.END)
        self.hint.config(state = tk.DISABLED, bg = self.disabled_bg)
        self.edit_def.config(state = tk.DISABLED)
        self.input.focus()
        
    ###########################################################################
    #KEY BINDINGS                                                             #
    ###########################################################################
    def return_what(self, event = None):
        '''
        Performs action when user presses "Enter/Return" according to what
        widget has focus
        '''
        focus = self.controller.focus_get()
        if focus == self.input:
            self.create_list()
        elif focus == self.list_names:
            self.edit_list()
        elif focus == self.vocab_list:
            self.edit_word()
        elif focus == self.word_entry:
            self.hint.focus()
        else:
            pass
        
    def edit_what(self, event = None):
        '''
        Edit either list or word, depending on which widget has focus
        '''
        focus = self.controller.focus_get()
        if focus == self.list_names:
            self.edit_list()
        elif focus == self.vocab_list:
            self.edit_word()
        else:
            pass
        
    def delete_what(self, event = None):
        '''
        Delete an entire list or a word from a list, depending on which widget
        has focus
        '''
        focus = self.controller.focus_get()
        if focus == self.list_names:
            print("LIST NAME")
            self.delete_list()
        elif focus == self.vocab_list:
            print("VOCAB")
            self.delete_word()
        else:
            pass
    def focus_next_(self, event = None):
        '''
        Override Textbox's built in binding for 'Tab', move to next widget
        instead of performing an indent
        '''
        print("Focus Next")
        focus = self.controller.focus_get()
        print(focus)
        if focus == self.hint:
            print('FOCUS ON HINT')
            event.tk_focusNext().focus()
            return("break")
        else:
            print('NO FOCUS')

'''
app = Hangman_shell()
#Open Game in approximate middle of screen,
x = app.winfo_screenwidth() // 3
y = 20
app.geometry("+%d+%d" % (x,y))


app.mainloop()
'''
if __name__ == '__main__':
    pass

