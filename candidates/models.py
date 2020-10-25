from django.db import models

class Position (models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    position_type = models.CharField(max_length=100)
    max_con = models.PositiveIntegerField()
    winning_format = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Metadata
    class Meta:
        ordering = ['id']

    #Methods
    def __str__(self):
        return self.name

    @property
    def get_winning_format(self):
        if self.winning_format == '51':
            return '50+1'
        else:
            return 'Majority'

    @property
    def get_gender(self):
        return self.gender.capitalize()

    @property
    def get_position_type(self):
        return self.position_type.capitalize()
    
    @property
    def name_underscore(self):
        return self.name.replace(' ','_')


class Candidate (models.Model):
    position = models.ForeignKey(Position, related_name='candidates', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    vote = models.IntegerField(default=0)
    department = models.CharField(max_length=100, null=True, blank=True)
    house = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='candidates', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Metadata
    class Meta:
        ordering = ['id']

    #Methods
    def __str__(self):
        return self.name
        
    @property
    def get_gender(self):
        return self.gender.capitalize()

