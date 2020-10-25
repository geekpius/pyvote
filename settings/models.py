from django.db import models


class Setting (models.Model):
    title = models.CharField(max_length=100)
    year = models.CharField(max_length=10)
    is_programme = models.BooleanField(default=False)
    is_department = models.BooleanField(default=False)
    is_house = models.BooleanField(default=False)
    is_form = models.BooleanField(default=False)
    closing_time = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Metadata
    class Meta :
        ordering = ['id']

    #Methods
    def __str__(self):
        return f"{self.title}"
