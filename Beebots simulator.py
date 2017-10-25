#!/usr/bin/python

import tkinter as tk
import time
import _thread
import random
from PIL import Image, ImageTk


# Constants
START_DIRECTION = 3
BLINK_COLOR = 'white'
UP = '00'
LEFT = '01'
RIGHT = '02'
DOWN = '03'
TOP_GEOMETRY = '500x500+0+500'
TOP_X = 500
TOP_Y = 500
CANVAS_X = 485
CANVAS_Y = 465
CANVAS_PAD_X = 5
CANVAS_PAD_Y = 1
CANVAS_BAKGROUND = "#D2D2D2" #Gray
NMB_BUTTONS = 4
DIRECTION_MIN = 3
DIRECTION_MAX = 12
DIRECTION_STEP = 3
FRAME_BAKGROUND = 'yellow2'
FRAME_WIDTH = 78 #54
FRAME_HEIGHT = 78 #83
FRAME_DIFF = FRAME_HEIGHT - FRAME_WIDTH
START_BUTTON_HEIGHT = 25
TARGET_SIZE_20 = 20
STEP_SIZE_20 = 20
STEP_SIZE_40 = 40
STEP_SIZE_80 = 80
TARGET_SIZE = TARGET_SIZE_20
STEP_SIZE = STEP_SIZE_80
RASTER_ADJUST_Y = 0 #STEP_SIZE-STEP_SIZE_20
RASTER_ADJUST_X = 0 #STEP_SIZE-STEP_SIZE_20
STOP_COLOR = 'red2'
TARGET_AREA = 100
TARGET_FOUND_COLOR_1 = 'yellow2'
TARGET_FOUND_COLOR_2 = 'black'

# Global variables
LARGE_FONT = ("Verdana",9)

class _zo : pass
zo = _zo()
zo.a = {}
zo.the_way_to_go = []
zo.color = "blue","red","green","yellow","gray"
zo.color2 = "orange","dark violet","navy","red" #"yellow2","black","black","yellow2"
zo.text = '↑','←','→','↓'
zo.text2 = 'Ꙩ Ꙩ','','',''
zo.text3 = 'Ꙩ\nꙨ','','',''
zo.win_x = 0
zo.win_y = 0
zo.moves = ([[STEP_SIZE,0],[0,STEP_SIZE],[-STEP_SIZE,0],[0,-STEP_SIZE]])
zo.direction = 12
zo.exit_thread = False
zo.o_x0 = 0
zo.o_y0 = 0
zo.stopped_at_target = False

#                            LEFT,EAST               LEFT,SOUTH     LEFT,WEST   LEFT,NORTH
zo.beebots_turn_border = ([[FRAME_DIFF,-FRAME_DIFF],[0,FRAME_DIFF] , [0,0] , [-FRAME_DIFF,0]\
#							RIGHT,EAST     RIGHT,SOUTH            RIGHT,WEST     RIGHT,NORTH
						,[FRAME_DIFF,0],[-FRAME_DIFF,FRAME_DIFF],[0,-FRAME_DIFF],[0,0]])

#                            LEFT,EAST                    LEFT,SOUTH                  LEFT,WEST                     LEFT,NORTH
zo.beebots_turn_middle = ([[FRAME_DIFF/2,-FRAME_DIFF/2],[-FRAME_DIFF/2,FRAME_DIFF/2],[FRAME_DIFF/2,-FRAME_DIFF/2],[-FRAME_DIFF/2,FRAME_DIFF/2] \
#                            RIGHT,EAST                   RIGHT,SOUTH                 RIGHT,WEST                    RIGHT,NORTH
						  ,[FRAME_DIFF/2,-FRAME_DIFF/2],[-FRAME_DIFF/2,FRAME_DIFF/2],[FRAME_DIFF/2,-FRAME_DIFF/2],[-FRAME_DIFF/2,FRAME_DIFF/2]])

