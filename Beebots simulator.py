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
FRAME_WIDTH = 54
FRAME_HEIGHT = 83
START_BUTTON_HEIGHT = 25


# Global variables
LARGE_FONT = ("Verdana",10)

class _zo : pass
zo = _zo()
zo.a = {}
zo.the_way_to_go = []
zo.color = "blue","red","green","yellow","gray"
zo.color2 = "pale green","dark green","dark green","dark green"
zo.text = '↑','←','→','↓'
zo.text2 = 'Ꙩ Ꙩ','','',''
zo.text3 = 'Ꙩ\nꙨ','','',''
zo.win_x = 0
zo.win_y = 0
zo.moves = ([[20,0],[0,20],[-20,0],[0,-20]])           
zo.direction = 12
zo.exit_thread = False 


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
		self.reset_frame()
		self.do_buttons ()


	def do_buttons (self):
		
		for x in range(NMB_BUTTONS):
			butn = tk.Button(self.frame, bg=zo.color[x], font=LARGE_FONT, text = zo.text[x])
			if x == 0:
				butn.config(command = lambda: self.vilken_direction(UP))
				butn.grid(column=0, row=0, sticky = tk.N, columnspan = 2, ipadx = 34/2)

			elif x == 1:
				butn.config(command = lambda: self.vilken_direction(LEFT))
				butn.grid(column=0, row=1, sticky = tk.W, ipadx = 1)
			elif x == 2:
				butn.config(command = lambda: self.vilken_direction(RIGHT))
				butn.grid(column=1, row=1, sticky = tk.E, ipadx = 1)

			else:
				butn.config(command = lambda: self.vilken_direction(DOWN))
				butn.grid(column=0, row=3, sticky = tk.S, columnspan = 2, ipadx = 34/2)

				
			zo.a["%0.2d"%(x)] = butn
		
		
	def do_buttons_direction (self):
		self.destroy_boxes()	
			
		for x in range(NMB_BUTTONS):
			butn = tk.Button(self.frame, bg=zo.color2[x], font=LARGE_FONT, text = zo.text2[x], relief=tk.FLAT)
			if x == int(UP):
				if zo.direction == 9 : butn.grid(column=0, row=0, sticky = tk.W, rowspan = 2, ipady = 12/2, ipadx = 8/2) ; butn.config(text = zo.text3[x])
				elif zo.direction == 3 : butn.grid(column=3, row=0, sticky = tk.E, rowspan = 2, ipady = 12/2, ipadx = 8/2) ; butn.config(text = zo.text3[x])
				elif zo.direction == 12 : butn.grid(column=0, row=0, sticky = tk.N, columnspan = 2, ipadx = 20/2)# 34/2
				else : butn.grid(column=0, row=3, sticky = tk.S, columnspan = 2, ipadx = 20/2)# 34/2
				hs_up = butn.winfo_reqheight()
				ws_up = butn.winfo_reqwidth()
				
			elif x == int(LEFT):
				if zo.direction == 9 : butn.grid(column=1, row=1, sticky = tk.S, ipadx = 18/2)
				elif zo.direction == 3 : butn.grid(column=1, row=0, sticky = tk.N, ipadx = 18/2)
				elif zo.direction == 12 : butn.grid(column=0, row=1, sticky = tk.W, ipadx = 18/2)
				else : butn.grid(column=1, row=1, sticky = tk.E, ipadx = 18/2)
							
			elif x == int(RIGHT):
				if zo.direction == 9 : butn.grid(column=1, row=0, sticky = tk.N, ipadx = 18/2)
				elif zo.direction == 3 : butn.grid(column=1, row=1, sticky = tk.S, ipadx = 18/2)
				elif zo.direction == 12 : butn.grid(column=1, row=1, sticky = tk.E, ipadx = 14/2)# 2
				else : butn.grid(column=0, row=1, sticky = tk.W, ipadx = 14/2)# 2
				hs_right = butn.winfo_reqheight()
				ws_right = butn.winfo_reqwidth()
				
			else:
				if zo.direction == 9 : butn.grid(column=3, row=0, sticky = tk.E, rowspan = 2, ipady = 28/2, ipadx = 16/2)
				elif zo.direction == 3 : butn.grid(column=0, row=0, sticky = tk.W, rowspan = 2, ipady = 28/2, ipadx = 16/2)
				elif zo.direction == 12 : butn.grid(column=0, row=3, sticky = tk.S, columnspan = 2, ipadx = 44/2)# 34/2
				else : butn.grid(column=0, row=0, sticky = tk.N, columnspan = 2, ipadx = 44/2)# 34/2
				hs_down = butn.winfo_reqheight()
				ws_down = butn.winfo_reqwidth()
				
			zo.a["%0.2d"%(x)] = butn
		# do UP and DOWN buttons twice as long as LEFT and RIGHT buttons	
		#print("hs_up", hs_up)
		#print("ws_up", ws_up)
		#print("hs_right", hs_right)
		#print("ws_right", ws_right)
		#print("hs_down", hs_down)
		#print("ws_down", ws_down)
		
		
		if zo.direction == 12 or zo.direction == 6 :
			zo.win_x +=14
			zo.win_y -=14
			self.frame.place(width = FRAME_WIDTH, height= FRAME_HEIGHT, x = zo.win_x, y = zo.win_y)

		else:
			zo.win_x -=14
			zo.win_y +=14
			self.frame.place(width = FRAME_HEIGHT, height= FRAME_WIDTH, x = zo.win_x, y = zo.win_y)
	
	def vilken_direction(self, vart):
		zo.the_way_to_go.append(vart)
		
		
	def start_begin_now(self, frame, f_direction, check_position):
		f_direction()
			
		for n in zo.the_way_to_go:
		# exit for-loop if flag set
			if zo.exit_thread: break
			
			lbbg = zo.a[n].cget("bg")
			zo.a[n].config(bg = BLINK_COLOR)
			# Move the box
			if n == LEFT:
				zo.direction -= DIRECTION_STEP
				if zo.direction < DIRECTION_MIN : zo.direction = DIRECTION_MAX
				f_direction()
			elif n == RIGHT:
				zo.direction += DIRECTION_STEP
				if zo.direction > DIRECTION_MAX : zo.direction = DIRECTION_MIN
				f_direction()
			elif n == UP:
				x,y = zo.moves[int(zo.direction/DIRECTION_STEP)-1]
				zo.win_x += x
				zo.win_y += y
				check_position()
				frame.place(x = zo.win_x, y = zo.win_y)
			else: #DOWN
				x,y = zo.moves[int(zo.direction/DIRECTION_STEP)-1]
				zo.win_x -= x
				zo.win_y -= y
				check_position()
				frame.place(x = zo.win_x, y = zo.win_y)

	
			time.sleep(0.5)
			zo.a[n].config(bg = lbbg)
			time.sleep(0.5)
			
		#return the exit-flag to normal 
		zo.exit_thread = False
		
	def begin_now(self):
		self.reset_frame()
		self.do_buttons ()
		zo.exit_thread = False
			
		_thread.start_new_thread(App.start_begin_now,(None, self.frame, lambda: self.do_buttons_direction(), lambda: self.check_window_border() ))
		
		
	def reset_now(self):
		zo.the_way_to_go = []
		zo.exit_thread = True
		time.sleep(0.2) # Time for the task to end
		self.reset_frame()
		
		self.do_buttons()
		
	def reset_frame (self):
		self.destroy_boxes()
		
		self._win_x, self._win_y = TOP_X/2-FRAME_WIDTH/2, TOP_Y-FRAME_HEIGHT
		zo.win_x, zo.win_y = self._win_x-14, self._win_y+14		
		self.frame.place(width = FRAME_WIDTH, height= FRAME_HEIGHT, x = self._win_x, y = self._win_y)
		zo.direction = 12
		
	def destroy_boxes (self):
		for x in zo.a:
			zo.a[x].destroy()	

	def check_window_border (self):
							
		# Check end of TOP window
		
		w_req, h_req = top.winfo_width(), top.winfo_height()
		#print("w_req, h_req", w_req, h_req)
		#print("zo.win_x, zo.win_y", zo.win_x, zo.win_y)
		if zo.win_x + FRAME_HEIGHT > w_req:
			zo.win_x = w_req-FRAME_HEIGHT
		elif zo.win_x  < 0 + START_BUTTON_HEIGHT:
			zo.win_x = 0
			
		if zo.win_y + FRAME_HEIGHT > h_req:
			zo.win_y = h_req-FRAME_HEIGHT
		elif zo.win_y  < 0:
			zo.win_y = 0


top = tk.Tk()
top.geometry(TOP_GEOMETRY)
app = App(top)

top.mainloop()

#top.destroy()
