from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib import messages
from . forms import SidenavForm, TableFileForm
from . models import Category, TableFile

from tablib import Dataset
from . resources import TableFileResource
import datetime
from django.core.paginator import Paginator

# def login(request):
#     return render(request, 'login.html')

@login_required(login_url="/login/")
def index(request):
    new_records = TableFile.objects.all()
    paginator = Paginator(new_records, 10)
    page_number = request.GET.get('page')
    new_records = paginator.get_page(page_number)
    context = {
        'segment': 'index', 
        'new_records':new_records,
        }

    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def sidenavcreate(request):
    if request.method == 'POST':
        form = SidenavForm(request.POST)
        if form.is_valid():
            # Save the form data manually
            sidenav = form.save(commit=False)
            sidenav.save()
            messages.success(request, 'Message sent')
            return redirect('/')  
    else:
        form = SidenavForm()
    context = {
        'form': form,
    }
    return render(request, 'includes/sidenavcreate.html', context)

def create_folder(request):
    return render(request, 'pages/folder.html')

def create_file(request):
    return render(request, 'pages/file.html')

# export data
@login_required(login_url="/login/")
def export_data(request):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    person_resource = TableFileResource()
    dataset = person_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename="file_{timestamp}.xls"'
    return response

# import excell file
@login_required(login_url="/login/")
def import_data(request):
    if request.method == 'POST':
        form = TableFileResource()
        dataset = Dataset()
        new_person = request.FILES['import_data']
        imported_data = dataset.load(new_person.read(), format='xlsx')
        for data in imported_data:
            value = TableFile(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6],
                data[7],
                data[8],
                data[9],
                data[10],
                data[11],
                # data[12],

            )
            value.save()
    return render(request, 'pages/import.html')

@login_required(login_url="/login/")
def add_data(request):
    if request.method == 'POST':
        form = TableFileForm(request.POST)
        print(form.data)
        if form.is_valid():
            form.save()
            # form_data = form.save(commit=False)
            # form_data.save()
            messages.success(request, 'data added sucessfully!')
            return redirect('/')
    else:
        form = TableFileForm()
    context = {
        'form':form,
    }
    return render(request, 'pages/add_data.html', context)   

def remove_data(request, pk):
    data_removed = TableFile.objects.get(id=pk)
    data_removed.delete()
    return redirect('/')

def edit_data(request, pk):
    record_edit_model = TableFile.objects.get(id=pk)
    record_edit_form = TableFileForm(request.POST or None, instance=record_edit_model)
    if record_edit_form.is_valid():
        record_edit_form.save()
        messages.success(request, ' You have updated a record.')
        return redirect('/')
        
    context = {
        'form':record_edit_form
    }
    return render(request, 'pages/edit.html', context)
    # return redirect(reverse('index'))