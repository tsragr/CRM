from django.test import TestCase
from rest_framework.test import APIClient
import json
from django.urls import reverse
from django.contrib.auth.models import User
from crm.serializers import CompanyCreateSerializers, CompanySerializer, CompanyDetailSerializer
from crm.models import Company, Office, Cooperation, Worker, Profile, UserSkill, UserLanguage
from knox.models import AuthToken
from rest_framework.response import Response

client = APIClient()


class GetCreateRetrieveUpdateDeleteCompany(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Maxim', password='123qwe')
        self.admin = User.objects.create_superuser(username='Admin', password='123qwe')
        Company.objects.create(name='Apple', about='Apple company', is_active=True)
        Company.objects.create(name='Amazon', about='Amazon company', is_active=True)
        Company.objects.create(name='Google', about='Google company', is_active=True)

    def test_valid_get_all_companies(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + AuthToken.objects.create(self.user)[1])
        response = client.get('/company/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_invalid_get_all_companies(self):
        response = client.get('/company/')
        self.assertEqual(response.status_code, 401)

    def test_valid_create_company(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + AuthToken.objects.create(self.admin)[1])
        response = client.post('/company/', {"name": "Tesla", "about": "Tesla company", "is_active": True,
                                             'created_at': '1996-09-17'})
        self.assertEqual(response.data, {"name": "Tesla", "about": "Tesla company", "is_active": True,
                                         'created_at': '1996-09-17'})
        self.assertEqual(response.status_code, 201)

    def test_invalid_create_company(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + AuthToken.objects.create(self.user)[1])
        response = client.post('/company/', {"name": "Tesla", "about": "Tesla company", "is_active": True,
                                             'created_at': '1996-09-17'})
        self.assertEqual(response.status_code, 403)

    def test_valid_get_one_company(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + AuthToken.objects.create(self.user)[1])
        response = client.get(f'/detail/{Company.objects.first().id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'name': 'Apple', 'about': 'Apple company', 'offices': [], 'workers': [],
                                         'created_at': '2021-09-21'})

    def test_invalid_get_one_company(self):
        response = client.get(f'/detail/{Company.objects.first().id}/')
        self.assertEqual(response.status_code, 401)

    def test_valid_put_one_company(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + AuthToken.objects.create(self.admin)[1])
        response = client.put(f'/detail/{Company.objects.first().id}/',
                              {"name": "Apple new logo", "about": "Apple company updated"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'name': 'Apple new logo', 'about': 'Apple company updated', 'is_active': True,
                                         'created_at': '2021-09-21'})

    def test_valid_patch_one_company(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + AuthToken.objects.create(self.admin)[1])
        response = client.patch(f'/detail/{Company.objects.first().id}/',
                                {"about": "Apple company updated"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'name': 'Apple', 'about': 'Apple company updated', 'is_active': True,
                                         'created_at': '2021-09-21'})

    def test_valid_delete_one_company(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + AuthToken.objects.create(self.admin)[1])
        response = client.delete(f'/detail/{Company.objects.first().id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Company.objects.first().is_active, False)

    def test_invalid_put_one_company(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + AuthToken.objects.create(self.user)[1])
        response = client.put(f'/detail/{Company.objects.first().id}/',
                              {"name": "Apple new logo", "about": "Apple company updated"})
        self.assertEqual(response.status_code, 403)

    def test_invalid_patch_one_company(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + AuthToken.objects.create(self.user)[1])
        response = client.patch(f'/detail/{Company.objects.first().id}/',
                                {"about": "Apple company updated"})
        self.assertEqual(response.status_code, 403)

    def test_invalid_delete_one_company(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + AuthToken.objects.create(self.user)[1])
        response = client.delete(f'/detail/{Company.objects.first().id}/')
        self.assertEqual(response.status_code, 403)


class ModelsTest(TestCase):

    def setUp(self):
        apple = Company.objects.create(name='Apple', about='Apple company', is_active=True)
        amazon = Company.objects.create(name='Amazon', about='Amazon company', is_active=True)
        Office.objects.create(name='Apple\'s offices', company=apple, location='USA', is_active=True)
        Office.objects.create(name='Amazon\'s offices', company=amazon, location='GB', is_active=True)
        Office.objects.create(name='Amazon\'s offices #2', company=amazon, location='GB', is_active=True)
        user1 = User.objects.create_user(username='Maxim', password='123qwe')
        user2 = User.objects.create_user(username='Misha', password='123qwe')
        user3 = User.objects.create_user(username='Masha', password='123qwe')
        profile1 = Profile.objects.create(user=user1)
        profile2 = Profile.objects.create(user=user2)
        profile3 = Profile.objects.create(user=user3)
        Worker.objects.create(employer=profile1, company=apple, position='python developer')
        Worker.objects.create(employer=profile2, company=apple, position='devops')
        Worker.objects.create(employer=profile3, company=amazon, position='HR')

    def test_company(self):
        apple_company = Company.objects.get(name='Apple')
        amazon_company = Company.objects.get(name='Amazon')
        self.assertEqual(amazon_company.offices.count(), 2)
        self.assertEqual(apple_company.offices.count(), 1)
        self.assertEqual(amazon_company.workers.count(), 1)
        self.assertEqual(apple_company.workers.count(), 2)
        self.assertEqual(apple_company.about, 'Apple company')
        self.assertEqual(amazon_company.about, 'Amazon company')

    def test_office(self):
        apple_office = Office.objects.get(name='Apple\'s offices')
        amazon_office = Office.objects.get(name='Amazon\'s offices')
        self.assertEqual(apple_office.company.name, 'Apple')
        self.assertEqual(apple_office.location.name, 'United States of America')
        self.assertEqual(amazon_office.company.name, 'Amazon')
        self.assertEqual(amazon_office.location.name, 'United Kingdom')

    def test_worker(self):
        maxim = Worker.objects.filter(employer=Profile.objects.get(user=User.objects.get(username='Maxim'))).first()
        misha = Worker.objects.filter(employer=Profile.objects.get(user=User.objects.get(username='Misha'))).first()
        masha = Worker.objects.filter(employer=Profile.objects.get(user=User.objects.get(username='Masha'))).first()
        self.assertEqual(maxim.company.name, 'Apple')
        self.assertEqual(misha.company.name, 'Apple')
        self.assertEqual(masha.company.name, 'Amazon')
        self.assertEqual(maxim.position, 'python developer')
        self.assertEqual(misha.position, 'devops')
        self.assertEqual(masha.position, 'HR')
