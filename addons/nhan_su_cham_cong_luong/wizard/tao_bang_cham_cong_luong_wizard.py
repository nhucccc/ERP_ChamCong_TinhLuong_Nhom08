# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TaoBangChamCongLuongWizard(models.TransientModel):
    _name = 'tao.bang.cham.cong.luong.wizard'
    _description = 'Wizard tạo bảng chấm công và lương'

    thang = fields.Integer('Tháng', required=True, default=lambda self: fields.Date.today().month)
    nam = fields.Integer('Năm', required=True, default=lambda self: fields.Date.today().year)

    # Dùng hr.employee theo yêu cầu Giai đoạn 1
    employee_ids = fields.Many2many(
        'hr.employee',
        string='Nhân viên',
        help='Để trống để tạo cho tất cả nhân viên'
    )

    tao_bang_cham_cong = fields.Boolean('Tạo bảng chấm công', default=True)
    tao_bang_luong = fields.Boolean('Tạo bảng lương', default=True)
    ghi_de_neu_ton_tai = fields.Boolean('Ghi đè nếu đã tồn tại', default=False)

    def action_tao_bang(self):
        self.ensure_one()
        employee_ids = self.employee_ids.ids or self.env['hr.employee'].search([]).ids

        if self.ghi_de_neu_ton_tai:
            if self.tao_bang_cham_cong:
                self.env['bang.cham.cong.thang'].search([
                    ('employee_id', 'in', employee_ids),
                    ('thang', '=', self.thang), ('nam', '=', self.nam)
                ]).unlink()
            if self.tao_bang_luong:
                self.env['bang.luong.thang'].search([
                    ('employee_id', 'in', employee_ids),
                    ('thang', '=', self.thang), ('nam', '=', self.nam)
                ]).unlink()

        created_cc = self.env['bang.cham.cong.thang']
        created_luong = self.env['bang.luong.thang']

        if self.tao_bang_cham_cong:
            created_cc = self.env['bang.cham.cong.thang'].tao_bang_cham_cong_thang(
                thang=self.thang, nam=self.nam, employee_ids=employee_ids
            )
        if self.tao_bang_luong:
            created_luong = self.env['bang.luong.thang'].tao_bang_luong_thang(
                thang=self.thang, nam=self.nam, employee_ids=employee_ids
            )

        parts = []
        if created_cc:
            parts.append(f"{len(created_cc)} bảng chấm công")
        if created_luong:
            parts.append(f"{len(created_luong)} bảng lương")
        msg = f"Đã tạo: {', '.join(parts)} cho tháng {self.thang:02d}/{self.nam}" if parts \
              else "Không có bảng mới nào được tạo (đã tồn tại)"

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {'title': 'Hoàn thành', 'message': msg, 'type': 'success', 'sticky': False}
        }