# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta
from functools import partial
from itertools import groupby

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.misc import formatLang, get_lang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare



from werkzeug.urls import url_encode


class managment_obt_bi_tracing(models.Model):
	_name = 'managment_obt_bi_tracing'
	#_inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'sequence.mixin']
	_description = u'Seguimiento Terneros'
	

	
	name = fields.Char(string='N * ',required=False,readonly=True,index=False,help="Name",size=50,translate=True,default=lambda self: _('Cria/Engorde_'))

	unidad_negocio_id = fields.Many2one(
		'managment_obt_bi_unidades_negocio',
		string='Unidad de Negocio',
	)

	date_ingreso = fields.Datetime(
		string='Fecha de Ingreso',
	)

	date_sale = fields.Datetime(
		string='Fecha de Venta',
	)

	dias_engorde = fields.Integer(
		string='Dias total Engorde',
	)

	state = fields.Selection([
        ('engorde', 'Engorde'),
        ('corral_engorde', 'Corral de Engorde'),
        ('sale', 'Venta'),
        ], string='Status', default='engorde')

	cant_cow_ids = fields.One2many(
		'managment_cant_cow',
		'managment_obt_bi_id',
		string='Cantidad',
	)

	weight_cow_ids = fields.One2many(
		'managment_weight_cow',
		'managment_obt_bi_id',
		string='Control de Peso',
	)

	cost_cow_ids = fields.One2many(
		'managment_cost',
		'managment_obt_bi_id',
		string='Gastos',
	)

	transfer_cow_ids = fields.One2many(
		'managment_tranfer',
		'managment_obt_bi_id',
		string='Transferencias',
	)

class ManagmentCantCow(models.Model):
	_name = 'managment_cant_cow'
	_description = 'Control de Peso'


	unidad_negocio_id = fields.Many2one(
		'managment_obt_bi_unidades_negocio',
		string='Unidad de Negocio',
	)

	raza_ternero_id = fields.Many2one(
		'managment_obt_bi_cow',
		string='Ternero',
	)

	cantidad = fields.Integer(
		string='Cantidad',
	)

	managment_obt_bi_id = fields.Many2one(
		'managment_obt_bi_tracing',
		string='Cantidad de Terneros',
	)


class ManagmentWeightCow(models.Model):
	_name = 'managment_weight_cow'
	_description = 'Control de Peso'


	date_peso = fields.Datetime(
		string='Fecha de Peso',
	)

	total_weight = fields.Float(
		string='Total Peso',
	)
	total_avg_weight = fields.Float(
		string='Total Promedio Peso',
	)

	managment_obt_bi_id = fields.Many2one(
		'managment_obt_bi_tracing',
		string='Cantidad de Terneros',
	)
	unidad_de_negocio = fields.Many2one('managment_obt_bi_tracing',string='Seguimiento',store=True,related='managment_obt_bi_id.unidad_negocio_id')

class managmentCost(models.Model):
	_name = 'managment_cost'
	_description = 'Costos'


	unidad_negocio_id = fields.Many2one(
		'managment_obt_bi_unidades_negocio',
		string='Unidad de Negocio',
	)

	amount_cost = fields.Float(
		string='Valor',
	)

	description = fields.Char(
		string='Descripción',
	)

	date_operations = fields.Datetime(
		string='Fecha de Operacion',
	)

	managment_obt_bi_id = fields.Many2one(
		'managment_obt_bi_tracing',
		string='Costos de Produccion',
	)

	unidad_de_negocio = fields.Many2one('managment_obt_bi_tracing',string='Unidad de Negocio',store=True,related='managment_obt_bi_id.unidad_negocio_id')


class managment_tranfer(models.Model):
	_name = 'managment_tranfer'
	_description = 'Tranferencias'

	unidad_negocio_id_origen = fields.Many2one(
		'managment_obt_bi_unidades_negocio',
		string='Unidad de Negocio Origen',
	)

	unidad_negocio_id_destino = fields.Many2one(
		'managment_obt_bi_unidades_negocio',
		string='Unidad de Negocio Destino',
	)

	date_operations = fields.Datetime(
		string='Fecha de Operacion',
	)

	cantidad = fields.Float(
		string='Cantidad',
	)

	managment_obt_bi_id = fields.Many2one(
		'managment_obt_bi_tracing',
		string='Trasnferencias de unidades',
	)




class managment_obt_bi_cow(models.Model):
	_name = 'managment_obt_bi_cow'
	_description = u'Terneros'
	
	name = fields.Char(string='Nombre',required=False,readonly=False,index=False,help="Nombre",size=50,translate=True)
	number = fields.Char(string='Numero',required=False,readonly=False,index=False,help="Numero",size=50,translate=True)


class managment_obt_bi_unidades_negocio(models.Model):
	_name = 'managment_obt_bi_unidades_negocio'
	_description = u'Unidades de Negocio'
	
	name = fields.Char(string='Unidad de Negocio',required=False,readonly=False,index=False,help="Name",size=50,translate=True)

	class_id = fields.Many2one(
		'managment_obt_bi_unidades_negocio_clase',
		string='Clase',
	)


	sub_class_id = fields.Many2one(
		'managment_obt_bi_unidades_negocio_sub_clase',
		string='Sub Clase',
	)



class managment_obt_bi_unidades_negocio_clase(models.Model):
	_name = 'managment_obt_bi_unidades_negocio_clase'
	_description = u'Unidades de Negocio Clase'

	code = fields.Char(string='Codigo',required=False,readonly=False,index=False,help="Name",size=50,translate=True)
	name = fields.Char(string='Clase',required=False,readonly=False,index=False,help="Name",size=50,translate=True)

class managment_obt_bi_unidades_negocio_sub_clase(models.Model):
	_name = 'managment_obt_bi_unidades_negocio_sub_clase'
	_description = u'Unidades de Negocio Sub Clase'
	_rec_name = 'code'
	
	code = fields.Char(string='Codigo',required=False,readonly=False,index=False,help="Name",size=50,translate=True)
	sub_clase = fields.Char(string='Sub Clase',required=False,readonly=False,index=False,help="Name",size=50,translate=True)
	

class managment_obt_bi_unidades_negocio_categoria(models.Model):
	_name = 'managment_obt_bi_unidades_negocio_categoria'
	_description = u'Unidades de Negocio'
	
	code = fields.Char(string='Codigo',required=False,readonly=False,index=False,help="Name",size=50,translate=True)
	name = fields.Char(string='Categoria',required=False,readonly=False,index=False,help="Name",size=50,translate=True)



class managment_obt_bi_informe(models.Model):
	_name = 'managment_obt_bi_informe'
	_description = u'informe'
	
	name = fields.Char(string='Name',required=False,readonly=False,index=False,help="Name",size=50,translate=True)



class managment_obt_bi_config(models.Model):
	_name = 'managment_obt_bi_config'
	_description = u'configuracion'
	
	name = fields.Char(string='Name',required=False,readonly=False,index=False,help="Name",size=50,translate=True)

