from django.db import models

class Image(models.Model):
    title = models.CharField(max_length=255)
    original_image = models.ImageField(upload_to='images/')
    enhanced_image = models.ImageField(upload_to='enhanced/', blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