class App:

	def __init__ (self, master):

		#self.target_id = None
		# Type of Beebots turning
		zo.beebots_turn = zo.beebots_turn_border # Fill in the type of Beebots turning border or middle<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
		master.title("Beebots")

        #create canvas
		self.canvas1 = tk.Canvas(master, relief = tk.FLAT, background = CANVAS_BAKGROUND, width = CANVAS_X, height = CANVAS_Y)
		self.canvas1.pack(side = tk.BOTTOM, anchor = tk.SW, padx = CANVAS_PAD_X, pady = CANVAS_PAD_Y)
       	# Create lines
		nmb_raster_lines = CANVAS_X/STEP_SIZE
		for n in range (int(nmb_raster_lines)):
			self.canvas1.create_line(0, (n*STEP_SIZE)+RASTER_ADJUST_Y , CANVAS_X, (n * STEP_SIZE)+RASTER_ADJUST_Y, fill='gray', dash=(1,))
			self.canvas1.create_line((n*STEP_SIZE)+RASTER_ADJUST_X, 6 , (n*STEP_SIZE)+RASTER_ADJUST_X, CANVAS_Y, fill = 'gray', dash = (1,))

		frame1 = tk.Frame (master)
		frame1.pack(expand = 1, anchor = tk.N, fill = tk.X)
		# Creating the START button
		self.reset_button = tk.Button (frame1, text = "Börja om", command = self.reset_now)
		self.reset_button.pack(side = tk.RIGHT, padx=5)
		# Creating the RESET button
		self.start_button = tk.Button (frame1, text = " START", command = self.begin_now)
		self.start_button.pack(side = tk.LEFT, padx=5)
		# Creating the Place target button
		self.start_button = tk.Button (frame1, text = "Ny blomman", command = self.place_target)
		self.start_button.pack(side = tk.TOP)

	# Creating the thing with the arrows
		self.frame = tk.Frame (master, bg= FRAME_BAKGROUND)
		self.reset_frame()
		self.do_buttons ()


	def do_buttons (self):

		for x in range(NMB_BUTTONS):
			butn = tk.Button(self.frame, bg=zo.color[x], font=LARGE_FONT, text = zo.text[x])
			if x == int(UP):
				if zo.direction == 9 	: butn.grid(column=0, row=0, sticky = tk.W, rowspan = 2, ipadx = 1, ipady = 27); butn.config(text = zo.text[x+1])
				elif zo.direction == 3 	: butn.grid(column=3, row=0, sticky = tk.E, rowspan = 2, ipadx = 1, ipady = 27) ; butn.config(text = zo.text[x+2])
				elif zo.direction == 12 : butn.grid(column=0, row=0, sticky = tk.N, columnspan = 2, ipadx = 30, ipady = 1); butn.config(text = zo.text[x])
				else 					: butn.grid(column=0, row=3, sticky = tk.S, columnspan = 2, ipadx = 30, ipady = 1); butn.config(text = zo.text[x+3])

			elif x== int(DOWN): # DOWN
				if zo.direction == 9 	: butn.grid(column=3, row=0, sticky = tk.E, rowspan = 2, ipadx = 1, ipady = 27); butn.config(text = zo.text[x-1])
				elif zo.direction == 3 	: butn.grid(column=0, row=0, sticky = tk.W, rowspan = 2, ipadx = 1, ipady = 27); butn.config(text = zo.text[x-2])
				elif zo.direction == 12 : butn.grid(column=0, row=3, sticky = tk.S, columnspan = 2, ipadx = 30, ipady = 1); butn.config(text = zo.text[x])
				else 					: butn.grid(column=0, row=0, sticky = tk.N, columnspan = 2, ipadx = 30, ipady = 1); butn.config(text = zo.text[x-3])

			elif x == int(LEFT):
				if zo.direction == 9 	: butn.grid(column=1, row=1, sticky = tk.S, ipady = 8, ipadx = 4); butn.config(text = zo.text[x+2])
				elif zo.direction == 3 	: butn.grid(column=1, row=0, sticky = tk.N, ipady = 8, ipadx = 4); butn.config(text = zo.text[x-1])
				elif zo.direction == 12 : butn.grid(column=0, row=1, sticky = tk.W, ipadx = 9); butn.config(text = zo.text[x])
				else 					: butn.grid(column=1, row=1, sticky = tk.E, ipadx = 9); butn.config(text = zo.text[x+1])

			elif x == int(RIGHT):
				if zo.direction == 9 	: butn.grid(column=1, row=0, sticky = tk.N, ipady = 8, ipadx = 4); butn.config(text = zo.text[x-2])
				elif zo.direction == 3 	: butn.grid(column=1, row=1, sticky = tk.S, ipady = 8, ipadx = 4); butn.config(text = zo.text[x+1])
				elif zo.direction == 12 : butn.grid(column=1, row=1, sticky = tk.E, ipadx = 9); butn.config(text = zo.text[x])
				else 					: butn.grid(column=0, row=1, sticky = tk.W, ipadx = 9); butn.config(text = zo.text[x-1])

			zo.a["%0.2d"%(x)] = butn

	def do_buttons_direction (self, start):
		self.destroy_boxes()
		for x in range(NMB_BUTTONS):
			butn = tk.Button(self.frame, bg=zo.color2[x], font=LARGE_FONT, text = zo.text2[x], relief=tk.FLAT)

			if x == int(UP):
				if zo.direction == 9 	: butn.grid(column=0, row=0, rowspan = 2, ipadx = 4, ipady = 24) ; butn.config(text = zo.text3[x])
				elif zo.direction == 3 	: butn.grid(column=3, row=0, rowspan = 2, ipadx = 4, ipady = 24) ; butn.config(text = zo.text3[x])
				elif zo.direction == 12 : butn.grid(column=0, row=0, columnspan = 2, ipadx = 24, ipady = 1)
				else 					: butn.grid(column=0, row=3, columnspan = 2, ipadx = 24, ipady = 1)
			elif x== int(DOWN): # DOWN
				if zo.direction == 9 	: butn.grid(column=3, row=0, rowspan = 2, ipadx = 7, ipady = 31)
				elif zo.direction == 3 	: butn.grid(column=0, row=0, rowspan = 2, ipadx = 7, ipady = 31)
				elif zo.direction == 12 : butn.grid(column=0, row=3, columnspan = 2, ipadx = 34, ipady = 1)
				else 					: butn.grid(column=0, row=0, columnspan = 2, ipadx = 34, ipady = 1)
			elif x == int(LEFT):
				if zo.direction == 9 	: butn.grid(column=1, row=1, ipadx = 6, ipady = 10)
				elif zo.direction == 3 	: butn.grid(column=1, row=0, ipadx = 6, ipady = 8)
				elif zo.direction == 12 : butn.grid(column=0, row=1, ipadx = 14)
				else 					: butn.grid(column=1, row=1, ipadx = 14)
			elif x == int(RIGHT):
				if zo.direction == 9 	: butn.grid(column=1, row=0, ipadx = 6, ipady = 8)
				elif zo.direction == 3 	: butn.grid(column=1, row=1, ipadx = 6, ipady = 10)
				elif zo.direction == 12 : butn.grid(column=1, row=1, ipadx = 14)
				else 					: butn.grid(column=0, row=1, ipadx = 14)

			zo.a["%0.2d"%(x)] = butn

	def vilken_direction(self, vart):
		zo.the_way_to_go.append(vart)


	def start_begin_now(self, frame, f_direction, check_position):
		f_direction(False)

		for n in zo.the_way_to_go:
		# exit for-loop if flag set
			if zo.exit_thread: break
			_x0 = zo.win_x
			_y0 = zo.win_y
			#print("0- _x0, zo.win_x",_x0, zo.win_x)
			#print("0-_y0, zo.win_y", _y0, zo.win_y)
			lbbg = zo.a[n].cget("bg")
			prev_direction = zo.direction

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
				#if check_position(): zo.a[n].config(bg = 'maroon1')
			else: #DOWN
				x,y = zo.moves[int(zo.direction/DIRECTION_STEP)-1]
				zo.win_x -= x
				zo.win_y -= y
				#if check_position(): zo.a[n].config(bg = 'maroon1')

			if n == LEFT or n == RIGHT:
				if zo.direction == 12 or zo.direction == 6 :
					frame.place(width = FRAME_WIDTH, height= FRAME_HEIGHT, x = zo.win_x, y = zo.win_y)
				else:
					frame.place(width = FRAME_HEIGHT, height= FRAME_WIDTH, x = zo.win_x, y = zo.win_y)
				f_direction(False)
			#Place frame when changing direction
				turn = ((prev_direction/3) + 4*(int(n)-1))-1
				turn_x, turn_y = zo.beebots_turn[int(turn)]
				#print("before zo.win_x, zo.win_y",zo.win_x, zo.win_y)
				zo.win_x +=turn_x
				zo.win_y +=turn_y
				if check_position(): zo.a[UP].config(bg = 'maroon1')
				time.sleep(0.25)
				#print("turn, n, turn_x, turn_y, zo.win_x, zo.win_y",int(turn),n, turn_x, turn_y, zo.win_x, zo.win_y)
				frame.place(x = zo.win_x, y = zo.win_y)

			else: #UP and DOWN
				check_position()
				_x= 1 if _x0 - zo.win_x < 0  else -1
				_y= 1 if _y0 - zo.win_y < 0  else -1
				#print("1-_x, _x0, zo.win_x",_x, _x0, zo.win_x)
				#print("1-_y, _y0, zo.win_y",_y, _y0, zo.win_y)
				for m in range(int(abs(_x0-zo.win_x))):
					#print("x", end="")
					if _x0 == zo.win_x : break
					_x0 += _x
					frame.place(x = _x0)
					time.sleep(0.05)
				#print("")
				for o in range(int(abs(_y0-zo.win_y))):
					#print("y", end="")
					if _y0 == zo.win_y : break
					_y0 += _y
					frame.place(y = _y0)
					time.sleep(0.05)
				#print("")
				#print("2-_x, _x0, zo.win_x",_x, _x0, zo.win_x)
				#print("2-_y, _y0, zo.win_y",_y, _y0, zo.win_y)

				if check_position():
					zo.a[n].config(bg = 'maroon1')
				else:
					zo.a[n].config(bg = BLINK_COLOR)

			time.sleep(0.15)
			zo.a[n].config(bg = lbbg)
			time.sleep(0.15)

		#return the exit-flag to normal
		zo.exit_thread = False
		_thread.start_new_thread(App.check_if_stopped_at_target,(None,check_position))

	def begin_now(self):
		self.reset_frame()
		self.do_buttons () # Varför behövs detta anrop?
		zo.stopped_at_target = False
		zo.exit_thread = False
		_thread.start_new_thread(App.start_begin_now,(None, self.frame, lambda start: self.do_buttons_direction(start), lambda: self.check_window_border() ))



	def check_if_stopped_at_target(self, check_position):
		zo.stopped_at_target = True
		while zo.stopped_at_target:
			if check_position():
				for n in (LEFT, RIGHT): #UP, DOWN,
					zo.a[n].config(bg = TARGET_FOUND_COLOR_1)
				if not zo.stopped_at_target : break
				time.sleep(0.5)
				for n in (LEFT, RIGHT):#UP, DOWN,
					zo.a[n].config(bg = TARGET_FOUND_COLOR_2)
				if not zo.stopped_at_target : break
				time.sleep(0.5)


	def reset_now(self):
		zo.the_way_to_go = []
		zo.exit_thread = True
		zo.stopped_at_target = False
		time.sleep(0.2) # Time for the task to end
		self.reset_frame()
		#self.do_buttons_direction(True)
		self.do_buttons()

	def reset_frame (self):
		self.destroy_boxes()

		self._win_x, self._win_y = CANVAS_PAD_X+1, START_BUTTON_HEIGHT+ CANVAS_PAD_Y+5
		# OP_X/2-FRAME_WIDTH/2, TOP_Y-FRAME_HEIGHT
		zo.win_x, zo.win_y = self._win_x, self._win_y  #-14   +14
		self.frame.place(width = FRAME_WIDTH, height= FRAME_HEIGHT, x = self._win_x, y = self._win_y)
		zo.direction = START_DIRECTION

	def destroy_boxes (self):
		#print("knappar", zo.a)
		for x in zo.a:
			zo.a[x].destroy()
			#print("destroy knappar",x)
		#time.sleep(10)

	def check_window_border (self):
	# Check end of TOP window
		w_req, h_req = top.winfo_width(), top.winfo_height()
		if zo.direction == 12 or zo.direction == 6 :
			if 0 > zo.win_x :
				zo.win_x = 0
			elif zo.win_x > w_req - FRAME_WIDTH:
				zo.win_x = w_req - FRAME_WIDTH
			if START_BUTTON_HEIGHT > zo.win_y:
				zo.win_y = START_BUTTON_HEIGHT
			elif zo.win_y > h_req - FRAME_HEIGHT:
				zo.win_y = h_req-FRAME_HEIGHT
		else:
			if 0 > zo.win_x :
				zo.win_x = 0
			elif zo.win_x > w_req - FRAME_HEIGHT:
				zo.win_x = w_req-FRAME_HEIGHT
			if START_BUTTON_HEIGHT > zo.win_y:
				zo.win_y = START_BUTTON_HEIGHT
			elif zo.win_y > h_req - FRAME_WIDTH:
				zo.win_y = h_req-FRAME_WIDTH

		# Check also position from target
		target_center_x = zo.o_x0 + TARGET_SIZE/2
		target_center_y = zo.o_y0 + TARGET_SIZE/2
		target_xlength = FRAME_HEIGHT
		target_ylength = FRAME_WIDTH
		if zo.direction == 12 or zo.direction == 6 :
			target_xlength = FRAME_WIDTH
			target_ylength = FRAME_HEIGHT

		if zo.win_x + target_xlength-(TARGET_SIZE/2) > (target_center_x+5) >= zo.win_x+(TARGET_SIZE/2):
			if zo.win_y + target_ylength-(TARGET_SIZE/2) >= (target_center_y+31) > zo.win_y+(TARGET_SIZE/2):
				return True

		return False

	def place_target(self):

		#if self.target_id: self.canvas1.delete(self.target_id)
		zo.o_x0 = random.randint(CANVAS_PAD_X + TARGET_AREA, CANVAS_X-TARGET_SIZE -TARGET_AREA)
		zo.o_y0 = random.randint(CANVAS_PAD_X+TARGET_AREA, CANVAS_Y - FRAME_HEIGHT-TARGET_SIZE-TARGET_AREA)
		# Make target and place it
		#zo.o_x0 = 218 #251
		#zo.o_y0 = 350 #289
		# To resize the image
		#lbimage = Image.open('./flower.gif')
		#lbimage = lbimage.resize((21,21), Image.ANTIALIAS)
		#lbimage.save('./flower_size.gif')
		#print("zo.o_x0,zo.o_y0",zo.o_x0,zo.o_y0)
		self.picture = ImageTk.PhotoImage(file = './flower_size.gif')
		#self.target_id = self.canvas1.create_oval(zo.o_x0, zo.o_y0, zo.o_x0+TARGET_SIZE, zo.o_y0+TARGET_SIZE, fill='red', outline='red')
		self.canvas1.create_image(zo.o_x0+ (TARGET_SIZE/2), zo.o_y0+(TARGET_SIZE/2), image = self.picture)



top = tk.Tk()
top.geometry(TOP_GEOMETRY)
app = App(top)



top.mainloop()

#top.destroy()
