# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class videoclub(models.Model):
#     _name = 'videoclub.videoclub'
#     _description = 'videoclub.videoclub'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

from odoo import models, fields, api
from dateutil.relativedelta import *
from datetime import date
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError

class socio(models.Model):
	_name = 'videoclub.socio'
	_description = 'Permite gestionar los socios que alquilan en el videoclub.'

	name = fields.Char(string='Código socio', required=True, help='Código de socio. Está compuesto por 6 dígitos.')
	nombre = fields.Char(string='Nombre', required=True, help='Nombre del socio.')
	apellido1 = fields.Char(string='Primer apellido', required=True, help='Primer apellido del socio.')
	apellido2 = fields.Char(string='Segundo apellido', help='Segundo apellido del socio.')
	fechadealta = fields.Date(string='Fecha de alta', required=True, default = fields.date.today(), help='Fecha en la que el socio se da de alta.')
	antiguedad = fields.Integer('Antigüedad', compute='_get_antiguedad', help='Años en los que el socio es cliente del videoclub.') 
	fechadebaja = fields.Date(string='Fecha de baja', help='Fecha en la que el socio se da de baja.')
	baja = fields.Boolean('Baja', help='Se activa cuando el socio se da de baja del videoclub.')
	#poner "store=True" al lado de "compute" no es conveniente en este caso porque lo que hace es guardar el campo
	#en la BB.DD. y no nos interesa porque nosotros queremos que el campo se autocalcule cada vez que el campo "fechadealta"
	#se modifica

	#Relaciones entre tablas
	alquiler_ids = fields.One2many('videoclub.alquiler', 'socio_id', string='Alquileres', help='Alquileres que ha realizado el socio.')

	@api.depends('fechadealta') #esta función se disparará cuando haya un cambio en el campo "fechadealta"
	def _get_antiguedad(self):
		for socio in self:
			avui=date.today()
			socio.antiguedad = relativedelta(avui,socio.fechadealta).years

	@api.constrains('name')
	def _check_namelength(self):
		for socio in self:
			if len(socio.name) > 6 or len(socio.name) < 6:
				raise ValidationError("El código de socio debe estar compuesto por 6 digítos, ni más, ni menos.")

	#Restricciones, mismo formato que en la BB.DD.
	_sql_constraints=[('name_uniq', 'unique(name)', 'El código de socio que estás introduciendo ya existe. Prueba con otro código de socio que no exista.')]

class pelicula(models.Model):
	_name = 'videoclub.pelicula'
	_description = 'Permite gestionar las películas que los socios pueden alquilar.'
	_order = 'name'

	name = fields.Char(string='Nombre', required=True, help='Nombre de la película.')
	categoria = fields.Selection(string='Género', selection=[('d', 'Drama'),('t','Terror'),('m', 'Musical'),('s', 'Suspense'),('f', 'Fantasía'),('c', 'Comedia'),('cf', 'Ciencia ficción')], required=True, help='Género de la película.')
	pais = fields.Many2one('res.country', string='País', help='País de la película.')
	sinopsis = fields.Text('Sinopsis', required=True, help='Resumen breve de la película.')
	caratula = fields.Image(string='Carátula', required=True, help='Carátula de la película.')
	imagen1 = fields.Image(help='Escena de la película.')
	imagen2 = fields.Image(help='Escena de la película.')
	
	#Relaciones entre tablas
	alquiler_ids = fields.Many2many('videoclub.alquiler', string='Alquileres', help='Alquileres en los que la película ha sido alquilada.')
	actor_ids = fields.Many2many('videoclub.actor', string='Actores', help='Actores que aparecen en la película.')

