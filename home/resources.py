from import_export import resources
from . models import TableFile

class TableFileResource(resources.ModelResource):
    class Meta:
        model = TableFile
        # fields = '__all__'
