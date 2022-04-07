import tkinter as tk
from tkinter import ttk, Frame, Tk, Menu, RAISED, Button, LEFT, TOP, X, NW, Canvas, Toplevel, Scale, HORIZONTAL, Label, Scrollbar
import random
#from tkinter.ttk import *
from tkinter import filedialog
from PIL import ImageTk, Image, ImageGrab
from tkinter.colorchooser import askcolor
from io import BytesIO
import math
import threading
import concurrent.futures

#Mask testing
import cv2
from matplotlib import pyplot as plt
import numpy as np
import os

# Image masks, etc
import modules

thread_pool_executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)

# Here, we are creating our class, Window, and inheriting from the Frame
# class.
class Window(Frame):

    # Define settings upon initialization.
    def __init__(self, master=None):
        
        # parameters that you want to send through the Frame class. 
        Frame.__init__(self, master)   
              
        self.master = master

        self.init_window()
        
        self.init_toolbar()
        
        self.init_canvas()
        
    def switch(self):
        if self.button33["state"] == "normal":
            self.button33["state"] = "disabled"
            self.button32["state"] = "disabled"
        else:
            self.button33["state"] = "normal"
            self.button32["state"] = "normal"
    
    def init_toolbar(self):
        usepen = False
        
        self.frame14 = ttk.Frame(self.master)
        self.frame20 = tk.Frame(self.frame14)
        self.frame51 = tk.Frame(self.frame20)
        self.frame52 = tk.Frame(self.frame51)
        self.button30 = tk.Button(self.frame52, command=self.select_mode)
        #self.img_cursor = tk.PhotoImage(file='cursor.png')
        # IMAGES tools
        filename = os.path.dirname(os.path.abspath(__file__))+"\\resources\\cursor.png"
        filename = filename.replace("\\", "/")
        selectimg = Image.open(filename)
        selectimg = selectimg.resize((60, 60), Image.ANTIALIAS)
        self.img_cursor = ImageTk.PhotoImage(selectimg)
        
        filename = os.path.dirname(os.path.abspath(__file__))+"\\resources\\pencil.png"
        filename = filename.replace("\\", "/")
        selectimg = Image.open(filename)
        selectimg = selectimg.resize((60, 60), Image.ANTIALIAS)
        self.img_pencil = ImageTk.PhotoImage(selectimg)
        
        filename = os.path.dirname(os.path.abspath(__file__))+"\\resources\\eraser.png"
        filename = filename.replace("\\", "/")
        selectimg = Image.open(filename)
        selectimg = selectimg.resize((60, 60), Image.ANTIALIAS)
        self.img_eraser = ImageTk.PhotoImage(selectimg)
        
        self.button30.configure(bitmap='error', compound='top', default='normal', font='TkDefaultFont')
        self.button30.configure(height='60', image=self.img_cursor, overrelief='flat', relief='raised')
        self.button30.configure(repeatdelay='0', repeatinterval='0', takefocus=False)
        self.button30.configure(width='60')
        self.button30.pack(padx='5', pady='10', side='left')
        self.frame52.configure(background='#d7d7d7', height='200', width='200')
        self.frame52.pack(side='top')
        self.frame53 = tk.Frame(self.frame51)
        self.label55 = tk.Label(self.frame53)
        self.label55.configure(background='#d7d7d7', state='normal', text='Select', width='7')
        self.label55.pack(padx='5', pady='5', side='left')
        self.frame53.configure(background='#d7d7d7', height='200', width='200')
        self.frame53.pack(side='right')
        self.frame51.configure(background='#d7d7d7', height='200', width='200')
        self.frame51.pack(side='left')
        self.frame54 = tk.Frame(self.frame20)
        self.frame55 = tk.Frame(self.frame54)
        self.button32 = tk.Button(self.frame55, command=self.use_pen)
        self.button32.configure(bitmap='error', compound='top', default='normal', font='TkDefaultFont')
        self.button32.configure(height='60', image=self.img_pencil, overrelief='flat', relief='raised')
        self.button32.configure(repeatdelay='0', repeatinterval='0', takefocus=False)
        self.button32.configure(width='60')
        self.button32.pack(padx='5', pady='10', side='left')
        self.frame55.configure(background='#d7d7d7', height='200', width='200')
        self.frame55.pack(side='top')
        self.frame56 = tk.Frame(self.frame54)
        self.label56 = tk.Label(self.frame56)
        self.label56.configure(background='#d7d7d7', state='normal', text='Pencil', width='7')
        self.label56.pack(padx='5', pady='5', side='left')
        self.frame56.configure(background='#d7d7d7', height='200', width='200')
        self.frame56.pack(side='right')
        self.frame54.configure(background='#d7d7d7', height='200', width='200')
        self.frame54.pack(side='left')
        self.frame57 = tk.Frame(self.frame20)
        self.frame58 = tk.Frame(self.frame57)
        self.button33 = tk.Button(self.frame58, command=self.use_eraser)
        self.button33.configure(bitmap='error', compound='top', default='normal', font='TkDefaultFont')
        self.button33.configure(height='60', image=self.img_eraser, overrelief='flat', relief='raised')
        self.button33.configure(repeatdelay='0', repeatinterval='0', takefocus=False)
        self.button33.configure(width='60')
        self.button33.pack(padx='5', pady='10', side='left')
        self.frame58.configure(background='#d7d7d7', height='200', width='200')
        self.frame58.pack(side='top')
        self.frame59 = tk.Frame(self.frame57)
        self.label57 = tk.Label(self.frame59)
        self.label57.configure(background='#d7d7d7', state='normal', text='Eraser', width='7')
        self.label57.pack(padx='5', pady='5', side='left')
        self.frame59.configure(background='#d7d7d7', height='200', width='200')
        self.frame59.pack(side='right')
        self.frame57.configure(background='#d7d7d7', height='200', width='200')
        self.frame57.pack(side='left')
        # Pencil size
        self.frame1 = tk.Frame(self.frame20)
        self.label1 = tk.Label(self.frame1)
        self.label1.configure(background='#d7d7d7', text='Size', width='3')
        self.label1.pack(padx='5', pady='5', side='left')
        self.pencil_size_value = tk.StringVar()
        self.pencil_size_value.trace('w',self.on_field_change)
        self.combobox1 = ttk.Combobox(self.frame1)
        self.combobox1.configure(width='6', textvariable = self.pencil_size_value)
        self.combobox1['values'] = ([i for i in range(1,201,1)])
        self.combobox1.current(9)
        self.combobox1.pack(padx='5', pady='5', side='left')
        self.frame1.configure(background='#d7d7d7', height='200', width='200')
        self.frame1.pack(side='left')
        # -----
        self.separator10 = ttk.Separator(self.frame20)
        self.separator10.configure(orient='vertical')
        self.separator10.pack(expand='false', fill='y', padx='5', pady='5', side='left')
        self.frame19 = ttk.Frame(self.frame20)
        self.frame30 = tk.Frame(self.frame19)
        self.label39 = tk.Label(self.frame30)
        self.label39.configure(background='#d7d7d7', text='Distance', width='8')
        self.label39.pack(padx='5', pady='5', side='left')
        self.combobox20 = ttk.Combobox(self.frame30)
        self.distance_value = tk.StringVar()
        self.distance_value.trace('w',self.on_field_change)
        self.combobox20.configure(width='6', textvariable = self.distance_value)
        self.combobox20['values'] = ([i for i in range(1,201,1)])
        self.combobox20.current(9)
        self.combobox20.pack(padx='5', pady='5', side='left')
        self.frame30.configure(background='#d7d7d7', height='200', width='200')
        self.frame30.pack(side='top')
        self.frame31 = tk.Frame(self.frame19)
        self.label40 = tk.Label(self.frame31)
        self.label40.configure(background='#d7d7d7', text='Noise', width='8')
        self.label40.pack(padx='5', pady='5', side='left')
        self.combobox21 = ttk.Combobox(self.frame31)
        self.noise_value = tk.StringVar()
        self.noise_value.trace('w',self.on_field_change)
        self.combobox21.configure(width='6', textvariable = self.noise_value)
        value_list=[]
        for i in range(10000):
            value_list.append((i+1)*0.0001)
        #[i for i in range(0.0001,1,0.0001)]
        self.combobox21['values'] = (value_list)
        self.combobox21.current(9)
        self.combobox21.pack(padx='5', pady='5', side='left')
        self.frame31.configure(background='#d7d7d7', height='200', width='200')
        self.frame31.pack(side='bottom')
        self.frame32 = tk.Frame(self.frame19)
        self.label41 = tk.Label(self.frame32)
        self.label41.configure(background='#d7d7d7', text='Radius', width='8')
        self.label41.pack(padx='5', pady='5', side='left')
        self.combobox22 = ttk.Combobox(self.frame32)
        self.radius_value = tk.StringVar()
        self.radius_value.trace('w',self.on_field_change)
        self.combobox22.configure(width='6', textvariable = self.radius_value)
        self.combobox22['values'] = ([i for i in range(1,201,1)])
        self.combobox22.current(1)
        self.combobox22.pack(padx='5', pady='5', side='left')
        self.frame32.configure(background='#d7d7d7', height='200', width='200')
        self.frame32.pack(side='bottom')
        self.frame19.configure(height='200', width='200')
        self.frame19.pack(side='left')
        # IMAGES views
        filename = os.path.dirname(os.path.abspath(__file__))+"\\resources\\masks.png"
        filename = filename.replace("\\", "/")
        selectimg = Image.open(filename)
        selectimg = selectimg.resize((60, 60), Image.ANTIALIAS)
        self.img_masks = ImageTk.PhotoImage(selectimg)
        
        filename = os.path.dirname(os.path.abspath(__file__))+"\\resources\\edges.png"
        filename = filename.replace("\\", "/")
        selectimg = Image.open(filename)
        selectimg = selectimg.resize((60, 60), Image.ANTIALIAS)
        self.img_edges = ImageTk.PhotoImage(selectimg)
        
        filename = os.path.dirname(os.path.abspath(__file__))+"\\resources\\final.png"
        filename = filename.replace("\\", "/")
        selectimg = Image.open(filename)
        selectimg = selectimg.resize((60, 60), Image.ANTIALIAS)
        self.img_final = ImageTk.PhotoImage(selectimg)
        # --------
        # Masks and paramaters
        self.separator1 = ttk.Separator(self.frame20)
        self.separator1.configure(orient='vertical', takefocus=True)
        self.separator1.pack(expand='false', fill='y', padx='5', pady='5', side='left')
        self.frame2 = tk.Frame(self.frame20)
        self.frame3 = tk.Frame(self.frame2)
        
        # Masks button
        self.button1 = tk.Button(self.frame3, command=self.masks_view)
        self.button1.configure(bitmap='error', compound='top', default='normal', font='TkDefaultFont')
        self.button1.configure(height='60', image=self.img_masks, overrelief='flat', relief='raised')
        self.button1.configure(repeatdelay='0', repeatinterval='0', takefocus=False)
        self.button1.configure(width='60')
        self.button1.pack(padx='5', pady='10', side='left')
        self.frame3.configure(background='#d7d7d7', height='200', width='200')
        self.frame3.pack(side='top')
        self.frame4 = tk.Frame(self.frame2)
        self.label2 = tk.Label(self.frame4)
        self.label2.configure(background='#d7d7d7', state='normal', text='Masks', width='7')
        self.label2.pack(padx='5', pady='5', side='left')
        self.frame4.configure(background='#d7d7d7', height='200', width='200')
        self.frame4.pack(side='right')
        self.frame2.configure(background='#d7d7d7', height='200', width='200')
        self.frame2.pack(side='left')
        self.frame5 = tk.Frame(self.frame20)
        self.frame6 = tk.Frame(self.frame5)
        
        # Edges button
        self.button2 = tk.Button(self.frame6, command=self.edges_view)
        self.button2.configure(bitmap='error', compound='top', default='normal', font='TkDefaultFont')
        self.button2.configure(height='60', image=self.img_edges, overrelief='flat', relief='raised')
        self.button2.configure(repeatdelay='0', repeatinterval='0', takefocus=False)
        self.button2.configure(width='60')
        self.button2.pack(padx='5', pady='10', side='left')
        self.frame6.configure(background='#d7d7d7', height='200', width='200')
        self.frame6.pack(side='top')
        self.frame7 = tk.Frame(self.frame5)
        self.label3 = tk.Label(self.frame7)
        self.label3.configure(background='#d7d7d7', state='normal', text='Edge', width='7')
        self.label3.pack(padx='5', pady='5', side='left')
        self.frame7.configure(background='#d7d7d7', height='200', width='200')
        self.frame7.pack(side='right')
        self.frame5.configure(background='#d7d7d7', height='200', width='200')
        self.frame5.pack(side='left')
        self.frame8 = tk.Frame(self.frame20)
        self.frame9 = tk.Frame(self.frame8)
        
        # Dotted button
        self.button3 = tk.Button(self.frame9, command=self.dotted_view)
        self.button3.configure(bitmap='error', compound='top', default='normal', font='TkDefaultFont')
        self.button3.configure(height='60', image=self.img_final, overrelief='flat', relief='raised')
        self.button3.configure(repeatdelay='0', repeatinterval='0', takefocus=False)
        self.button3.configure(width='60')
        self.button3.pack(padx='5', pady='10', side='left')
        self.frame9.configure(background='#d7d7d7', height='200', width='200')
        self.frame9.pack(side='top')
        self.frame10 = tk.Frame(self.frame8)
        self.label4 = tk.Label(self.frame10)
        self.label4.configure(background='#d7d7d7', state='normal', text='Dots', width='7')
        self.label4.pack(padx='5', pady='5', side='left')
        self.frame10.configure(background='#d7d7d7', height='200', width='200')
        self.frame10.pack(side='right')
        self.frame8.configure(background='#d7d7d7', height='200', width='200')
        self.frame8.pack(side='left')
        self.separator2 = ttk.Separator(self.frame20)
        self.separator2.configure(orient='vertical', takefocus=True)
        self.separator2.pack(expand='false', fill='y', padx='5', pady='5', side='left')
        self.frame21 = tk.Frame(self.frame20)
        self.frame23 = tk.Frame(self.frame21)
        self.label27 = tk.Label(self.frame23)
        self.label27.configure(background='#d7d7d7', text='Canny edge parameters', width='18')
        self.label27.pack(padx='5', pady='5', side='left')
        self.frame23.configure(height='200', width='200', background='#d7d7d7')
        self.frame23.pack(side='bottom')
        self.frame41 = tk.Frame(self.frame21)
        self.frame45 = tk.Frame(self.frame41)
        self.frame46 = tk.Frame(self.frame45)
        self.label34 = tk.Label(self.frame46)
        self.label34.configure(background='#d7d7d7', text='Threshold 1', width='9')
        self.label34.pack(padx='5', pady='5', side='left')

        # Canny parameter 1
        self.canny_param_1 = tk.StringVar()
        self.canny_param_1.trace('w', self.update_edges)
        self.combobox30 = ttk.Combobox(self.frame46, textvariable = self.canny_param_1)
        self.combobox30['values'] = ([i for i in range(1,201,1)])
        self.combobox30.current(79)
        self.combobox30.configure(width='6')
        self.combobox30.pack(padx='5', pady='5', side='left')
        self.frame46.configure(background='#d7d7d7', height='200', width='200')
        self.frame46.pack(side='top')
        self.frame47 = tk.Frame(self.frame45)
        self.label35 = tk.Label(self.frame47)
        self.label35.configure(background='#d7d7d7', text='Threshold 2', width='9')
        self.label35.pack(padx='5', pady='5', side='left')
        
        # Canny parameter 2
        self.canny_param_2 = tk.StringVar()
        self.canny_param_1.trace('w', self.update_edges)
        self.combobox31 = ttk.Combobox(self.frame47, textvariable = self.canny_param_2)
        self.combobox31['values'] = ([i for i in range(1,201,1)])
        self.combobox31.current(199)
        self.combobox31.configure(width='6')
        self.combobox31.pack(padx='5', pady='5', side='left')
        self.frame47.configure(background='#d7d7d7', height='200', width='200')
        self.frame47.pack(side='top')
        self.frame45.configure(height='200', width='200')
        self.frame45.pack(side='left')
        self.frame26 = ttk.Frame(self.frame41)
        self.frame50 = tk.Frame(self.frame26)
        self.frame60 = tk.Frame(self.frame50)
        self.label40 = tk.Label(self.frame60)
        self.label40.configure(background='#d7d7d7', text='ApetureSize', width='9')
        self.label40.pack(padx='5', pady='5', side='left')
        self.combobox36 = ttk.Combobox(self.frame60)
        self.combobox36.configure(width='6')
        self.combobox36.pack(padx='5', pady='5', side='left')
        self.frame60.configure(background='#d7d7d7', height='200', width='200')
        self.frame60.pack(side='top')
        self.frame61 = tk.Frame(self.frame50)
        self.label41 = tk.Label(self.frame61)
        self.label41.configure(background='#d7d7d7', text='L2gradient', width='9')
        self.label41.pack(padx='5', pady='5', side='left')
        self.combobox37 = ttk.Combobox(self.frame61)
        self.combobox37.configure(width='6')
        self.combobox37.pack(padx='5', pady='5', side='left')
        self.frame61.configure(background='#d7d7d7', height='200', width='200')
        self.frame61.pack(side='top')
        self.frame50.configure(height='200', width='200')
        self.frame50.pack(side='top')
        self.frame26.configure(height='200', width='200')
        self.frame26.pack(side='left')
        self.frame41.configure(height='200', width='200')
        self.frame41.pack(side='top')
        self.frame21.configure(height='200', width='200', background='#d7d7d7')
        self.frame21.pack(side='left')
        # -------------------
        self.frame20.configure(background='#d7d7d7', borderwidth='1', height='200', relief='raised')
        self.frame20.configure(width='200')
        self.frame20.pack(anchor='nw', expand='false', fill='x', side='top')
        self.frame14.configure(cursor='arrow', height='200', relief='raised', takefocus=False)
        self.frame14.configure(width='200')
        
        self.switch()
        
        self.frame14.pack(anchor='nw', expand='true', fill='both', side='top')
    
    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def onCanvasConfigure(self, event):
        self.canvas.itemconfig(self.window, width=event.width, height=event.height)
        try:
            self.width
        except:
            if (event.width<1800):
                self.canvas.itemconfig(self.window, width=1800)
            if (event.height<400):
                self.canvas.itemconfig(self.window, height=400)
        else:
            if (event.width<self.width*3):
                self.canvas.itemconfig(self.window, width=self.width*3+50)
            if (event.height<self.height):
                self.canvas.itemconfig(self.window, height=self.height*20+20)
    
    def updateCanvasSize(self):
        root.update_idletasks()
        self.canvas.itemconfig(self.window, width=self.frame20.winfo_width())
        self.canvas.itemconfig(self.window, height=self.frame14.winfo_height()-self.frame20.winfo_height())
        
        
    def init_canvas(self):
        #Scrollbar
        #everything in one window, paramaters on main window for canny detection,
        #buttons to change views, image scale is automatic, image size must be 100% correct,
        #files get saved in a folder that is automatically created

        
        self.canvas=Canvas(self.frame14)
        self.frame01 = tk.Frame(self.canvas)
        
        # Editing canvas layout frame
        self.frame02 = tk.Frame(self.frame01)
        self.frame62 = tk.Frame(self.frame02)
        self.canvas1 = tk.Canvas(self.frame62)
        self.canvas1.configure(background='#aac1c4')
        self.canvas1.bind("<Button-1>", self.get_x_and_y)
        self.canvas1.bind("<B1-Motion>", self.draw_smth)
        self.canvas1.bind("<ButtonRelease-1>", self.check_changes)
        #self.canvas1.bind("<B1-Motion>", self.erase_smth)
        self.canvas1.pack(anchor='center', expand='true', padx='10', pady='10', side='left')
        self.canvas2 = tk.Canvas(self.frame62)
        self.canvas2.configure(background='#aac1c4')
        self.canvas2.pack(anchor='center', expand='true', pady='10', side='left')
        self.canvas3 = tk.Canvas(self.frame62)
        self.canvas3.configure(background='#aac1c4')
        self.canvas3.pack(anchor='center', expand='true', padx='10', pady='10', side='left')
        self.frame62.configure(background='#868686', height='200', width='200')
        #self.frame62.pack(anchor='n', expand='true', fill='both', side='bottom')
        self.frame62.pack(anchor='center', expand='true', fill='none', side='top')
        self.frame02.configure(background='#768686', height='200', width='200')
        self.frame02.pack(anchor='center', expand='true', fill='both', side='top')
        self.frame02.pack_forget()
        
        # Mask buttons layout frame (top layer)
        self.frame03 = tk.Frame(self.frame01)
        self.frame04 = tk.Frame(self.frame03)
        self.frame08 = tk.Frame(self.frame04)
        self.mask_canvas1 = tk.Canvas(self.frame08)
        self.mask_canvas1.configure(background='#aac1c4')
        self.mask_canvas1.pack(anchor='center', expand='true', padx='10', pady='10', side='left')
        self.mask_canvas2 = tk.Canvas(self.frame08)
        self.mask_canvas2.configure(background='#aac1c4')
        self.mask_canvas2.pack(anchor='center', expand='true', pady='10', side='left')
        self.mask_canvas3 = tk.Canvas(self.frame08)
        self.mask_canvas3.configure(background='#aac1c4')
        self.mask_canvas3.pack(anchor='center', expand='true', padx='10', pady='10', side='left')
        self.frame08.configure(background='#868686', height='200', width='200')
        self.frame08.pack(anchor='center', expand='true', fill='none', side='top')
        
        # Mask buttons bottom layer
        self.frame07 = tk.Frame(self.frame04)
        self.mask_canvas4 = tk.Canvas(self.frame07)
        self.mask_canvas4.configure(background='#aac1c4')
        self.mask_canvas4.pack(anchor='center', expand='true', padx='10', pady='10', side='left')
        self.mask_canvas5 = tk.Canvas(self.frame07)
        self.mask_canvas5.configure(background='#aac1c4')
        self.mask_canvas5.pack(anchor='center', expand='true', pady='10', side='left')
        self.mask_canvas6 = tk.Canvas(self.frame07)
        self.mask_canvas6.configure(background='#aac1c4')
        self.mask_canvas6.pack(anchor='center', expand='true', padx='10', pady='10', side='left')
        self.frame07.configure(background='#868686', height='200', width='200')
        self.frame07.pack(anchor='center', expand='true', fill='none', side='bottom')
        
        self.frame04.configure(background='#868686', height='200', width='200')
        self.frame04.pack(anchor='center', expand='true', fill='none', side='top')
        self.frame03.configure(background='#768686', height='200', width='200')
        self.frame03.pack(anchor='center', expand='true', fill='both', side='top')
        #self.frame03.pack_forget()
        
        # Edges buttons layout frame
        self.frame05 = tk.Frame(self.frame01)
        self.frame06 = tk.Frame(self.frame05)
        self.edges_canvas = tk.Canvas(self.frame06)
        self.edges_canvas.configure(background='#aac1c4')
        self.edges_canvas.pack(anchor='center', expand='true', padx='10', pady='10', side='left')
        self.frame06.configure(background='#868686', height='200', width='200')
        self.frame06.pack(anchor='center', expand='true', fill='none', side='top')
        self.frame05.configure(background='#768686', height='200', width='200')
        self.frame05.pack(anchor='center', expand='true', fill='both', side='top')
        self.frame05.pack_forget()
        
        self.yscrollbar = Scrollbar(self.frame14, orient="vertical", command=self.canvas.yview)
        self.yscrollbar.pack(side="right",fill="y")
        self.xscrollbar = Scrollbar(self.frame14, orient="horizontal", command=self.canvas.xview)
        self.xscrollbar.pack(side="bottom",fill="x")
        self.canvas.configure(background='#868686', height='0', width='0')
        self.canvas.configure(yscrollcommand=self.yscrollbar.set)
        self.canvas.configure(xscrollcommand=self.xscrollbar.set)
        self.canvas.pack(anchor='n', expand='true', fill='both', side='bottom')
        self.window = self.canvas.create_window((0,0), window=self.frame01, anchor="nw", tags="self.frame01")
        self.canvas.bind("<Configure>", self.onCanvasConfigure)
        self.frame01.bind("<Configure>", self.onFrameConfigure)
        
        ## middle mode
        #self.frame01.pack(anchor='n', expand='true', fill='both', side='bottom')
        ##
        #-------

    def loading_screen(self):
        self.temp_win = Toplevel()
        self.message_label = Label(self.temp_win , text = "Loading.. Please wait")
        self.message_label.pack()
        return "test"
    
    def masks_view(self):
        self.frame03.pack(anchor='center', expand='true', fill='both', side='top')
        self.frame02.pack_forget()
        self.frame05.pack_forget()
    
    def dotted_view(self):
        self.frame02.pack(anchor='center', expand='true', fill='both', side='top')
        self.frame03.pack_forget()
        self.frame05.pack_forget()
    
    def edges_view(self):
        self.frame05.pack(anchor='center', expand='true', fill='both', side='top')
        self.frame03.pack_forget()
        self.frame02.pack_forget()

    def masks_panel(self, filename):
        # Converting image to jpg (image error)
        if (filename.endswith(".png")):
            image1 = Image.open(filename)
            filename = os.path.dirname(os.path.abspath(__file__))+'\\temp\\temp_jpg_img.jpg'
            filename = filename.replace("\\", "/")
            image1 = image1.convert('RGB')
            image1.save(filename)
        
        
        with open(filename, 'rb') as f:
            np_image_string = np.array([f.read()])
        
        image = Image.open(filename)
        self.width, self.height = image.size
        
        segmentations = modules.detect(np_image_string,self.width,self.height)

        seg_length = len(segmentations)
        if (len(segmentations)>=3):
            seg_length = 3
        
        # Converting segmentations from 0 and 1 into 0 and 255
        for i in range(len(segmentations)):
            segmentations[i] = segmentations[i].astype('uint8')*255
        
        self.masks_view()
        
        try:
            self.mask1.destroy()
            self.mask2.destroy()
            self.mask3.destroy()
            self.mask4.destroy()
            self.mask5.destroy()
            self.mask6.destroy()
            self.mask_canvas1.pack_forget()
            self.mask_canvas2.pack_forget()
            self.mask_canvas3.pack_forget()
            self.mask_canvas4.pack_forget()
            self.mask_canvas5.pack_forget()
            self.mask_canvas6.pack_forget()
        except:
            pass
        
        for i in range(seg_length):
            data = Image.fromarray(segmentations[i])
            segme = segmentations[i]
            if (i+1==3):
                data = Image.fromarray(segmentations[0] + segmentations[1] + segmentations[2])
                segme = segmentations[0] + segmentations[1] + segmentations[2]
            photo= ImageTk.PhotoImage(data)
            
            # EXTREMELY CRUTIAL DONT REMOVE
            imagetest= Label(self, image= photo)
            imagetest.image= photo
            if (i==0):
                self.mask_canvas1.pack(anchor='center', expand='true', padx='10', pady='10', side='left')
                self.mask1 = Button(self.mask_canvas1, text = 'Click Me !', image = photo, command = lambda:  [self.edges_panel(image, segme)])
                self.mask1.pack(side = LEFT)
            if (i==1):
                self.mask_canvas2.pack(anchor='center', expand='true', pady='10', side='left')
                self.mask2 = Button(self.mask_canvas2, text = 'Click Me !', image = photo, command = lambda:  [self.edges_panel(image, segme)])
                self.mask2.pack(side = LEFT)
            if (i==2):
                self.mask_canvas3.pack(anchor='center', expand='true', padx='10', pady='10', side='left')
                self.mask3 = Button(self.mask_canvas3, text = 'Click Me !', image = photo, command = lambda:  [self.edges_panel(image, segme)])
                self.mask3.pack(side = LEFT)
        
        if (seg_length==3):
            # Combination 1
            data1 = Image.fromarray(segmentations[0] + segmentations[1])
            segme1 = segmentations[0] + segmentations[1]
            photo= ImageTk.PhotoImage(data1)
            imagetest= Label(self, image= photo)
            imagetest.image= photo
            self.mask_canvas4.pack(anchor='center', expand='true', padx='10', pady='10', side='left')
            self.mask4 = Button(self.mask_canvas4, text = 'Click Me !', image = photo, command = lambda:  [self.edges_panel(image, segme1)])
            self.mask4.pack(side = LEFT)
            
            # Combination 2
            data2 = Image.fromarray(segmentations[2] + segmentations[1])
            segme2 = segmentations[2] + segmentations[1]
            photo= ImageTk.PhotoImage(data2)
            imagetest= Label(self, image= photo)
            imagetest.image= photo
            self.mask_canvas5.pack(anchor='center', expand='true', pady='10', side='left')
            self.mask5 = Button(self.mask_canvas5, text = 'Click Me !', image = photo, command = lambda:  [self.edges_panel(image, segme2)])
            self.mask5.pack(side = LEFT)
            
            # Combination 3
            data3 = Image.fromarray(segmentations[0] + segmentations[2])
            segme3 = segmentations[0] + segmentations[2]
            photo= ImageTk.PhotoImage(data3)
            imagetest= Label(self, image= photo)
            imagetest.image= photo
            self.mask_canvas6.pack(anchor='center', expand='true', padx='10', pady='10', side='left')
            self.mask6 = Button(self.mask_canvas6, text = 'Click Me !', image = photo, command = lambda:  [self.edges_panel(image, segme3)])
            self.mask6.pack(side = LEFT)
    
    def edges_panel(self, original_image, segmentation):
        
        self.edges_view()
        
        try:
            self.edges_selector.destroy()
        except:
            pass
        
        self.original_image = original_image
        image = np.array(original_image)
        self.seg = segmentation # one may have to chose 1,2 or 3 shapes here
        self.seg[np.where(self.seg>0) ]=1
        for l in range(3):
            image[:,:,l]= image[:,:,l]*self.seg
        edges_out = cv2.Canny(self.seg,1,1) # segment outer edge, some images may look better not including this
        image = cv2.blur(image, (3,3))
        edges = cv2.Canny(image,int(self.canny_param_1.get()),int(self.canny_param_2.get())) # the parameters of this is one choice that user may have to make # 80, 200
        edges = edges | edges_out # again some images may look better without the outser edge
        
        photo = ImageTk.PhotoImage(Image.fromarray(edges))
        
        # EXTREMELY CRUTIAL DONT REMOVE
        imagetest= Label(self, image= photo)
        imagetest.image= photo
        self.edges_selector = Button(self.edges_canvas, text = 'Click Me !', image = photo, command = lambda:  [self.editor_mode(image, segmentation)])
        self.edges_selector.pack(side = LEFT)
        
        self.updateCanvasSize()
    
    def update_edges(self, index, value, op):
        try:
            self.edges_selector.destroy()
        except:
            pass
        
        try:
            image = np.array(self.original_image)
        except:
            return
        
        self.seg[np.where(self.seg>0) ]=1
        for l in range(3):
            image[:,:,l]= image[:,:,l]*self.seg
        edges_out = cv2.Canny(self.seg,1,1) # segment outer edge, some images may look better not including this
        image = cv2.blur(image, (3,3))
        edges = cv2.Canny(image,int(self.canny_param_1.get()),int(self.canny_param_2.get())) # the parameters of this is one choice that user may have to make # 80, 200
        edges = edges | edges_out # again some images may look better without the outser edge
        
        photo = ImageTk.PhotoImage(Image.fromarray(edges))
        
        # EXTREMELY CRUTIAL DONT REMOVE
        imagetest= Label(self, image= photo)
        imagetest.image= photo
        self.edges_selector = Button(self.edges_canvas, text = 'Click Me !', image = photo, command = lambda:  [self.editor_mode(image, self.seg)])
        self.edges_selector.pack(side = LEFT)
        
        self.updateCanvasSize()


    #Creation of init_window
    def init_window(self):

        # changing the title of our master widget      
        self.master.title("Constellations GUI")

        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # create the file object)
        file = Menu(menu, tearoff=False)
        
        file.add_command(label="Open File", command=self.open_file)
        file.add_command(label="Open Project", command=self.open_file)
        file.add_command(label="Save Project", command=self.save_files)
        #file.add_command(label="Save File", command=quit)
        file.add_command(label="Exit", command=quit)#command=self.client_exit

        menu.add_cascade(label="File", menu=file)

        edit = Menu(menu, tearoff=False)
        edit.add_command(label="Undo")

        menu.add_cascade(label="Edit", menu=edit)
        self.pack()

    
    def client_exit(self):
        exit()
    
    def open_file(self):
        global imagelabel
        filename = filedialog.askopenfilename(parent=root, title='Choose a file', filetypes=[
            ('image files', ('.png', '.jpg')),])
        if filename:
            self.masks_panel(filename)
            #self.init_preview_panel(filename)
    
    def save_files(self):
        global imagelabel
        foldername = filedialog.askdirectory()
        if foldername:
            #Need to add folder location
            ps = self.canvas1.postscript()#file = "canvas1_temp.ps"                         
            im = self.open_eps(ps, dpi=144)#144 was the only number that wouldnt create issues
            im.save(foldername+"/edges.ps", dpi=(144, 144))#119.5
            img = Image.open(foldername+"/edges" + '.ps')
            w, h = img.size
            img = img.crop([1, 0, w-2, h-3])
            img.save(foldername+"/edges" + '.png', 'png')
            #print(str(self.width) +" "+ str(self.height))
            #print(img.size)
            # Dotted
            ps = self.canvas2.postscript()#file = "canvas1_temp.ps"                         
            im = self.open_eps(ps, dpi=144)#144 was the only number that wouldnt create issues
            im.save(foldername+"/dotted.ps", dpi=(144, 144))#119.5
            img = Image.open(foldername+"/dotted" + '.ps')
            w, h = img.size
            img = img.crop([1, 0, w-2, h-3])
            img.save(foldername+"/dotted" + '.png', 'png')
            # Final
            ps = self.canvas3.postscript()#file = "canvas1_temp.ps"                         
            im = self.open_eps(ps, dpi=144)#144 was the only number that wouldnt create issues
            im.save(foldername+"/final.ps", dpi=(144, 144))#119.5
            img = Image.open(foldername+"/final" + '.ps')
            w, h = img.size
            img = img.crop([1, 0, w-2, h-3])
            img.save(foldername+"/final" + '.png', 'png')
    
    
    
    def editor_mode(self, original_image, segmentation):
        
        self.frame02.pack(anchor='center', expand='true', fill='both', side='top')
        self.frame03.pack_forget()
        self.frame05.pack_forget()
        
        global isEditable
        try:
            isEditable
        except NameError:
            isEditable = True
        else:
            isEditable = True
        try:
            self.image_edges.destroy()
            self.image_dotted.destroy()
            self.image_noise.destroy()
        except:
            pass
        self.canvas1.delete("all")
        
        self.button33["state"] = "normal"
        self.button32["state"] = "normal"
        
        image = np.array(original_image)
        seg = segmentation # one may have to chose 1,2 or 3 shapes here
        seg[np.where(seg>0) ]=1
        for l in range(3):
            image[:,:,l]= image[:,:,l]*seg
        edges_out = cv2.Canny(seg,1,1) # segment outer edge, some images may look better not including this
        image = cv2.blur(image, (3,3))
        edges = cv2.Canny(image,int(self.canny_param_1.get()),int(self.canny_param_2.get())) # the parameters of this is one choice that user may have to make # 80, 200
        edges = edges | edges_out # again some images may look better without the outser edge
        
        self.photo_edges = ImageTk.PhotoImage(Image.fromarray(edges))
        self.canvas1.config(width=self.photo_edges.width()-2, height=self.photo_edges.height()-2)
        self.canvas1.create_image(0, 0, image = self.photo_edges, anchor = NW, tag = "edges")
        
        dotted = modules.generate_image_dotted(edges,10,2)
        self.photo_dotted = ImageTk.PhotoImage(dotted)
        self.canvas2.config(width=self.photo_dotted.width()-2, height=self.photo_dotted.height()-2)
        self.canvas2.create_image(0, 0, image = self.photo_dotted, anchor = NW)
        
        final = modules.add_noise(dotted,prob = 0.001,dot =2 )
        self.photo_final = ImageTk.PhotoImage(Image.fromarray(final))
        self.canvas3.config(width=self.photo_final.width()-2, height=self.photo_final.height()-2)
        self.canvas3.create_image(0, 0, image = self.photo_final, anchor = NW)
        
        self.updateCanvasSize()
    
    
    def get_x_and_y(self, event):
        global lasx, lasy
        lasx, lasy = event.x, event.y

    def draw_smth(self, event):
        global lasx, lasy
        try:
            usepen
        except NameError:
            return
        else:
            if (usepen):
                #self.canvas1.create_line((lasx, lasy, event.x, event.y), 
                                  #fill='white', 
                                  #width=self.pencil_size_value.get())
                self.canvas1.create_oval((lasx, lasy, event.x, event.y), 
                                  fill='white', outline='white',
                                  width=self.pencil_size_value.get())
        try:
            useEraser
        except NameError:
            return
        else:
            if (useEraser):
                self.canvas1.create_oval((lasx, lasy, event.x, event.y), 
                                  fill='black', 
                                  width=self.pencil_size_value.get())
        lasx, lasy = event.x, event.y
    
    def check_changes(self, event):
        global lasx, lasy
        try:
            usepen
        except NameError:
            return
        else:
            if (usepen):
                self.update_canvas()
        try:
            useEraser
        except NameError:
            return
        else:
            if (useEraser):
                self.update_canvas()
        lasx, lasy = event.x, event.y

    def open_eps(self, ps, dpi=300.0):
            img = Image.open(BytesIO(ps.encode('utf-8')))
            original = [float(d) for d in img.size]
            scale = dpi/72.0            
            if dpi is not 0:
                img.load(scale = math.ceil(scale))
            if scale != 1:
                img.thumbnail([round(scale * d) for d in original], Image.ANTIALIAS)
            return img
    
    def on_field_change(self, index, value, op):
        global isEditable
        try:
            isEditable
        except NameError:
            isEditable = False
        else:
            if (isEditable):
                self.update_canvas()
    
    def update_canvas(self):
        ps = self.canvas1.postscript()#file = "canvas1_temp.ps"                         

        """ canvas postscripts seem to be saved at 0.60 scale, so we need to increase the default dpi (72) by 60 percent """
        im = self.open_eps(ps, dpi=144)#144 was the only number that wouldnt create issues
        
        im.save("tester.ps", dpi=(144, 144))#119.5
        img = Image.open("tester" + '.ps')
        w, h = img.size
        img = img.crop([1, 0, w-2, h-3])
        img.save("tester" + '.png', 'png')
        
        img = cv2.imread("tester.png")
        edges = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        dotted = modules.generate_image_dotted(edges,int(self.distance_value.get()),int(self.radius_value.get()))
        self.photo_dotted = ImageTk.PhotoImage(dotted)
        self.canvas2.config(width=self.photo_dotted.width()-2, height=self.photo_dotted.height()-2)
        self.canvas2.create_image(0, 0, image = self.photo_dotted, anchor = NW)
        
        final = modules.add_noise(dotted,prob = float(self.noise_value.get()),dot =int(self.radius_value.get()) )#0.001 #smallest 0.0001
        self.photo_final = ImageTk.PhotoImage(Image.fromarray(final))
        self.canvas3.config(width=self.photo_final.width()-2, height=self.photo_final.height()-2)
        self.canvas3.create_image(0, 0, image = self.photo_final, anchor = NW)
        #print(self.photo_final.width())
    
    def select_mode(self):
        global usepen
        global useEraser
        try:
            usepen
        except NameError:
            usepen = False
        else:
            usepen = False
        try:
            usepen
        except NameError:
            usepen = False
        else:
            usepen = False
    
    def use_pen(self):
        global usepen
        global useEraser
        try:
            usepen
        except NameError:
            usepen = True
        else:
            usepen = not usepen
        try:
            useEraser
        except NameError:
            useEraser = False
        else:
            useEraser = False
    
    def use_eraser(self):
        global usepen
        global useEraser
        try:
            useEraser
        except NameError:
            useEraser = True
        else:
            useEraser = not useEraser
        try:
            usepen
        except NameError:
            usepen = False
        else:
            usepen = False

class Splash(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title("Loading...")
        self.message_label = Label(self, text = "Loading.. Please wait")
        self.message_label.pack()
        ## required to make window show before the program gets to the mainloop
        self.update()


# root window created.
root = Tk()

window_height = 800
window_width = 1280

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
#root.geometry("1280x800")
app = Window(root)

#mainloop 
root.mainloop()