from django.db import models
import feedparser
import pprint

# Create your models here.
class Category(models.Model):
  """Categories for Feeds"""
  name = models.CharField(unique=True,max_length=255)
  def __unicode__(self):
    """string rep"""
    return self.name
  class Admin:
    pass

class Feed(models.Model):
  """Feed to be aggregated"""
  url = models.URLField("Feed URL",max_length=255)
  title = models.TextField("Feed Title",blank=True)
  link = models.URLField("Link to site",verify_exists=False, max_length=255,blank=True)
  description = models.TextField("Feed description",blank=True)
  author_email = models.CharField("Author Email Address",max_length=255,blank=True)
  author_name = models.CharField("Author Name",max_length=255,blank=True)
  author_link = models.URLField("Author Link",verify_exists=False, max_length=255,blank=True)
  subtitle = models.TextField("Feed Subtitle",blank=True)
  created_at = models.DateTimeField("Time Created",auto_now_add=True,blank=True)
  updated_at = models.DateTimeField("Time Last Updated",auto_now=True,blank=True)
  next_retrieval = models.DateTimeField("Next Retrieval Time",auto_now_add=True)
  category = models.ForeignKey(Category)
  approved = models.BooleanField()
  class Admin:
    pass
		
  def __unicode__(self):
    """string rep"""
    return self.title
		
  def refresh(self):
    """refresh feed and feed items"""
    print self.__unicode__()+' is being updated\n'
    parsed = feedparser.parse(self.url)
    pp = pprint.PrettyPrinter(indent=4)
    # properties to take from parser
    self.title = parsed.feed.title
    self.link = getattr(parsed.feed, 'link', '')		
    self.description = getattr(parsed.feed, 'description', '')		
    self.author_name = getattr(parsed.feed.author_detail, 'name', '')		
    self.author_email = getattr(parsed.feed.author_detail, 'email', '')		
    self.author_link = getattr(parsed.feed.author_detail, 'href', '')		
    self.subtitle = getattr(parsed.feed, 'subtitle', '')
    self.save()
    pp.pprint(self.feeditem_set.all())
    for entry in parsed.entries:
      pass
    return self
	
class FeedItem(models.Model):
  """Item belonging to a feed"""
  title = models.TextField("Article Title")
  link = models.URLField("Article Link",verify_exists=False, max_length=255,blank=True)
  feed = models.ForeignKey(Feed,blank=True)
  description = models.TextField("Article description",blank=True)
  author_name = models.CharField("Author Name",max_length=255,blank=True)
  author_email = models.CharField("Author Email",max_length=255,blank=True)
  author_link = models.URLField("Author Link",verify_exists=False, max_length=255,blank=True)
  content = models.TextField("Content of Item",blank=True)
  pub_date = models.TimeField("Publication Date",blank=True)
  unique_id = models.TextField("Item unique ID",blank=True)
  enclosure = models.TextField("Enclosure",blank=True)
  created_at = models.DateTimeField("Time Created",auto_now_add=True)
  updated_at = models.DateTimeField("Time Last Updated",auto_now=True)
  def __unicode__(self):
    """string rep"""
    return self.title