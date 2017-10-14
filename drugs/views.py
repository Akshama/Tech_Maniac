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
	fh = open("imageToSave.png", "wb")
	fh.write(stringIMAGE.decode('base64'))
	fh.close()
	im = Image.open("imageToSave.png") # the second one 
	im = im.filter(ImageFilter.MedianFilter())
	enhancer = ImageEnhance.Contrast(im)
	im = enhancer.enhance(2)
	im = im.convert('RGB')
	im.save('imageToSave2.png')
	text ='Success'
	text = text + pytesseract.image_to_string(Image.open('imageToSave2.png'))
	print(text)
	'''if(text):
		print(text)
	else:
		print("No text")'''
	return HttpResponse(text)
