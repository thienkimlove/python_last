from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.

@login_required(login_url='/admin/login/')
def index(request):
    return render(request, 'core/index.html')

def banners(request):
    return render(request, 'core/banners/index.html')

def positions(request):
    return render(request, 'core/positions/index.html')