class alquiler(models.Model):
	_name = 'videoclub.alquiler'
	_description = 'Permite gestionar los alquileres que realizan los socios.'
	_order = 'name'

	name = fields.Char(string='Número de alquiler', required=True, help='Código del alquiler. Está compuesto por 6 dígitos.')
	fechaalquiler = fields.Date(string='Fecha de alquiler', required=True, default = fields.date.today(), help='Fecha en la que se realiza el alquiler de películas.')
	fechadevolucion = fields.Date(string='Fecha de devolución', compute='_get_fechadevolucion', help='Cada alquiler tiene cómo límite 5 días para devolverlo.')
	diasrestantes = fields.Integer('Días restantes', compute='_get_diasrestantes', help='Días que le quedan al socio para devolver el alquiler.') 
	devolucion = fields.Boolean(string='Devolución efectuada', default=False, help='Se han devuelto las películas alquiladas.')	
	#currency_id = fields.Many2one('res.currency', string='Currency', required=True, domain=[('id', '=', '1')]). Esto es como estaba hecho anteriormente. No funciona.
	currency_id = fields.Many2one('res.currency',default=lambda self: self.env['res.currency'].search([('name', '=', 'EUR')]).id, required=True, readonly=True)	#Dentro de "currency_id" también podría poner: default=lambda self: self.env.company.currency_id.
	#"self.env.company" will return the current company. The company object has a field called "currency_id" which contains the default currency ID.
	#El "domain" que he puesto "id" = 1 es porque el EUR tiene el id 1, pero también podría poner "name" en lugar de "id" y poner el valor que me interese
	#de la columna "name" de la tabla 'res.currency' que hay en la BB.DD. (DBeaver)
	importe = fields.Monetary(string='Importe',currency_field='currency_id', required=True, help='Importe del alquiler.')

	#Relaciones entre tablas
	socio_id = fields.Many2one('videoclub.socio', string='Socio', required=True, help='Socio que ha realizado el alquiler.')
	pelicula_ids = fields.Many2many('videoclub.pelicula', string='Películas', required=True, help='Películas alquiladas.')

	#Restricciones, mismo formato que en la BB.DD.
	_sql_constraints=[('name_uniq', 'unique(name)', 'El número de alquiler que estás introduciendo ya existe. Prueba con otro número de alquiler que no exista.')]

	@api.depends('fechadevolucion', 'devolucion') #esta función se disparará cuando haya un cambio en el campo "fechadevolucion"
	def _get_diasrestantes(self):
		for alquiler in self:
			if alquiler.devolucion:
				alquiler.diasrestantes = 0
			else:
				avui=date.today()
				alquiler.diasrestantes = relativedelta(alquiler.fechadevolucion, avui).days
					
	@api.depends('fechaalquiler') #esta función se disparará cuando haya un cambio en el campo "fechaalquiler"
	def _get_fechadevolucion(self):
		for alquiler in self:
			alquiler.fechadevolucion = alquiler.fechaalquiler + timedelta(days=5)
	
	@api.constrains('name')
	def _check_namelength(self):
		for alquiler in self:
			if len(alquiler.name) > 6 or len(alquiler.name) < 6:
				raise ValidationError("El número del alquiler debe estar compuesto por 6 digítos, ni más, ni menos.")

	@api.constrains('importe')
	def _check_importe(self):
		for alquiler in self:
			if alquiler.importe <= 0:
				raise ValidationError("El importe debe tener un valor superior a 0€.")

class actor(models.Model):
	_name = 'videoclub.actor'
	_description = 'Permite gestionar los actores que participan en las películas.'
	_order = 'name'

	name = fields.Char(string='Nombre completo del actor', required=True, help='Nombre del actor/actriz.')
	fechanacimiento = fields.Date(string='Fecha de nacimiento', required=True, help='Fecha de nacimiento del actor/actriz.')
	anos = fields.Integer('Años', compute='_get_anos', help='Años que tiene actualmente el actor/actriz.')
	pais = fields.Many2one('res.country', string='País', help='País del que es originario el actor/actriz.')
	fallecido = fields.Boolean(string='Fallecido/a', help='El actor/actriz ha fallecido.')
	foto = fields.Image(string='Foto', required=True, help='Fotografía del actor/actriz.')
	anosguardados = fields.Integer('Variable auxiliar para guardar los años del actor/actriz por si fallece.')

	#Relaciones entre tablas
	pelicula_ids = fields.Many2many('videoclub.pelicula', string='Películas', help='Películas en las que ha participado el/la actor/actriz.')

	@api.depends('fechanacimiento', 'fallecido') #esta función se disparará cuando haya un cambio en el campo "fechadevolucion"
	def _get_anos(self):
		for actor in self:
			if not actor.fallecido:
				avui=date.today()
				actor.anos = relativedelta(avui, actor.fechanacimiento).years
				actor.anosguardados = actor.anos
			else:
				actor.anos = actor.anosguardados


