from django.db import models

class Voter (models.Model):
    access_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    programme = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    house = models.CharField(max_length=100, null=True, blank=True)
    form = models.CharField(max_length=10, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_voted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Metadata
    class Meta:
        ordering = ['id']

    #Methods
    def __str__(self):
        return f"{self.access_number}"

    
    @property
    def get_gender(self):
        return self.gender.capitalize()

    @property
    def get_verified(self):
        if self.is_verified:
            return 'Yes'
        else:
            return 'No'

    @property
    def get_voted(self):
        if self.is_voted:
            return 'Yes'
        else:
            return 'No'



class Programme (models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Metadata
    class Meta:
        ordering = ['id']

    #Methods
    def __str__(self):
        return self.name
