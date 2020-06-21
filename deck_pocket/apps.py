from django.apps import AppConfig

class DeckPocketConfig(AppConfig):
    name = 'deck_pocket'

    def ready(self):
        import deck_pocket.signals
