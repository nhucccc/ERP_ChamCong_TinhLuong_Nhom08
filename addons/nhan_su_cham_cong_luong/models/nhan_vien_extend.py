# -*- coding: utf-8 -*-

from odoo import models, fields, api


class NhanVienExtend(models.Model):
    _inherit = 'nhan_vien'

    # Liên kết với bảng chấm công
    bang_cham_cong_ids = fields.One2many(
        'bang.cham.cong.thang',
        'nhan_vien_id',
        string='Bảng chấm công'
    )
    
    # Liên kết với bảng lương
    bang_luong_ids = fields.One2many(
        'bang.luong.thang',
        'nhan_vien_id',
        string='Bảng lương'
    )
    
    # Thống kê
    so_thang_cham_cong = fields.Integer(
        'Số tháng có chấm công',
        compute='_compute_so_thang_cham_cong'
    )
    
    so_thang_luong = fields.Integer(
        'Số tháng có lương',
        compute='_compute_so_thang_luong'
    )
    
    # Liên kết với hr.employee
    hr_employee_id = fields.Many2one(
        'hr.employee',
        string='HR Employee',
        help='Liên kết với hr.employee để đồng bộ dữ liệu'
    )

    @api.depends('bang_cham_cong_ids')
    def _compute_so_thang_cham_cong(self):
        for record in self:
            record.so_thang_cham_cong = len(record.bang_cham_cong_ids)

    @api.depends('bang_luong_ids')
    def _compute_so_thang_luong(self):
        for record in self:
            record.so_thang_luong = len(record.bang_luong_ids)

    def action_view_bang_cham_cong(self):
        """Xem bảng chấm công của nhân viên"""
        self.ensure_one()
        return {
            'name': f'Bảng chấm công - {self.ho_va_ten}',
            'type': 'ir.actions.act_window',
            'res_model': 'bang.cham.cong.thang',
            'view_mode': 'tree,form',
            'domain': [('nhan_vien_id', '=', self.id)],
            'context': {'default_nhan_vien_id': self.id}
        }

    def action_view_bang_luong(self):
        """Xem bảng lương của nhân viên"""
        self.ensure_one()
        return {
            'name': f'Bảng lương - {self.ho_va_ten}',
            'type': 'ir.actions.act_window',
            'res_model': 'bang.luong.thang',
            'view_mode': 'tree,form',
            'domain': [('nhan_vien_id', '=', self.id)],
            'context': {'default_nhan_vien_id': self.id}
        }

    def tao_bang_cham_cong_luong_thang_hien_tai(self):
        """Tạo bảng chấm công và lương cho tháng hiện tại"""
        self.ensure_one()
        
        # Tạo bảng chấm công
        self.env['bang.cham.cong.thang'].tao_bang_cham_cong_thang(
            nhan_vien_ids=[self.id]
        )
        
        # Tạo bảng lương
        self.env['bang.luong.thang'].tao_bang_luong_thang(
            nhan_vien_ids=[self.id]
        )
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Thành công',
                'message': f'Đã tạo bảng chấm công và lương tháng hiện tại cho {self.ho_va_ten}',
                'type': 'success'
            }
        }