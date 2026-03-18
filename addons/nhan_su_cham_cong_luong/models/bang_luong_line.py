# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BangLuongLine(models.Model):
    _name = 'bang.luong.line'
    _description = 'Chi tiết dòng phiếu lương'
    _order = 'loai desc, sequence, id'

    bang_luong_id = fields.Many2one(
        'bang.luong.thang',
        string='Phiếu lương',
        required=True,
        ondelete='cascade'
    )
    sequence = fields.Integer('Thứ tự', default=10)
    name = fields.Char('Nội dung', required=True)
    loai = fields.Selection([
        ('cong', 'Cộng (+)'),
        ('tru', 'Trừ (-)')
    ], string='Loại', required=True, default='cong')
    so_tien = fields.Monetary(
        'Số tiền',
        currency_field='currency_id',
        required=True,
        default=0.0
    )
    currency_id = fields.Many2one(
        related='bang_luong_id.currency_id',
        store=True
    )
    ghi_chu = fields.Char('Ghi chú')

    @api.depends('loai', 'so_tien')
    def _compute_so_tien_signed(self):
        for rec in self:
            rec.so_tien_signed = rec.so_tien if rec.loai == 'cong' else -rec.so_tien

    so_tien_signed = fields.Monetary(
        'Giá trị',
        currency_field='currency_id',
        compute='_compute_so_tien_signed'
    )
