#!/usr/bin/python

import tkinter as tk
import time
import _thread
import random
from PIL import Image, ImageTk


# Constants
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
NMB_BUTTONS = 4
DIRECTION_MIN = 3
DIRECTION_MAX = 12
DIRECTION_STEP = 3
FRAME_WIDTH = 54
FRAME_HEIGHT = 83
FRAME_DIFF = FRAME_HEIGHT - FRAME_WIDTH
START_BUTTON_HEIGHT = 25
TARGET_SIZE_20 = 20
STEP_SIZE_20 = 20
STEP_SIZE_40 = 40
TARGET_SIZE = TARGET_SIZE_20
STEP_SIZE = STEP_SIZE_40

# Global variables
LARGE_FONT = ("Verdana",10)

class _zo : pass
zo = _zo()
zo.a = {}
zo.the_way_to_go = []
zo.color = "blue","red","green","yellow","gray"
zo.color2 = "yellow2","black","black","yellow2"
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
#                            LEFT,EAST               LEFT,SOUTH     LEFT,WEST   LEFT,NORTH     RIGHT,EAST     RIGHT,SOUTH            RIGHT,WEST     RIGHT,NORTH
zo.beebots_turn_border = ([[FRAME_DIFF,-FRAME_DIFF],[0,FRAME_DIFF] , [0,0] , [-FRAME_DIFF,0],[FRAME_DIFF,0],[-FRAME_DIFF,FRAME_DIFF],[0,-FRAME_DIFF],[0,0]])

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
		self.canvas1 = tk.Canvas(master, relief = tk.FLAT, background = "#D2D2D2", width = CANVAS_X, height = CANVAS_Y)
		self.canvas1.pack(side = tk.BOTTOM, anchor = tk.SW, padx = CANVAS_PAD_X, pady = CANVAS_PAD_Y)
       	# Create lines
		for n in range (25):
			self.canvas1.create_line(0, 6+(n*STEP_SIZE) , CANVAS_X, 6+(n * STEP_SIZE), fill='gray', dash=(1,))
			self.canvas1.create_line(4+(n*STEP_SIZE), 6 , 4+(n*STEP_SIZE), CANVAS_Y, fill = 'gray', dash = (1,))

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
				elif zo.direction == 12 : butn.grid(column=0, row=0, sticky = tk.N, columnspan = 2, ipadx = TARGET_SIZE/2)# 34/2
				else : butn.grid(column=0, row=3, sticky = tk.S, columnspan = 2, ipadx = TARGET_SIZE/2)# 34/2
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



	def vilken_direction(self, vart):
		zo.the_way_to_go.append(vart)


	def start_begin_now(self, frame, f_direction, check_position):
		f_direction()

		for n in zo.the_way_to_go:
		# exit for-loop if flag set
			if zo.exit_thread: break

			lbbg = zo.a[n].cget("bg")
			prev_direction = zo.direction
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
				if check_position(): zo.a[n].config(bg = 'maroon1')
			else: #DOWN
				x,y = zo.moves[int(zo.direction/DIRECTION_STEP)-1]
				zo.win_x -= x
				zo.win_y -= y
				if check_position(): zo.a[n].config(bg = 'maroon1')

			if n == LEFT or n == RIGHT:
				f_direction()
			#Place frame when changing direction
				turn = ((prev_direction/3) + 4*(int(n)-1))-1
				turn_x, turn_y = zo.beebots_turn[int(turn)]
				#print("before zo.win_x, zo.win_y",zo.win_x, zo.win_y)
				zo.win_x +=turn_x
				zo.win_y +=turn_y
				#print("turn, n, turn_x, turn_y, zo.win_x, zo.win_y",int(turn),n, turn_x, turn_y, zo.win_x, zo.win_y)

				if zo.direction == 12 or zo.direction == 6 :
					frame.place(width = FRAME_WIDTH, height= FRAME_HEIGHT)
				else:
					frame.place(width = FRAME_HEIGHT, height= FRAME_WIDTH)

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
		zo.win_x, zo.win_y = self._win_x, self._win_y  #-14   +14
		self.frame.place(width = FRAME_WIDTH, height= FRAME_HEIGHT, x = self._win_x, y = self._win_y)
		zo.direction = 12

	def destroy_boxes (self):
		for x in zo.a:
			zo.a[x].destroy()

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
		zo.o_x0 = random.randint(CANVAS_PAD_X, CANVAS_X-TARGET_SIZE)
		zo.o_y0 = random.randint(CANVAS_PAD_X, CANVAS_Y - FRAME_HEIGHT-TARGET_SIZE)
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
