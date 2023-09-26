from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from . forms import SidenavForm, TableFileForm, FileForm
from . models import TableFile, File
from authentication.models import Account
from authentication.forms import RegistrationForm
from .models import Activity
from django.contrib.admin.views.decorators import staff_member_required
from tablib import Dataset
from . resources import TableFileResource
import datetime
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import IntegrityError


@login_required(login_url="/login/")
def index(request):
   
    pdf_count = File.objects.filter(file__icontains='.pdf').count()
    excel_count = File.objects.filter(file__icontains='.xlsx').count()
    video_count = File.objects.filter(file__icontains='.mp4').count()
    word_count = File.objects.filter(file__icontains='.doc').count()  
    ppt_count = File.objects.filter(file__icontains='.ppt').count()  

    audio_count = (
        File.objects.filter(file__icontains='.mp3').count() +
        File.objects.filter(file__icontains='.wav').count()
    )
    image_count = (
        File.objects.filter(file__icontains='.png').count() +
        File.objects.filter(file__icontains='.jpeg').count() +
        File.objects.filter(file__icontains='.jpg').count()
    )



    total_count = (
        pdf_count + excel_count + video_count + audio_count + image_count + word_count + ppt_count
    )
    recent_files = Activity.objects.all()
    context = {
        'segment': 'index', 
        'pdf_count':pdf_count,
        'excel_count':excel_count,
        'video_count':video_count,
        'audio_count':audio_count,
        'image_count':image_count,
        'word_count':word_count,
        'total_count':total_count,
        'ppt_count': ppt_count,
        'recent_files':recent_files,
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
def sidenav(request):
    user = request.user
    role = user.role
    context = {
        'role':role,
    }
    return render (request,'includes/sidenav.html', context)

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
            return redirect('file_list')
        else:
            messages.error(request, 'Data not valid. Please check the form.')
    else:
        form_file = FileForm()
    
    context = {
        'form_file': form_file,
    }
    return render(request, 'pages/file.html', context)

def file_list(request):
    files = File.objects.all()
    files_count = files.count()

    paginator = Paginator(files, 10)
    page_number = request.GET.get('page')
    files = paginator.get_page(page_number)

    context = {
        'files':files,
        'files_count':files_count,
        }
    return render(request, 'pages/file-list.html', context)

def edit_file(request, pk):
    record_edit_model = File.objects.get(id=pk)
    form_file = FileForm(request.POST or None, instance=record_edit_model)
    
    if request.method == 'POST':
        if form_file.is_valid():
            activity = Activity(
                file_name=record_edit_model.file_name,
                action=f'File {record_edit_model.file_name} Edited',
                uploaded_by=record_edit_model.uploaded_by,
                file=record_edit_model.file,
                modified_by=request.user.username,
            )
            activity.save()
            form_file.save()
            messages.success(request, 'You have updated the file.')
            return redirect('file_list')

    context = {
        'form_file': form_file,
    }
    return render(request, 'pages/edit-file.html', context)


def delete_file(request, pk):
    data_removed = File.objects.get(id=pk)

    activity = Activity(
        file_name = data_removed.file_name,
        action = f'file {data_removed.file_name} removed ',
        uploaded_by = data_removed.uploaded_by,
        file = data_removed.file,
        modified_by = request.user.username,
        )
    activity.save()

    data_removed.delete()
    messages.success(request, 'File removed!')
    return redirect('file_list')


@login_required(login_url="/login/")
def export_data(request):
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        person_resource = TableFileResource()
        dataset = person_resource.export()

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="file_{timestamp}.xls"'
        response.write(dataset.xls)

        return response
    except Exception as e:
        messages.error(request, f'Error exporting data: {str(e)}')
        return redirect('your_error_view')



@login_required(login_url="/login/")
def import_data(request):
    if request.method == 'POST':
        form = TableFileResource()
        dataset = Dataset()
        new_person = request.FILES['import_data']
        imported_data = dataset.load(new_person.read(), format='xlsx')

        for data in imported_data:
            if len(data) != 12:
                messages.error(request, 'Invalid data format. Please check the Excel file.')
                return redirect('import_data')
            try:
                value = TableFile(
                    id = data[0] if data[0] else None,
                    accusor_name = data[1] if data[1] else None,
                    defendent_name = data[2] if data[2] else None,
                    house_number = data[3] if data[3] else None,
                    id_number = data[4] if data[4] else None,
                    court_house = data[5] if data[5] else None,
                    debate_type = data[6] if data[6] else None,
                    date_archive_initiated = data[7] if data[7] else None,
                    date_court_decision_made = data[8] if data[8] else None,
                    date_court_decision_copy_sent = data[9] if data[9] else None,
                    status = data[10] if data[10] else None,
                    prosecutor = data[11] if data[10] else None,
                )
                value.save()
            except IntegrityError as e:
                messages.error(request, f'Error importing data: {str(e)}')
                return redirect('import_data')

        messages.success(request, 'You have imported records!')
        return redirect('records')

    return render(request, 'pages/import.html')


@login_required(login_url="/login/")
def add_data(request):
    if request.method == 'POST':
        form = TableFileForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'data added sucessfully!')
            return redirect('records')
        else:
            messages.error(request, 'Please fill the data based on the formate!')
    else:
        form = TableFileForm()
    context = {
        'form':form,
    }
    return render(request, 'pages/add_data.html', context)   


