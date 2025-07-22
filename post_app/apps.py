from django.apps import AppConfig

class PostAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'post_app'

    # Initializing a global trie that can be used across views for searching
    def ready(self):
        from .models import PostRaw
        from .services.trie_service import Trie
        from . import global_trie
        global_trie.trie = Trie()

        for post in PostRaw.objects.all():
            global_trie.trie.insert(post.title)