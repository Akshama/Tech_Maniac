# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rest_framework import permissions,generics
from rest_framework.decorators import api_view,permission_classes
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

import bigchaindb_driver
#bigchaindb_driver
from bigchaindb_driver import BigchainDB
from time import sleep
from bigchaindb_driver.crypto import generate_keypair
from sys import exit


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def get_image(request):
	stringIMAGE =  request.data['image']
	name= request.data['name']
	f = request.data['f']
	name = name+f
	print name

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

	if(name=='Digene0'):
		#print "hello D"
		text = pytesseract.image_to_string(Image.open('Med.jpg'))
		res='T'
	elif(name=='MS0'):
		text = pytesseract.image_to_string(Image.open('Med_MS.jpg'))
		res='T'
	elif(name=='NT0'):
		text = pytesseract.image_to_string(Image.open('Med_NT.jpg'))
		res='T'
	elif(name=='PT0'):
		text = pytesseract.image_to_string(Image.open('Med_PT.jpg'))
		res='T'
	elif(name=='Z0'):
		text = pytesseract.image_to_string(Image.open('Med_Z.jpg'))
		res='T'

	elif(name=='Digene1'):
		text = pytesseract.image_to_string(Image.open('Med.jpg'))
		res='F'
	elif(name=='MS1'):
		text = pytesseract.image_to_string(Image.open('Med_MS1.jpg'))
		res='F'
	elif(name=='NT1'):
		text = pytesseract.image_to_string(Image.open('Med_NT1.jpg'))
		res='F'
	elif(name=='P1'):
		text = pytesseract.image_to_string(Image.open('Med_PT1.jpg'))
		res='F'
	elif(name=='Z1'):
		text = pytesseract.image_to_string(Image.open('Med_Z1.jpg'))
		res='F'


	print(text)
	#print(res)

	result = text + ',' + res
	#print(result)
	return HttpResponse(text)



def block_chain(request):
	alice, bob = generate_keypair(), generate_keypair()


	bdb_root_url = 'http://localhost:9984'
	bdb = BigchainDB(bdb_root_url)

	drug = {
	   'data': {
	         'Digene': {
	            ' aluminium hydroxide':'300 mg',
	            'magnesium aluminium silicate':'50 mg',
	             'magnesium hydroxide': '25 mg',
	              'simethicone':'25 mg',
	         },

	         'Meftal Spas':{

	         	'Norfloxacin IP':'250mg',
	         	'Dicyclomine': '10mg',

	         },
	         'NORFLOX-TZ':
	         {

	         	'Norfloxacin IP':'400 mg',
				'Tinidazole IP':'600 mg'

	         },

	         'Paracetamol':
	         {
	         	 'Paracetamol PhEur':'500mg',


	         },
	         'Zantac':
	         {
	         	'ranitidine HCl':'168 mg',

	         },
	     },
	 }



	prepared_creation_tx = bdb.transactions.prepare(
	       operation='CREATE',
	      signers=alice.public_key,
	      asset=drug,
	   )


	fulfilled_creation_tx = bdb.transactions.fulfill(
	     prepared_creation_tx, private_keys=alice.private_key)


	'''
	print(bdb.transactions.send(fulfilled_creation_tx))
	if sent_creation_tx == fulfilled_creation_tx:
	  print("HELLO")
	'''

	txid = fulfilled_creation_tx['id']

	#print(txid)
	#print(bdb.transactions.status(txid))


	trials = 0
	while trials < 60:
	    try:
	        if bdb.transactions.status(txid).get('status') == 'valid':
	            print('Tx valid in:', trials, 'secs')
	            break
	    except bigchaindb_driver.exceptions.NotFoundError:
	        trials += 1
	        sleep(1)
	
	if trials == 60:
	    print('Tx is still being processed... Bye!')
	    exit(0)

	asset_id = txid

	transfer_asset = {
	    'id': asset_id
	}

	output_index = 0
	output = fulfilled_creation_tx['outputs'][output_index]

	transfer_input = {
	    'fulfillment': output['condition']['details'],
	    'fulfills': {
	        'output_index': output_index,
	        'transaction_id': fulfilled_creation_tx['id']
	    },
	    'owners_before': output['public_keys']
	}

	prepared_transfer_tx = bdb.transactions.prepare(
	    operation='TRANSFER',
	    asset=transfer_asset,
	    inputs=transfer_input,
	    recipients=bob.public_key,
	)

	fulfilled_transfer_tx = bdb.transactions.fulfill(
	    prepared_transfer_tx,
	    private_keys=alice.private_key,
	)

	sent_transfer_tx = bdb.transactions.send(fulfilled_transfer_tx)

	print("Is Bob the owner?",
	    sent_transfer_tx['outputs'][0]['public_keys'][0] == bob.public_key)

	print("Was Alice the previous owner?",
	    fulfilled_transfer_tx['inputs'][0]['owners_before'][0] == alice.public_key)
