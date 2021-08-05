from tkinter import *
from tkinter import font as tkFont
from tkinter import ttk, messagebox, Frame
from random import choice, shuffle
import tkinter as tk
import clipboard
import pickle

FILENAME = "save.password"

NumString = "0123456789"
NumStringEX = "123456789"
SymString = "!@#$%^&*?(){}[]:;~<>.,'"
SymStringEX = "!@#$%^&*?"
UppString = "QWERTYUIOPASDFGHJKLZXCVBNM"
UppStringEX = "QWERTYUPASDFGHJKZXCVBNM"
LowString = "qwertyuiopasdfghjklzxcvbnm"
LowStringEX = "qwertyupasdfghjkzxcvbnm"
ExSimilarString = "lLiIoO0"
ExAmbigString = "(){}[]:;~<>.,'"

class Generator(tk.Frame):
    """Basic class set to trigger with __main__() at the end of this code
    firstly widgets are created, along with getting the saved preset if it 
    was saved in the first place"""

    def __init__(self, parent):
        self.create_widgets(parent)
        self.restore_preset()

    def create_widgets(self, parent):
        tk.Frame.__init__(self, parent)

        ArialRegular = tkFont.Font(family = 'Arial', size = 10)
        ArialBold = tkFont.Font(family = 'Arial', size = 10, weight = 'bold')

        #Lines 34-71 basic labels with text representing their "counterpart" of input boxes

        Label(self, text = "Password Length:",
          font = ArialBold, justify=LEFT, anchor="w").grid(sticky = W,column = 0,
          row = 5, padx=15, pady=15)

        Label(self, text = "Include Numbers:",
          font = ArialRegular, justify=LEFT, anchor="w").grid(sticky = W,column = 0,
          row = 6, padx=15)

        Label(self, text = "Include Symbols:",
          font = ArialRegular, justify=LEFT, anchor="w").grid(sticky = W,column = 0,
          row = 7, padx=15)

        Label(self, text = "Include Uppercase Characters:",
          font = ArialRegular, justify=LEFT, anchor="w").grid(sticky = W,column = 0,
          row = 8, padx=15)

        Label(self, text = "Include Lowercase Characters:",
          font = ArialRegular, justify=LEFT, anchor="w").grid(sticky = W,column = 0,
          row = 9, padx=15)

        Label(self, text = "Exclude Similar Characters:",
          font = ArialRegular, justify=LEFT, anchor="w").grid(sticky = W,column = 0,
          row = 10, padx=15)

        Label(self, text = "Exclude Ambiguous Characters:",
          font = ArialRegular, justify=LEFT, anchor="w").grid(sticky = W,column = 0,
          row = 11, padx=15)

        Label(self, text = "Save my preset:",
          font = ArialRegular, justify=LEFT, anchor="w").grid(sticky = W,column = 0,
          row = 12, padx=15)

        Label(self, text = "Your new password:",
          font = ArialRegular, justify=LEFT, anchor="w").grid(sticky = W,column = 0,
          row = 14, padx=15)

        # Lines 70-105 are input boxes, entries and checkboxes

        self.xint = tk.StringVar()
        PasswordLength = ttk.Combobox(self, width = 30, textvariable = self.xint) 
        PasswordLength['values'] = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20)
        PasswordLength.grid(sticky = tk.W,column = 1, row = 5)
        PasswordLength.current()

        self.num = IntVar()
        numbers = Checkbutton(self, text ='(ex. 123456789)', variable = self.num, justify=LEFT, anchor="w").grid(sticky = W, column = 1, row = 6)

        self.sym = IntVar()
        symbols = Checkbutton(self, text ='(ex. @$%&)', variable = self.sym, justify=LEFT, anchor="w").grid(sticky = W, column = 1, row = 7)

        self.upp = IntVar()
        uppercase = Checkbutton(self, text ='(ex. ABCDEFGH)', variable = self.upp, justify=LEFT, anchor="w").grid(sticky = W, column = 1, row = 8)

        self.low = IntVar()
        lowercase = Checkbutton(self, text ='(ex. abcdefgh)', variable = self.low, justify=LEFT, anchor="w").grid(sticky = W, column = 1, row = 9)

        self.similar = IntVar()
        exsimilar = Checkbutton(self, text ='(ex. i,I,l,L,o,O,0)', variable = self.similar, justify=LEFT, anchor="w").grid(sticky = W, column = 1, row = 10)

        self.ambig = IntVar()
        exambiguous = Checkbutton(self, text ='(ex. []{}()\/:;"~<>.,)', variable = self.ambig, justify=LEFT, anchor="w").grid(sticky = W, column = 1, row = 11)

        self.save = IntVar()
        savepreset = Checkbutton(self, text ='(Save this preset for later.)', variable = self.save, justify=LEFT, anchor="w").grid(sticky = W, column = 1, row = 12)  

        GenerateButton = Button(self, text="Generate", activebackground="grey", command = self.logic, font = 15, bg="light gray",justify=LEFT, anchor="w").grid(sticky=W, column = 1, row = 13, pady = 5)

        self.npw = StringVar()
        newpassword = Entry(self, width=40, textvariable = self.npw).grid(column = 1, row = 14, pady = 5)

        CopyButton = Button(self, text="Copy", activebackground="grey", command = self.CopyFunc , font = 15, bg="light gray",justify=LEFT, anchor="w").grid(sticky=W, column = 2, row = 14, padx = 5)
        root.wm_protocol("WM_DELETE_WINDOW", self.save_preset)


    def logic(self):

        """This functions checks the logic of the input if it would work or not
        also some operations to split the job between char types if more than one 
        are selected"""

        try:
 
            y = [1 for i in (self.num.get(), self.sym.get(), self.upp.get(), self.low.get()) if i==1]
            tickedboxes = len(y)
            wantedlength = self.xint.get()
            slices = int(wantedlength)//tickedboxes
            leftover = int(wantedlength)%tickedboxes
            self.main(slices, leftover)

        except:

            messagebox.showinfo(title="New Password", message="Input incorrect, try again.")
   

    def main(self, slices, leftover):

        dictnumerator = {1:self.num.get(), 2:self.sym.get(), 3:self.upp.get(),
         4:self.low.get(), 5:self.save.get(), 6:self.similar.get(),
          7:self.ambig.get()}

        passlen = len(self.xint.get()) 
        newpasslen = 0
        newpass = ""
        numlbr = 0
        numbr = 0
        symbr = 0
        uppbr = 0
        lowbr = 0

        numbox = dictnumerator[1]
        symbox = dictnumerator[2]
        uppbox = dictnumerator[3]
        lowbox = dictnumerator[4]
        savebox = dictnumerator[5]
        similarbox = dictnumerator[6]
        ambigbox = dictnumerator[7] 

        try:

            """This block of code has a lot of elifs that check what is the status on checked boxes
            which are checked and which not, I think in this block of code this much elifs 
            are redundant, will fix it later"""

            while newpasslen < int(self.xint.get()):
                
                if numbox == 1 and numbr < slices and similarbox == 0:
                    numc = choice(NumString)
                    newpasslen += 1
                    newpass += numc
                    numbr += 1

                elif numbox == 1 and numbr < slices and similarbox == 1:
                    numc = choice(NumStringEX)
                    newpasslen += 1
                    newpass += numc
                    numbr += 1

                elif symbox == 1 and symbr < slices and ambigbox == 0:
                    symc = choice(SymString)
                    newpasslen += 1
                    newpass += symc
                    symbr += 1

                elif symbox == 1 and symbr < slices and ambigbox == 1:
                    symc = choice(SymStringEX)
                    newpasslen += 1
                    newpass += symc
                    symbr += 1

                elif uppbox == 1 and uppbr < slices and similarbox == 0:
                    uppc = choice(UppString)
                    newpasslen += 1
                    newpass += uppc
                    uppbr += 1

                elif uppbox == 1 and uppbr < slices and similarbox == 1:
                    uppc = choice(UppStringEX)
                    newpasslen += 1
                    newpass += uppc
                    uppbr += 1

                elif lowbox == 1 and lowbr < slices and similarbox == 0:
                    lowc = choice(LowString)
                    newpasslen += 1
                    newpass += lowc
                    lowbr += 1
            
                elif lowbox == 1 and lowbr < slices and similarbox == 1:
                    lowc = choice(LowStringEX)
                    newpasslen += 1
                    newpass += lowc
                    lowbr += 1

                elif leftover > numlbr and similarbox == 0:
                    numl = choice(NumString)
                    newpasslen += 1
                    newpass += numl
                    numlbr += 1

                elif leftover > numlbr and similarbox == 1:
                    numl = choice(NumStringEX)
                    newpasslen += 1
                    newpass += numl
                    numlbr += 1
                
        except SyntaxError:

            print("This is a syntax error.")

        finally:

            """This block of code checks if the savebox is ticked and responds accordingly"""

            if savebox == 1:
                self.last_preset = {1:numbox, 2:symbox, 3:uppbox, 4:lowbox, 5:similarbox, 6:ambigbox, 7:savebox}

            else:
                self.last_preset = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
                
            l = list(newpass)
            shuffle(l)
            result = ''.join(l)
            self.npw.set(result)


    def CopyFunc(self):

        """This function using clipboard module saves the generated password in the clipboard"""

        print("Radi")
        clipboard.copy(self.npw.get())  
        text = clipboard.paste()


    def save_preset(self):

        """This function saves the preset in txt file"""

        try:

            data = self.last_preset
            with open(FILENAME, "wb") as f:
                pickle.dump(data, f)

        except:

            print("Save unsuccessfull")

        root.destroy()


    def restore_preset(self):

        """This function restores previously saved preset, and ticks the checkboxes as saved"""

        try:

            with open(FILENAME, "rb") as f:
                data = pickle.load(f)
            self.last_preset = data
            listset = [self.num, self.sym, self.upp, self.low, self.similar, self.ambig, self.save]
            listvalue = self.last_preset.values()
            print(listvalue)
            br = 0
            for i in listvalue:
                listset[br].set(i)
                br+=1

        except:
            print("Error")

if __name__ == "__main__":
    root = tk.Tk()
    Generator(root).pack(fill="both", expand=True)
    root.mainloop()