from .models import *

menu = [{'title': "Home", 'url_name': 'base'},
        {'title': "Contact", 'url_name': 'contact'},
        {'title': "Help", 'url_name': 'help'}
]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context["menu"] = menu
        if "selected_category" not in context:
            context["selected_category"] = 0
        return context
