from django.urls import reverse


class Selects(object):
    def type_transport(self):
        return(
            ('is_land', 'Terrestre'),
            ('is_maritime', 'Maritimo'),
            ('is_fluvial', 'Fluvial'),
        )

    def type_vissel(self):
        return(
            ('Curiara', 'Curiara'),
            ('Canoa', 'Canoa')
        )

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
            ('V', 'V'),
            ('E', 'E'),
            ('G', 'G'),
            ('J', 'J'),
            ('C', 'C'),
            ('P', 'P')

        )

    def type_document_user(self):
        return (
            ('V', 'V'),
            ('E', 'E'),
        )

    def level_user_url(self):
        return {
            'is_admin_or_coordinator': reverse('authentication:list'),
            'is_acuicul': reverse('acuicultura:home'),
            'is_sanid': reverse('sanidad:home'),
            # 'is_ord_pesque':
            # 'is_tvc',
            # 'is_fomen',
        }

    def inspection_result(self):
        return(
            ('is_verygood', 'Muy Bueno'),
            ('is_good', 'Bueno'),
            ('is_bad', 'Malo')
        )
