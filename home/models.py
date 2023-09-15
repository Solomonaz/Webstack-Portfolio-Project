from django.db import models

class Category(models.Model):
    category_name = models.CharField(verbose_name='categories', max_length=100)

    def __str__(self):
        return self.category_name

class Folder(models.Model):
    folder_name = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.folder_name

class File(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='files/')
    
    def __str__(self):
        return self.name

class TableFile(models.Model):
    file_name = models.CharField(max_length=255)
    # case = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name
    
# class AddFile(models.Model):
