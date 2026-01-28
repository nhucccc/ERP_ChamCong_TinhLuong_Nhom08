# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date


class TaoBangChamCongLuongWizard(models.TransientModel):
    _name = 'tao.bang.cham.cong.luong.wizard'
    _description = 'Wizard tạo bảng chấm công và lương'

    thang = fields.Integer('Tháng', required=True, default=lambda self: date.today().month)
    nam = fields.Integer('Năm', required=True, default=lambda self: date.today().year)
    
    nhan_vien_ids = fields.Many2many(
        'nhan_vien',
        string='Nhân viên',
        help='Để trống để tạo cho tất cả nhân viên'
    )
    
    tao_bang_cham_cong = fields.Boolean('Tạo bảng chấm công', default=True)
    tao_bang_luong = fields.Boolean('Tạo bảng lương', default=True)
    
    ghi_de_neu_ton_tai = fields.Boolean(
        'Ghi đè nếu đã tồn tại', 
        default=False,
        help='Xóa và tạo lại nếu đã có bảng cho tháng này'
    )

    def action_tao_bang(self):
        """Thực hiện tạo bảng chấm công và lương"""
        self.ensure_one()
        
        # Lấy danh sách nhân viên
        if self.nhan_vien_ids:
            nhan_vien_ids = self.nhan_vien_ids.ids
        else:
            nhan_vien_ids = self.env['nhan_vien'].search([]).ids
        
        created_cham_cong = self.env['bang.cham.cong.thang']
        created_luong = self.env['bang.luong.thang']
        
        # Xử lý ghi đè nếu cần
        if self.ghi_de_neu_ton_tai:
            if self.tao_bang_cham_cong:
                existing_cham_cong = self.env['bang.cham.cong.thang'].search([
                    ('nhan_vien_id', 'in', nhan_vien_ids),
                    ('thang', '=', self.thang),
                    ('nam', '=', self.nam)
                ])
                existing_cham_cong.unlink()
            
            if self.tao_bang_luong:
                existing_luong = self.env['bang.luong.thang'].search([
                    ('nhan_vien_id', 'in', nhan_vien_ids),
                    ('thang', '=', self.thang),
                    ('nam', '=', self.nam)
                ])
                existing_luong.unlink()
        
        # Tạo bảng chấm công
        if self.tao_bang_cham_cong:
            created_cham_cong = self.env['bang.cham.cong.thang'].tao_bang_cham_cong_thang(
                thang=self.thang,
                nam=self.nam,
                nhan_vien_ids=nhan_vien_ids
            )
        
        # Tạo bảng lương
        if self.tao_bang_luong:
            created_luong = self.env['bang.luong.thang'].tao_bang_luong_thang(
                thang=self.thang,
                nam=self.nam,
                nhan_vien_ids=nhan_vien_ids
            )
        
        # Thông báo kết quả
        message = f"Đã tạo thành công:\n"
        if created_cham_cong:
            message += f"- {len(created_cham_cong)} bảng chấm công\n"
        if created_luong:
            message += f"- {len(created_luong)} bảng lương\n"
        message += f"Cho tháng {self.thang:02d}/{self.nam}"
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Thành công',
                'message': message,
                'type': 'success',
                'sticky': False,
            }
        }

    @api.onchange('thang')
    def _onchange_thang(self):
        """Validate tháng"""
        if self.thang and (self.thang < 1 or self.thang > 12):
            return {
                'warning': {
                    'title': 'Cảnh báo',
                    'message': 'Tháng phải từ 1 đến 12'
                }
            }

    @api.onchange('nam')
    def _onchange_nam(self):
        """Validate năm"""
        if self.nam and (self.nam < 2000 or self.nam > 2100):
            return {
                'warning': {
                    'title': 'Cảnh báo',
                    'message': 'Năm phải từ 2000 đến 2100'
                }
            }