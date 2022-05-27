# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime


class purchase_request(models.Model):
    _name = 'purchase_request'
    _description = 'purchase_request'
    _inherit = ['mail.thread']

    request_name = fields.Char(required=True)
    requested_by = fields.Many2one('res.users', required=True, default=lambda self: self.env.user)
    start_date = fields.Date(string="Start Date", default=datetime.today())
    end_date = fields.Date(string="End Date")
    rejection_reason = fields.Text(readonly=True, default="None")
    orderline = fields.One2many('purchase.request.line', 'line_id', string='Order Line')
    total_price = fields.Float(compute="_line_total")
    state = fields.Selection([('option1', 'draft'), ('option2', 'to be approved'), ('option3', 'approved')
                                  , ('option4', 'reject'), ('option5', 'cancel')], string='state', default='option1')
    check_readonly_bool = fields.Boolean(compute='check_readonly')

    @api.onchange('orderline')
    def _line_total(self):
        line = self.orderline
        self.total_price = 0.0
        for each in line:
            self.total_price += each.total

    @api.depends('state')
    def submit_for_approval(self):
        for record in self:
            record.state = 'option2'

    @api.depends('state')
    def cancel(self):
        for record in self:
            record.state = 'option5'

    @api.depends('state')
    def approve(self):
        for record in self:
            record.state = 'option3'
        display_msg = "Purchase Request (" + self.request_name + ") has been approved"
        self.message_post(body=display_msg)
        #all_users = self.env['res.users'].search(['active','=',True])
        #user_obj = self.pool.get('res.users')
        #user_group = user_obj.browse(cr,uid,uid).grou
        #my_users_group = all_users.filtered(lambda user: user.has_group("Manager"))
        desired_group_name = self.env['res.groups'].search([('name','=','Manager')])
        print(desired_group_name.users.ids)
        for i in range(0, len(desired_group_name.users)):
            item = desired_group_name.users[i]
            item.message_post("Purchase Request (" + self.request_name + ") has been approved")
        #mail_template = self.env.ref('purchase_request1.email_template_purchase')
        #mail_template.send_mail(self.id, force_send=True)

    @api.depends('state')
    def reset(self):
        for record in self:
            record.state = 'option1'

    @api.depends('state')
    def check_readonly(self):
        for record in self:
            if record.state == "option3":
                record.check_readonly_bool = False
            elif record.state == "option4":
                record.check_readonly_bool = False
            elif record.state == "option5":
                record.check_readonly_bool = False
            else:
                record.check_readonly_bool = True










