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
        # IMAGES
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
        '''
        # Pencil size
        self.frame1 = tk.Frame(self.frame20)
        self.label1 = tk.Label(self.frame1)
        self.label1.configure(background='#d7d7d7', text='Size', width='3')
        self.label1.pack(padx='5', pady='5', side='left')
        self.combobox1 = ttk.Combobox(self.frame1)
        self.combobox1.configure(width='6')
        self.combobox1.pack(padx='5', pady='5', side='left')
        self.frame1.configure(background='#d7d7d7', height='200', width='200')
        self.frame1.pack(side='left')
        # -----'''
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
    
    def init_canvas(self):
        #Scrollbar
        #everything in one window, paramaters on main window for canny detection,
        #buttons to change views, image scale is automatic, image size must be 100% correct,
        #files get saved in a folder that is automatically created

        
        self.canvas=Canvas(self.frame14)
        self.frame01 = tk.Frame(self.canvas)
        
        self.frame62 = tk.Frame(self.frame01)
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
        self.frame62.pack(anchor='n', expand='true', fill='both', side='bottom')
        
        self.yscrollbar=Scrollbar(self.frame14,orient="vertical",command=self.canvas.yview)
        self.yscrollbar.pack(side="right",fill="y")
        self.xscrollbar=Scrollbar(self.frame14,orient="horizontal",command=self.canvas.xview)
        self.xscrollbar.pack(side="bottom",fill="x")
        self.canvas.configure(background='#868686', height='0', width='0')
        self.canvas.configure(yscrollcommand=self.yscrollbar.set)
        self.canvas.configure(xscrollcommand=self.xscrollbar.set)
        self.canvas.pack(anchor='n', expand='true', fill='both', side='bottom')
        self.canvas.create_window((0,0), window=self.frame01, anchor="nw",tags="self.frame")
        self.frame01.bind("<Configure>", self.onFrameConfigure)
        #-------
        
        '''
        #New canvas
        self.frame62 = tk.Frame(self.frame14)
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
        self.frame62.pack(anchor='n', expand='true', fill='both', side='bottom')
        '''

    def loading_screen(self):
        self.temp_win = Toplevel()
        self.message_label = Label(self.temp_win , text = "Loading.. Please wait")
        self.message_label.pack()
        return "test"
    
    def init_preview_panel(self, filename):
        # Converting image to jpg
        '''
        image1 = Image.open(filename)
        filename = os.path.dirname(os.path.abspath(__file__))+'\\temp\\temp_jpg_img.jpg'
        filename = filename.replace("\\", "/")
        image1 = image1.convert('RGB')
        image1.save(filename)'''
        
        with open(filename, 'rb') as f:
            np_image_string = np.array([f.read()])
        
        image = Image.open(filename)
        width, height = image.size
        
        splash = Splash(self)
        
        segmentations = modules.detect(np_image_string,width,height)
        splash.destroy()
        #self.temp_win.destroy()
        self.newWindow = Toplevel(self.master)
 
        # sets the title of the
        # Toplevel widget
        self.newWindow.title("Mask Selector")
        
        
        seg_length = len(segmentations)
        if (len(segmentations)>=3):
            seg_length = 3
        # sets the geometry of mask selector
        self.newWindow.geometry(str(width*seg_length)+"x"+str(height+80))#default 200x200
        
        #Parameters frame
        self.frame68 = tk.Frame(self.newWindow)
        # Paramaters for Canny edge detection
        self.frame70 = tk.Frame(self.frame68)
        self.label47 = tk.Label(self.frame70)
        self.label47.configure(text='parameter 1', width='11')
        self.label47.pack(padx='5', pady='5', side='top')
        self.canny_param_1 = tk.DoubleVar()
        self.parameter_1 = Scale(self.frame70, from_=0, to=200, orient=HORIZONTAL, variable = self.canny_param_1)
        self.parameter_1.set(80)
        self.parameter_1.pack(side='top')
        self.frame70.pack(anchor='n', expand='false', fill='both', side='left')
        
        self.frame71 = tk.Frame(self.frame68)
        self.label48 = tk.Label(self.frame71)
        self.label48.configure(text='parameter 2', width='11')
        self.label48.pack(padx='5', pady='5', side='top')
        
        self.canny_param_2 = tk.DoubleVar()
        self.parameter_2 = Scale(self.frame71, from_=0, to=200, orient=HORIZONTAL, variable = self.canny_param_2)
        self.parameter_2.set(200)
        self.parameter_2.pack(side='top')
        self.frame71.pack(anchor='n', expand='false', fill='both', side='left')
        #self.canny_param_3 = tk.DoubleVar()
        #self.parameter_3 = Scale(self.frame68, from_=0, to=10, orient=HORIZONTAL, variable = self.canny_param_3)
        #self.parameter_3.pack()
        self.frame68.pack(anchor='n', expand='false', fill='both', side='top')
        
        #Segmentations frame
        self.frame69 = tk.Frame(self.newWindow)
        # Converting segmentations from 0 and 1 into 0 and 255
        for i in range(len(segmentations)):
            segmentations[i] = segmentations[i].astype('uint8')*255
        
        for i in range(seg_length):
            #print(segmentations[i])
            data = Image.fromarray(segmentations[i])
            segme = segmentations[i]
            if (i+1==3):
                data = Image.fromarray(segmentations[0] + segmentations[1] + segmentations[2])
                segme = segmentations[0] + segmentations[1] + segmentations[2]
            photo= ImageTk.PhotoImage(data)
            
            mask1 = filename
            # EXTREMELY CRUTIAL DONT REMOVE
            imagetest= Label(self.newWindow, image= photo)
            imagetest.image= photo
            #editor_mode(self, original_image, segmentation):
            Button(self.frame69, text = 'Click Me !', image = photo, command = lambda:  [self.editor_mode(image, segme), self.newWindow.destroy()]).pack(side = LEFT)
        self.frame69.pack(anchor='n', expand='true', fill='both', side='top')


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
        file.add_command(label="Save File", command=quit)
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
            self.init_preview_panel(filename)
    
    def save_files(self):
        global imagelabel
        foldername = filedialog.askdirectory()
        if foldername:
            #Need to add folder location
            ps = self.canvas1.postscript()#file = "canvas1_temp.ps"                         
            im = self.open_eps(ps, dpi=144)#144 was the only number that wouldnt create issues
            print(foldername)
            im.save(foldername+"/edges.ps", dpi=(144, 144))#119.5
            img = Image.open(foldername+"/edges" + '.ps')
            w, h = img.size
            img = img.crop([1, 1, w-3, h-3])
            img.save(foldername+"/edges" + '.png', 'png')
    
    def editor_mode(self, original_image, segmentation):
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
        '''
        self.image_noise = Label(self.canvas3, image= photo)
        self.image_noise.image = photo
        self.image_noise.pack(side=tk.LEFT)'''
    
    
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
                self.canvas1.create_line((lasx, lasy, event.x, event.y), 
                                  fill='white', 
                                  width=2)
        try:
            useEraser
        except NameError:
            return
        else:
            if (useEraser):
                self.canvas1.create_line((lasx, lasy, event.x, event.y), 
                                  fill='black', 
                                  width=2)
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
        img = img.crop([1, 1, w-3, h-3])
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

