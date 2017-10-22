#!/usr/bin/python

import tkinter as tk
import time
import _thread

# Contants
BLINK_COLOR = 'white'
UP = '00'
LEFT = '01'
RIGHT = '02'
DOWN = '03'

# Global variables
LARGE_FONT = ("Verdana",10)

class _zo : pass
zo = _zo()
zo.a = {}
zo.the_way_to_go = []
zo.frame = None
zo.color = "blue","red","green","yellow","orange","brown","dodgerblue","pink"
zo.text = "/\\","<--","-->", "\\/"


class App:
	def __init__ (self, master):
	# Creating the STP and START button		
		frame1 = tk.Frame (master)
		frame1.pack(expand = 1, anchor = tk.N, fill = tk.X)
		
		self.reset_button = tk.Button (frame1, text = " RESET", command = self.reset_now)
		self.reset_button.pack(side = tk.RIGHT)

		self.start_button = tk.Button (frame1, text = " START", command = self.begin_now)
		self.start_button.pack(side = tk.LEFT)
		
		
	# Creating the thing with the arrows
		frame = tk.Frame (master, bg= 'red')
		frame.pack(expand = 1, anchor = tk.S)
		
		zo.frame = frame
		self.do_buttons (2)
		
	def do_buttons (self, nmb):
		bx = nmb
		
		for x in range(bx):
			for y in range(bx):
				ind = (x*bx) + y  
				 
				butn = tk.Button(zo.frame, bg=zo.color[ind], font=LARGE_FONT, text = zo.text[ind])
				if ind == 0:
					butn.config(command = lambda: self.vilken_direction(UP))
					butn.grid(column=0, row=0, sticky = tk.N, columnspan = 2)
					
					ws_up = butn.winfo_reqwidth()
				elif ind == 1:
					butn.config(command = lambda: self.vilken_direction(LEFT))
					butn.grid(column=0, row=1, sticky = tk.W)
					
					
				elif ind == 2:
					butn.config(command = lambda: self.vilken_direction(RIGHT))
					butn.grid(column=1, row=1, sticky = tk.E)
					
					ws_right = butn.winfo_reqwidth()
				else:
					butn.config(command = lambda: self.vilken_direction(DOWN))
					butn.grid(column=0, row=3, sticky = tk.S, columnspan = 2)
					
				
				zo.a["%0.2d"%(ind)] = butn
		# do UP and DOWN buttons twice as long as LEFT and RIGHT buttons		
		zo.a['00'].grid(ipadx = 2*(ws_right-ws_up+0.5))
		zo.a['03'].grid(ipadx = 2*(ws_right-ws_up+0.5))

	
	def vilken_direction(self, vart):
		zo.the_way_to_go.append(vart)
		
		
	def start_begin_now(self):
		numb = len (zo.the_way_to_go)
		
		for n in range(numb):
			lbbg = zo.a[zo.the_way_to_go[n]].cget("bg")
			zo.a[zo.the_way_to_go[n]].config(bg = BLINK_COLOR)
			time.sleep(0.5)
			zo.a[zo.the_way_to_go[n]].config(bg = lbbg)
			time.sleep(0.5)
		
		
	def begin_now(self):
		_thread.start_new_thread(App.start_begin_now,(None,))
		
	def reset_now(self):
		zo.the_way_to_go = []
		



top = tk.Tk()
top.geometry("500x500")
app = App(top)

top.mainloop()

#top.destroy()
