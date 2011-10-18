from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from hunchworks.models import Evidence, Hunch

class EvidencesFeed(Feed):

  def get_object(self, request, hunch_id):
      return get_object_or_404(Hunch, pk=hunch_id)

  def title(self, obj):
    return "Hunchworks evidence for %s" % obj.title

  def description(self, obj):
    return "Recently updated evidence on HunchWorks for %s" % obj.title

  def link(self, obj):
    return obj.get_absolute_url()

  def items(self, obj):
    return obj.evidences.all()

  def item_title(self, item):
    return item.title

  def item_description(self, item):
    return item.description

  def item_link(self, item):
    return "/evidences/"

class RecentHunchFeed(Feed):
  title = "HunchWorks Recently Updated Hunches"
  link = "/hunches"
  description = "Recently updated hunches on HunchWorks"

  def items(self):
    return Hunch.objects.order_by('-time_modified')[:20]

  def item_title(self, item):
    return item.title

  def item_description(self, item):
    return item.description

  def item_link(self, item):
    return "/hunches/" + str(item.id)

