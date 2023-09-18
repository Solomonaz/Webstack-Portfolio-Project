from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from . forms import SidenavForm, TableFileForm, FileForm
from . models import TableFile, File
from authentication.models import Account
from authentication.forms import RegistrationForm


from tablib import Dataset
from . resources import TableFileResource
import datetime
from django.core.paginator import Paginator



@login_required(login_url="/login/")
def index(request):
    new_records = TableFile.objects.all()
    files = File.objects.all()
    paginator = Paginator(new_records, 10)
    page_number = request.GET.get('page')
    new_records = paginator.get_page(page_number)

    context = {
        'segment': 'index', 
        'new_records':new_records,
        'files':files,
        }

    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))



@login_required(login_url="/login/")
def pages(request):
    context = {}

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
    if request.method == 'POST':
        form_file = FileForm(request.POST, request.FILES)
        if form_file.is_valid():
            instance = form_file.save(commit=False)

            # Calculate file size in MB
            file_size_in_bytes = request.FILES['file'].size
            file_size_in_mb = file_size_in_bytes / (1024 * 1024)
            instance.file_size = round(file_size_in_mb, 2)  # Rounded to two decimal places

            instance.save()
            messages.success(request, 'Data added successfully!')
            return redirect('/')
        else:
            messages.error(request, 'Data not valid. Please check the form.')
    else:
        form_file = FileForm()
    
    context = {
        'form_file': form_file,
    }
    return render(request, 'pages/file.html', context)



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
            return redirect('/')
    return render(request, 'pages/import.html')

@login_required(login_url="/login/")
def add_data(request):
    if request.method == 'POST':
        form = TableFileForm(request.POST)
        # print(form.data)
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


def manage_user(request):
    accounts = Account.objects.all()
    context = {
        'accounts': accounts
    }
    return render(request, 'pages/manage-user.html',context)

def remove_user(request, pk):
    user_removed = Account.objects.get(id=pk)
    user_removed.delete()
    return redirect('manage_user')

def edit_user(request, pk):
    record_edit_model = Account.objects.get(id=pk)
    record_edit_form = RegistrationForm(request.POST or None, instance=record_edit_model)
    if record_edit_form.is_valid():
        record_edit_form.save()
        messages.success(request, ' You have updated a user.')
        return redirect('manage_user')
        
    context = {
        'form':record_edit_form
    }
    return render(request, 'pages/edit-user.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products  = TableFile.objects.order_by('-created_date').filter(Q(description__icontains = keyword) |  Q(product_name__icontains = keyword))
            product_count = products.count()
    context = {
        'products':products,
        'product_count':product_count
    }
    return render(request, 'store/store.html', context) 