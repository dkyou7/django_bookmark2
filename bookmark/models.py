from django.db import models

# Create your models here.
class Bookmark(models.Model):
    title = models.CharField('TITLE',max_length=100)
    url = models.URLField('URL',unique=True)

    from django.contrib.auth.models import User
    owner = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return "%s" %(self.title)