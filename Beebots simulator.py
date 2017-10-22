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
NMB_BUTTONS = 4
DIRECTION_MIN = 3
DIRECTION_MAX = 12
DIRECTION_STEP = 3

# Global variables
LARGE_FONT = ("Verdana",10)

class _zo : pass
zo = _zo()
zo.a = {}
zo.the_way_to_go = []
zo.color = "blue","red","green","yellow"
zo.text = '↑','←','→','↓' #"/\\","<--","-->", "\\/" 
zo.win_x = 0
zo.win_y = 0
zo.moves = ([[20,0],[0,20],[-20,0],[0,-20]])           
zo.direction = 12


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
		self.do_buttons ()
		

	def do_buttons (self):
		for x in range(NMB_BUTTONS):
			butn = tk.Button(self.frame, bg=zo.color[x], font=LARGE_FONT, text = zo.text[x])
			if x == 0:
				butn.config(command = lambda: self.vilken_direction(UP))
				butn.grid(column=0, row=0, sticky = tk.N, columnspan = 2)
				hs_up = butn.winfo_reqheight()
				ws_up = butn.winfo_reqwidth()
			elif x == 1:
				butn.config(command = lambda: self.vilken_direction(LEFT))
				butn.grid(column=0, row=1, sticky = tk.W)
			elif x == 2:
				butn.config(command = lambda: self.vilken_direction(RIGHT))
				butn.grid(column=1, row=1, sticky = tk.E)
				hs_right = butn.winfo_reqheight()
				ws_right = butn.winfo_reqwidth()
			else:
				butn.config(command = lambda: self.vilken_direction(DOWN))
				butn.grid(column=0, row=3, sticky = tk.S, columnspan = 2)
				hs_down = butn.winfo_reqheight()
				
			zo.a["%0.2d"%(x)] = butn
		# do UP and DOWN buttons twice as long as LEFT and RIGHT buttons		
		zo.a[UP].grid(ipadx = 1+(2*hs_right-hs_up)/2)
		zo.a[DOWN].grid(ipadx = 1+(2*hs_right-hs_up)/2)
		self._win_x, self._win_y = TOP_X/2-ws_right, TOP_Y-(hs_up + hs_right + hs_down)
		zo.win_x, zo.win_y = self._win_x, self._win_y
		self.frame.place(width = (2 * ws_right), height= (hs_up + hs_right + hs_down), x = self._win_x, y = self._win_y)
		zo.direction = 12
		
	def do_buttons_direction (self):
		for x in zo.a:
			zo.a[x].destroy()
			_direction = zo.direction
			
		for x in range(NMB_BUTTONS):
			butn = tk.Button(self.frame, bg=zo.color[x], font=LARGE_FONT, text = zo.text[x])
			if x == int(UP):
				if _direction == 9 : butn.grid(column=0, row=0, sticky = tk.W, rowspan = 2)
				elif _direction == 3 : butn.grid(column=3, row=0, sticky = tk.E, rowspan = 2)
				elif _direction == 12 : butn.grid(column=0, row=0, sticky = tk.N, columnspan = 2)
				else : butn.grid(column=0, row=3, sticky = tk.S, columnspan = 2)
				hs_up = butn.winfo_reqheight()
				ws_up = butn.winfo_reqwidth()
			elif x == int(LEFT):
				if _direction == 9 : butn.grid(column=1, row=1, sticky = tk.S)
				elif _direction == 3 : butn.grid(column=1, row=0, sticky = tk.N)
				elif _direction == 12 : butn.grid(column=0, row=1, sticky = tk.W)
				else : butn.grid(column=1, row=1, sticky = tk.E)
							
			elif x == int(RIGHT):
				if _direction == 9 : butn.grid(column=1, row=0, sticky = tk.N)
				elif _direction == 3 : butn.grid(column=1, row=1, sticky = tk.S)
				elif _direction == 12 : butn.grid(column=1, row=1, sticky = tk.E)
				else : butn.grid(column=0, row=1, sticky = tk.W)
				hs_right = butn.winfo_reqheight()
				ws_right = butn.winfo_reqwidth()
			else:
				if _direction == 9 : butn.grid(column=3, row=0, sticky = tk.E, rowspan = 2)
				elif _direction == 3 : butn.grid(column=0, row=0, sticky = tk.W, rowspan = 2)
				elif _direction == 12 : butn.grid(column=0, row=3, sticky = tk.S, columnspan = 2)
				else : butn.grid(column=0, row=0, sticky = tk.N, columnspan = 2)
				hs_down = butn.winfo_reqheight()
				ws_down = butn.winfo_reqwidth()
				
			zo.a["%0.2d"%(x)] = butn
		# do UP and DOWN buttons twice as long as LEFT and RIGHT buttons	
		
		if zo.direction == 12 or zo.direction == 6 :
			self.frame.place(width = 2*ws_right, height= hs_up + hs_right + hs_down)
			zo.a[UP].grid(ipadx = 1+(2*hs_right-hs_up)/2)
			zo.a[DOWN].grid(ipadx = 1+(2*hs_right-hs_up)/2)
		else:
			self.frame.place(width = ws_up+ws_right+ws_down, height= 2*hs_right)
			zo.a[UP].grid(ipady = (2*hs_right-hs_up)/2)
			zo.a[DOWN].grid(ipady = (2*hs_right-hs_down)/2)
	
	def vilken_direction(self, vart):
		zo.the_way_to_go.append(vart)
		
		
	def start_begin_now(self, frame, f_direction):

		for n in zo.the_way_to_go:
			lbbg = zo.a[n].cget("bg")
			zo.a[n].config(bg = BLINK_COLOR)
			# Move the box
			if n == LEFT:
				zo.direction -= DIRECTION_STEP
				if zo.direction < DIRECTION_MIN : zo.direction = DIRECTION_MAX
			elif n == RIGHT:
				zo.direction += DIRECTION_STEP
				if zo.direction > DIRECTION_MAX : zo.direction = DIRECTION_MIN
			elif n == UP:
				x,y = zo.moves[int(zo.direction/DIRECTION_STEP)-1]
				zo.win_x += x
				zo.win_y += y
				frame.place(x = zo.win_x, y = zo.win_y)
			else: #DOWN
				x,y = zo.moves[int(zo.direction/DIRECTION_STEP)-1]
				zo.win_x -= x
				zo.win_y -= y
				frame.place(x = zo.win_x, y = zo.win_y)
			
			f_direction()
			time.sleep(0.5)
			zo.a[n].config(bg = lbbg)
			time.sleep(0.5)
		
	def begin_now(self):
		_thread.start_new_thread(App.start_begin_now,(None, self.frame, lambda: self.do_buttons_direction() ))
		
	def reset_now(self):
		zo.the_way_to_go = []
		
		for x in zo.a:
			zo.a[x].destroy()
		self.do_buttons()



top = tk.Tk()
top.geometry(TOP_GEOMETRY)
app = App(top)

top.mainloop()

#top.destroy()
