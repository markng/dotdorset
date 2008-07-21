from django.db import models, connection
import urllib2, feedparser, pprint, datetime, pickle, base64
import djangofeedparserdates

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
  url = models.TextField("Feed URL",max_length=255)
  username = models.CharField("Feed Username", max_length=255, blank=True)
  password = models.CharField("Feed Password", max_length=255, blank=True)
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
  last_modified = models.DateTimeField("Time Last Modified at server", null=True, blank=True)
  etag = models.TextField("Etag from server", null=True, blank=True)
  category = models.ForeignKey(Category)
  approved = models.BooleanField()
  class Admin:
    pass
		
  def __unicode__(self):
    """string rep"""
    return self.title
		
  def refresh(self):
    """refresh feed and feed items"""
    if self.etag:
      parsed = feedparser.parse(self.url, etag=self.etag)
    elif self.last_modified:
      parsed = feedparser.parse(self.url, modified = djangofeedparserdates.datetimetotuple(self.last_modified))
    else:
      parsed = feedparser.parse(self.url)
    # if we get a 304, stop here
    if getattr(parsed, 'status', 200) == 304:
      return self, 'not changed'
    
    # properties to take from parser
    self.title = parsed.feed.title
    self.link = getattr(parsed.feed, 'link', '')		
    self.description = getattr(parsed.feed, 'description', '')		
    if hasattr(parsed.feed, 'author_detail'):
      self.author_name = getattr(parsed.feed.author_detail, 'name', '')		
      self.author_email = getattr(parsed.feed.author_detail, 'email', '')		
      self.author_link = getattr(parsed.feed.author_detail, 'href', '')      
    self.etag = getattr(parsed, 'etag', '')
    if hasattr(parsed, 'modified'):
      self.last_modified = djangofeedparserdates.tupletodatetime(parsed.modified)
    self.subtitle = getattr(parsed.feed, 'subtitle', '')
    self.save()
    for entry in parsed.entries:
      try:
        #handle dates - we need a date for ordering
        if hasattr(entry,'published_parsed'):
          pubdate_transformed = djangofeedparserdates.tupletodatetime(entry.published_parsed)
        elif hasattr(entry,'updated_parsed'):
          pubdate_transformed = djangofeedparserdates.tupletodatetime(entry.updated_parsed)
        else:
          pubdate_transformed = datetime.datetime.utcnow()
          
        #get or create, to avoid duplicates, use link and feed as identifiers.
        feeditem_gc = self.feeditem_set.get_or_create(link=entry.link, feed=self, defaults={'pub_date': pubdate_transformed})
        feeditem = feeditem_gc[0]
        feeditem.title = getattr(entry, 'title', '')
        feeditem.description = getattr(entry, 'summary', '')
        if hasattr(entry, 'author_detail'):
          feeditem.author_name = getattr(entry.author_detail, 'name', '')		
          feeditem.author_email = getattr(entry.author_detail, 'email', '')		
          feeditem.author_link = getattr(entry.author_detail, 'href', '')
        if hasattr(entry,'content'):
          feeditem.content = entry.content[0].value
        feeditem.pickle = base64.b64encode(pickle.dumps(entry))
        feeditem.unique_id = getattr(entry, 'id', '')
        feeditem.save()
      except Exception, e:
        #just print the exception, don't stop execution - this will break refreshes
        print e
      return self, 'updated'
	
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
  pub_date = models.DateTimeField("Publication Date")
  unique_id = models.TextField("Item unique ID",blank=True)
  enclosure = models.TextField("Enclosure",blank=True)
  pickle = models.TextField("Pickled feed parser item", blank=True)
  created_at = models.DateTimeField("Time Created",auto_now_add=True)
  updated_at = models.DateTimeField("Time Last Updated",auto_now=True)
  def __unicode__(self):
    """string rep"""
    return self.title
  
  def fpitem(self):
    """return original feedparser item"""
    if not hasattr(self, 'unpickled'):
      self.unpickled = pickle.loads(self.pickle)
    return self.unpickled
  
  def get_absolute_url(self):
    """return url for feed class"""
    return self.link