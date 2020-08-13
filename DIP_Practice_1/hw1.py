from PIL import Image, ImageTk
from tkinter import messagebox
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
#import cv2 as cv
#from tkinter import ttk

window = tk.Tk()					# create window
window.title( 'B063040061 hw1' )	# name title

flagOpen = False					# file open flag
flagBrightnessContrast = True		# True : Brightness, False : Contrast
method = tk.IntVar()				# radiobutton value
alpha = tk.DoubleVar()				#	
beta = tk.DoubleVar()				# scale value variable
zoom = tk.DoubleVar()				#
lr = tk.DoubleVar()
ud = tk.DoubleVar()
method.set(0)						# initialize radiobutton value
zoom.set(1)							# initialize scale value

def WarningMessage() :
	# warning message show if image name not found
	a = tk.messagebox.showwarning( 'Warning', 'File Not Found!\nPlease try again!' )
	
def ShowInfo() :
	# successful message saved
	a = tk.messagebox.showinfo( 'Success', 'File Saved!' )
	
def ShowWarning() :
	# successful message saved
	a = tk.messagebox.showwarning( 'Failed', 'Unknowed type' )

def oCBOpen() :
	# open or reset the image
	global flagOpen, render, imgOri, imgEdit, curimage, load
	if flagOpen == False :
		#flagOpen = True
		
		try :
			curimage = Image.open( o.get() ).resize( ( 300, 300 ), Image.ANTIALIAS )
			load = Image.open( o.get() ).resize( ( 300, 300 ), Image.ANTIALIAS )
			render = ImageTk.PhotoImage( load )					# load load
			#im = cv.imread( e.get() )
			#new_image = np.zeros( im.shape, im.dtype )
		
			imgOri.config( image = render )				# edit label image
			imgOri.image = render
			
			imgEdit.config( image = render )			# edit label image
			imgEdit.image = render
			
			#img.pack()
			scaleZoom.config( command = ZoomBilinear )
			method.set(0)						# reset radiobutton value
			zoom.set(1)							# reset scale value
			
		except Exception :		# or IOError
			# when something wrong with image
			WarningMessage()
		
def oCBSave() :
	# save current image
	try :
		curimage.save(s.get())
		ShowInfo()
	except Exception :
		ShowWarning()
		
def oCBBC() :
	# on click button brightness/contrast
	global flagBrightnessContrast
	if flagBrightnessContrast == True :
		flagBrightnessContrast = False
		btnBC.config( text = 'Contrast' )
	else :
		flagBrightnessContrast = True 
		btnBC.config( text = 'Brightness' )
		
def editCB(q) :
	# edit contrast/brightness
	global curimage, flagBrightnessContrast
	newim = []			# new image
	curimage = load.resize((int(zoom.get()*300), int(zoom.get()*300)), Image.BILINEAR )
	if method.get() == 1 :										# linearly
		if flagBrightnessContrast == True :
			#alpha.set()
			for x in curimage.getdata() :						# load
				newim.append( x*alpha.get()+beta.get() )
		else :
			beta.set(128-128*alpha.get())
			for x in curimage.getdata() :						# load
				newim.append( x*alpha.get()+beta.get() )
	elif method.get() == 2 :									# exponential
		for x in curimage.getdata() :							# load
			newim.append( np.exp( x*alpha.get() )+beta.get()-1 )	
	else :														# logarithmically
		al = alpha.get()
		for x in curimage.getdata() :							# load
			newim.append( 255/np.log( 1+255*al )*np.log( x*al+beta.get() )-64 )		
	#curimage = Image.new( curimage.mode, curimage.size )		# load load
	curimage.putdata(newim)
	imgtk = ImageTk.PhotoImage( image = curimage )
	imgOri.config( image = imgtk )
	imgOri.image = imgtk
	
def adjustCB() :
	# adjust contrast/brightness of scale function
	if  method.get() == 1 :
		scaleA.config( from_ = 0, to = 5, tickinterval = 1, resolution = 0.1,
					   variable = alpha, command = editCB )
		scaleA.set(1)
		scaleB.config( from_ = -512, to = 256, tickinterval = 20, resolution = 1,
					   variable = beta, command = editCB )
	
	elif method.get() == 2 :
		scaleA.config( from_ = 0, to = 1, tickinterval = 0.1, resolution = 0.01,
					   variable = alpha, command = editCB )
		scaleA.set(0.05)
		scaleB.config( from_ = -5, to = 255, tickinterval = 5, resolution = 1,
					   variable = beta, command = editCB )
		
	else :
		scaleA.config( from_ = 0.1, to = 5, tickinterval = 1, resolution = 0.1,
					   variable = alpha, command = editCB )
		scaleA.set(0.1)
		scaleB.config( from_ = 1, to = 100, tickinterval = 20, resolution = 1,
					   variable = beta, command = editCB )
					   
