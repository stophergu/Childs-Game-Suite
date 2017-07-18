import tkinter as tk
from tkinter import ttk
import hangman, matchgame

class Master_frame(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.master_shell = tk.Frame(self)
        self.master_shell.pack()

        self.games = {}
        for GAME in (Main_game_master,
                     hangman.Hangman_shell,
                     matchgame.Match_game_shell
                     ):
            page_name = GAME.__name__
            frame = GAME(parent = self.master_shell, controller = self)
            self.games[page_name] = frame

            frame.grid(row = 0, column = 0, sticky = 'news')
        self.show_frame("Main_game_master")
        

    def __str__(self):
        return 'Master Game Controller'

    def show_frame(self, page_name):
        '''
        Raise page_name to top of stack
        '''
        frame = self.games[page_name]
        
        ##########################################################################
        #                           KEY BINDINGS                                 #
        ##########################################################################

        ###############
        #Front Page   #
        ###############
        if page_name == 'Main_game_master':
            self.bind("<Escape>", self.quit)
            self.bind("<Return>", self.override_bind)
            self.bind("<Down>", self.override_bind)
            self.bind("<Up>", self.override_bind)
            self.bind("<Button-1>", self.override_bind)
        ###############
        #Hangman      #
        ###############
        elif page_name == 'Hangman_shell':
            self.bind('<Escape>', lambda x: self.show_frame('Main_game_master'))
            self.bind("<Return>", frame.frames['Main'].menu_choice)
            self.bind("<Down>", frame.frames['Main'].next_option)
            self.bind("<Up>", frame.frames['Main'].prev_option)
            self.bind("<Button-1>", self.override_bind)
        ###############
        #Match Game   #    
        ###############
        elif page_name == 'Match_game_shell':
            self.bind('<Escape>', lambda x: self.show_frame('Main_game_master'))
            self.bind('<Return>', frame.frames['Match_main'].menu_choice)
            self.bind("<Down>", frame.frames['Match_main'].next_option)
            self.bind("<Up>", frame.frames['Match_main'].prev_option)
            self.bind("<Button-1>",self.override_bind)
        frame.tkraise()

    def quit(self, *args):
        self.destroy()

    def override_bind(self, event = None):
        pass

class Main_game_master(tk.Frame):
    '''
    A Frame of Buttons used to call Various other Frames, Secondary Frames are
    raised when corrosponding button is pressed by user, Master_frame is raised
    when secondary frame is closed
    '''
    def __init__(self, parent, controller):
        
        #GUI Styling
        self.bg = 'plum2'
        #self.button_bg = 'MediumOrchid4'
        self.button_bg = 'grey'
        self.button_fg =  'cyan2'
        self.button_highlight = 'cyan2'
        self.header_fg = 'dark slate blue'
        self.header_font = ('Comic Sans MS', 18)
        self.button_font = ('Comic Sans MS', 12)
        self.button_width = 25
        self.button_border = 10
        #Everything Else
        self.controller = controller
        tk.Frame.__init__(self, parent, bg = self.bg)
        self.main_frame = tk.Frame(self, bg = self.bg)
        self.main_frame.pack()
        self.create_widgets()
        self.HANGMAN.focus()
    def create_widgets(self):
        #Main Header
        self.header = tk.Label(self.main_frame,
                               text = '{}\n{}\n{}'.format(
                                   '_'*42,
                                   ' '*25 + "Madison's Game Suite" + ' '*25,
                                   '_'*42),
                               font = self.header_font,
                               bg = self.bg,
                               fg = self.header_fg)
        self.header.grid(row = 0, column = 0)

        ##############
        #Game Links: #
        ##############
        self.game_links = tk.Frame(self.main_frame, bg = self.bg)
        self.game_links.grid(row = 1, column = 0)
        ##############
        #Column 1    #
        ##############
        #Hangman Button
        self.HANGMAN = tk.Button(self.game_links,
                                 text = 'Hangman',
                                 font = self.button_font,
                                 width = self.button_width,
                                 bg = self.button_bg,
                                 fg = self.button_fg,
                                 highlightcolor = self.button_highlight,
                                 highlightthickness = 2,
                                 bd = self.button_border,
                                 relief  = 'raised',
                                 command = self.raise_hangman)
        self.HANGMAN.grid(row = 0, column = 0)
       
        #Matchgame Button
        self.MATCHGAME = tk.Button(self.game_links,
                                   text = 'Match Game',
                                   font = self.button_font,
                                   width = self.button_width,
                                   bg = self.button_bg,
                                   fg = self.button_fg,
                                   highlightcolor = self.button_highlight,                                   
                                   bd = self.button_border,
                                   relief = 'raised',
                                   command = self.raise_matchgame)
        self.MATCHGAME.grid(row = 1, column = 0)

        #############
        #Column 2   #
        #############
        #Blanks for spacing and visual cue
        self.BLANK_1 = tk.Button(self.game_links,
                                 text = '',
                                 font = self.button_font,
                                 width = self.button_width,
                                 bd = self.button_border,
                                 bg = self.button_bg,
                                 fg = self.button_fg,
                                 highlightcolor = self.button_highlight,
                                 relief = 'raised',
                                 state = tk.DISABLED)
        self.BLANK_1.grid(row = 0, column = 1)

        self.BLANK_2 = tk.Button(self.game_links,
                                 text = '',
                                 font = self.button_font,
                                 width = self.button_width,
                                 bd = self.button_border,
                                 bg = self.button_bg,
                                 fg = self.button_fg,
                                 highlightcolor = self.button_highlight,
                                 relief = 'raised',
                                 state = tk.DISABLED)
        self.BLANK_2.grid(row = 1, column = 1)

        ################
        #Exit Button   #
        ################
        self.exit = tk.Button(self.game_links,
                              text = "Exit",
                              font = self.button_font,
                              width = self.button_width,
                              bd = self.button_border,
                              bg = self.button_bg,
                              fg = self.button_fg,
                              highlightcolor = self.button_highlight,
                              relief = 'raised',
                              command = self.quit)
        self.exit.grid(row = 20, column = 0, columnspan = 2)
        

    def raise_hangman(self):
        '''
        Open Hangman Game
        '''
        self.controller.show_frame('Hangman_shell')



    def raise_matchgame(self):
        '''
        Open Matchgame
        '''
        self.controller.show_frame('Match_game_shell')

    def quit(self):
        '''
        Close Game Suite
        '''
        self.controller.controller.show_frame('Main_game_master')

app = Master_frame()
app.mainloop()
        
