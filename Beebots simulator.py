#!/usr/bin/python

import tkinter as tk
import time
import _thread
import random
from PIL import Image, ImageTk


# Constants
START_DIRECTION = 3
BLINK_COLOR = 'white'
FORWARD = '00'
LEFT = '01'
RIGHT = '02'
BACKWARD = '03'
STEP_SIZE_20 = 20
STEP_SIZE_40 = 40
STEP_SIZE_80 = 80
STEP_SIZE = STEP_SIZE_80
START_BUTTON_HEIGHT = 25
WINDOW_TITLE_HIGHT = 0
CANVAS_PAD_X = 5
CANVAS_PAD_Y = 1
TOP_X_GEOMETRY = (6*STEP_SIZE)+2*CANVAS_PAD_X
TOP_Y_GEOMETRY =TOP_X_GEOMETRY+START_BUTTON_HEIGHT+WINDOW_TITLE_HIGHT
TOP_GEOMETRY = '500x500+0+400'
TOP_X = 500
TOP_Y = 500
CANVAS_X = 6*STEP_SIZE
CANVAS_Y = 6*STEP_SIZE
CANVAS_BAKGROUND = "#D2D2D2" #Gray
NMB_BUTTONS = 4
DIRECTION_MIN = 3
DIRECTION_MAX = 12
DIRECTION_STEP = 3
FRAME_BAKGROUND = 'yellow2'
FRAME_WIDTH = 78
FRAME_HEIGHT = FRAME_WIDTH # Make Beeboot as a square
FRAME_DIFF = FRAME_HEIGHT - FRAME_WIDTH
TARGET_SIZE_20 = 20
TARGET_SIZE = TARGET_SIZE_20
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
zo.color2 = "yellow2","black","black","yellow2" #"orange","dark violet","navy","red"
zo.text = '→','↓','←','↑','→','↓','←','↑'
zo.text2 = 'Ꙩ Ꙩ','','',''
zo.text3 = 'Ꙩ\nꙨ','','',''
zo.win_x = 0
zo.win_y = 0
zo.moves = ([[STEP_SIZE,0],[0,STEP_SIZE],[-STEP_SIZE,0],[0,-STEP_SIZE]])
zo.new_direction = START_DIRECTION
zo.direction = zo.new_direction
zo.exit_thread = False
zo.o_x0 = 0
zo.o_y0 = 0
zo.stopped_at_target = False
zo.at_border = False

#                            LEFT,EAST               LEFT,SOUTH     LEFT,WEST   LEFT,NORTH
zo.beebots_turn_border = ([[FRAME_DIFF,-FRAME_DIFF],[0,FRAME_DIFF] , [0,0] , [-FRAME_DIFF,0]\
#							RIGHT,EAST     RIGHT,SOUTH            RIGHT,WEST     RIGHT,NORTH
						,[FRAME_DIFF,0],[-FRAME_DIFF,FRAME_DIFF],[0,-FRAME_DIFF],[0,0]])

#                            LEFT,EAST                    LEFT,SOUTH                  LEFT,WEST                     LEFT,NORTH
zo.beebots_turn_middle = ([[FRAME_DIFF/2,-FRAME_DIFF/2],[-FRAME_DIFF/2,FRAME_DIFF/2],[FRAME_DIFF/2,-FRAME_DIFF/2],[-FRAME_DIFF/2,FRAME_DIFF/2] \
#                            RIGHT,EAST                   RIGHT,SOUTH                 RIGHT,WEST                    RIGHT,NORTH
						  ,[FRAME_DIFF/2,-FRAME_DIFF/2],[-FRAME_DIFF/2,FRAME_DIFF/2],[FRAME_DIFF/2,-FRAME_DIFF/2],[-FRAME_DIFF/2,FRAME_DIFF/2]])
#						EAST (3)					SOUTH(6)					WEST(9)						NORTH(12)
zo.buttons_place=[[tk.RIGHT, tk.BOTTOM,tk.TOP],[tk.BOTTOM, tk.LEFT,tk.RIGHT],[tk.LEFT, tk.TOP,tk.BOTTOM],[tk.TOP, tk.RIGHT,tk.LEFT]]
zo.button_frame = []
zo.start_x = CANVAS_PAD_X+1
zo.start_y = START_BUTTON_HEIGHT+ CANVAS_PAD_Y+5
zo.name_text= [['AL','VE'],['VE','AL'],['VE','AL'],['AL','VE']]

