from django.db import models
from django.utils import timezone

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
    # folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=100)
    uploaded_by  = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')
    file_size = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.file_name

class TableFile(models.Model):
    accusor_name = models.CharField(max_length=255, verbose_name='ከሳሽ መልስ ሰጭ')
    defendent_name = models.CharField(max_length=255, verbose_name='ተከሳሽ መልስ  ሰጭ')
    house_number = models.CharField(max_length=255, verbose_name='የቤት ቁጥር')
    id_number = models.CharField(max_length=255, verbose_name='የመ.ቁ ')
    court_house = models.CharField(max_length=255, verbose_name='ክርክሩ የነበረበት ፍ/ቤት')
    debate_type = models.CharField(max_length=255, verbose_name='የክርክሩ አይነት')
    date_archive_initiated = models.DateTimeField(auto_now_add=False, verbose_name='መዝገቡ የመጣበት ቀን')
    date_court_decision_made = models.DateTimeField(auto_now_add=False, verbose_name='ፍርድ ቤቱ ውሳኔ የሰጠበት ቀን')
    date_court_decision_copy_sent = models.DateTimeField(auto_now_add=False, verbose_name='የውሳኔ ግልባጭ የተላከበት ቀን')
    status = models.CharField(max_length=255, verbose_name='በፍ/ቤቱ ውሳኔ መሰረት ተፈፅሞል/አልተፈፀመም')
    prosecutor = models.CharField(max_length=255, verbose_name='ጉዳዩን የያዘው ዐቃቤ ህግ ስም')

    def __str__(self):
        return self.prosecutor
    
