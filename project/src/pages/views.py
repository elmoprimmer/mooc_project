from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Q
from .models import File
from .models import Nickname, Message, No
from django.db import transaction
import sys
import sqlite3
import string
import pkg_resources
pkg_resources.require("aadhaar-py==2.0.0") # Fix for Vulnerable and Outdated Components: remove this line and import version of aadhar with updated security
from aadhaar.secure_qr import extract_data 




def htmlspecialchars(text):
    return (
        text.replace("&", "&amp;").
        replace('"', "&quot;").
        replace("<", "&lt;").
        replace(">", "&gt;")
    )

#to fix weak encryption, this should be replaced with a better encryption method, e.g. AES. 
#For example the aes-cipher package works well.
def caesar(plaintext, n): 
	alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	ciphertext = ""
	for i in range(0, len(plaintext)):
		for j in range(0,len(alphabet)):
			if plaintext[i] == alphabet[j]:
				ciphertext += alphabet[(j+n) % len(alphabet)]
	return ciphertext


@login_required
def deleteView(request):
	f = File.objects.get(pk=request.POST.get('id'))
	# Fix for broken access control:
	# owner_id = f.owner_id
	# user = request.user
	# if user.id == owner_id:
	# 	f.delete()
	f.delete()
	return redirect('/')
	

@login_required
def downloadView(request, fileid):
	f = File.objects.get(pk=fileid)

	filename = f.data.name.split('/')[-1]
	owner_id = f.owner_id
	user = request.user
	if user.id == owner_id:
		response = HttpResponse(f.data, content_type='text/plain')
		response['Content-Disposition'] = 'attachment; filename=%s' % filename
	else:
		response = redirect('/')

	return response


@login_required
def addNicknameView(request):
	data = caesar(request.POST.get('nickname'),3)
	f = Nickname(owner=request.user,id = 1, nickname=data)
	f.save()
	return redirect('/')

@login_required
def addView(request):
	data = request.FILES.get('file')
	f = File(owner=request.user, data=data)
	f.save()
	return redirect('/')


@login_required
def sendView(request):
	target = User.objects.get(username=request.POST.get('to'))
	Message.objects.create(source=request.user, target=target, content=htmlspecialchars(request.POST.get('content')))
	return redirect('/')





@login_required
def homePageView(request):
	files = File.objects.filter(owner=request.user)
	uploads = [{'id': f.id, 'name': f.data.name.split('/')[-1]} for f in files]
	try:
		nickname = Nickname.objects.filter(owner = request.user)

	except:
		Nickname.objects.create(owner = request.user, nickname = 'default')
		nickname = Nickname.objects.filter(owner = request.user)

	for nick in nickname:
		nick.nickname = caesar(nick.nickname,49)

	messages = Message.objects.filter(Q(source=request.user) | Q(target=request.user))
	# Fix for XSS:
	# for msg in messages:
	# 	msg.content = htmlspecialchars(msg.content)


	users = User.objects.exclude(pk=request.user.id)



	received_qr_code_data = nickname
	try:
		extracted_data = extract_data(received_qr_code_data).to_dict()
	except:
		extracted_data = No.objects.filter(id=1)[0]

	return render(request, 'pages/index.html', {'uploads': uploads,'nickname':nickname[0],'msgs': messages, 'users': users,'qr': extracted_data})