class App:

	def __init__ (self, master):

		#self.target_id = None
		# Type of Beebots turning
		zo.beebots_turn = zo.beebots_turn_border # Fill in the type of Beebots turning border or middle<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
		master.title("Beeboots")

        #create canvas
		self.canvas1 = tk.Canvas(master, relief = tk.FLAT, background = CANVAS_BAKGROUND, width = CANVAS_X, height = CANVAS_Y)
		self.canvas1.pack(side = tk.BOTTOM, anchor = tk.SW, padx = CANVAS_PAD_X, pady = CANVAS_PAD_Y)
		print(self.canvas1.winfo_geometry())
       	# Create lines
		nmb_raster_lines = CANVAS_X/STEP_SIZE
		for n in range (int(nmb_raster_lines)):
			self.canvas1.create_line(0, (n*STEP_SIZE)+RASTER_ADJUST_Y , CANVAS_X, (n * STEP_SIZE)+RASTER_ADJUST_Y, fill='gray', dash=(1,))
			self.canvas1.create_line((n*STEP_SIZE)+RASTER_ADJUST_X, 6 , (n*STEP_SIZE)+RASTER_ADJUST_X, CANVAS_Y, fill = 'gray', dash = (1,))

		frame1 = tk.Frame (master)
		frame1.pack(expand = 1, anchor = tk.N, fill = tk.X)
		# Creating the START button
		self.reset_button = tk.Button (frame1, text = "Börja om", command = self.reset_now).pack(side = tk.RIGHT)

		# Creating the RESET button
		self.start_button = tk.Button (frame1, text = " START", command = self.begin_now).pack(side = tk.LEFT)

		# Creating the Place target button
		self.target_button = tk.Button (frame1, text = "Ny blomman", command = self.place_target).pack(side = tk.LEFT,expand = True)

		# Creating the new Place Beeboot start
		self.target_button = tk.Button (frame1, text = "Ny början", command = self.place_new_frame).pack(side = tk.RIGHT,expand = True)


	# Creating the Beeboot with the arrows
		self.frame = tk.Frame (master, bg= FRAME_BAKGROUND)

		self.frame_forward = tk.Frame (self.frame, bg= 'yellow2')
		self.frame_forward.pack(fill=tk.BOTH, expand = True)
		self.frame_turns = tk.Frame (self.frame, bg= 'black')
		self.frame_turns.pack(fill=tk.BOTH, expand = True)
		self.frame_backward = tk.Frame (self.frame, bg= 'yellow2')
		self.frame_backward.pack(fill=tk.BOTH, expand = True)

		zo.button_frame = [self.frame_forward,self.frame_turns,self.frame_turns,self.frame_backward]

		self.place_frame_do_buttons(zo.start_x,zo.start_y)


	def do_buttons (self):
		print("do_buttons IN")
		_dir = int(zo.direction/DIRECTION_STEP)
		self.frame_forward.pack(side = zo.buttons_place[_dir-1][0])# NORTH ->TOP, EAST -> RIGHT, WEST -> LEFT, SOUTH -> BOTTOM
		self.frame_turns.pack(side = zo.buttons_place[_dir-1][0])# NORTH ->TOP, EAST -> RIGHT, WEST -> LEFT, SOUTH -> BOTTOM
		self.frame_backward.pack(side = zo.buttons_place[_dir-1][0])# NORTH ->TOP, EAST -> RIGHT, WEST -> LEFT, SOUTH -> BOTTOM

		for x in [FORWARD,RIGHT,LEFT,BACKWARD]:
			butn = tk.Button(zo.button_frame[int(x)], bg=zo.color[int(x)], \
							font=LARGE_FONT)
			zo.a[x] = butn

		zo.a[FORWARD].pack(expand = True, fill= tk.BOTH)
		zo.a[FORWARD].config(text=zo.text[_dir-1],command = lambda: self.vilken_direction(FORWARD),fg='yellow')
		zo.a[RIGHT].pack(expand = True, fill= tk.BOTH, side = zo.buttons_place[_dir-1][1])# NORTH ->RIGHT, EAST -> BOTTOM, WEST -> TOP, SOUTH -> LEFT
		zo.a[RIGHT].config(text=zo.text[_dir],command = lambda: self.vilken_direction(RIGHT))
		zo.a[LEFT].pack(expand = True, fill= tk.BOTH, side = zo.buttons_place[_dir-1][2])# NORTH ->LEFT, EAST -> TOP, WEST -> BOTTOM, SOUTH -> RIGHT
		zo.a[LEFT].config(text=zo.text[_dir+2],command = lambda: self.vilken_direction(LEFT))
		zo.a[BACKWARD].pack(expand = True, fill= tk.BOTH)
		zo.a[BACKWARD].config(text=zo.text[_dir+1],command = lambda: self.vilken_direction(BACKWARD))

		print("do_buttons OUT")


	def do_buttons_direction (self):
		print("do_buttons_direction IN")
		self.destroy_boxes()
		_dir = int(zo.direction/DIRECTION_STEP)
		self.frame_forward.pack(side = zo.buttons_place[_dir-1][0])# NORTH ->TOP, EAST -> RIGHT, WEST -> LEFT, SOUTH -> BOTTOM
		self.frame_turns.pack(side = zo.buttons_place[_dir-1][0])# NORTH ->TOP, EAST -> RIGHT, WEST -> LEFT, SOUTH -> BOTTOM
		self.frame_backward.pack(side = zo.buttons_place[_dir-1][0])# NORTH ->TOP, EAST -> RIGHT, WEST -> LEFT, SOUTH -> BOTTOM

		for x in [FORWARD,RIGHT,LEFT,BACKWARD]:
			butn = tk.Label(zo.button_frame[int(x)], bg=zo.color2[int(x)], font=LARGE_FONT, text = zo.text2[int(x)], relief=tk.FLAT)
			butn.pack(expand = True, fill= tk.BOTH)
			#time.sleep(0.5)
			if x == FORWARD:
				if zo.direction == 9 	: butn.config(text = zo.text3[int(x)])
				elif zo.direction == 3 	: butn.config(text = zo.text3[int(x)])
			elif x == LEFT				: butn.pack(side = zo.buttons_place[_dir-1][2]);butn.config(text = zo.name_text[_dir-1][0],fg='white')
			elif x == RIGHT				: butn.pack(side = zo.buttons_place[_dir-1][1]);butn.config(text = zo.name_text[_dir-1][1],fg='white')
			zo.a[x] = butn

		print("do_buttons_direction OUT")

	def vilken_direction(self, vart):
		zo.the_way_to_go.append(vart)
		print("vilken_direction: zo.the_way_to_go",zo.the_way_to_go)


	def start_begin_now(self, frame, f_direction, check_position):
		print("start_begin_now IN")
		f_direction()
		#print("zo.the_way_to_go",zo.the_way_to_go)
		for n in zo.the_way_to_go:
		# exit for-loop if flag set
			if zo.exit_thread: break
			_x0 = zo.win_x
			_y0 = zo.win_y
			#print("0- n _x0, zo.win_x",n, _x0, zo.win_x)
			#print("0-n _y0, zo.win_y",n, _y0, zo.win_y)
			lbbg = zo.a[n].cget("bg")
			prev_direction = zo.direction

			# Move the box
			if n == LEFT:
				zo.direction -= DIRECTION_STEP
				if zo.direction < DIRECTION_MIN : zo.direction = DIRECTION_MAX
			elif n == RIGHT:
				zo.direction += DIRECTION_STEP
				if zo.direction > DIRECTION_MAX : zo.direction = DIRECTION_MIN
			elif n == FORWARD:
				#print("FORWARD    zo.direction, zo.moves",zo.direction, zo.moves)
				x,y = zo.moves[int(zo.direction/DIRECTION_STEP)-1]
				#print("x,y", x,y)
				zo.win_x += x
				zo.win_y += y
			else: #BACKWARD
				#print("BACKWARD  zo.direction, zo.moves",zo.direction, zo.moves)
				x,y = zo.moves[int(zo.direction/DIRECTION_STEP)-1]
				zo.win_x -= x
				zo.win_y -= y
			#print("1- _x0, zo.win_x",_x0, zo.win_x)
			#print("1-_y0, zo.win_y", _y0, zo.win_y)
			if n == LEFT or n == RIGHT:
				if zo.direction == 12 or zo.direction == 6 :
					frame.place(width = FRAME_WIDTH, height= FRAME_HEIGHT, x = zo.win_x, y = zo.win_y)
				else:
					frame.place(width = FRAME_HEIGHT, height= FRAME_WIDTH, x = zo.win_x, y = zo.win_y)
				f_direction()
				#Place frame when changing direction
				turn = ((prev_direction/3) + 4*(int(n)-1))-1
				turn_x, turn_y = zo.beebots_turn[int(turn)]
				#print("before zo.win_x, zo.win_y",zo.win_x, zo.win_y)
				zo.win_x +=turn_x
				zo.win_y +=turn_y
				if check_position(): zo.a[FORWARD].config(bg = 'maroon1')
				#print("turn, n, turn_x, turn_y, zo.win_x, zo.win_y",int(turn),n, turn_x, turn_y, zo.win_x, zo.win_y)
				frame.place(x = zo.win_x, y = zo.win_y)

			else: #FORWARD and BACKWARD
				if zo.exit_thread: break
				check_position()
				_x= 1 if _x0 - zo.win_x < 0  else -1
				_y= 1 if _y0 - zo.win_y < 0  else -1
				#print("1-_x, _x0, zo.win_x",_x, _x0, zo.win_x)
				#print("1-_y, _y0, zo.win_y",_y, _y0, zo.win_y)
				for m in range(int(abs(_x0-zo.win_x))):
					#print("x", end="")
					if _x0 == zo.win_x : break
					_x0 += _x
					if zo.exit_thread: break
					frame.place(x = _x0)
					time.sleep(0.04)
				#print("")
				for o in range(int(abs(_y0-zo.win_y))):
					#print("y", end="")
					if _y0 == zo.win_y : break
					_y0 += _y
					if zo.exit_thread: break
					frame.place(y = _y0)
					time.sleep(0.04)
				#print("")
				#print("2-_x, _x0, zo.win_x",_x, _x0, zo.win_x)
				#print("2-_y, _y0, zo.win_y",_y, _y0, zo.win_y)
				if zo.exit_thread: break
				if check_position():
					zo.a[n].config(bg = 'maroon1')
				elif zo.at_border == True:
					zo.a[n].config(bg = STOP_COLOR)
				else:
					zo.a[n].config(bg = BLINK_COLOR)
			if zo.exit_thread: break
			time.sleep(0.1)
			zo.a[n].config(bg = lbbg)
			if zo.exit_thread: break
			time.sleep(0.1)
		#return the exit-flag to normal
		if not zo.exit_thread:
			_thread.start_new_thread(App.check_if_stopped_at_target,(None,check_position))
		zo.exit_thread = False
		print("start_begin_now OUT")

	def begin_now(self):
		#self.place_frame_do_buttons(zo.start_x,zo.start_y)
		zo.stopped_at_target = False
		zo.exit_thread = False
		_thread.start_new_thread(App.start_begin_now,(None, self.frame, lambda: self.do_buttons_direction(), lambda: self.check_window_border() ))



	def check_if_stopped_at_target(self, check_position):
		print("check_if_stopped_at_target IN")
		zo.stopped_at_target = True
		nmb_blink = 20
		while zo.stopped_at_target and nmb_blink:
			nmb_blink -=1
			if check_position():
				for n in (LEFT, RIGHT): #FORWARD, BACKWARD,
					zo.a[n].config(bg = TARGET_FOUND_COLOR_1)
				if not zo.stopped_at_target : break
				if zo.exit_thread: break
				time.sleep(0.15)
				for n in (LEFT, RIGHT):#FORWARD, BACKWARD,
					zo.a[n].config(bg = TARGET_FOUND_COLOR_2)
				if not zo.stopped_at_target : break
				if zo.exit_thread: break
				time.sleep(0.15)
		print("check_if_stopped_at_target OUT")

	def reset_now(self):
		zo.the_way_to_go = []
		zo.exit_thread = True
		zo.stopped_at_target = False
		#time.sleep(0.5) # Time for the task to end
		self.place_frame_do_buttons(zo.start_x,zo.start_y)


	def place_frame_do_buttons (self,x0,y0):#Place the frame at startposition
		self.destroy_boxes()
		print("1-zo.win_x, zo.win_y = x0,y0",zo.win_x, zo.win_y, x0,y0)
		zo.win_x, zo.win_y = x0,y0
		#time.sleep(1)
		self.frame.place(width = FRAME_WIDTH, height= FRAME_HEIGHT, x = zo.win_x, y = zo.win_y)
		zo.direction = zo.new_direction
		self.do_buttons()


	def destroy_boxes (self):
		#print("knappar", zo.a)
		for x in zo.a:
			zo.a[x].destroy()

	def place_new_frame (self):#Place the frame at a new startposition
		x0 = random.randint(0,(CANVAS_X/STEP_SIZE)-1)
		y0 = random.randint(0,(CANVAS_X/STEP_SIZE)-1)
		zo.start_x,zo.start_y = (CANVAS_PAD_X+1)+x0*STEP_SIZE,(START_BUTTON_HEIGHT+ CANVAS_PAD_Y+5)+y0*STEP_SIZE
		zo.new_direction = random.randint(DIRECTION_MIN,DIRECTION_MAX/DIRECTION_STEP)*DIRECTION_STEP
		self.reset_now()

	def check_window_border (self): # return True if within target
		print("check_window_border IN")
	# Check end of TOP window
		zo.at_border = False
		w_req, h_req = top.winfo_width(), top.winfo_height()
		#print("1-w_req,zo.win_x , offset, new_x",w_req,zo.win_x,-FRAME_WIDTH-CANVAS_PAD_X,w_req-FRAME_WIDTH-CANVAS_PAD_X)
		#print("1-h_req,zo.win_y ",h_req,zo.win_y)
		if zo.direction == 12 or zo.direction == 6 :
			if   zo.win_x < CANVAS_PAD_X : 					  zo.win_x = CANVAS_PAD_X; zo.at_border = True
			elif zo.win_x >= w_req - FRAME_WIDTH-CANVAS_PAD_X: zo.win_x = w_req - FRAME_WIDTH-CANVAS_PAD_X; zo.at_border = True
			if   zo.win_y < START_BUTTON_HEIGHT+6: 			  zo.win_y = START_BUTTON_HEIGHT+6; zo.at_border = True
			elif zo.win_y >= h_req - FRAME_HEIGHT-CANVAS_PAD_X:
				zo.win_y = h_req-FRAME_HEIGHT-CANVAS_PAD_X; zo.at_border = True
		else:
			if   zo.win_x < CANVAS_PAD_X:					  zo.win_x = CANVAS_PAD_X; zo.at_border = True
			elif zo.win_x >= w_req - FRAME_HEIGHT-CANVAS_PAD_X:zo.win_x = w_req-FRAME_HEIGHT-CANVAS_PAD_X; zo.at_border = True
			if   zo.win_y < START_BUTTON_HEIGHT:			  zo.win_y = START_BUTTON_HEIGHT; zo.at_border = True
			elif zo.win_y >= h_req - FRAME_WIDTH-CANVAS_PAD_Y: zo.win_y = h_req-FRAME_WIDTH-CANVAS_PAD_Y; zo.at_border = True

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
				print("return True")
				print("check_window_border OUT")
				return True
		#print("2-w_req,zo.win_x , offset",w_req,zo.win_x,-FRAME_WIDTH-(CANVAS_PAD_X))
		#print("2-h_req,zo.win_y ",h_req,zo.win_y)
		print("check_window_border OUT")
		return False

	def place_target(self):

		#if self.target_id: self.canvas1.delete(self.target_id)
		#zo.o_x0 = random.randint(CANVAS_PAD_X + TARGET_AREA, CANVAS_X-TARGET_SIZE -TARGET_AREA)
		#zo.o_y0 = random.randint(CANVAS_PAD_X+TARGET_AREA, CANVAS_Y - FRAME_HEIGHT-TARGET_SIZE-TARGET_AREA)
		zo.o_x0 = random.randint(0,(CANVAS_X/STEP_SIZE)-1)*STEP_SIZE+(STEP_SIZE/2)-TARGET_SIZE/2
		zo.o_y0 = random.randint(0,(CANVAS_X/STEP_SIZE)-1)*STEP_SIZE+(STEP_SIZE/2)-TARGET_SIZE/2

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
geo = str(TOP_X_GEOMETRY)+'x'+str(TOP_Y_GEOMETRY)
top.geometry(geo)
app = App(top)



top.mainloop()

#top.destroy()
