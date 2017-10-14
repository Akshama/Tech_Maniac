# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rest_framework import permissions,generics
from rest_framework.decorators import api_view,permission_classes
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter



@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def get_image(request):
	stringIMAGE =  request.data['image']
	name= request.data['name']
	f = request.data['f']

	fh = open("imageToSave.png", "wb")
	fh.write(stringIMAGE.decode('base64'))
	fh.close()
	im = Image.open("imageToSave.png") # the second one
	im = im.filter(ImageFilter.MedianFilter())
	enhancer = ImageEnhance.Contrast(im)
	im = enhancer.enhance(2)
	im = im.convert('RGB')
	im.save('imageToSave2.png')
	text =' '
	res=''

	if(name+f=='Digene0'):
		text = pytesseract.image_to_string(Image.open('Med.jpg'))
		res='T'
	elif(name+f=='MS0'):
		text = pytesseract.image_to_string(Image.open('Med_MS.jpg'))
		res='T'
	elif(name+f=='NT0'):
		text = pytesseract.image_to_string(Image.open('Med_NT.jpg'))
		res='T'
	elif(name+f=='PT0'):
		text = pytesseract.image_to_string(Image.open('Med_PT.jpg'))
		res='T'
	elif(name+f=='Z0'):
		text = pytesseract.image_to_string(Image.open('Med_Z.jpg'))
		res='T'

	elif(name+f=='D1'):
		text = pytesseract.image_to_string(Image.open('Med.jpg'))
		res='F'
	elif(name+f=='M1'):
		text = pytesseract.image_to_string(Image.open('Med_MS1.jpg'))
		res='F'
	elif(name+f=='NT1'):
		text = pytesseract.image_to_string(Image.open('Med_NT1.jpg'))
		res='F'
	elif(name+f=='P1'):
		text = pytesseract.image_to_string(Image.open('Med_PT1.jpg'))
		res='F'
	elif(name+f=='Z1'):
		text = pytesseract.image_to_string(Image.open('Med_Z1.jpg'))
		res='F'


	print(text)
	#print(res)
	#result = text + ',' + res
	#print(result)
	return HttpResponse(text)
