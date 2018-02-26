from django import template
import logging
import json

logger = logging.getLogger('debug')
register = template.Library()

def dict_get(value, arg):
    #custom template tag used like so:
    #{{dictionary|dict_get:var}}
    #where dictionary is duh a dictionary and var is a variable representing
    #one of it's keys

    return value[0]

def toJsData(value):
    v = json.dumps(value)
    return v

register.filter('dict_get', dict_get)
register.filter('toJsData', toJsData)
