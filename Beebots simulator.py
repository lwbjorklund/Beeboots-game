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
TOP_GEOMETRY = '500x500+0+500'
TOP_X = 500
TOP_Y = 500

# Global variables
LARGE_FONT = ("Verdana",10)

class _zo : pass
zo = _zo()
zo.a = {}
zo.the_way_to_go = []
zo.color = "blue","red","green","yellow","orange","brown","dodgerblue","pink"
zo.text = "/\\","<--","-->", "\\/"
zo.win_x = 0
zo.win_y = 0
zo.moves = ([[0,-20],[-20,0],[20,0],[0,20]])


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
	# Record coordinates for window to avoid asking them every time
				
		self.frame = tk.Frame (master, bg= 'red')
		#self.frame.place(x = zo.win_x, y = zo.win_y)
		#self.frame.pack(expand = 1, anchor = tk.S)

		self.do_buttons (2)
		

	def do_buttons (self, nmb):
		bx = nmb
		
		for x in range(bx):
			for y in range(bx):
				ind = (x*bx) + y  
				 
				butn = tk.Button(self.frame, bg=zo.color[ind], font=LARGE_FONT, text = zo.text[ind])
				if ind == 0:
					butn.config(command = lambda: self.vilken_direction(UP))
					butn.grid(column=0, row=0, sticky = tk.N, columnspan = 2)
					hs_up = butn.winfo_reqheight()
					ws_up = butn.winfo_reqwidth()
				elif ind == 1:
					butn.config(command = lambda: self.vilken_direction(LEFT))
					butn.grid(column=0, row=1, sticky = tk.W)
					
					
				elif ind == 2:
					butn.config(command = lambda: self.vilken_direction(RIGHT))
					butn.grid(column=1, row=1, sticky = tk.E)
					hs_right = butn.winfo_reqheight()
					ws_right = butn.winfo_reqwidth()
				else:
					butn.config(command = lambda: self.vilken_direction(DOWN))
					butn.grid(column=0, row=3, sticky = tk.S, columnspan = 2)
					hs_down = butn.winfo_reqheight()
				
				zo.a["%0.2d"%(ind)] = butn
		# do UP and DOWN buttons twice as long as LEFT and RIGHT buttons		
		zo.a['00'].grid(ipadx = 2*(ws_right-ws_up+0.5))
		zo.a['03'].grid(ipadx = 2*(ws_right-ws_up+0.5))
		self._win_x, self._win_y = TOP_X/2-ws_right, TOP_Y-(hs_up + hs_right + hs_down)
		zo.win_x, zo.win_y = self._win_x, self._win_y
		self.frame.place(width = (2 * ws_right), height= (hs_up + hs_right + hs_down), x = self._win_x, y = self._win_y)
	
	def vilken_direction(self, vart):
		zo.the_way_to_go.append(vart)
		
		
	def start_begin_now(self, frame):
		numb = len (zo.the_way_to_go)
				
		for n in range(numb):
			lbbg = zo.a[zo.the_way_to_go[n]].cget("bg")
			zo.a[zo.the_way_to_go[n]].config(bg = BLINK_COLOR)
			# Move the box
			x,y = zo.moves[int(zo.the_way_to_go[n])]
			zo.win_x += x
			zo.win_y += y
			frame.place(x = zo.win_x, y = zo.win_y)
			
			time.sleep(0.5)
			zo.a[zo.the_way_to_go[n]].config(bg = lbbg)
			time.sleep(0.5)
		
		
	def begin_now(self):
		_thread.start_new_thread(App.start_begin_now,(None, self.frame,))
		
	def reset_now(self):
		zo.the_way_to_go = []
		zo.win_x, zo.win_y = self._win_x, self._win_y
		self.frame.place (x = self._win_x, y = self._win_y)
		
		



top = tk.Tk()
top.geometry(TOP_GEOMETRY)
app = App(top)

top.mainloop()

#top.destroy()
