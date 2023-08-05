#!/usr/bin/python
from tkinter import *
import os
import sys
import time
import datetime
import subprocess

def future_editor():
	#styling of the button and textbox is given here
	fg="white"
	bg="black"
	font="courier"

	#takes the code from the text-box and saves it as a file using python in usrs/ directory
	global i
	i = 0
	def run_code():
		code_given = str(code.get("1.0",'end-1c'))
		date = str(datetime.datetime.now())
		create_file =  open("future-editor-cache.py","w+")
		create_file.write(code_given)
		create_file.close()
		os.system("python future-editor-cache.py")
	def copy_():
		code_given = str(code.get("1.0",'end-1c'))
		subprocess.run("pbcopy", universal_newlines=True, input=code_given)


	def theme_():
		window_theme = Toplevel()
		window_theme.title("Theme")
		label_coming_soon = Label(window_theme,text = "Coming soon",bg="white",fg="black",font=font)
		label_coming_soon.grid(row=0,column=0)

	window = Tk()
	window.resizable(False, False) # not resizable in both directions
	window.title("Future-editor")

	code = Text(window,bg=bg,fg=fg,insertbackground=fg)
	code.grid(row=1,column=0,columnspan=4)

	run = Button(window,bg="white",fg="black",command=run_code,font=font,text="Run")
	run.grid(row=2,column=0,columnspan=4,sticky=W+E)

	copy_code = Button(window,bg="white",fg="black",command=copy_,font=font,text="copy code")
	copy_code.grid(row=0,column=0,sticky=W+E)

	theme_code = Button(window,bg="white",fg="black",command=theme_,font=font,text="Theme")
	theme_code.grid(row=0,column=2,sticky=W+E)


	window.mainloop()

if __name__=='__main__':
	future_editor()
	future_editor()