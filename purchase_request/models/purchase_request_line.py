from odoo import models, fields, api
from datetime import datetime


class Purchaseline(models.Model):
    _name = 'purchase.request.line'
    _description = 'purchase.request.line'

    line_id = fields.Many2one('purchase_request', ondelete='cascade', string='Line')
    product_id = fields.Many2one("product.product", required=True)
    descpription = fields.Char()
    quantity = fields.Float(default=1)
    cost_price = fields.Float()
    total = fields.Float(readonly=True, compute="_price_total")

    @api.depends('cost_price', 'quantity')
    def _price_total(self):
        for record in self:
            record.total = float(record.quantity) * float(record.cost_price)

    @api.onchange('product_id')
    def link_price(self):
        for record in self:
            record.descpription = record.product_id.name
            record.cost_price = record.product_id.standard_price