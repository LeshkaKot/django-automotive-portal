menu = [{'title': "About", 'url_name': 'about'},
        {'title': "Add Article", 'url_name': 'add_page'},
        {'title': "Contact Us", 'url_name': 'contact'},
]

class DataMixin:
    paginate_by = 3
    title_page = None
    cat_selected = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page


        if self.cat_selected is not None:
            self.extra_context['cat_selected'] = self.cat_selected

    def get_mixin_context(self, context, **kwargs):
        context['cat_selected'] = None
        context.update(kwargs)
        return context