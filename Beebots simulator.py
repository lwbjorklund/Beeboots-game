#!/usr/bin/python

import tkinter as tk
import time
import _thread

# Contants
UP_COLOR = 'blue'
DOWN_COLOR = 'yellow'
LEFT_COLOR = 'red'
RIGHT_COLOR = 'green'
BLINK_COLOR = 'white'

# Global variables
LARGE_FONT = ("Verdana",20)
UP = "00"
DOWN = "03"
LEFT = "01"
RIGHT = "02"

class _zo : pass
zo = _zo()
zo.a = {}
zo.up_button = {}
zo.down_button = {}
zo.right_button = {}
zo.left_button = {}
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
		'''
		self.set_down_button (frame, 'on')
		self.set_up_button (frame, 'on')
		self.set_right_button (frame, 'on')
		self.set_left_button (frame, 'on')
		'''
		self.do_buttons (2)
		
	def do_buttons (self, nmb):
		bx = nmb
		
		for x in range(bx):
			for y in range(bx):
				ind = (x*bx) + y  
				 
				butn = tk.Button(zo.frame, bg=zo.color[ind], font=LARGE_FONT, text = zo.text[ind])
				if ind == 0:
					butn.config(command = lambda: self.vilken_direction('00'))
					butn.grid(column=0, row=0, sticky = tk.N, columnspan = 2, ipadx = 47)
					
				elif ind == 1:
					butn.config(command = lambda: self.vilken_direction('01'))
					butn.grid(column=0, row=1, sticky = tk.W)
					
				elif ind == 2:
					butn.config(command = lambda: self.vilken_direction('02'))
					butn.grid(column=1, row=1, sticky = tk.E)
					
				else:
					butn.config(command = lambda: self.vilken_direction('03'))
					butn.grid(column=0, row=3, sticky = tk.S, columnspan = 2, ipadx = 47)
					
				
				zo.a["%0.2d"%(ind)] = butn
				
		
		
	def set_up_button (self, frame, conf):
		# The UP-button
		zo.up_button = tk.Button(frame, text = " /\ ", command = lambda: self.vilken_direction('up'), fg = 'yellow', bg = UP_COLOR)
		zo.up_button.pack(side = tk.TOP, expand = 1, fill = tk.X)
		
	def set_down_button (self, frame, conf):
	# The DOWN-button
		zo.down_button = tk.Button (frame, text = " \/", command = lambda: self.vilken_direction('down'), fg = 'blue', bg = DOWN_COLOR)
		zo.down_button.pack(side = tk.BOTTOM, expand = 1, fill = tk.X, anchor = tk.S)

	def set_right_button (self, frame, conf):	
		# The RIGHT-button
		zo.right_button = tk.Button (frame, text = "-->", command = lambda: self.vilken_direction('right'), fg = 'red', bg = RIGHT_COLOR)
		zo.right_button.pack(side = tk.RIGHT)
		
	def set_left_button (self, frame, conf):
		# The LEFT-button
		zo.left_button = tk.Button (frame, text = "<--", command = lambda: self.vilken_direction('left'), fg = 'green', bg = LEFT_COLOR)
		zo.left_button.pack(side = tk.LEFT)

	
	def vilken_direction(self, vart):
			
		zo.the_way_to_go.append(vart)
		
		print ('vilken_direction ', str(vart))
		
	def start_begin_now(self):
				
		nn = sorted(zo.a.keys())
		numb = len (zo.the_way_to_go)
		
		print ("lengd", numb)
		
		for n in range(numb):
			lbbg = zo.a[zo.the_way_to_go[n]].cget("bg")
			if zo.the_way_to_go[n] == UP :
				print ('Hej 2! ', str(n))
				zo.a[zo.the_way_to_go[n]].config(bg = BLINK_COLOR)
				time.sleep(0.5)
				zo.a[zo.the_way_to_go[n]].config(bg = lbbg)
				
			elif zo.the_way_to_go[n] == DOWN :
				print ('Hej 3! ', str(n))
				zo.a[zo.the_way_to_go[n]].config(bg = BLINK_COLOR)
				time.sleep(0.5)			
				zo.a[zo.the_way_to_go[n]].configure(bg = lbbg)
				
			elif zo.the_way_to_go[n] == LEFT : 
				print ('Hej 4! ', str(n))
				zo.a[zo.the_way_to_go[n]].config(bg = BLINK_COLOR)
				time.sleep(0.5)
				zo.a[zo.the_way_to_go[n]].configure(bg = lbbg)
				
			elif zo.the_way_to_go[n] == RIGHT :
				print ('Hej 5! ', str(n))
				zo.a[zo.the_way_to_go[n]].config(bg = BLINK_COLOR)	
				time.sleep(0.5)
				zo.a[zo.the_way_to_go[n]].configure(bg = lbbg)
				
			else :
				print ('Hej fel! ', str(n))
						
			
			time.sleep(0.5)

		
		
	def begin_now(self):
		_thread.start_new_thread(App.start_begin_now,(None,))
		
	def reset_now(self):
				
		zo.the_way_to_go = []
		print ('reset_now ', str(zo.the_way_to_go))



top = tk.Tk()
top.geometry("500x500")
app = App(top)

top.mainloop()

#top.destroy()
