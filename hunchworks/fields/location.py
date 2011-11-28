#!/usr/bin/env python

from django import forms
from hunchworks import models


class LocationWidget(forms.MultiWidget):
  def __init__(self, attrs=None):
    widgets = (
      forms.TextInput(attrs={"class": "lat"}),
      forms.TextInput(attrs={"class": "lng"}),
      forms.TextInput(attrs={"class": "name"}))
    super(LocationWidget, self).__init__(widgets, attrs)

  def decompress(self, value):
    if isinstance(value, int):
      value = models.Location.objects.get(pk=value)

    if value is not None:
      return [value.latitude, value.longitude, value.name]

    return [None, None, None]

  def render(self, name, value, attrs=None):

    # take note of the name before calling super, so we can access it from
    # format_output without reimplementing the whole of MultiWidget.render.
    self._name = name

    return super(LocationWidget, self).render(
      name, value, attrs)

  def format_output(self, rendered_widgets):
    lat, lng, name = rendered_widgets
    lat_id = "id_%s_0" % self._name
    lng_id = "id_%s_1" % self._name

    return """
      <div class="loc-widget">
        <ul class="type">
          <li class="active" data-type="latlng">GIS Coordinates</li>
          <li data-type="map">Pin on Map</li>
          <li data-type="name" style="display: none;">Location Name</li>
        </ul>
        <div class="latlng">
          <div class="widgets">
            %s
            %s
            <div class="clear-hack"></div>
          </div>
          <div class="labels">
            <label class="lat" for="%s">Latitude</label>
            <label class="lng" for="%s">Longitude</label>
            <div class="clear-hack"></div>
          </div>
        </div>
        <div class="map hidden"></div>
        <div class="name hidden">%s</div>
      </div>
    """ % (lat, lng, lat_id, lng_id, name)


class LocationField(forms.MultiValueField):
  widget = LocationWidget

  def __init__(self, *args, **kwargs):
    fields = (forms.DecimalField(), forms.DecimalField(), forms.CharField())
    super(LocationField, self).__init__(fields, *args, **kwargs)

  def compress(self, data_list):
    if data_list:
      return models.Location.objects.create(
        latitude  = data_list[0],
        longitude = data_list[1],
        name      = data_list[2])
