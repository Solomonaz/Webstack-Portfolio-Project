from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache
from django.contrib import messages
from . forms import SidenavForm
from . models import Category, TableFile


# def login(request):
#     return render(request, 'login.html')

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

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

def tablefile(request):
    tables = TableFile.objects.all()
    return render(request,'index.html',{'tables':tables})