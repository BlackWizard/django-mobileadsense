from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django import template
from django.shortcuts import render

from adsense.adsense import adsense

register = template.Library()

fail_silently = getattr(settings, "ADSENSE_DEBUG", None) or settings.DEBUG
default_publisher_id = getattr(settings, "ADSENSE_PUBLISHER_ID", None)
default_slot_id = getattr(settings, "ADSENSE_SLOT_ID", None)

class MobileAdSenseNode(template.Node):
    def __init__(self, publisher_id, slot_id):
        self.publisher_id = template.Variable(publisher_id)
        self.slot_id = template.Variable(slot_id)

    def render(self, context):
        assert "request" in context, "AdSense tag requires request in context."

        if self.publisher_id is not None:
            publisher_id = self.publisher_id.resolve(context)
        else:
            publisher_id = default_publisher_id

        if self.slot_id is not None:
            slot_id = self.slot_id.resolve(context)
        else:
            slot_id = default_slot_id
        
        if publisher_id is None or slot_id is None:
            raise ImproperlyConfigured("No AdSense publisher or slot id given.")

        res = adsense(context["request"], publisher_id, slot_id,  
                       fail_silently=fail_silently)

        if not res or res == '<!-- google_afm -->':
            res = render(context["request"], 'adsense.html').content

        return res

@register.tag
def mobileadsense(parser, token):
    try:
        tag_name, publisher_id, slot_id = token.split_contents() 
    except ValueError:
        publisher_id = None
        slot_id = None

    return MobileAdSenseNode(publisher_id, slot_id)
