# pylint: disable=C0103, C0111, R0201, R0903, F0401
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item, TodoList


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = TodoList()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) todo_list item'
        first_item.todo_list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.todo_list = list_
        second_item.save()

        saved_list = TodoList.objects.first()
        assert saved_list == list_

        saved_items = Item.objects.all()
        assert saved_items.count() == 2

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        assert first_saved_item.text == 'The first (ever) todo_list item'
        assert first_saved_item.todo_list == list_
        assert second_saved_item.text == 'Item the second'
        assert second_saved_item.todo_list == list_


class HomePageTest(TestCase):

    def test_root_url_resolves_to_homepage_view(self):
        found = resolve('/')
        assert found.func == home_page

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        assert response.content.decode() == expected_html


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = TodoList.objects.create()
        response = self.client.get('/lists/{}/'.format(list_.id))
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = TodoList.objects.create()
        Item.objects.create(text='itemey 1', todo_list=correct_list)
        Item.objects.create(text='itemey 2', todo_list=correct_list)
        other_list = TodoList.objects.create()
        Item.objects.create(text='other list item 1', todo_list=other_list)
        Item.objects.create(text='other list item 2', todo_list=other_list)

        response = self.client.get('/lists/{}/'.format(correct_list.id))

        assert 'itemey 1' in response.content.decode()
        assert 'itemey 2' in response.content.decode()
        assert 'other list item 1' not in response.content.decode()
        assert 'other list item 2' not in response.content.decode()

    def test_passes_correct_list_to_template(self):
        other_list = TodoList.objects.create()
        correct_list = TodoList.objects.create()
        response = self.client.get('/lists/{}/'.format(correct_list.id))
        assert response.context['todo_list'] == correct_list

class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})

        assert Item.objects.count() == 1
        new_item = Item.objects.first()
        assert new_item.text == 'A new list item'

    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new', data={'item_text': 'A new list item'}
        )
        new_list = TodoList.objects.first()
        self.assertRedirects(response, '/lists/{}/'.format(new_list.id))


class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = TodoList.objects.create()
        correct_list = TodoList.objects.create()

        self.client.post(
            '/lists/{}/add_item'.format(correct_list.id),
            data={'item_text': 'A new item for an existing list'}
        )

        assert Item.objects.count() == 1
        new_item = Item.objects.first()
        assert new_item.text == 'A new item for an existing list'
        assert new_item.todo_list == correct_list

    def test_redirects_to_list_view(self):
        other_list = TodoList.objects.create()
        correct_list = TodoList.objects.create()

        response = self.client.post(
            '/lists/{}/add_item'.format(correct_list.id),
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, '/lists/{}/'.format(correct_list.id))
