#!/usr/bin/env python
# vim: et ts=2 sw=2

import re
import csv
import urllib
import urllib2
from datetime import datetime
import pyquery
import numpy


class GoogleInsightsAgent(object):
  LOGIN_URL = "https://www.google.com/accounts/ServiceLogin"

  SECTIONS = {
    "interest":        r"^Interest over time$",
    "regions":         r"^Top regions for (.+)$",
    "cities":          r"^Top cities for (.+)$",
    "top_searches":    r"^Top searches for (.+)$",
    "rising_searches": r"^Rising searches for (.+)$"
  }

  def __init__(self, name, username, password, terms):
    self._opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    self._login(username, password)
    self._terms = terms

  def _login(self, username, password):
    f = self._opener.open(self.LOGIN_URL)
    pq = pyquery.PyQuery(f.read())
    form = pq("form")[0]

    data = dict(form.fields, Email=username, Passwd=password)
    self._opener.open(form.action, urllib.urlencode(data))

  def poll(self):
    data = self._fetch(self._url())
    parts = self._parse(data)

    past_interest = []

    for row in parts["interest"]:
      week_start, week_end = self._parse_week(row.pop("Week"))
      interest = self._interest(row.values())
      past_interest.append(interest)

      if len(past_interest) > 12:
        past_interest.pop(0)

      if interest:
        print "%s = %d" % (
          week_start.strftime("W%W"),
          interest)

    # std dev of the past 12 months, excluding the current month
    past_deviation = numpy.std(past_interest[:-1])
    
    if (past_interest[-2] + past_deviation) < interest:
      print "Something related to %s is happening!" % (self._terms)

  def _interest(self, terms):
    return sum(map(self._int, terms))

  def _int(self, value):
    try:
      return int(value)

    except:
      return 0

  def _parse_week(self, week_str):
    return map(self._parse_date, week_str.split(" - "))

  def _parse_date(self, date_str):
    return datetime.strptime(
      date_str.strip(),
      "%Y-%m-%d")

  def _fetch(self, url):
    return self._opener.open(url).read()

  def _parse(self, data):
    chunks = data.strip().split("\n\n")
    output = {}

    for chunk in chunks:
      lines = chunk.strip().split("\n")
      header = lines.pop(0)
      parsed = None

      for name, pattern in self.SECTIONS.items():
        match = re.match(pattern, header)
        if match is not None:

          parsed = self._parse_chunk(lines)
          if match.groups():

            if not name in output: output[name] = {}
            output[name][match.group(1)] = parsed

          # This chunk is unique (e.g. it only appears once, however many terms
          # are being searched for), so store it as-is.
          else:
            output[name] = parsed

          break

    return output

  def _url(self):
    query = ",".join(self._terms)
    params = urllib.urlencode({
      "cmpt": "q",
      "content": 1,
      "export": 1,

      "geo": "US",
      "date": "10/2009 24m",
      "q": query })
    return "http://www.google.com/insights/search/overviewReport?%s" % params

  def _parse_chunk(self, data):
    return csv.DictReader(data, quoting=csv.QUOTE_NONE)
