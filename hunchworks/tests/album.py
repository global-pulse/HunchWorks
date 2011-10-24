#!/usr/bin/env python

from hunchworks.tests.helpers import ViewTestHelpers
from django.test import TestCase
from hunchworks.models import Album


class AlbumViewsTest(TestCase, ViewTestHelpers):
  fixtures = ("test_users", "test_albums", "test_evidences")

  def test_index(self):
    with self.login("one"):
      resp = self.get("albums")
      self.assertTemplateUsed(resp, "albums/all.html")

  def test_all(self):
    with self.login("one"):
      resp = self.get("all_albums")
      self.assertTemplateUsed(resp, "albums/all.html")

  def test_edit(self):
    with self.login("one"):
      old_album = Album.objects.get(pk=1)
      get_resp = self.get("edit_album", album_id=1)
      self.assertTemplateUsed(get_resp, "albums/edit.html")

      post_resp = self.submit_form(get_resp, {
        "name": "Test Edit Album",
      })

      new_album = Album.objects.get(pk=1)
      self.assertEqual(new_album.name, "Test Edit Album")
      self.assertEqual(old_album.id, new_album.id)
      self.assertRedirects(post_resp, new_album.get_absolute_url())
    
  def test_create(self):
    with self.login("one"):
      get_resp = self.get("create_album")
      self.assertTemplateUsed(get_resp, "albums/create.html")
      
  def test_show(self):
    with self.login("one"):
      get_resp = self.get("album", album_id=1)
      self.assertTemplateUsed(get_resp, "albums/show.html")
      self.assertQuery(get_resp, "article.album", count=1)
      self.assertQuery(get_resp, "article.evidence", count=1)