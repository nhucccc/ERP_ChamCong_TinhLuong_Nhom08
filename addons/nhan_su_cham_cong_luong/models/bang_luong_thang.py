# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
import calendar


class BangLuongThang(models.Model):
    _name = 'bang.luong.thang'
    _description = 'Bảng lương theo tháng'
    _rec_name = 'ten_bang_luong'
    _order = 'nam desc, thang desc, nhan_vien_id'

    # Thông tin cơ bản
    nhan_vien_id = fields.Many2one(
        'nhan_vien', 
        string='Nhân viên', 
        required=True
    )
    thang = fields.Integer('Tháng', required=True)
    nam = fields.Integer('Năm', required=True)
    ten_bang_luong = fields.Char(
        'Tên bảng lương', 
        compute='_compute_ten_bang_luong', 
        store=True
    )
    
    # Liên kết với bảng chấm công
    bang_cham_cong_id = fields.Many2one(
        'bang.cham.cong.thang',
        string='Bảng chấm công',
        compute='_compute_bang_cham_cong_id',
        store=True
    )
    
    # Liên kết với hợp đồng
    hr_contract_id = fields.Many2one(
        'hr.contract',
        string='Hợp đồng',
        compute='_compute_hr_contract_id',
        store=True
    )
    
    # Dữ liệu lương cơ bản
    luong_co_ban = fields.Monetary(
        'Lương cơ bản',
        currency_field='currency_id',
        compute='_compute_luong_co_ban',
        store=True,
        help='Lương cơ bản từ hợp đồng'
    )
    
    # Dữ liệu chấm công
    so_ngay_lam_viec = fields.Integer(
        'Số ngày làm việc',
        related='bang_cham_cong_id.so_ngay_lam_viec',
        store=True
    )
    so_ngay_cong_chuan = fields.Integer(
        'Số ngày công chuẩn',
        related='bang_cham_cong_id.so_ngay_cong_chuan',
        store=True
    )
    tong_gio_lam_viec = fields.Float(
        'Tổng giờ làm việc',
        related='bang_cham_cong_id.tong_gio_lam_viec',
        store=True
    )
    
    # Tính toán lương
    ty_le_cong = fields.Float(
        'Tỷ lệ công (%)',
        compute='_compute_ty_le_cong',
        store=True,
        help='Tỷ lệ số ngày làm việc / số ngày công chuẩn'
    )
    luong_theo_ngay_cong = fields.Monetary(
        'Lương theo ngày công',
        currency_field='currency_id',
        compute='_compute_luong_theo_ngay_cong',
        store=True,
        help='Lương cơ bản * tỷ lệ công'
    )
    
    # Các khoản phụ cấp và khấu trừ
    phu_cap_khac = fields.Monetary(
        'Phụ cấp khác',
        currency_field='currency_id',
        default=0.0,
        help='Các khoản phụ cấp khác (nhập thủ công)'
    )
    khau_tru_khac = fields.Monetary(
        'Khấu trừ khác',
        currency_field='currency_id',
        default=0.0,
        help='Các khoản khấu trừ khác (nhập thủ công)'
    )
    
    # Tổng lương
    tong_luong = fields.Monetary(
        'Tổng lương',
        currency_field='currency_id',
        compute='_compute_tong_luong',
        store=True,
        help='Lương theo ngày công + phụ cấp - khấu trừ'
    )
    
    # Trạng thái
    trang_thai = fields.Selection([
        ('draft', 'Nháp'),
        ('calculated', 'Đã tính'),
        ('confirmed', 'Đã xác nhận'),
        ('paid', 'Đã thanh toán')
    ], string='Trạng thái', default='draft')
    
    # Tiền tệ
    currency_id = fields.Many2one(
        'res.currency',
        string='Tiền tệ',
        default=lambda self: self.env.company.currency_id
    )
    
    # Ghi chú
    ghi_chu = fields.Text('Ghi chú')

    @api.depends('nhan_vien_id', 'thang', 'nam')
    def _compute_ten_bang_luong(self):
        for record in self:
            if record.nhan_vien_id and record.thang and record.nam:
                record.ten_bang_luong = f"Lương {record.nhan_vien_id.ho_va_ten} - {record.thang:02d}/{record.nam}"
            else:
                record.ten_bang_luong = "Bảng lương"

    @api.depends('nhan_vien_id', 'thang', 'nam')
    def _compute_bang_cham_cong_id(self):
        """Tìm bảng chấm công tương ứng"""
        for record in self:
            if record.nhan_vien_id and record.thang and record.nam:
                bang_cham_cong = self.env['bang.cham.cong.thang'].search([
                    ('nhan_vien_id', '=', record.nhan_vien_id.id),
                    ('thang', '=', record.thang),
                    ('nam', '=', record.nam)
                ], limit=1)
                record.bang_cham_cong_id = bang_cham_cong.id if bang_cham_cong else False
            else:
                record.bang_cham_cong_id = False

    @api.depends('nhan_vien_id', 'thang', 'nam')
    def _compute_hr_contract_id(self):
        """Tìm hợp đồng hiệu lực trong tháng"""
        for record in self:
            if record.nhan_vien_id and record.thang and record.nam:
                # Tìm hr.employee tương ứng
                hr_employee = self.env['hr.employee'].search([
                    '|',
                    ('name', 'ilike', record.nhan_vien_id.ho_va_ten),
                    ('work_email', '=', record.nhan_vien_id.email)
                ], limit=1)
                
                if hr_employee:
                    # Tìm hợp đồng hiệu lực trong tháng
                    ngay_dau_thang = date(record.nam, record.thang, 1)
                    ngay_cuoi_thang = date(record.nam, record.thang, 
                                         calendar.monthrange(record.nam, record.thang)[1])
                    
                    contract = self.env['hr.contract'].search([
                        ('employee_id', '=', hr_employee.id),
                        ('state', '=', 'open'),
                        ('date_start', '<=', ngay_cuoi_thang),
                        '|',
                        ('date_end', '=', False),
                        ('date_end', '>=', ngay_dau_thang)
                    ], limit=1)
                    
                    record.hr_contract_id = contract.id if contract else False
                else:
                    record.hr_contract_id = False
            else:
                record.hr_contract_id = False

    @api.depends('hr_contract_id')
    def _compute_luong_co_ban(self):
        """Lấy lương cơ bản từ hợp đồng"""
        for record in self:
            if record.hr_contract_id:
                record.luong_co_ban = record.hr_contract_id.wage
            else:
                record.luong_co_ban = 0.0

    @api.depends('so_ngay_lam_viec', 'so_ngay_cong_chuan')
    def _compute_ty_le_cong(self):
        """Tính tỷ lệ công"""
        for record in self:
            if record.so_ngay_cong_chuan > 0:
                record.ty_le_cong = (record.so_ngay_lam_viec / record.so_ngay_cong_chuan) * 100
            else:
                record.ty_le_cong = 0.0

    @api.depends('luong_co_ban', 'ty_le_cong')
    def _compute_luong_theo_ngay_cong(self):
        """Tính lương theo ngày công"""
        for record in self:
            record.luong_theo_ngay_cong = record.luong_co_ban * (record.ty_le_cong / 100)

    @api.depends('luong_theo_ngay_cong', 'phu_cap_khac', 'khau_tru_khac')
    def _compute_tong_luong(self):
        """Tính tổng lương"""
        for record in self:
            record.tong_luong = record.luong_theo_ngay_cong + record.phu_cap_khac - record.khau_tru_khac

    @api.model
    def tao_bang_luong_thang(self, thang=None, nam=None, nhan_vien_ids=None):
        """
        Tạo bảng lương cho tháng và nhân viên chỉ định
        """
        if not thang:
            thang = date.today().month
        if not nam:
            nam = date.today().year
        
        if not nhan_vien_ids:
            nhan_vien_ids = self.env['nhan_vien'].search([]).ids
        
        created_records = self.env['bang.luong.thang']
        
        for nhan_vien_id in nhan_vien_ids:
            # Kiểm tra xem đã tồn tại bảng lương chưa
            existing = self.search([
                ('nhan_vien_id', '=', nhan_vien_id),
                ('thang', '=', thang),
                ('nam', '=', nam)
            ])
            
            if not existing:
                # Tạo bảng chấm công trước nếu chưa có
                self.env['bang.cham.cong.thang'].tao_bang_cham_cong_thang(
                    thang=thang, 
                    nam=nam, 
                    nhan_vien_ids=[nhan_vien_id]
                )
                
                # Tạo bảng lương
                record = self.create({
                    'nhan_vien_id': nhan_vien_id,
                    'thang': thang,
                    'nam': nam
                })
                created_records |= record
        
        return created_records

    def action_calculate(self):
        """Tính toán lương"""
        # Trigger recompute của các trường computed
        self._compute_bang_cham_cong_id()
        self._compute_hr_contract_id()
        self._compute_luong_co_ban()
        self._compute_ty_le_cong()
        self._compute_luong_theo_ngay_cong()
        self._compute_tong_luong()
        
        self.write({'trang_thai': 'calculated'})

    def action_confirm(self):
        """Xác nhận bảng lương"""
        self.write({'trang_thai': 'confirmed'})

    def action_mark_paid(self):
        """Đánh dấu đã thanh toán"""
        self.write({'trang_thai': 'paid'})

    def action_reset_to_draft(self):
        """Đưa về trạng thái nháp"""
        self.write({'trang_thai': 'draft'})

    _sql_constraints = [
        ('unique_nhan_vien_thang_nam', 
         'unique(nhan_vien_id, thang, nam)', 
         'Mỗi nhân viên chỉ có một bảng lương cho mỗi tháng!')
    ]