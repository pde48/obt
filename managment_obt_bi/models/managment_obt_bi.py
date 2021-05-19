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




class managment_obt_bi_cow(models.Model):
	_name = 'managment_obt_bi_cow'
	_inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
	_description = u'Cria y engorde de Ternero'

	@api.depends('name')
	def _compute_get_purchase_count(self):
		for order in self:
			order.order_count1 = self.env['managment_obt_bi_tracing'].search_count([('cow_id','=',self.id)])

	@api.depends('name')
	def _compute_get_purchase_count1(self):
		amount_t = 0
		for order in self:
			res_2 = self.env['managment_tracing_obt_bi_expenses'].search_read([('unidad_negocio_id','=',self.unidad_negocio_id.id)],['amount'])
			for rec_3434 in res_2:
				amount_t = rec_3434['amount'] + amount_t

		order.order_count2 = amount_t


	@api.depends('name')
	def _compute_get_purchase_count2(self):
		amount_t = 0
		for order in self:
			res_2 = self.env['managment_tracing_obt_bi_expenses_cow'].search_read([('managment_transfer_obt_bi_id','=',self.id)],['amount'])
			for rec_3434 in res_2:
				amount_t = rec_3434['amount'] + amount_t

		order.order_count3 = amount_t
	
	name = fields.Char(string='Nombre',required=False,readonly=False,index=False,help="Nombre",size=50,translate=True,track_visibility='true',)
	number = fields.Char(string='N°',required=False,readonly=False,index=False,help="Numero",size=50,translate=True,track_visibility='true',)

	unidad_negocio_id = fields.Many2one('managment_obt_bi_unidades_negocio',string='Unidad de Negocio',
	)

	order_count1 = fields.Integer(string='Count',default=0,compute='_compute_get_purchase_count',)
	order_count2 = fields.Integer(string='Count',default=0,compute='_compute_get_purchase_count1',)
	order_count3 = fields.Integer(string='Count',default=0,compute='_compute_get_purchase_count2',)
	pricing_purchase = fields.Float(string='Precio de Compra',)
	supplier_id = fields.Many2one('res.partner',string='Proveedor',	)
	date_purchase = fields.Datetime(string='Fecha de Compra',)
	weight_purchase = fields.Float(string='Peso Compra (KG)',)
	weight_actuality = fields.Float(string='Peso Actual (KG)',)

	notes_purchase = fields.Text(string='Observaciones',)

	date_sale = fields.Datetime(string='Fecha de Venta',)
	weight_sale = fields.Float(string='Peso Final de Venta (KG)',)
	pricing_sale = fields.Float(string='Precio de Venta',)





	trasnfer_ids = fields.One2many(
		'managment_tranfer',
		'cow_id',
		string='Traslados o Movimientos',
		track_visibility='true',
	)

	state = fields.Selection([
		('ingreso', 'Ingreso'),
		('cria_engorde', 'Cria y engorde'),
		('sale', 'Vendido'),
		], string='Status', default='ingreso')

	tracing_id = fields.Many2one(
		'managment_obt_bi_tracing',
		string='tracing',
	)


	def button_1(self):	
		self.ensure_one()
		action = {
			'res_model': 'managment_obt_bi_tracing',
			'type': 'ir.actions.act_window',
		}

		action.update({
			'name': _('Compra de Terneros %s', self.name),
			'domain': [('cow_id', '=', self.id)],
			'view_mode': 'tree,form',
		})

		return action


	def button_2(self):	
		self.ensure_one()
		action = {
			'res_model': 'managment_tracing_obt_bi_expenses',
			'type': 'ir.actions.act_window',
		}

		action.update({
			'name': _('  %s', self.name),
			'domain': [('unidad_negocio_id', '=', self.unidad_negocio_id.id)],
			'view_mode': 'tree',
		})

		return action


	def button_3(self):	
		action = {
			'res_model': 'managment_tracing_obt_bi_expenses_cow',
			'type': 'ir.actions.act_window',
		}

		action.update({
			'name': _('  %s', self.name),
			'domain': [('managment_transfer_obt_bi_id', '=', self.id)],
			'view_mode': 'tree',
		})

		return action



