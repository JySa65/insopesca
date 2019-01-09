class Selects(object):

	def role(self):
		return(
			('is_coordinator', 'Coordinador'),
			('is_worker', 'Trabajador')
		)

	def level(self):
		return(
			('is_ord_pesque', 'Ordenación Pesquera'),
			('is_acuicul', 'Acuicultura'),
		)