def record(request):
    new_records = TableFile.objects.all()
    new_records_count = new_records.count()

    paginator = Paginator(new_records, 10)
    page_number = request.GET.get('page')
    new_records = paginator.get_page(page_number)

    context = { 
        'new_records':new_records,
        'new_records_count':new_records_count,
        }

    return render(request, 'pages/records.html', context)



def remove_data(request, pk):
    data_removed = TableFile.objects.get(id=pk)
    data_removed.delete()
    return redirect('records')

def edit_data(request, pk):
    record_edit_model = TableFile.objects.get(id=pk)
    record_edit_form = TableFileForm(request.POST or None, instance=record_edit_model)
    if record_edit_form.is_valid():
        record_edit_form.save()
        messages.success(request, ' You have updated a record.')
        return redirect('records')
        
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

@login_required
def remove_user(request, pk):
    user_removed = Account.objects.get(id=pk)
    if request.user != user_removed and request.user.role !='admin':
        messages.warning(request, "You don't have the right permission to remove this user")
        return redirect('manage_user')
    
    user_removed.delete()
    messages.success(request, 'File removed!')
    return redirect('manage_user')

@login_required
def edit_user(request, pk):
    record_edit_model = get_object_or_404(Account, id=pk)

    if request.user != record_edit_model and request.user.role !='admin':
        messages.success(request, "You don't have the right permission to edit user")
        return redirect('manage_user')

    if request.method == 'POST':
        record_edit_form = RegistrationForm(request.POST, instance=record_edit_model)
        if record_edit_form.is_valid():
            record_edit_form.save()
            messages.success(request, 'You have updated your profile.')
            return redirect('manage_user')

    else:
        record_edit_form = RegistrationForm(instance=record_edit_model)

    context = {
        'form': record_edit_form,
    }
    return render(request, 'pages/edit-user.html', context)


def global_search(request):
    query = request.GET.get('q', '')
    record_file = []
    file_results = []

    if query:
        record_file = TableFile.objects.filter(
            Q(accusor_name__icontains=query) | Q(defendent_name__icontains=query) | Q(prosecutor__icontains=query))
        record_file_count = record_file.count()

        file_results = File.objects.filter(
            Q(uploaded_by__icontains=query) | Q(file_name__icontains=query) | Q(file__icontains=query))
        file_results_count = file_results.count()

    context = {
        'query': query,
        'file_results': file_results,
        'record_file': record_file,
        'record_file_count':record_file_count,
        'file_results_count':file_results_count,
    }

    return render(request, 'pages/search.html', context)

def download_file(request, file_id):
    uploaded_file = get_object_or_404(File, id=file_id)
    file_path = uploaded_file.file.path
    try:
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename=' + uploaded_file.file.name.split('/')[-1]
            return response
    except FileNotFoundError:
        raise Http404("File not found")


def show_files_by_type(request, file_type):
    supported_file_types = {
        'pdf': '.pdf',
        'excel': '.xlsx',
        'video': '.mp4',
        'audio': ['.mp3', '.wav'],
        'image': ['.png', '.jpeg', '.jpg'],
        'word': '.docx',
        'ppt':'.ppt',
    }

    if file_type not in supported_file_types:
        return render(request, 'error.html', {'message': 'Unsupported file type'})

    extension = supported_file_types[file_type]

    files = File.objects.filter(file__iendswith=extension)

    file_counts = {}
    for type_key, type_extension in supported_file_types.items():
        file_counts[type_key] = File.objects.filter(file__iendswith=type_extension).count()
    
    context = {
        'files': files,
        'file_type': file_type, 
        'file_counts': file_counts
        }

    return render(request, 'pages/file_type.html', context)








