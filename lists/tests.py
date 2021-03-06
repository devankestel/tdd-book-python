from django.urls import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest, response


from lists.views import home_page, new_list
from lists.models import Item, List

# Create your tests here.

class HomePageTest(TestCase): 
    
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):

        my_list = List()
        my_list.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = my_list
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = my_list
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, my_list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, my_list)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, my_list)

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        my_list = List.objects.create()
        response = self.client.get(f'/lists/{my_list.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):

        correct_list = List.objects.create()
        Item.objects.create(text='item1', list=correct_list)
        Item.objects.create(text='item2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='other_list_item_1', list=other_list)
        Item.objects.create(text='other_list_item_2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')
        self.assertNotContains(response, 'other_list_item_1')
        self.assertNotContains(response, 'other_list_item_2')

class NewListTest(TestCase):

    def test_can_save_a_post_request(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_post(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()

        self.assertEqual(response['location'], f'/lists/{new_list.id}/')
        self.assertEqual(response.status_code, 302)
        

class NewItemTest(TestCase):

    def test_can_save_a_post_request_to_an_existing_list(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')

