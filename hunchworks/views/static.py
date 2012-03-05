#!/usr/bin/env python
# encoding: utf-8

from django.shortcuts import render_to_response


def page(req, template):
  return render_to_response("static/%s.html" % template)