class managment_obt_bi_tracing(models.Model):
	_name = 'managment_obt_bi_tracing'
	_inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
	_description = u'Compra de Ternero'

	name = fields.Char(string='Nombre',required=True,index=False,help="Name",size=50,translate=True,track_visibility='true',)
	number = fields.Char(string='N°',required=True,index=False,help="Name",size=50,translate=True,track_visibility='true',)
	unidad_negocio_id = fields.Many2one(
		'managment_obt_bi_unidades_negocio',
		string='Unidad de Negocio',
	)

	pricing_purchase = fields.Float(string='Precio de Compra',track_visibility='true',)
	supplier_id = fields.Many2one('res.partner',string='Proveedor',	track_visibility='true',)
	date_purchase = fields.Datetime(string='Fecha de Compra',track_visibility='true',)
	weight_purchase = fields.Float(string='Peso  (KG)',track_visibility='true',)

	notes_purchase = fields.Text(string='Observaciones',track_visibility='true',)

	date_ingreso = fields.Datetime(string='Fecha de Ingreso',)
	date_sale = fields.Datetime(string='Fecha de Venta',)
	dias_engorde = fields.Integer(string='Dias total Engorde',)

	state = fields.Selection([
		('draft', 'Borrador'),
		('purchase', 'Comprado'),
		], string='Status', default='draft')


	cow_id = fields.Many2one(
		'managment_obt_bi_cow',
		string='Cow',
	)


	@api.model
	def create(self, vals):
		result = super(managment_obt_bi_tracing, self).create(vals)
		#Generate creacion ternera
		name = vals['name']
		number = vals['number']
		vals_g = {
			'name': vals['name'], 
			'number': vals['number'],
			'tracing_id': result.id,
			'unidad_negocio_id': vals['unidad_negocio_id'] ,
			'pricing_purchase': vals['pricing_purchase'] ,
			'supplier_id': vals['supplier_id'] ,
			'date_purchase': vals['date_purchase'] ,
			'weight_purchase': vals['weight_purchase'] ,
			'notes_purchase': vals['notes_purchase'] ,
			}
		res_1 = self.env['managment_obt_bi_cow'].create(vals_g)
		result.write({'cow_id': res_1.id})

		return result


class ManagmentTracingObtBiExpenses(models.Model):
	_name = 'managment_tracing_obt_bi_expenses'
	_description = 'Description'

	gasto_id = fields.Many2one('managment_obt_bi_expenses',
		string='Gasto',required=True,)
	unidad_negocio_id = fields.Many2one('managment_obt_bi_unidades_negocio',
		string='Unidad de Negocio',required=True,)
	date_operations = fields.Datetime(string='Fecha de Operacion',required=True,)
	amount = fields.Float(string='Valor',required=True,)


class ManagmentTracingObtBiExpensesCow(models.Model):
	_name = 'managment_tracing_obt_bi_expenses_cow'
	_description = 'Description'

	gasto_id = fields.Many2one('managment_obt_bi_expenses',
		string='Gasto',required=True,)
	date_operations = fields.Datetime(string='Fecha de Operacion',required=True,)
	amount = fields.Float(string='Valor',required=True,)
	managment_transfer_obt_bi_id = fields.Many2one('managment_obt_bi_cow',string='Ternero',required=True,)


class ManagmentObtBiExpensesCompany(models.Model):
	_name = 'managment_obt_bi_expenses_company'
	_description = 'Description'

	gasto_id = fields.Many2one('managment_obt_bi_expenses',
		string='Gasto',)
	date_operations = fields.Datetime(string='Fecha de Operacion',)
	amount = fields.Float(string='Valor',)

class ManagmentObtBiExpenses(models.Model):
	_name = 'managment_obt_bi_expenses'
	_description = 'Description'

	name = fields.Char(string='Nombre',size=64,required=False,readonly=False,)
	clase_expénse = fields.Selection([
		('direct', 'Directo'),
		('indirect', 'Indirecto'),
		], string='Tipo de Gasto', default='direct')

	type_expense_id = fields.Many2one(
		'managment_obt_bi_type_expenses',
		string='Field Label',
	)


class ManagmentObtBiTypeExpenses(models.Model):
	_name = 'managment_obt_bi_type_expenses'
	_description = 'Description'

	name = fields.Char(string='Nombre',size=64,required=False,readonly=False,)


