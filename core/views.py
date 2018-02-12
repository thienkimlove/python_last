from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required

# Create your views here.
from core.forms import *
from core.models import Position


@login_required(login_url='/admin/login/')
def index(request):
    return render(request, 'core/index.html')

def banner_list(request):
    return render(request, 'core/banners/index.html')


def position_list(request):
    return render(request, 'core/positions/index.html')

@permission_required('position.add')
def position_create(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PositionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            Position.objects.create(name=form.cleaned_data['name'])
            # redirect to a new URL:
            return redirect('core_position_index')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = PositionForm(auto_id='%s')

    return render(request, 'core/positions/create.html', {'form': form})

def position_edit(request, pk):
    position = get_object_or_404(Position, pk=pk)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PositionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            position.name=form.cleaned_data['name']
            position.save()
            # redirect to a new URL:
            return redirect('core_position_index')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = PositionForm(initial={ 'name' : position.name })

    return render(request, 'core/positions/edit.html', {'form': form, 'content' : position})
