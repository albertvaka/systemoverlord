import datetime

from django.conf import settings
from django.utils import timesince
from django.utils import timezone
from mezzanine import template

register = template.Library()


@register.filter
def optional_timesince(d):
  """Formats the time d as "timesince" if <settings.TIMESINCE_LIMIT"""
  try:
    limit = datetime.timedelta(seconds=settings.TIMESINCE_LIMIT)
  except AttributeError:
    limit = datetime.timedelta(hours=24)

  if not isinstance(d, datetime.datetime):
    d = datetime.datetime(d.year, d.month, d.day)

  now = datetime.datetime.now(timezone.utc if timezone.is_aware(d) else None)
  
  if now - d > limit:
    return d.astimezone(timezone.get_current_timezone()).strftime(
        '%Y/%m/%d %H:%M')
  return timesince.timesince(d) + " ago"
