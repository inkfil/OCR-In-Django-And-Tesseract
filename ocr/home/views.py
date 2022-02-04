from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from . import filocrapi
#import numpy as np
#import pandas as pd
#import matplotlib.pyplot as plt

def fillogin(request):
	return render(request, 'login.html')

def filhome(request):
	#username = request.POST['username']
	return render(request, 'bootstrapcard.html')

def filshowcode(request):
	return render(request, 'showcode.html')

def filreadimage(request):
	content={}
	if request.method=='POST':
		imghtml=request.FILES['imgread']
		fs=FileSystemStorage()
		fs.save(imghtml.name,imghtml)
		del(fs)
		print(type(imghtml))
		content['orignaltext'],content['summarizedtext']=filocrapi.imageSummary(imghtml)
	return render(request, 'readImageTemplate.html', content)

def filreadtext(request):
	content={}
	if request.method=='POST':
		txthtml=request.FILES['txtread']
		fs=FileSystemStorage()
		fs.save(txthtml.name,txthtml)
		#print(txthtml)
		del(fs)
		content['orignaltext'],content['summarizedtext']=filocrapi.textsummary(txthtml.name)
	return render(request, 'readTextTemplate.html', content)

def filreadpdf(request):
	content={}
	if request.method=='POST':
		pdfhtml=request.FILES['pdf']
		fs=FileSystemStorage()
		fs.save(pdfhtml.name,pdfhtml)
		del(fs)
		#print(fs)
		content['orignaltext'],content['summarizedtext']=filocrapi.pdfsummary(pdfhtml.name)
	return render(request, 'readPdfTemplate.html', content)

def filreaddoc(request):
	content={}
	if request.method=='POST':
		dochtml=request.FILES['doc']
		fs=FileSystemStorage()
		fs.save(dochtml.name,dochtml)
		del(fs)
		#print(fs)
		content['orignaltext'],content['summarizedtext']=filocrapi.docsummary(dochtml)
	return render(request, 'readDocTemplate.html', content)
	
'''
def extractFromImage():
	return render()

def extractFromText():
	return render()

def extractFromPdf():
	return render()

def extractFromDoc():
	return render()

def textSummarize():
	return render()
'''