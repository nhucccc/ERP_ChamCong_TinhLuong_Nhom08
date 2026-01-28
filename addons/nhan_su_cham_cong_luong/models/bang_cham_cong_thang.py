# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar


class BangChamCongThang(models.Model):
    _name = 'bang.cham.cong.thang'
    _description = 'Bảng chấm công theo tháng'
    _rec_name = 'ten_bang_cham_cong'
    _order = 'nam desc, thang desc, nhan_vien_id'

    # Thông tin cơ bản
    nhan_vien_id = fields.Many2one(
        'nhan_vien', 
        string='Nhân viên', 
        required=True,
        help='Nhân viên từ module nhan_su'
    )
    thang = fields.Integer('Tháng', required=True)
    nam = fields.Integer('Năm', required=True)
    ten_bang_cham_cong = fields.Char(
        'Tên bảng chấm công', 
        compute='_compute_ten_bang_cham_cong', 
        store=True
    )
    
    # Thông tin chấm công tổng hợp
    so_ngay_lam_viec = fields.Integer(
        'Số ngày làm việc', 
        compute='_compute_cham_cong_data', 
        store=True,
        help='Số ngày thực tế có chấm công'
    )
    tong_gio_lam_viec = fields.Float(
        'Tổng giờ làm việc', 
        compute='_compute_cham_cong_data', 
        store=True,
        help='Tổng số giờ làm việc trong tháng'
    )
    so_ngay_cong_chuan = fields.Integer(
        'Số ngày công chuẩn',
        compute='_compute_so_ngay_cong_chuan',
        store=True,
        help='Số ngày công chuẩn trong tháng (trừ chủ nhật)'
    )
    
    # Trạng thái
    trang_thai = fields.Selection([
        ('draft', 'Nháp'),
        ('confirmed', 'Đã xác nhận'),
        ('locked', 'Đã khóa')
    ], string='Trạng thái', default='draft')
    
    # Liên kết với hr.employee để lấy dữ liệu chấm công
    hr_employee_id = fields.Many2one(
        'hr.employee',
        string='HR Employee',
        compute='_compute_hr_employee_id',
        store=True,
        help='Liên kết với hr.employee để lấy dữ liệu chấm công'
    )
    
    # Chi tiết chấm công
    chi_tiet_cham_cong_ids = fields.One2many(
        'hr.attendance',
        compute='_compute_chi_tiet_cham_cong',
        string='Chi tiết chấm công'
    )

    @api.depends('nhan_vien_id', 'thang', 'nam')
    def _compute_ten_bang_cham_cong(self):
        for record in self:
            if record.nhan_vien_id and record.thang and record.nam:
                record.ten_bang_cham_cong = f"Chấm công {record.nhan_vien_id.ho_va_ten} - {record.thang:02d}/{record.nam}"
            else:
                record.ten_bang_cham_cong = "Chấm công"

    @api.depends('nhan_vien_id')
    def _compute_hr_employee_id(self):
        """
        Tìm hr.employee tương ứng với nhan_vien dựa trên tên hoặc email
        """
        for record in self:
            if record.nhan_vien_id:
                # Tìm hr.employee có tên hoặc email trùng khớp
                hr_employee = self.env['hr.employee'].search([
                    '|',
                    ('name', 'ilike', record.nhan_vien_id.ho_va_ten),
                    ('work_email', '=', record.nhan_vien_id.email)
                ], limit=1)
                record.hr_employee_id = hr_employee.id if hr_employee else False
            else:
                record.hr_employee_id = False

    @api.depends('thang', 'nam')
    def _compute_so_ngay_cong_chuan(self):
        """
        Tính số ngày công chuẩn trong tháng (trừ chủ nhật)
        """
        for record in self:
            if record.thang and record.nam:
                # Lấy số ngày trong tháng
                so_ngay_trong_thang = calendar.monthrange(record.nam, record.thang)[1]
                
                # Đếm số chủ nhật trong tháng
                so_chu_nhat = 0
                for ngay in range(1, so_ngay_trong_thang + 1):
                    ngay_trong_tuan = date(record.nam, record.thang, ngay).weekday()
                    if ngay_trong_tuan == 6:  # Chủ nhật = 6
                        so_chu_nhat += 1
                
                record.so_ngay_cong_chuan = so_ngay_trong_thang - so_chu_nhat
            else:
                record.so_ngay_cong_chuan = 0

    @api.depends('hr_employee_id', 'thang', 'nam')
    def _compute_cham_cong_data(self):
        """
        Tính toán dữ liệu chấm công từ hr.attendance
        """
        for record in self:
            if record.hr_employee_id and record.thang and record.nam:
                # Xác định khoảng thời gian của tháng
                ngay_dau_thang = date(record.nam, record.thang, 1)
                ngay_cuoi_thang = date(record.nam, record.thang, 
                                     calendar.monthrange(record.nam, record.thang)[1])
                
                # Tìm tất cả bản ghi chấm công trong tháng
                attendances = self.env['hr.attendance'].search([
                    ('employee_id', '=', record.hr_employee_id.id),
                    ('check_in', '>=', datetime.combine(ngay_dau_thang, datetime.min.time())),
                    ('check_in', '<=', datetime.combine(ngay_cuoi_thang, datetime.max.time())),
                    ('check_out', '!=', False)  # Chỉ lấy những bản ghi đã check out
                ])
                
                # Tính toán
                record.so_ngay_lam_viec = len(set(
                    att.check_in.date() for att in attendances
                ))
                record.tong_gio_lam_viec = sum(attendances.mapped('worked_hours'))
            else:
                record.so_ngay_lam_viec = 0
                record.tong_gio_lam_viec = 0.0

    @api.depends('hr_employee_id', 'thang', 'nam')
    def _compute_chi_tiet_cham_cong(self):
        """
        Lấy chi tiết chấm công trong tháng
        """
        for record in self:
            if record.hr_employee_id and record.thang and record.nam:
                ngay_dau_thang = date(record.nam, record.thang, 1)
                ngay_cuoi_thang = date(record.nam, record.thang, 
                                     calendar.monthrange(record.nam, record.thang)[1])
                
                attendances = self.env['hr.attendance'].search([
                    ('employee_id', '=', record.hr_employee_id.id),
                    ('check_in', '>=', datetime.combine(ngay_dau_thang, datetime.min.time())),
                    ('check_in', '<=', datetime.combine(ngay_cuoi_thang, datetime.max.time()))
                ])
                record.chi_tiet_cham_cong_ids = attendances
            else:
                record.chi_tiet_cham_cong_ids = False

    @api.model
    def tao_bang_cham_cong_thang(self, thang=None, nam=None, nhan_vien_ids=None):
        """
        Tạo bảng chấm công cho tháng và nhân viên chỉ định
        Nếu không chỉ định thì tạo cho tháng hiện tại và tất cả nhân viên
        """
        if not thang:
            thang = date.today().month
        if not nam:
            nam = date.today().year
        
        if not nhan_vien_ids:
            nhan_vien_ids = self.env['nhan_vien'].search([]).ids
        
        created_records = self.env['bang.cham.cong.thang']
        
        for nhan_vien_id in nhan_vien_ids:
            # Kiểm tra xem đã tồn tại bảng chấm công chưa
            existing = self.search([
                ('nhan_vien_id', '=', nhan_vien_id),
                ('thang', '=', thang),
                ('nam', '=', nam)
            ])
            
            if not existing:
                record = self.create({
                    'nhan_vien_id': nhan_vien_id,
                    'thang': thang,
                    'nam': nam
                })
                created_records |= record
        
        return created_records

    def action_confirm(self):
        """Xác nhận bảng chấm công"""
        self.write({'trang_thai': 'confirmed'})

    def action_lock(self):
        """Khóa bảng chấm công"""
        self.write({'trang_thai': 'locked'})

    def action_reset_to_draft(self):
        """Đưa về trạng thái nháp"""
        self.write({'trang_thai': 'draft'})

    _sql_constraints = [
        ('unique_nhan_vien_thang_nam', 
         'unique(nhan_vien_id, thang, nam)', 
         'Mỗi nhân viên chỉ có một bảng chấm công cho mỗi tháng!')
    ]