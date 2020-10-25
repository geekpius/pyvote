from django.test import TestCase, Client

from .models import Position, Candidate
class CandidateTestCases(TestCase):
    def setUp(self):
        #create positions
        president = Position.objects.create(name='President', gender='both', position_type='general', 
                                            max_con=2, winning_format='51')
        general_secretary = Position.objects.create(name='General Secretary', gender='both', position_type='general', 
                                            max_con=2, winning_format='majority')
        tresurer = Position.objects.create(name='Tresurer', gender='both', position_type='general', 
                                            max_con=1, winning_format='majority')

        #create candidates
        Candidate.objects.create(name='Fiifi Pius', gender='male', position=president)
        Candidate.objects.create(name='Kwame Akwah', gender='male', position=president)
        Candidate.objects.create(name='Gifty Akwah', gender='female', position=general_secretary)
        Candidate.objects.create(name='Grace Ampah', gender='female', position=general_secretary)
        Candidate.objects.create(name='Akosua Marfo', gender='female', position=tresurer)

    
    def test_contestant_count(self):
        positions = Position.objects.filter()
        for position in positions:
            count_can = Candidate.objects.filter(position=position).count()
            self.assertEqual(position.max_con, count_can)

    def test_index_page(self):
        c = Client()
        response = c.get('/portal/candidates')
        self.assertEqual(response.status_code, 301)

    def test_upload_page(self):
        candidate = Candidate.objects.get(name='Fiifi Pius')
        c = Client()
        response = c.post(f"/portal/candidates/{candidate.id}/upload")
        self.assertEqual(response.status_code, 302)
