from odoo import models, fields, api
from datetime import datetime

class reject_wizard(models.Model):
    _name = 'reject_wizard'
    _description = 'reject_wizard'

    purchase_id = fields.Many2one('purchase_request')
    po = fields.Char(string="po", related="purchase_id.request_name")
    wizard_field = fields.Text()

    def reject(self):
        current_id = self.env["purchase_request"].browse(self._context.get('active_id'))
        current_id.rejection_reason = self.wizard_field
        current_id.state = 'option4'