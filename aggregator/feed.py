from django.contrib.syndication.feeds import Feed as DjangoFeed
from django.contrib.syndication.feeds import FeedDoesNotExist
from dotdorset.aggregator.models import FeedItem, Feed, Category

class CategoryFeed(DjangoFeed):
  """Category Feed"""
  title = "dotdorset feed"
  link = "http://dotdorset.org/"
  description = "test"
  
  def get_object(self, bits):
    # In case of "/rss/beats/0613/foo/bar/baz/", or other such clutter,
    # check that bits has only one member.
    if len(bits) != 1:
        raise ObjectDoesNotExist
    return Category.objects.get(name__exact=bits[0])
  
  def items(self, obj):
    """return items"""
    return FeedItem.objects.filter(feed__category__id=obj.id).order_by('-pub_date')[:30]


class FullFeed(DjangoFeed):
  """Full Feed"""
  title = "dotdorset feed"
  link = "http://dotdorset.org/"
  description = "test"

  def items(self):
    """return items"""
    return FeedItem.objects.order_by('-pub_date')[:30]
