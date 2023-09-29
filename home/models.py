from django.db import models
from authentication.models import Account



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
    accusor_name = models.CharField(max_length=255, verbose_name='ከሳሽ መልስ ሰጭ', null=True, blank=True)
    defendent_name = models.CharField(max_length=255, verbose_name='ተከሳሽ መልስ  ሰጭ', null=True, blank=True)
    house_number = models.CharField(max_length=255, verbose_name='የቤት ቁጥር', null=True, blank=True)
    id_number = models.CharField(max_length=255, verbose_name='የመ.ቁ ', null=True, blank=True)
    court_house = models.CharField(max_length=255, verbose_name='ክርክሩ የነበረበት ፍ/ቤት', null=True, blank=True)
    debate_type = models.CharField(max_length=255, verbose_name='የክርክሩ አይነት', null=True, blank=True)
    date_archive_initiated = models.DateTimeField(auto_now_add=False, verbose_name='መዝገቡ የመጣበት ቀን', null=True, blank=True)
    date_court_decision_made = models.DateTimeField(auto_now_add=False, verbose_name='ፍርድ ቤቱ ውሳኔ የሰጠበት ቀን', null=True, blank=True)
    date_court_decision_copy_sent = models.DateTimeField(auto_now_add=False, verbose_name='የውሳኔ ግልባጭ የተላከበት ቀን', null=True, blank=True)
    status = models.CharField(max_length=255, verbose_name='በፍ/ቤቱ ውሳኔ መሰረት ተፈፅሞል/አልተፈፀመም', null=True, blank=True)
    prosecutor = models.CharField(max_length=255, verbose_name='ጉዳዩን የያዘው ዐቃቤ ህግ ስም')

    def __str__(self):
        return self.prosecutor

class RecordActivity(models.Model):
    accusor_name = models.CharField(max_length=255, verbose_name='ከሳሽ መልስ ሰጭ', null=True, blank=True)
    defendent_name = models.CharField(max_length=255, verbose_name='ተከሳሽ መልስ  ሰጭ', null=True, blank=True)
    house_number = models.CharField(max_length=255, verbose_name='የቤት ቁጥር', null=True, blank=True)
    id_number = models.CharField(max_length=255, verbose_name='የመ.ቁ ', null=True, blank=True)
    court_house = models.CharField(max_length=255, verbose_name='ክርክሩ የነበረበት ፍ/ቤት', null=True, blank=True)
    debate_type = models.CharField(max_length=255, verbose_name='የክርክሩ አይነት', null=True, blank=True)
    date_archive_initiated = models.DateTimeField(auto_now_add=False, verbose_name='መዝገቡ የመጣበት ቀን', null=True, blank=True)
    date_court_decision_made = models.DateTimeField(auto_now_add=False, verbose_name='ፍርድ ቤቱ ውሳኔ የሰጠበት ቀን', null=True, blank=True)
    date_court_decision_copy_sent = models.DateTimeField(auto_now_add=False, verbose_name='የውሳኔ ግልባጭ የተላከበት ቀን', null=True, blank=True)
    prosecutor = models.CharField(max_length=255, verbose_name='ጉዳዩን የያዘው ዐቃቤ ህግ ስም')
    status = models.CharField(max_length=255, verbose_name='በፍ/ቤቱ ውሳኔ መሰረት ተፈፅሞል/አልተፈፀመም', null=True, blank=True)
    date_modified = models.DateTimeField(auto_now_add=True)
    edited_or_deleted = models.CharField(max_length=255)
    modified_by = models.CharField(max_length=255)


    def __str__(self):
        return self.prosecutor
    

class Activity(models.Model):
    file_name = models.CharField(max_length=255)
    uploaded_by = models.CharField(max_length=255)
    modified_by = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    file = models.FileField(upload_to='recent/')
    file_size = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)
    edited_or_deleted = models.CharField(max_length=255)




    def __str__(self):
        return self.file_name
    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'