'''
Created on 14 april 2015

@author: Reem
'''

from gui import GUI
import tkinter

def main():
    root = tkinter.Tk()
    root.title("2048")
    root.resizable(width=False, height=False)
    gui = GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()