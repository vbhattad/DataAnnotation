from django.db import models
from django.utils.encoding import smart_text

# Create your models here.
class classify(models.Model):
    #file_name = models.FileField(max_length=255, null=True, blank=True)
    document = models.FileField(upload_to='$HOME/Desktop')
    # pass

    def __unicode__(self):
        return smart_text(self.email)