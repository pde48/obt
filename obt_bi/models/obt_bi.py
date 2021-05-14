# -*- coding: utf-8 -*-

from odoo import models, fields, api

class obt_bi(models.Model):
	_name = 'obt_bi'
	_description = u'Seguimiento Terneros'
	
	name = fields.Char(string='Name',required=False,readonly=False,index=False,help="Name",size=50,translate=True)



class obt_bi_cow(models.Model):
	_name = 'obt_bi_cow'
	_description = u'Terneros'
	
	name = fields.Char(string='Nombre',required=False,readonly=False,index=False,help="Nombre",size=50,translate=True)
	number = fields.Char(string='Numero',required=False,readonly=False,index=False,help="Numero",size=50,translate=True)


class obt_bi_unidades_negocio(models.Model):
	_name = 'obt_bi_unidades_negocio'
	_description = u'Terneros'
	
	name = fields.Char(string='Name',required=False,readonly=False,index=False,help="Name",size=50,translate=True)
	


class obt_bi_informe(models.Model):
	_name = 'obt_bi_informe'
	_description = u'informe'
	
	name = fields.Char(string='Name',required=False,readonly=False,index=False,help="Name",size=50,translate=True)



class obt_bi_config(models.Model):
	_name = 'obt_bi_config'
	_description = u'configuracion'
	
	name = fields.Char(string='Name',required=False,readonly=False,index=False,help="Name",size=50,translate=True)




class AccountInvoiceSend(models.TransientModel):
	_inherit = 'account.invoice.send'

	is_email = fields.Boolean('Email', default=lambda self: self.env.user.company_id.invoice_is_email)
	invoice_without_email = fields.Text(compute='_compute_invoice_without_email', string='invoice(s) that will not be sent')
	is_print = fields.Boolean('Print', default=lambda self: self.env.user.company_id.invoice_is_print)
	printed = fields.Boolean('Is Printed', default=False)
	#invoice_ids = fields.Many2many('account.invoice', 'account_invoice_account_invoice_send_rel', string='Invoices')
	partner_ids = fields.Many2many('res.partner', 'res_partner_account_invoice_send_rel', string='Clientes')

	composer_id = fields.Many2one('mail.compose.message', string='Composer', required=True, ondelete='cascade')
	template_id = fields.Many2one(
		'mail.template', 'Use template', index=True,
		domain="[('model', '=', 'account.invoice')]"
		)

	@api.model
	def default_get(self, fields):
		print("fields")
		print(fields)

		res = super(AccountInvoiceSend, self).default_get(fields)
		res_ids = self._context.get('active_ids')
		print(res)
		print(res_ids)
		print("HOLAAAAAAAAAAAAAAAAAAAAAA")

		#{'composition_mode': 'comment', 'is_print': True, 'snailmail_is_letter': False, 
		#'is_email': True, 'template_id': 7, 'email_from': '"Administrator" <admin@example.com>',
		# 'subject': 'Re: INV/2021/0001 ', 'body': '', 'invoice_ids': [1], 'composer_id': 3}


		composer = self.env['mail.compose.message'].create({
			'composition_mode': 'comment' if len(res_ids) == 1 else 'mass_mail',
		})
		res.update({
			'partner_ids': 7,
			#'invoice_ids': res_ids,
			'composer_id': composer.id,
		})
		return res