from django.urls import reverse


class Selects(object):
    def sex(self):
        return(
            ('is_male', 'Masculino'),
            ('is_female', 'Femenino')
        )

    def role(self):
        return(
            ('is_coordinator', 'Coordinador'),
            ('is_worker', 'Trabajador')
        )

    def level(self):
        return(
            ('is_ord_pesque', 'Ordenación Pesquera'),
            ('is_acuicul', 'Acuicultura'),
            ('is_sanid', 'Sanidad'),
            ('is_tvc', 'Tramitación Vigilancia y Control'),
            ('is_fomen', 'Fomento Pesquero y Acuicola')
        )

    def type_document(self):
        return (
            ('CEDULA', 'CEDULA'),
            ('PASAPORTE', 'PASAPORTE'),
            ('RIF', 'RIF')
        )

    def level_user_url(self):
        return {
            'is_admin_or_coordinator': reverse('authentication:list'),
            'is_acuicul': reverse('acuicultura:home'),
            'is_sanid': reverse('sanidad:list'),
            # 'is_ord_pesque':
            # 'is_tvc',
            # 'is_fomen',
        }
