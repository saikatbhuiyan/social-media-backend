from django.apps import AppConfig


class AuthenticationAppConfig(AppConfig):
    name = 'user'
    label = 'user'
    verbose_name = 'User'

    def ready(self):
        import user.signals

# This is how we register our custom app config with Django. Django is smart
# enough to look for the `default_app_config` property of each registered app
# and use the correct app config based on that value.
default_app_config = 'user.AuthenticationAppConfig'