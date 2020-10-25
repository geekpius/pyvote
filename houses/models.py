from django.db import models

class House (models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Metadata
    class Meta :
        ordering = ['name']

    #Methods
    def __str__(self):
        return self.name
