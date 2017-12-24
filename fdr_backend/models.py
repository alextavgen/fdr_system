from django.db import models
import django_filters



class Face(models.Model):
    uuid = models.CharField(max_length=36, unique=False)
    face_encoding_json = models.TextField(null=False)
    image =models.CharField(max_length=200, null=True)
    timestamp = models.DateTimeField('Date created')


    def __str__(self):
        return self.uuid


    def __unicode__(self):
        return self.uuid




# Create your models here.
class FaceEntry(models.Model):
    face = models.ForeignKey(Face, on_delete=models.CASCADE)
    image =models.CharField(max_length=200, null=False)
    timestamp = models.DateTimeField('Date detected')

    def __unicode__(self):
        return self.timestamp.strftime("%Y-%d-%m %H:%M:%S")

    class Meta:
        ordering = ('timestamp',)

class FaceEntryFilter(django_filters.FilterSet):
    class Meta:
        model = FaceEntry
        fields = ['timestamp', 'face', ]

