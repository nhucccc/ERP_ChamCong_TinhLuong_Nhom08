# -*- coding: utf-8 -*-

from odoo import models, fields, api


class NhanVienExtend(models.Model):
    """
    Mở rộng model nhan_vien của khoa với thống kê chấm công/lương.
    Lưu ý: Dữ liệu chấm công/lương thực tế lưu trên hr.employee (Giai đoạn 1).
    """
    _inherit = 'nhan_vien'

    # Liên kết với hr.employee để tra cứu dữ liệu chấm công/lương
    hr_employee_id = fields.Many2one(
        'hr.employee',
        string='HR Employee',
        help='Liên kết với hr.employee để đồng bộ dữ liệu chấm công/lương'
    )

    so_thang_cham_cong = fields.Integer(
        'Số tháng có chấm công',
        compute='_compute_so_thang_cham_cong'
    )
    so_thang_luong = fields.Integer(
        'Số tháng có lương',
        compute='_compute_so_thang_luong'
    )

    @api.depends('hr_employee_id')
    def _compute_so_thang_cham_cong(self):
        for rec in self:
            if rec.hr_employee_id:
                rec.so_thang_cham_cong = self.env['bang.cham.cong.thang'].search_count([
                    ('employee_id', '=', rec.hr_employee_id.id)
                ])
            else:
                rec.so_thang_cham_cong = 0

    @api.depends('hr_employee_id')
    def _compute_so_thang_luong(self):
        for rec in self:
            if rec.hr_employee_id:
                rec.so_thang_luong = self.env['bang.luong.thang'].search_count([
                    ('employee_id', '=', rec.hr_employee_id.id)
                ])
            else:
                rec.so_thang_luong = 0
