from django.db import models

from voters.models import Voter
from candidates.models import Candidate


class Vote (models.Model):
    voter = models.ForeignKey(Voter, related_name='votes', on_delete=models.CASCADE)
    candidate = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Metadata
    class Meta :
        ordering = ['id']

    #Methods
    def __str__(self):
        return f"{self.voter}"


class VoteCart (models.Model):
    voter = models.ForeignKey(Voter, related_name='votecarts', on_delete=models.CASCADE)
    candidate = models.CharField(max_length=60)
    position = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Metadata
    class Meta :
        ordering = ['id']

    #Methods
    def __str__(self):
        return f"{self.voter}"

    @property
    def candidate_image(self):
        candidate = Candidate.objects.filter(name=self.candidate).first()
        if candidate == None:
            return self.candidate
        else:
            return candidate.image.url

    @property
    def position_slug(self):
        return self.position.lower().replace(' ', '-')

