from django.contrib import admin
from .models import Category, TableFile, File, Activity, RecordActivity
from import_export.admin import ImportExportModelAdmin


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'uploaded_by','date_created','file','file_size')

class SidenavAdmin(admin.ModelAdmin):
    list_display = ('category_name',)

@admin.register(Activity)
class RecentFiles(admin.ModelAdmin):
    list_display = ('file_name', 'uploaded_by','modified_by','date_modified','file')

@admin.register(RecordActivity)
class RecentRecord(admin.ModelAdmin):
    list_display = ( 
        'accusor_name',
        'defendent_name',
        'house_number',
        'id_number',
        'court_house',
        'debate_type',
        'date_archive_initiated',
        'date_court_decision_made',
        'date_court_decision_copy_sent',
        'prosecutor',
        'status'
          )


@admin.register(TableFile)
class TableFileAdmin(ImportExportModelAdmin):
    list_display =(
        'id',
        'accusor_name',
        'defendent_name',
        'house_number',
        'id_number',
        'court_house',
        'debate_type',
        'date_archive_initiated',
        'date_court_decision_made',
        'date_court_decision_copy_sent',
        'prosecutor',
        'status'
        )

 