# coding: utf-8
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.template import RequestContext
from lists.views import home_page
from lists.models import Item, List


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')  # получить функцию
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string("home.html", context_instance=RequestContext(request))
        self.assertEqual(response.content.decode(), expected_html)

    # def test_home_page_can_save_a_POST_request(self):
    #     request = HttpRequest()
    #     request.method = "POST"
    #     request.POST["item_text"] = "A new list item"
    #
    #     home_page(request)
    #
    #     self.assertEqual(Item.objects.count(), 1)
    #     new_item = Item.objects.first()
    #     self.assertEqual(new_item.text, "A new list item")

    # def test_home_page_redirects_after_POST(self):
    #     request = HttpRequest()
    #     request.method = "POST"
    #     request.POST["item_text"] = "A new list item"
    #
    #     response = home_page(request)
    #
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response['location'], '/lists/user-1/')


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = "The first ever list item"
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "The second item"
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first ever list item")
        # self.assertEqual(first_saved_item.list, list_)
        # self.assertEqual(second_saved_item.text, "The second item")
        # self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get("/lists/user-1/")
        self.assertTemplateUsed(response, "list.html")

    def test_displays_all_item(self):
        Item.objects.create(text="item_1")
        Item.objects.create(text="item_2")

        response = self.client.get("/lists/user-1/")

        self.assertContains(response, "item_1")
        self.assertContains(response, "item_2")


class NewListTest(TestCase):
    def test_saving_POST_request(self):
        self.client.post("/lists/new", data={"item_text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirect_after_POST(self):
        response = self.client.post('/lists/new', data={"item_text": "A new list item"})
        self.assertRedirects(response, "/lists/user-1/")

    def new_test(self):
        pass