def ZoomBilinear(z) :
	# bilinear zoom algorithm
	global curimage, load
	try :
		re = curimage.resize((int(zoom.get()*300), int(zoom.get()*300)), Image.BILINEAR )
	except Exception :
		re = load.resize((int(zoom.get()*300), int(zoom.get()*300)), Image.BILINEAR )
	
	if zoom.get() > 1 :				# zoom image using bar to view hall image
		scaleLR.config( from_ = 150, to = zoom.get()*300-150, variable = lr )
		scaleUD.config( from_ = 150, to = zoom.get()*300-150, variable = ud )
		scaleLR.place( x = 120, y = 340 )
		scaleUD.place( x = 420, y = 40 ) 
		area = ( lr.get()-150, ud.get()-150, lr.get()+150, ud.get()+150 )
		cropped_img = re.crop(area)
		imgtk = ImageTk.PhotoImage( image = cropped_img )
	else :
		scaleLR.place_forget()
		scaleUD.place_forget()
		imgtk = ImageTk.PhotoImage( image = re )
	
	imgOri.config( image = imgtk ) #anchor
	imgOri.image = imgtk
	
def Histequalize( image_array,image_bins = 256 ):
	
	# 將圖像矩陣轉化成直方圖數據，返回元組(頻數，直方圖區間座標)
	image_array2,bins = np.histogram( image_array.flatten(), image_bins )
	# 計算直方圖的累積函數
	cdf = image_array2.cumsum()
	# 將累積函數轉化到區間[0,255]
	cdf = ( 255.0/cdf[-1] )*cdf
	# 原圖像矩陣利用累積函數進行轉化，插值過程
	image2_array = np.interp( image_array.flatten(), bins[:-1], cdf)
	# 返回均衡化後的圖像矩陣和累積函數
	return image2_array.reshape( image_array.shape )
    
def Hist() :
	# Histogram function
	global curimage
	image_array = np.array( curimage )
	plt.subplot( 2, 2, 1 )
	plt.hist( image_array.flatten(), 256 )
	plt.subplot( 2, 2, 2 )
	plt.imshow( image_array, cmap = 'gray' )
	plt.axis( "off" )
	# 利用剛定義的直方圖均衡化函數對圖像進行均衡化處理
	afterHistEqu = Histequalize( image_array )
	plt.subplot( 2, 2, 3 )
	plt.hist( afterHistEqu.flatten(), 256 )
	plt.subplot( 2, 2, 4 )
	plt.imshow( afterHistEqu, cmap = 'gray' )
	plt.axis( "off" )
	#plt.show()
	
	curimage = Image.fromarray( afterHistEqu )
	curimage = curimage.convert( 'L' )
	imgtk = ImageTk.PhotoImage( image = curimage )
	imgOri.config( image = imgtk )
	imgOri.image = imgtk
	plt.show()

#--------------------using tkinter GUI-----------------------

imgOri = tk.Label( window, width = 300, height = 300 )
imgEdit = tk.Label( window, width = 300, height = 300 )
oName = tk.Label( window, text = 'Open File : ', width = 10, height = 1 )
sName = tk.Label( window, text = 'Save File : ', width = 10, height = 1 )
o = tk.Entry( window )
s = tk.Entry( window )
btnOpen = tk.Button( window, width = 10, height = 1, text = 'open / reset', command = oCBOpen )
btnSave = tk.Button( window, width = 10, height = 1, text = 'save', command = oCBSave ) 
btnBC = tk.Button( window, width = 10, height = 1, text = 'Brightness', command = oCBBC )
scaleA = tk.Scale( window, label = 'a', orient = tk.HORIZONTAL, length = 630, 
					width = 10 ) 
scaleB = tk.Scale( window, label = 'b', orient = tk.HORIZONTAL, length = 630, 
					width = 10 ) 
rbtnAdujust1 = tk.Radiobutton( window, text = 'Linearly', variable = method,
							   value = 1, command = adjustCB ) 
rbtnAdujust2 = tk.Radiobutton( window, text = 'Exponentially', variable = method,
							   value = 2, command = adjustCB ) 
rbtnAdujust3 = tk.Radiobutton( window, text = 'Logarithmically', variable = method,
							   value = 3, command = adjustCB )
zoomLabel = tk.Label( window, text = 'Zoom', width = 10, height = 1 )
scaleZoom = tk.Scale( window, label = 'Zoom', orient = tk.HORIZONTAL, length = 630,
					  to = 3, from_ = 0.1, resolution = 0.1, width = 10,
					  variable = zoom ) 
btnHis = tk.Button( window, width = 10, height = 1, text = 'Histogram', command = Hist )
scaleLR = tk.Scale( window, orient = tk.HORIZONTAL, length = 300, showvalue = 0,
					width = 10, command = ZoomBilinear ) 
scaleUD = tk.Scale( window, orient = tk.VERTICAL, length = 300, showvalue = 0,
					width = 10, command = ZoomBilinear ) 

imgOri.place( x = 120, y = 40 )
imgEdit.place( x = 450, y = 40 )
oName.place( x = 30, y = 5 )
sName.place( x = 360, y = 5 )
o.place( x = 120, y = 5 )
s.place( x = 450, y = 5 )
btnOpen.place( x = 10 , y = 40 ) 
btnSave.place( x = 10 , y = 80 ) 
btnBC.place( x = 10, y = 350 )
scaleA.place ( x = 120, y = 350 )
scaleB.place ( x = 120, y = 410 )
rbtnAdujust1.place( x = 0, y = 390 )
rbtnAdujust2.place( x = 0, y = 415 )
rbtnAdujust3.place( x = 0, y = 440 )
zoomLabel.place( x = 20, y = 510 )
scaleZoom.place( x = 120, y = 470 )
btnHis.place( x = 10, y = 550 )

#--------------------using tkinter GUI-----------------------

window.geometry( "800x600" )
window.mainloop()

