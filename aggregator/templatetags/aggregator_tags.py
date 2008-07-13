from django import template
from genshi.filters import HTMLSanitizer
from genshi.input import HTML

register = template.Library()

@register.filter
def sanitize(value):
  """sanitize html using genshi"""
  html = HTML(value)
  sanitizer = HTMLSanitizer()
  return html | sanitizer

def twitterize(value):
  """do twitter autolinking"""
  return(value)
