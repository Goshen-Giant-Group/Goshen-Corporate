from django.test import TestCase
from django.urls import reverse

from .models import Job


class JobApplicationRoutingTests(TestCase):
	def setUp(self):
		self.join_job = Job.objects.create(
			title='Store Manager',
			external_id='join-123',
			location='uyo',
			job_type='full-time',
			description='Manage the store',
			requirements='Leadership',
			join_com_url='https://join.com/jobs/123',
		)
		self.local_job = Job.objects.create(
			title='Warehouse Assistant',
			external_id='local-456',
			location='uyo',
			job_type='full-time',
			description='Support warehouse operations',
			requirements='Physical stamina',
		)

	def test_job_detail_apply_now_targets_join_when_join_url_exists(self):
		response = self.client.get(reverse('job_detail', args=[self.join_job.pk]))

		self.assertContains(response, 'href="https://join.com/jobs/123"')
		self.assertContains(response, 'Apply Now')
		self.assertNotContains(response, reverse('general_application'))

	def test_job_application_redirects_to_join_when_join_url_exists(self):
		response = self.client.get(reverse('job_application', args=[self.join_job.pk]))

		self.assertRedirects(response, 'https://join.com/jobs/123', fetch_redirect_response=False)

	def test_job_application_falls_back_to_general_application_without_join_url(self):
		response = self.client.get(reverse('job_application', args=[self.local_job.pk]))

		self.assertRedirects(
			response,
			f"{reverse('general_application')}?job={self.local_job.pk}",
			fetch_redirect_response=False,
		)

# Create your tests here.
