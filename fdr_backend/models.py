from django.db import models

# Create your models here.
class FaceEntry(models.Model):
    uuid = models.CharField(max_length=36, unique=True)
    face_encoding_json = models.TextField(null=True)
    image = models.ImageField('img', upload_to='detected_faces/')
    def __str__(self):
        return self.title




class Event(models.Model):
    faces = models.ManyToManyField(FaceEntry)
    timestamp = models.DateTimeField('date published')

    def __str__(self):
        return self.timestamp

    class Meta:
        ordering = ('timestamp',)

