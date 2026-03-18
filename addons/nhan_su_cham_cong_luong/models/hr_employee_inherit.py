# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    # Các trường mở rộng theo yêu cầu Giai đoạn 1
    que_quan = fields.Char(string='Quê quán')
    so_cccd = fields.Char(string='Số CCCD')
    ngay_cap = fields.Date(string='Ngày cấp CCCD')

    # Liên kết ngược với bảng chấm công và lương
    bang_cham_cong_ids = fields.One2many(
        'bang.cham.cong.thang',
        'employee_id',
        string='Bảng chấm công'
    )
    bang_luong_ids = fields.One2many(
        'bang.luong.thang',
        'employee_id',
        string='Bảng lương'
    )

    @api.constrains('birthday')
    def _check_birthday(self):
        for rec in self:
            if rec.birthday and rec.birthday > fields.Date.today():
                raise ValidationError("Ngày sinh không được lớn hơn ngày hiện tại!")
