from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'miner/index.html')

def keyList(request):
    return render(request, 'miner/key.html')