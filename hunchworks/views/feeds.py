from django.contrib.syndication.views import Feed
from hunchworks.models import Evidence

class EvidencesFeed(Feed):
  title = "HunchWorks Recently Updated Evidence"
  link = "/evidences"
  description = "Recently updated evidence on HunchWorks"

  def items(self):
    return Evidence.objects.order_by('-time_modified')[:20]

  def item_title(self, item):
    return item.title

  def item_description(self, item):
    return item.description

  def item_link(self, item):
    return "/evidences/"