class AutoScrollbar(ttk.Scrollbar):
    ''' A scrollbar that hides itself if its not needed.
        Works only if you use the grid geometry manager '''
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
            ttk.Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise tk.TclError('Cannot use pack with this widget')

    def place(self, **kw):
        raise tk.TclError('Cannot use place with this widget')

class CanvasImage:
    """ Display and zoom image """
    def __init__(self, placeholder, path):
        """ Initialize the ImageFrame """
        self.imscale = 1.0  # scale for the canvas image zoom, public for outer classes
        self.__delta = 1.3  # zoom magnitude
        self.__filter = Image.ANTIALIAS  # could be: NEAREST, BILINEAR, BICUBIC and ANTIALIAS
        self.__previous_state = 0  # previous state of the keyboard
        self.path = path  # path to the image, should be public for outer classes
        # Create ImageFrame in placeholder widget
        self.__imframe = ttk.Frame(placeholder)  # placeholder of the ImageFrame object
        # Vertical and horizontal scrollbars for canvas
        hbar = AutoScrollbar(self.__imframe, orient='horizontal')
        vbar = AutoScrollbar(self.__imframe, orient='vertical')
        hbar.grid(row=1, column=0, sticky='we')
        vbar.grid(row=0, column=1, sticky='ns')
        # Create canvas and bind it with scrollbars. Public for outer classes
        self.canvas = tk.Canvas(self.__imframe, highlightthickness=0,
                                xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvas.grid(row=0, column=0, sticky='nswe')
        self.canvas.update()  # wait till canvas is created
        hbar.configure(command=self.__scroll_x)  # bind scrollbars to the canvas
        vbar.configure(command=self.__scroll_y)
        # Bind events to the Canvas
        self.canvas.bind('<Configure>', lambda event: self.__show_image())  # canvas is resized
        self.canvas.bind('<ButtonPress-1>', self.__move_from)  # remember canvas position
        self.canvas.bind('<B1-Motion>',     self.__move_to)  # move canvas to the new position
        self.canvas.bind('<MouseWheel>', self.__wheel)  # zoom for Windows and MacOS, but not Linux
        self.canvas.bind('<Button-5>',   self.__wheel)  # zoom for Linux, wheel scroll down
        self.canvas.bind('<Button-4>',   self.__wheel)  # zoom for Linux, wheel scroll up
        # Handle keystrokes in idle mode, because program slows down on a weak computers,
        # when too many key stroke events in the same time
        self.canvas.bind('<Key>', lambda event: self.canvas.after_idle(self.__keystroke, event))
        # Decide if this image huge or not
        self.__huge = False  # huge or not
        self.__huge_size = 14000  # define size of the huge image
        self.__band_width = 1024  # width of the tile band
        Image.MAX_IMAGE_PIXELS = 1000000000  # suppress DecompressionBombError for the big image
        with warnings.catch_warnings():  # suppress DecompressionBombWarning
            warnings.simplefilter('ignore')
            self.__image = Image.open(self.path)  # open image, but down't load it
        self.imwidth, self.imheight = self.__image.size  # public for outer classes
        if self.imwidth * self.imheight > self.__huge_size * self.__huge_size and \
           self.__image.tile[0][0] == 'raw':  # only raw images could be tiled
            self.__huge = True  # image is huge
            self.__offset = self.__image.tile[0][2]  # initial tile offset
            self.__tile = [self.__image.tile[0][0],  # it have to be 'raw'
                           [0, 0, self.imwidth, 0],  # tile extent (a rectangle)
                           self.__offset,
                           self.__image.tile[0][3]]  # list of arguments to the decoder
        self.__min_side = min(self.imwidth, self.imheight)  # get the smaller image side
        # Create image pyramid
        self.__pyramid = [self.smaller()] if self.__huge else [Image.open(self.path)]
        # Set ratio coefficient for image pyramid
        self.__ratio = max(self.imwidth, self.imheight) / self.__huge_size if self.__huge else 1.0
        self.__curr_img = 0  # current image from the pyramid
        self.__scale = self.imscale * self.__ratio  # image pyramide scale
        self.__reduction = 2  # reduction degree of image pyramid
        w, h = self.__pyramid[-1].size
        while w > 512 and h > 512:  # top pyramid image is around 512 pixels in size
            w /= self.__reduction  # divide on reduction degree
            h /= self.__reduction  # divide on reduction degree
            self.__pyramid.append(self.__pyramid[-1].resize((int(w), int(h)), self.__filter))
        # Put image into container rectangle and use it to set proper coordinates to the image
        self.container = self.canvas.create_rectangle((0, 0, self.imwidth, self.imheight), width=0)
        self.__show_image()  # show image on the canvas
        self.canvas.focus_set()  # set focus on the canvas

    def smaller(self):
        """ Resize image proportionally and return smaller image """
        w1, h1 = float(self.imwidth), float(self.imheight)
        w2, h2 = float(self.__huge_size), float(self.__huge_size)
        aspect_ratio1 = w1 / h1
        aspect_ratio2 = w2 / h2  # it equals to 1.0
        if aspect_ratio1 == aspect_ratio2:
            image = Image.new('RGB', (int(w2), int(h2)))
            k = h2 / h1  # compression ratio
            w = int(w2)  # band length
        elif aspect_ratio1 > aspect_ratio2:
            image = Image.new('RGB', (int(w2), int(w2 / aspect_ratio1)))
            k = h2 / w1  # compression ratio
            w = int(w2)  # band length
        else:  # aspect_ratio1 < aspect_ration2
            image = Image.new('RGB', (int(h2 * aspect_ratio1), int(h2)))
            k = h2 / h1  # compression ratio
            w = int(h2 * aspect_ratio1)  # band length
        i, j, n = 0, 1, round(0.5 + self.imheight / self.__band_width)
        while i < self.imheight:
            print('\rOpening image: {j} from {n}'.format(j=j, n=n), end='')
            band = min(self.__band_width, self.imheight - i)  # width of the tile band
            self.__tile[1][3] = band  # set band width
            self.__tile[2] = self.__offset + self.imwidth * i * 3  # tile offset (3 bytes per pixel)
            self.__image.close()
            self.__image = Image.open(self.path)  # reopen / reset image
            self.__image.size = (self.imwidth, band)  # set size of the tile band
            self.__image.tile = [self.__tile]  # set tile
            cropped = self.__image.crop((0, 0, self.imwidth, band))  # crop tile band
            image.paste(cropped.resize((w, int(band * k)+1), self.__filter), (0, int(i * k)))
            i += band
            j += 1
        print('\r' + 30*' ' + '\r', end='')  # hide printed string
        return image

    def redraw_figures(self):
        """ Dummy function to redraw figures in the children classes """
        pass

    def grid(self, **kw):
        """ Put CanvasImage widget on the parent widget """
        self.__imframe.grid(**kw)  # place CanvasImage widget on the grid
        self.__imframe.grid(sticky='nswe')  # make frame container sticky
        self.__imframe.rowconfigure(0, weight=1)  # make canvas expandable
        self.__imframe.columnconfigure(0, weight=1)

    def pack(self, **kw):
        """ Exception: cannot use pack with this widget """
        raise Exception('Cannot use pack with the widget ' + self.__class__.__name__)

    def place(self, **kw):
        """ Exception: cannot use place with this widget """
        raise Exception('Cannot use place with the widget ' + self.__class__.__name__)

    # noinspection PyUnusedLocal
    def __scroll_x(self, *args, **kwargs):
        """ Scroll canvas horizontally and redraw the image """
        self.canvas.xview(*args)  # scroll horizontally
        self.__show_image()  # redraw the image

    # noinspection PyUnusedLocal
    def __scroll_y(self, *args, **kwargs):
        """ Scroll canvas vertically and redraw the image """
        self.canvas.yview(*args)  # scroll vertically
        self.__show_image()  # redraw the image

    def __show_image(self):
        """ Show image on the Canvas. Implements correct image zoom almost like in Google Maps """
        box_image = self.canvas.coords(self.container)  # get image area
        box_canvas = (self.canvas.canvasx(0),  # get visible area of the canvas
                      self.canvas.canvasy(0),
                      self.canvas.canvasx(self.canvas.winfo_width()),
                      self.canvas.canvasy(self.canvas.winfo_height()))
        box_img_int = tuple(map(int, box_image))  # convert to integer or it will not work properly
        # Get scroll region box
        box_scroll = [min(box_img_int[0], box_canvas[0]), min(box_img_int[1], box_canvas[1]),
                      max(box_img_int[2], box_canvas[2]), max(box_img_int[3], box_canvas[3])]
        # Horizontal part of the image is in the visible area
        if  box_scroll[0] == box_canvas[0] and box_scroll[2] == box_canvas[2]:
            box_scroll[0]  = box_img_int[0]
            box_scroll[2]  = box_img_int[2]
        # Vertical part of the image is in the visible area
        if  box_scroll[1] == box_canvas[1] and box_scroll[3] == box_canvas[3]:
            box_scroll[1]  = box_img_int[1]
            box_scroll[3]  = box_img_int[3]
        # Convert scroll region to tuple and to integer
        self.canvas.configure(scrollregion=tuple(map(int, box_scroll)))  # set scroll region
        x1 = max(box_canvas[0] - box_image[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
        y1 = max(box_canvas[1] - box_image[1], 0)
        x2 = min(box_canvas[2], box_image[2]) - box_image[0]
        y2 = min(box_canvas[3], box_image[3]) - box_image[1]
        if int(x2 - x1) > 0 and int(y2 - y1) > 0:  # show image if it in the visible area
            if self.__huge and self.__curr_img < 0:  # show huge image
                h = int((y2 - y1) / self.imscale)  # height of the tile band
                self.__tile[1][3] = h  # set the tile band height
                self.__tile[2] = self.__offset + self.imwidth * int(y1 / self.imscale) * 3
                self.__image.close()
                self.__image = Image.open(self.path)  # reopen / reset image
                self.__image.size = (self.imwidth, h)  # set size of the tile band
                self.__image.tile = [self.__tile]
                image = self.__image.crop((int(x1 / self.imscale), 0, int(x2 / self.imscale), h))
            else:  # show normal image
                image = self.__pyramid[max(0, self.__curr_img)].crop(  # crop current img from pyramid
                                    (int(x1 / self.__scale), int(y1 / self.__scale),
                                     int(x2 / self.__scale), int(y2 / self.__scale)))
            #
            imagetk = ImageTk.PhotoImage(image.resize((int(x2 - x1), int(y2 - y1)), self.__filter))
            imageid = self.canvas.create_image(max(box_canvas[0], box_img_int[0]),
                                               max(box_canvas[1], box_img_int[1]),
                                               anchor='nw', image=imagetk)
            self.canvas.lower(imageid)  # set image into background
            self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection

    def __move_from(self, event):
        """ Remember previous coordinates for scrolling with the mouse """
        self.canvas.scan_mark(event.x, event.y)

    def __move_to(self, event):
        """ Drag (move) canvas to the new position """
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        self.__show_image()  # zoom tile and show it on the canvas

    def outside(self, x, y):
        """ Checks if the point (x,y) is outside the image area """
        bbox = self.canvas.coords(self.container)  # get image area
        if bbox[0] < x < bbox[2] and bbox[1] < y < bbox[3]:
            return False  # point (x,y) is inside the image area
        else:
            return True  # point (x,y) is outside the image area

    def __wheel(self, event):
        """ Zoom with mouse wheel """
        x = self.canvas.canvasx(event.x)  # get coordinates of the event on the canvas
        y = self.canvas.canvasy(event.y)
        if self.outside(x, y): return  # zoom only inside image area
        scale = 1.0
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:  # scroll down, smaller
            if round(self.__min_side * self.imscale) < 30: return  # image is less than 30 pixels
            self.imscale /= self.__delta
            scale        /= self.__delta
        if event.num == 4 or event.delta == 120:  # scroll up, bigger
            i = min(self.canvas.winfo_width(), self.canvas.winfo_height()) >> 1
            if i < self.imscale: return  # 1 pixel is bigger than the visible area
            self.imscale *= self.__delta
            scale        *= self.__delta
        # Take appropriate image from the pyramid
        k = self.imscale * self.__ratio  # temporary coefficient
        self.__curr_img = min((-1) * int(math.log(k, self.__reduction)), len(self.__pyramid) - 1)
        self.__scale = k * math.pow(self.__reduction, max(0, self.__curr_img))
        #
        self.canvas.scale('all', x, y, scale, scale)  # rescale all objects
        # Redraw some figures before showing image on the screen
        self.redraw_figures()  # method for child classes
        self.__show_image()

    def __keystroke(self, event):
        """ Scrolling with the keyboard.
            Independent from the language of the keyboard, CapsLock, <Ctrl>+<key>, etc. """
        if event.state - self.__previous_state == 4:  # means that the Control key is pressed
            pass  # do nothing if Control key is pressed
        else:
            self.__previous_state = event.state  # remember the last keystroke state
            # Up, Down, Left, Right keystrokes
            if event.keycode in [68, 39, 102]:  # scroll right: keys 'D', 'Right' or 'Numpad-6'
                self.__scroll_x('scroll',  1, 'unit', event=event)
            elif event.keycode in [65, 37, 100]:  # scroll left: keys 'A', 'Left' or 'Numpad-4'
                self.__scroll_x('scroll', -1, 'unit', event=event)
            elif event.keycode in [87, 38, 104]:  # scroll up: keys 'W', 'Up' or 'Numpad-8'
                self.__scroll_y('scroll', -1, 'unit', event=event)
            elif event.keycode in [83, 40, 98]:  # scroll down: keys 'S', 'Down' or 'Numpad-2'
                self.__scroll_y('scroll',  1, 'unit', event=event)

    def crop(self, bbox):
        """ Crop rectangle from the image and return it """
        if self.__huge:  # image is huge and not totally in RAM
            band = bbox[3] - bbox[1]  # width of the tile band
            self.__tile[1][3] = band  # set the tile height
            self.__tile[2] = self.__offset + self.imwidth * bbox[1] * 3  # set offset of the band
            self.__image.close()
            self.__image = Image.open(self.path)  # reopen / reset image
            self.__image.size = (self.imwidth, band)  # set size of the tile band
            self.__image.tile = [self.__tile]
            return self.__image.crop((bbox[0], 0, bbox[2], band))
        else:  # image is totally in RAM
            return self.__pyramid[0].crop(bbox)

    def destroy(self):
        """ ImageFrame destructor """
        self.__image.close()
        map(lambda i: i.close, self.__pyramid)  # close all pyramid images
        del self.__pyramid[:]  # delete pyramid list
        del self.__pyramid  # delete pyramid variable
        self.canvas.destroy()
        self.__imframe.destroy()


# root window created.
root = Tk()

root.geometry("1280x800")
app = Window(root)

#mainloop 
root.mainloop()