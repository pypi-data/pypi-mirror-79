import tkinter as tk
from tkinter import messagebox
import threading

RED = "#ff0000"
GREEN = "#00ff00"
BLUE = "#0000ff"
BLACK = "#000000"
WHITE = "#ffffff"
DARKBG = "#2b2b2b"
LIGHTBG = "#3c3f41"
TEXTCOLOR = "#b5b5b5"

class VirtualTerminal(object):
    def __init__(self, startfunction=None, enterfunction=None):
        self.terminal_bgColor = DARKBG
        self.terminal_textColor = TEXTCOLOR
        self.terminal_insertColor = TEXTCOLOR
        self.terminal_justify = "left"

        self.input_bgColor = DARKBG
        self.input_textColor = TEXTCOLOR
        self.input_insertColor = TEXTCOLOR

        self.divider_height = 1
        self.divider_color = LIGHTBG

        self.terminal_font = ("Menlo-Regular.ttf", 19)
        self.input_font = ("Menlo-Regular.ttf", 19)
        self.title = "VTerminal"
        self.size = (700, 410)

        self.resizable = (True, True)

        self.root = tk.Tk()
        self.position = (int((self.root.winfo_screenwidth() / 2) - (self.size[0] / 2)), int((self.root.winfo_screenheight() / 2) - (self.size[1] / 2)))

        self.root.geometry(f"{self.size[0]}x{self.size[1]}+{self.position[0]}+{self.position[1]}")


        self.root.title(self.title)

        self.root.resizable(self.resizable[0], self.resizable[1])


        self.mainFrame = tk.Frame(self.root, bg=DARKBG)
        self.mainFrame.pack(expand=1, fill="both")

        self.terminalFrame = tk.Frame(self.mainFrame, bg=DARKBG)
        self.terminalFrame.pack(expand=1, fill="both")

        self.terminalDisplay = tk.Text(self.terminalFrame, bg=self.terminal_bgColor, insertbackground=self.terminal_insertColor, fg=self.terminal_textColor, height=1, highlightthickness=0,
                                       borderwidth=2,
                                       relief="flat", font=self.terminal_font)
        self.terminalDisplay.pack(expand=1, fill="both")

         #self.terminalDisplay.bind("<Key>", lambda test: "break")

        self.divider = tk.Frame(self.mainFrame, bg=self.divider_color, height=1)
        self.divider.pack(fill="x")

        self.inputFrame = tk.Frame(self.mainFrame, bg=DARKBG, height=40)
        self.inputFrame.pack(fill="x", side="bottom")

        self.inputEntry = tk.Entry(self.inputFrame, bg=self.input_bgColor, relief="flat", fg=self.input_textColor, borderwidth=2, insertbackground=self.input_insertColor, highlightthickness=0, font=self.input_font)
        self.inputEntry.pack(expand=1, fill="both")

        # Can't do right now (on mac)
        # inputButton = tk.Button(inputFrame, text="Enter", relief="flat")
        # inputButton.pack(side="right")

        self.start_function = startfunction
        self.enter_function = enterfunction

        self.inputEntry.bind("<Return>", self.__enter_pressed)

        self.asking = False
        self.answer = None

        # [selection, bgcolor, textcolor, fontpath, fontsize]
        # self.tags = {"0": [("1.0", "end"), self.terminal_bgColor, self.terminal_textColor, self.terminal_font[0], self.terminal_font[1]]}
        self.tags = {}
        # self.terminalDisplay.tag_configure("0", font=(self.tags["0"][3], self.tags["0"][4]))

        self.clickableTexts = {}

        self.option_result = None

        self.__update_config(False)

    def __index2tk(self, text, normal):
        counter = 0
        lineCount = 0
        for line in text.splitlines():
            lineCount += 1
            counter += len(line)
            if counter > normal:
                if len(line) - (counter - normal) - 1 < 0:

                    return f"{lineCount - 1}.{len(line)}"

                return f"{lineCount}.{len(line) - (counter - normal) - 1}"

    def __update_config(self, tags):
        if not tags:
            self.terminalDisplay.config(bg=self.terminal_bgColor,
                                        fg=self.terminal_textColor,
                                        insertbackground=self.terminal_insertColor,
                                        font=self.terminal_font)

            self.inputEntry.config(bg=self.input_bgColor,
                                   fg=self.input_textColor,
                                   insertbackground=self.input_insertColor,
                                   font=self.input_font)

        self.root.title(self.title)
        self.root.geometry(f"{self.size[0]}x{self.size[1]}+{self.position[0]}+{self.position[1]}")
        self.root.resizable(self.resizable[0], self.resizable[1])
        self.divider.config(height=self.divider_height, bg=self.divider_color)


        print(self.tags)
        for tag in self.tags:
            tagPrefs = self.tags[tag][1:]

            startTag = self.tags[tag][0][0]
            endTag = self.tags[tag][0][1]

            self.terminalDisplay.tag_add(tag, startTag, endTag)

            if tagPrefs[0]:
                self.terminalDisplay.tag_configure(tag, background=tagPrefs[0])
            if tagPrefs[1]:
                self.terminalDisplay.tag_configure(tag, foreground=tagPrefs[1])
            if tagPrefs[2]:
                self.terminalDisplay.tag_configure(tag, font=(tagPrefs[2], self.terminalDisplay.tag_cget(tag, "font").split()[1]))
            if tagPrefs[3]:
                if len(self.terminalDisplay.tag_cget(tag, "font").split()):

                    self.terminalDisplay.tag_configure(tag, font=(self.terminalDisplay.tag_cget(tag, "font").split()[0], tagPrefs[3]))
                else:
                    self.terminalDisplay.tag_configure(tag, font=(self.terminal_font[0], tagPrefs[3]))
            if tagPrefs[4]:
                self.terminalDisplay.tag_configure(tag, insertbackground=tagPrefs[4])

            if tagPrefs[5]:
                self.terminalDisplay.tag_configure(tag, justify=tagPrefs[5])


    def __enter_pressed(self, event):
        text = self.inputEntry.get()
        if self.asking:
            self.answer = text
            self.asking = False
        self.inputEntry.delete(0, "end")
        if self.enter_function:
            self.enter_function(text)

    def bind_input(self, function):
        self.enter_function = function
        # self.inputEntry.bind("<Return>", lambda e: function(self.inputEntry.get()))

    def bind_start(self, function):
        self.start_function = function


    def get_terminal(self):
        text = self.terminalDisplay.get(1.0, "end")
        return text[:len(text) - 1]

    def set_terminal(self, text):
        self.terminalDisplay.delete(1.0, "end")
        self.terminalDisplay.insert(1.0, text)

    def __rgb2hex(self, color):
        if isinstance(color, tuple):
            return '#%02x%02x%02x' % color
        else:
            return color



    def config_terminal(self, selection=None, line=None, bgcolor=None, textcolor=None, fontpath=None, fontsize=None, insertcolor=None, justify=None):
        if line:
            selection = (str(line) + ".0", str(line + 1) + ".0")

        if selection:
            self.tags[str(len(self.tags))] = [selection, self.__rgb2hex(bgcolor), self.__rgb2hex(textcolor), fontpath, fontsize, insertcolor, justify]
            self.__update_config(True)
        else:
            if bgcolor:
                self.terminal_bgColor = self.__rgb2hex(bgcolor)
            if textcolor:
                self.terminal_textColor = self.__rgb2hex(textcolor)

            if fontpath:
                self.terminal_font = (fontpath, self.input_font[1])

            if fontsize:
                self.terminal_font = (self.input_font[0], fontsize)

            if insertcolor:
                self.terminal_insertColor = self.__rgb2hex(insertcolor)

            self.__update_config(False)




    def config_input(self, bgcolor=None, textcolor=None, fontpath=None, fontsize=None, insertcolor=None):
        if bgcolor:
            self.input_bgColor = self.__rgb2hex(bgcolor)


        if textcolor:
            self.input_textColor = self.__rgb2hex(textcolor)


        if fontpath:
            self.input_font = (fontpath, self.input_font[1])

        if fontsize:
            self.input_font = (self.input_font[0], fontsize)

        if insertcolor:
            self.input_insertColor = self.__rgb2hex(insertcolor)

        self.__update_config(False)

    def config_window(self, title=None, size=None, position=None, resizable=None, dividercolor=None, dividerheight=None):
        if title:
            self.title = title
        if size:
            self.size = size

        if position:
            self.position = position

        if resizable:
            self.resizable = resizable

        if dividercolor:
            if isinstance(dividercolor, tuple):
                self.divider_color = self.__rgb2hex(dividercolor)
            else:
                self.divider_color = dividercolor

        if dividerheight:
            self.divider_height = dividerheight

        self.__update_config(False)

    def print(self, text, end="\n", bgcolor=None, textcolor=None, fontpath=None, fontsize=None, onclick=None, insertcolor=None, justify=None):
        startIndex = len(self.get_terminal().splitlines()) + 1
        self.set_terminal(self.get_terminal() + text + end)
        endIndex = startIndex + text.count("\n") + end.count("\n")
        splitTerminal = self.get_terminal().splitlines()

        if len(splitTerminal) > 1:
            selection = (str(startIndex) + ".0", str(endIndex) + "." + str(len(self.get_terminal().splitlines()[len(self.get_terminal().splitlines()) - 1])))
        else:
            selection = (str(startIndex) + ".0", str(endIndex) + ".0")

        tagName = str(len(self.tags))

        if bgcolor or textcolor or fontpath or fontsize or onclick:
            self.tags[tagName] = [selection, self.__rgb2hex(bgcolor), self.__rgb2hex(textcolor), fontpath, fontsize, insertcolor, justify]
            if onclick:
                if onclick[1]:
                    self.terminalDisplay.tag_bind(tagName, "<Button-1>", lambda x: self.__threadStarter(onclick[0]))
                else:
                    self.terminalDisplay.tag_bind(tagName, "<Button-1>", onclick)


        # if onclick:
        #     self.__new_clickable_text(selection, onclick)

        self.__update_config(True)

    def __threadStarter(self, function):
        threading.Thread(target=function).start()



    def input(self):
        self.asking = True

        while not self.answer:
            pass

        temp_answer = self.answer
        self.answer = None

        return temp_answer
    #
    # def __new_clickable_text(self, selection, function):
    #     # self.clickableTexts[]
    #     self.terminalDisplay.bind("<Button-1>", self.__test)
    #     # self.terminalDisplay.tag_bind('important', '<1>', popupImportantMenu)

    def cancel_input(self):
        self.asking = False

    def quit(self):
        self.root.quit()

    def strict_input(self, options, errormsg=None):
        answer = self.input()
        if answer not in options:
            if errormsg:
                self.print(errormsg)
            return self.strict_input(options, errormsg=errormsg)
        else:
            return answer

    def __option_result(self, result):
        self.option_result = result


    # def option_menu(self, options, configs=None, separator="\n"):
    #     if not configs:
    #         configs = []
    #         for x in range(len(options)):
    #             configs.append({"bgcolor": None, "textcolor": None, "fontpath": None, "fontsize": None})
    #
    #     for optionIndex in range(len(options)):
    #         option = options[optionIndex]
    #         config = configs[optionIndex]
    #         self.print(option, end=separator, onclick=lambda x: self.__option_result(optionIndex), **config)
    #
    #     while not self.option_result:
    #         pass
    #
    #     temp_result = self.option_result
    #     self.option_result = None
    #
    #     return temp_result
    #


    def popup(self, title, message):
        messagebox.showinfo(title, message)


    def mainloop(self):
        if self.start_function:
            threading.Thread(target=self.start_function).start()
        self.root.mainloop()