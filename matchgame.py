import tkinter as tk
import json, os, random, datetime, top_wins
from operator import itemgetter

class Match_game_shell(tk.Frame):
    '''
    A GUI shell for a game of hangman, multiple frames exist on top of
    each other,
    '''
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)
        for key, value in kwargs.items():
            self.__dict__[key] = value 
        #self.title("Madison's Game Suite 1.0")
        self.shell = tk.Frame(self)
        self.shell.pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        self.shell.grid_rowconfigure(0, weight = 1)
        self.shell.grid_columnconfigure(0, weight = 1)
        self.scores_fn = r'json\matchgame_times.jsn'
        self.level = None
        self.game_in_progress = False
        #Set a base number of rows and images per row, 'Main' frame adjusts
        #these values with menu_choice()
        self.ROWS = 2
        self.ROW_LEN = 8
        self.total_pics = 0
        self.times = self.load_times()
        #self.clear_times()

        #Game Title
        self.header = tk.Label(self.shell,
                               text = '{}\n{}\n{}'.format(
                                   '_'*122,
                                   ' '*36 + 'Match Game' + ' '*36,
                                   '_'*122))
        self.header.grid(row = 0, column = 0, sticky = 'news')

        #The stacked frames
        self.frames = {}
        for F in (Match_main,Game):
            page_name = F.__name__
            frame = F(parent=self.shell, controller=self)
            self.frames[page_name] = frame
            frame.grid(row = 1, column = 0)
        self.show_frame('Match_main')

    def __str__(self):
        return 'Match Game Controller'

    def load_times(self):
        '''
        Return list of times stored in self.scores_fn, return a list  of tuples
        for tuple in scores: name, score = scores
        '''
        with open(self.scores_fn) as infile:
            scores = json.load(infile)
            return scores
        
    def dump_times(self):
        '''
        Store top ten fastest times in json file, scores is a list of tuples
        '''
        for level, scores in self.times.items():
            #sort list of high scores fastest time to slowest, keep top 3
            high_scores = sorted(scores, key=itemgetter(1))[:3]
            self.times[level] = high_scores
        with open(self.scores_fn, 'w') as scores_to_write:
            json.dump(self.times, scores_to_write)

    def clear_times(self):
        '''
        Use to clear all HighScores
        '''
        self.times = {'Normal':[], 'Hard': [], 'Expert':[]}
        self.dump_times()

    def show_frame(self, page_name):
        '''
        Show frame of given page_name, set potentially overlapping keybindings
        as frame is raised and adjust appearance of contoller.header to fit page
        theme
        '''
        frame = self.frames[page_name]
        #prevent multiple "Game" frames from being opend simultaneously
        if self.game_in_progress:
            pass

        ###############
        #Main Page    #
        ###############
        elif page_name == "Match_main":
            ####################################################################
            #Header Config                                                     #
            ####################################################################
            self.shell.config(bg = frame.header_bg)
            text = '{}\n{}\n{}'.format('_'*56,
                                       ' '*36 + '\nMemory Match\n' + ' '*36,
                                       '_'*56)
            self.header.config(font = frame.title_font,
                               text = text,
                               fg = frame.header_fg,
                               bg = frame.header_bg)
            frame.populate_scorecard()

        ###############
        #Game Window  #
        ###############
        elif page_name == "Game":
            frame.setup()
            self.bind("<Escape>", frame.to_main)
        frame.tkraise()
        
    

