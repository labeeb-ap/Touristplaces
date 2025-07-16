from django.db import models

# Create your models here.
class Places(models.Model):
    name=models.CharField(max_length=100)
    wheather=models.CharField(max_length=50)
    state=models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    googlemaplink=models.CharField(max_length=200)

    def __str__(self):
        return self.name
class Images(models.Model):
    image=models.ImageField(upload_to="images/")
    place=models.ForeignKey(Places,on_delete=models.CASCADE,related_name='images')




