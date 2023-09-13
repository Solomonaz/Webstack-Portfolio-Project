from . models import Category
from django.contrib.auth.decorators import login_required


# @login_required() 
def getsidenav(request):
    sidenavs = Category.objects.all()
    context_data = {
        'sidenavs':sidenavs
    }
    return context_data