class Match_main(tk.Frame):
    '''
    Main Page of Match Game, Contain a set of radiobuttons to allow user to
    navigate to the other pages of game and a display of Top Ten High Scores
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
        left_flower = img_path + r'\Decor\left_flower.gif'
        left_flower_img = tk.PhotoImage(master = self,
                               file = left_flower)
        
        right_flower = img_path + r'\Decor\right_flower.gif'
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
                                   text = ' '*25)
        self.menu_title.pack()
        
        #Image Categories
        self.category_frame = tk.Frame(self.main_menu,
                                       bg = self.bg,
                                       highlightthickness = 1,
                                       highlightcolor = self.score_bg,
                                       bd = 1,
                                       relief = 'raised',
                                       padx = 4,
                                       pady = 4)
        self.category_frame.focus()
        self.category_frame.pack(anchor = 'n')
        self.category_label = tk.Label(self.category_frame,
                                       font = self.category_font,
                                       text = 'Image Categories',
                                       bg = self.bg,
                                       fg = self.label_color)
        self.category_label.pack(anchor = 'n')
        
        OPTIONS = [folder for folder in \
                   os.listdir(img_path + r'\match game tiles')\
                   if folder != 'Decor']
        
        self.category_variable = tk.StringVar()
        self.category_variable.set(OPTIONS[0])
        self.categories = tk.OptionMenu(self.category_frame,
                                        self.category_variable,
                                        *OPTIONS)
        
        self.categories.config(width = 12,
                               bg = self.selector_color,
                               fg = self.label_color,
                               highlightthickness = 0,
                               activeforeground = self.button_bg,
                               activebackground = self.button_fg
                               )
        self.categories['menu'].config(bg = self.button_fg,
                                       fg = self.button_bg)
        self.categories.pack(anchor = "n")

        #Menu Radio's
        self.menu_options = tk.IntVar()
        self.menu_options.set(1)
                                                
        #Radio: Easy
        self.easy = tk.Radiobutton(self.main_menu,
                                   font = self.label_font,
                                   fg = self.label_color,
                                   bg = self.bg,
                                   selectcolor = self.selector_color,
                                   text = 'Easy  ',
                                   variable = self.menu_options,
                                   value = 1)
        self.easy.pack(anchor = tk.N)
        
        #Radio: normal
        self.normal = tk.Radiobutton(self.main_menu,
                                   font = self.label_font,
                                   fg = self.label_color,
                                   bg = self.bg,
                                   selectcolor = self.selector_color,
                                   text = 'Normal',
                                   variable = self.menu_options,
                                   value = 2)
        self.normal.pack(anchor = tk.N)
        
        #Radio:Hard
        self.hard = tk.Radiobutton(self.main_menu,
                                   font = self.label_font,
                                   fg = self.label_color,
                                   bg = self.bg,
                                   selectcolor = self.selector_color,
                                   text = 'Hard  ',
                                   variable = self.menu_options,
                                   value = 3)
        self.hard.pack(anchor = tk.N)
        
        #Exit
        self.exit = tk.Radiobutton(self.main_menu,
                                   font = self.label_font,
                                   fg = self.label_color,
                                   bg = self.bg,
                                   selectcolor = self.selector_color,
                                   text = 'Exit  ',
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

        #Display fastes times
        #Scorecard Header
        self.score_header = tk.Label(self,
                                     bg = self.bg,
                                     fg = self.score_color,
                                     font = self.score_label_font,
                                     text = '\n\n\nHIGH SCORES')
        
        self.score_header.grid(row = 1,
                               column = 1,
                               sticky = 'EW')

        self.spacer_line = tk.Label(self,
                                    font = self.header_font,
                                    bg = self.bg,
                                    fg = self.label_color,
                                    text = '_'*57)

        #Scorecard
        self.score_card = tk.Frame(self)
        self.score_card.grid(row = 3,
                             column = 0,
                             columnspan = 3,
                             sticky = 'NEWS')
        #High Score 'Normal' difficulty
        self.high_score_normal = tk.Frame(self.score_card,
                                          bg = self.field_bg)
        for c in range(4):
            self.high_score_normal.columnconfigure(c, weight = 1)
        self.high_score_normal.pack(side = tk.TOP, fill = tk.X)
        self.normal_header = tk.Label(self.high_score_normal,
                                      text = 'Normal',
                                      font = self.label_font,
                                      bg = self.score_bg,
                                      fg = self.label_color,
                                      relief = tk.RAISED,
                                      anchor  = tk.CENTER)
        self.normal_header.grid(row = 0,
                                column = 0,
                                columnspan = 4,
                                sticky = 'EW')

        #High Scores 'Hard' difficulty
        self.high_score_hard = tk.Frame(self.score_card,
                                        bg = self.field_bg)
        for c in range(4):
            self.high_score_hard.columnconfigure(c, weight = 1)
        self.high_score_hard.pack(side = tk.TOP, fill = tk.X)
        self.hard_header = tk.Label(self.high_score_hard,
                                    font = self.label_font,
                                    fg = self.label_color,
                                    bg = self.score_bg,
                                    text = 'Hard',
                                    relief = tk.RAISED)
        self.hard_header.grid(row = 0,
                              column = 0,
                              columnspan = 4,
                              sticky = 'EW')
        #High Scores 'Expert' difficulty
        self.high_score_expert = tk.Frame(self.score_card,
                                          bg = self.field_bg)
        for c in range(4):
            self.high_score_expert.columnconfigure(c, weight = 1)
        self.high_score_expert.pack(side = tk.TOP, fill = tk.X)
        self.expert_header = tk.Label(self.high_score_expert,
                                      font = self.label_font,
                                      fg = self.label_color,
                                      bg = self.score_bg,
                                      text = 'Expert',
                                      relief = tk.RAISED)
        self.expert_header.grid(row = 0,
                                column = 0,
                                columnspan = 4,
                                sticky = 'EW')
    def populate_scorecard(self):
        relief = 'raised'
        scores = self.controller.load_times()
 
        for level, score_list in scores.items():
            while len(score_list) < 3:
                score_list.append(('','','',''))
            if level == "Normal":
                for indx, record in enumerate(score_list):
                    name, time, category, date = record
                    #Name
                    entry = tk.Label(self.high_score_normal,
                                     text = name,
                                     width = 15,
                                     bg = self.field_bg)
                    entry.grid(row = indx + 1, column = 0,sticky = 'EW')
                    #Time
                    entry = tk.Label(self.high_score_normal,
                                     text = time,
                                     bg = self.field_bg,
                                     anchor = 'center',
                                     width = 4)
                    entry.grid(row = indx + 1, column = 1, sticky = 'EW')
                    #Category
                    entry = tk.Label(self.high_score_normal,
                                     text = category,
                                     bg = self.field_bg,
                                     anchor = 'center',
                                     width = 4)
                    entry.grid(row = indx + 1, column = 2, sticky = 'EW')
                    #Date
                    entry = tk.Label(self.high_score_normal,
                                     text = date,
                                     bg = self.field_bg,
                                     width = 15)
                    entry.grid(row = indx + 1, column = 3, sticky = 'EW')
                    
            elif level == "Hard":
                for indx, record in enumerate(score_list):
                    name, time, category, date = record
                    #Name
                    entry = tk.Label(self.high_score_hard,
                                     text = name,
                                     width = 15,
                                     bg = self.field_bg)
                    entry.grid(row = indx + 1, column = 0,sticky = 'EW')
                    #Time
                    entry = tk.Label(self.high_score_hard,
                                     text = time,
                                     bg = self.field_bg,
                                     width = 4)
                    entry.grid(row = indx + 1, column = 1, sticky = 'EW')
                    #Category
                    entry = tk.Label(self.high_score_hard,
                                     text = category,
                                     bg = self.field_bg,
                                     width = 4)
                    entry.grid(row = indx + 1, column = 2, sticky = 'EW')
                    #Date
                    entry = tk.Label(self.high_score_hard,
                                     text = date,
                                     bg = self.field_bg,
                                     width = 15)
                    entry.grid(row = indx + 1, column = 3, sticky = 'EW')
                    
            elif level == "Expert":
                for indx, record in enumerate(score_list):
                    name, time, category, date = record
                    #Name
                    entry = tk.Label(self.high_score_expert,
                                     text = name,
                                     bg = self.field_bg,
                                     width = 15)
                    entry.grid(row = indx + 1, column = 0,sticky = 'EW')
                    #Time
                    entry = tk.Label(self.high_score_expert,
                                     text = time,
                                     bg = self.field_bg,
                                     width = 4)
                    entry.grid(row = indx + 1, column = 1, sticky = 'EW')
                    #Time
                    entry = tk.Label(self.high_score_hard,
                                     text = category,
                                     bg = self.field_bg,
                                     width = 4)
                    entry.grid(row = indx + 1, column = 2, sticky = 'EW')
                    #Date
                    entry = tk.Label(self.high_score_expert,
                                     text = date,
                                     bg = self.field_bg,
                                     width = 15)
                    entry.grid(row = indx + 1, column = 3, sticky = 'EW')
        
    def menu_choice(self, event = None):
        '''
        Return Value of Main Menu Radio Button Option,
        self.controller.ROWS = Value will adjust number of rows
        self.controller.ROW_LEN = Value will adjust number of pics per row, default is 8
        '''
        choice = self.menu_options.get()
        if choice == 1:
            self.controller.level = 'Normal'
            self.controller.ROWS = 2
            
        elif choice == 2:
            self.controller.level = 'Hard'
            self.controller.ROWS = 3
            
        elif choice == 3:
            self.controller.level = 'Expert'
            self.controller.ROWS = 4
            
        elif choice == 4:
            self.quit()
        if choice != 4:
            #Adjust number of images per row, default is 8
            self.controller.ROW_LEN = self.controller.ROW_LEN
            self.controller.total_pics = \
                            self.controller.ROW_LEN * self.controller.ROWS
            
            self.controller.show_frame('Game')
        
    
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

    def quit(self, *args):
        print("quit check")
        self.controller.controller.show_frame('Main_game_master')
        
        

class Game(tk.Frame):
    '''
    Create duplicate lists of randomized images, hides images, and allow User
    to select two images at a time.  If User selects two different images, they
    are re-hidden, if they match, leave them unmasked.
    '''
    def __init__(self, parent, controller, level = None):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.time_display = 'Time:  {:17}'
        self.seconds = 0
        self.minutes = 0
        self.finish_time = ''
        self.matched = 0
        self.img_path = os.getcwd() + r'\images'  
    
        self.card_1 = ''
        self.card_2 = ''
        self.cards = []
        self.turned = []
        self.state = False
        self.game_over = False
        
        self.img_mask = self.img_path + r'\Decor\mask.gif'

        
        #GUI style constants
        self.timer_font = ("Comic Sans MS", 18)
        self.bg = 'cornflower blue'
        self.header_font = ('Courier', 14)
        self.header_bg = 'cornflower blue'
        self.header_fg = 'misty rose'
        self.field_bg = 'bisque'
        #Button colors
        self.selector_color = 'steel blue'
        self.button_bg = 'slate blue'
        self.button_fg = 'orchid1'
        #label fg and Font
        self.label_color = 'misty rose'
        self.label_font = ("Comic Sans MS", 10)

        #Toplevel window styling
        self.top_bg = 'Aquamarine'
        self.top_label_color = 'black'
        self.top_button_bg = 'DarkTurquoise'
        self.top_button_fg = 'black'
        self.top_field_bg = 'pink'
        self.top_font = ('Courier', 12)
        
    def create_widgets(self):
        '''
        Create a Toplevel window to contain Match Game
        '''
        self.container = tk.Toplevel(self, bg = self.bg)

        #self.container.geometry("+%d+%d" % (x,y))
        self.container.title('Match Game: {}'.format(self.controller.level))
        self.container.focus_set()
        self.container.attributes("-fullscreen", self.state)
        self.container.bind("<Escape>", self.to_main)
        #Images Frame
        #Frame to hold multiple Labels, each holding a img
        self.frames_frame = tk.Frame(self.container, bg = self.bg)
        self.frames_frame.pack(side = tk.TOP)

        #Images
        self.create_rows()

        #Bottom Frame
        self.bottom_frame = tk.Frame(self.container, bg = self.bg)
        self.bottom_frame.pack(side = tk.BOTTOM, fill = tk.BOTH)
        self.hash(self.bottom_frame)

        #Back Button
        self.button_frame = tk.Frame(self.bottom_frame,
                                     bg = self.bg,
                                     padx = 2,
                                     pady = 2)
        self.button_frame.pack(side = tk.LEFT, fill = tk.X)
        
        self.back_button = tk.Button(self.button_frame,
                                     width = 8,
                                     text = 'Back',
                                     font = self.label_font,
                                     bg = self.button_bg,
                                     fg = self.button_fg,
                                     command = self.to_main)
        self.back_button.grid(row = 0, column = 0, sticky = 'w')

        #Time Display
        self.time_frame = tk.Frame(self.bottom_frame, bg = self.bg)
        self.time_frame.pack()
        self.hash(self.time_frame)
        self.timer = tk.Label(self.time_frame,
                              font = self.timer_font,
                              bg = self.bg,
                              text = self.time_display.format('00','00'))
        self.timer.pack()
        self.container.protocol("WM_DELETE_WINDOW", self.to_main)
        self.seconds = 0
        self.minutes = 0
        self.center_window(self.container)
    
    def create_rows(self):
        '''
        Populate rows with random images from category chosen by user in
        Optionmenu in "Main" frame menu, number of rows set by level.
        '''
        row = 0
        column = 0
        images = self.images
        rows = [[None]*self.controller.ROW_LEN\
                for r in range(self.controller.ROWS)]
 
        for r in rows:
            for frame in r:
                random.shuffle(images)
                file = images.pop()
                img = tk.PhotoImage(master= self.frames_frame,
                                    file = self.img_mask)
                self.card = tk.Label(self.frames_frame,
                                     image = img,
                                     bg = self.bg,
                                     relief = tk.GROOVE)
                
                self.card.bind("<Button-1>",
                               lambda card = self.card: self.turn(card))
                self.card.image = img
                self.card.fn = file
                self.card.grid(row = row, column = column)
                column += 1
                if column == self.controller.ROW_LEN:
                    column = 0
            row += 1

    def to_main(self, event = None):
        '''
        Destroy "Game" Toplevel Window and return controller to 'Main' frame
        '''
        self.container.destroy()
        self.controller.game_in_progress = False
        self.controller.show_frame("Match_main")
        

    def setup(self):
        '''
        Reset relvant variables for a fresh game each time "Game" Frame raised
        '''
        self.controller.game_in_progress = True
        #Reset Image folder path
        self.category = None
        self.tiles = self.img_path + r'\match game tiles\{}'
        #Pull Fresh Images
        self.images = self._images()
        #Reset number of matched tiles
        self.matched = 0
        #Reset Memory of overturned tiles
        self.cards = []
        self.turned = []
        #Reset Game Status
        self.game_over = False
        #Build Game Frame 
        self.create_widgets()
        #Start Game Timer
        self.tick()
             
    def _images(self):
        '''
        Generate a list of random images
        '''
        self.tiles = self.tiles.format(self.get_category())
        images = ["{}\{}".format(self.tiles,fn) \
                  for fn in os.listdir(self.tiles)]
        #if there are not enough images to populate number or rows to be created
        if (self.controller.total_pics / 2) > (len(images)):
            raise ValueError('Insufficient image files; Expected: {} Actual: {}'.format
                             ((self.controller.total_pics // 2), len(images)))
        else:
            random_images = []
            while len(random_images) != self.controller.total_pics / 2:
                img = random.choice(images)
                if img not in random_images:
                    random_images.append(img)
            set_1 = random_images[:]
            set_2 = random_images[:]
            all_images = set_1 + set_2
            return all_images

    def turn(self, card, *args):
        '''
        Reveal image by 'turning' card face up,
        once two cards are turned compare them
        '''
        if card.widget not in self.cards:
            self.cards.append(card.widget)
        if len(self.cards) < 3:
            fn = card.widget.fn
            if fn in self.turned:
                self.cards.remove(card.widget)
            else:
                img = tk.PhotoImage(master = self.frames_frame, file = fn)
                card.widget.config(image = img)
                card.widget.img = img
            if len(self.cards) == 2:
                self.compare(self.cards)

    def compare(self, cards):
        '''
        Check if two over turned cards are identical or not,
        if not, 'mask' them after 1 sec
        '''
        self.card_1 = self.cards[0].fn
        self.card_2 = self.cards[1].fn
        if self.card_1 == self.card_2:
            self.matched += 1
            self.turned.append(self.card_1)
            if self.matched == self.controller.total_pics / 2:
                self.game_over = True
                self.track_times()
            self.cards = []
        else:
            self.after(1000, lambda cards = self.cards: self.mask(cards))
    
    def mask(self, cards):
        '''
        Change image on overturned cards to designated 'masking' image
        '''
        if self.card_1 != self.card_2:
            img = tk.PhotoImage(master = self.frames_frame,
                                file = self.img_mask)
            for card in cards:
                if card.fn not in self.turned:
                    card.config(image = img)
                    card.img = img
        self.cards = []

    def get_category(self):
        return self.controller.frames['Match_main'].category_variable.get()

    def tick(self):
        '''
        A timer to start when game begins and end when final match is made.
        Fastes times are used as high scores
        '''
        if not self.game_over:
            
            if self.seconds == 60:
                self.minutes += 1
                self.seconds = 0

            if self.minutes < 10:
                minutes = '{:d}{:d}'.format(0, self.minutes)
            elif self.minutes >= 10:
                minutes = '{:d}'.format(self.minutes)

            if self.seconds < 10:
                seconds = '{:d}{:d}'.format(0, self.seconds)
            elif self.seconds >= 10:
                seconds = '{:d}'.format(self.seconds)
            timer = '{}:{}'.format(minutes, seconds)
            self.finish_time = timer
            self.timer.config(text = self.time_display.format(timer))
            self.timer.after(1000, self.tick)
            self.seconds += 1
            
    def track_times(self):
        '''
        If finish time is faster than slowest recorded time for current level,
        record new time record
        '''
        scores = self.controller.times[self.controller.level]        
        try:
            slowest_time = scores[-1][1]
        except IndexError:
            slowest_time = None
        if slowest_time == None or \
           self.finish_time < slowest_time or \
           len(scores) < 3:
            x = self.controller.winfo_rootx() + \
                (self.controller.winfo_width() /3)
            y = self.controller.winfo_rooty() + \
                (self.controller.winfo_width() /7)
            new_time = top_wins.Single_entry("NEW RECORD", "Your Name", 'Ok',
                                             font = self.label_font,
                                             bg = self.bg,
                                             label_color = self.label_color,
                                             field_bg = self.field_bg,
                                             button_bg = self.button_bg,
                                             button_fg = self.button_fg,
                                             x = x,
                                             y = y
                                             )
            name = new_time.name
            if name != str(name):
                name = 'Washington Irving'
            elif name == '':
                name = 'Irving Washington'
            today = datetime.date.today()
            date = today.strftime("%b %d, %Y")
            record = (name, self.finish_time, self.get_category(), date)
            scores.append(record)
            self.controller.dump_times()
    

    def center_window(self, window):
        '''
        Calculate screen size and set window geometry to centered position
        '''
        window.update_idletasks()
        w = window.winfo_screenwidth()
        h = window.winfo_screenheight()
        size = tuple(int(i) for i in window.geometry().split('+')[0].split('x'))
        x = w//3 - size[0]//3
        y = self.controller.winfo_y()
        window.geometry("%dx%d+%d+%d" % (size + (x, y)))

        
    def toggle_state(self, event = None):
        '''
        Open window in fullscreen
        '''
        self.state = False
        self.container.attributes("-fullscreen", False)
        return ("break")

    def hash(self, frame):
        '''
        A 3x3 grid of rows and columns, row=2/col=2 is center of frame,
        soley used to adjust GUI layout
        '''
        for i in range(3):
            frame.rowconfigure(i, weight = 1)
            frame.columnconfigure(i, weight = 1)
 
'''
app = Match_game_shell()
#Open Game in approximate middle of screen,
x = app.winfo_screenwidth() // 4
y = 0
app.geometry("+%d+%d" % (x,y))


app.mainloop()
'''