class managment_tranfer(models.Model):
	_name = 'managment_tranfer'
	_description = 'Tranferencias'

	unidad_negocio_id_origen = fields.Many2one('managment_obt_bi_unidades_negocio',string='Unidad de Negocio Origen',required=True,)
	unidad_negocio_id_destino = fields.Many2one('managment_obt_bi_unidades_negocio',
		string='Unidad de Negocio Destino',required=True,)

	date_operations = fields.Datetime(string='Fecha de Operacion',required=True,)
	weight = fields.Float(string='Peso Salida',required=True,)
	actuality_tracing = fields.Boolean(string='Actual',default=True)
	#weight_actuality = fields.Float(string='Peso Actual(KG)',)
	cow_id = fields.Many2one('managment_obt_bi_cow',string='Ternero',required=True,)

	state = fields.Selection([
		('draft', 'Borrador'),
		('done', 'Terminado'),
		], string='Status', default='draft')


	@api.model_create_multi
	def create(self, vals_list):
		res = super(managment_tranfer, self).create(vals_list)
		print(vals_list)
		for vals in vals_list:
			#[{'cow_id': 15, 'unidad_negocio_id_origen': 5, 'unidad_negocio_id_destino': 2, 'date_operations': '2021-05-19 06:36:50', 'weight': 600, 'state': 'draft'}]
			print(vals)

			id_cow = vals['cow_id']
			unidad_negocio_id_origen = vals['unidad_negocio_id_origen']
			unidad_negocio_id_destino = vals['unidad_negocio_id_destino']
			weight = vals['weight']

			res_write = self.env['managment_obt_bi_cow'].search([('id','=',id_cow)])
			for rec_wr in res_write:
				rec_wr.write({'unidad_negocio_id': unidad_negocio_id_destino,'weight_actuality': weight})


		res.write({'actuality_tracing':True,'state':'done'})

		return res

	def write(self, vals):
		print(self)
		#id_cow = vals['cow_id']
		#unidad_negocio_id_origen = vals_listvals['unidad_negocio_id_origen']
		#unidad_negocio_id_destino = vals['unidad_negocio_id_destino']
		#weight = vals['weight']
		
		write_result = super(managment_tranfer, self).write(vals)

		return write_result




class ManagmentCantCow(models.Model):
	_name = 'managment_cant_cow'
	_description = 'Control de Peso'

	unidad_negocio_id = fields.Many2one('managment_obt_bi_unidades_negocio',string='Unidad de Negocio',
	)

	raza_ternero_id = fields.Many2one('managment_obt_bi_cow',string='Ternero',)
	weight = fields.Float(string='Peso',)
	managment_cant_obt_bi_id = fields.Many2one('managment_obt_bi_tracing',string='Ternero',)


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

	weight_cow_obt_bi_id = fields.Many2one(
		'managment_obt_bi_tracing',
		string='Cantidad de Terneros',
	)
	#unidad_de_negocio = fields.Many2one('managment_obt_bi_tracing',string='Seguimiento',store=True,related='weight_cow_obt_bi_id.unidad_negocio_id')

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

	managment_cost_obt_bi_id = fields.Many2one(
		'managment_obt_bi_tracing',
		string='Costos de Produccion',
	)



class managment_obt_bi_unidades_negocio(models.Model):
	_name = 'managment_obt_bi_unidades_negocio'
	_description = u'Unidades de Negocio'
	
	name = fields.Char(string='Nombre Unidad de Negocio',required=True,readonly=False,index=False,help="Name",size=50,translate=True)

	class_id = fields.Many2one(
		'managment_obt_bi_unidades_negocio_clase',
		string='Clase',
		required=True,
	)

	sub_class_id = fields.Many2one(
		'managment_obt_bi_unidades_negocio_sub_clase',
		string='Sub Clase',
		required=True,
	)

	category_id = fields.Many2one(
		'managment_obt_bi_unidades_negocio_categoria',
		string='Categoria',
		required=True,
	)



class managment_obt_bi_unidades_negocio_clase(models.Model):
	_name = 'managment_obt_bi_unidades_negocio_clase'
	_description = u'Unidades de Negocio Clase'
	_rec_name = 'name'

	code = fields.Char(string='Codigo',required=False,readonly=False,index=False,help="Name",size=50,translate=True)
	name = fields.Char(string='Clase',required=False,readonly=False,index=False,help="Name",size=50,translate=True)

class managment_obt_bi_unidades_negocio_sub_clase(models.Model):
	_name = 'managment_obt_bi_unidades_negocio_sub_clase'
	_description = u'Unidades de Negocio Sub Clase'
	_rec_name = 'sub_clase'

	
	code = fields.Char(string='Codigo',required=False,readonly=False,index=False,help="Name",size=50,translate=True)
	sub_clase = fields.Char(string='Sub Clase',required=False,readonly=False,index=False,help="Name",size=50,translate=True)
	

class managment_obt_bi_unidades_negocio_categoria(models.Model):
	_name = 'managment_obt_bi_unidades_negocio_categoria'
	_description = u'Unidades de Negocio'
	_rec_name = 'name'

	
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

