from django.test import TestCase, Client

from .models import Voter

class VoterTestCases(TestCase):
    def setUp(self):
        #create voter
        Voter.objects.create(access_number='12345', name='Fiifi Pius', gender='male', is_verified=True, is_voted=True)
        Voter.objects.create(access_number='12346', name='Kwame Akwah', gender='male')
        Voter.objects.create(access_number='12347', name='Gifty Akwah', gender='female', is_verified=True, is_voted=True)
        Voter.objects.create(access_number='12348', name='Grace Ampah', gender='female')

    
    def test_get_verified_yes(self):
        voter = Voter.objects.get(access_number='12345')
        self.assertEqual(voter.get_verified, 'Yes')

    def test_get_verified_yes(self):
        voter = Voter.objects.get(access_number='12346')
        self.assertEqual(voter.get_verified, 'No')

    def test_index_page(self):
        c = Client()
        response = c.get('/portal/voters')
        self.assertEqual(response.status_code, 301)

