from suit.apps import DjangoSuitConfig
from suit.menu import ParentItem, ChildItem


class SuitConfig(DjangoSuitConfig):
    layout = 'horizontal'
    list_per_page = 30
    # menu = (
    #     ParentItem('Cuentas De Usuarios',
    #                app="authentication", icon='fa fa-lock'),
    #     ParentItem('Personas', app="persons", icon='fa fa-map-marker'),
    # )

    def ready(self):
        super(SuitConfig, self).ready()
        self.prevent_user_last_login()

    def prevent_user_last_login(self):
        """
        Disconnect last login signal
        """
        from django.contrib.auth import user_logged_in
        from django.contrib.auth.models import update_last_login
        user_logged_in.disconnect(update_last_login)
