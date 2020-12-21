from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    #User Signale müssen importiert werden
    def ready(self):
        import users.signals

