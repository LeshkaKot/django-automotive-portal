from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from student.models import Student



class GetPagesTestCase(TestCase):
    fixtures = ['student_student.json', 'student_category.json', 'student_manual.json', 'student_tagpost.json', 'users_user', 'users_user_group', 'auth_group']


    def setUp(self):
        "Инициализация перед выполнением каждого теста"


    def test_main_page(self):
        path = reverse('home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        #self.assertIn('student/index.html', response.template_name)
        self.assertTemplateUsed(response, 'student/index.html')
        self.assertEqual(response.context_data['title'], 'Honda UA')


    def test_redirect_addpage(self):
        path = reverse('add_page')
        redirect_uri = reverse('users:login') + '?next=' + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)


    def test_data_main_page(self):
        s = Student.published.all().select_related('cat')
        path = reverse('home')
        response = self.client.get(path)
        self.assertQuerySetEqual(response.context_data['posts'], s[:3])


    def test_paginate_main_page(self):
        path = reverse('home')
        page = 2
        paginate_by = 3
        response = self.client.get(path + f"?page={page}")
        s = Student.published.all().select_related('cat')
        self.assertQuerySetEqual(response.context_data['posts'], s[(page - 1) * paginate_by:page * paginate_by])


    def test_content_post(self):
        s = Student.published.get(pk=1)
        path = reverse('post', args=[s.slug])
        response = self.client.get(path)
        self.assertEqual(s.content, response.context_data['post'].content)


    def tearDown(self):
        "Действия после выполнения каждого теста"
