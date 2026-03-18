# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
import calendar


class BangChamCongThang(models.Model):
    _name = 'bang.cham.cong.thang'
    _description = 'Bảng chấm công theo tháng'
    _rec_name = 'ten_bang_cham_cong'
    _order = 'nam desc, thang desc, employee_id'

    # Trỏ thẳng tới hr.employee (Giai đoạn 1 - bắt buộc)
    employee_id = fields.Many2one(
        'hr.employee',
        string='Nhân viên',
        required=True,
        ondelete='cascade'
    )
    thang = fields.Integer('Tháng', required=True)
    nam = fields.Integer('Năm', required=True)
    ten_bang_cham_cong = fields.Char(
        'Tên bảng chấm công',
        compute='_compute_ten_bang_cham_cong',
        store=True
    )

    # Dữ liệu chấm công tổng hợp
    so_ngay_lam_viec = fields.Integer(
        'Số ngày làm việc',
        compute='_compute_cham_cong_data',
        store=True,
        help='Số ngày thực tế có chấm công'
    )
    tong_gio_lam_viec = fields.Float(
        'Tổng giờ làm việc',
        compute='_compute_cham_cong_data',
        store=True
    )
    so_ngay_cong_chuan = fields.Integer(
        'Số ngày công chuẩn',
        compute='_compute_so_ngay_cong_chuan',
        store=True,
        help='Số ngày trong tháng trừ chủ nhật'
    )

    trang_thai = fields.Selection([
        ('draft', 'Nháp'),
        ('confirmed', 'Đã xác nhận'),
        ('locked', 'Đã khóa')
    ], string='Trạng thái', default='draft')

    @api.depends('employee_id', 'thang', 'nam')
    def _compute_ten_bang_cham_cong(self):
        for rec in self:
            if rec.employee_id and rec.thang and rec.nam:
                rec.ten_bang_cham_cong = f"Chấm công {rec.employee_id.name} - {rec.thang:02d}/{rec.nam}"
            else:
                rec.ten_bang_cham_cong = "Chấm công"

    @api.depends('thang', 'nam')
    def _compute_so_ngay_cong_chuan(self):
        for rec in self:
            if rec.thang and rec.nam:
                so_ngay = calendar.monthrange(rec.nam, rec.thang)[1]
                so_chu_nhat = sum(
                    1 for d in range(1, so_ngay + 1)
                    if date(rec.nam, rec.thang, d).weekday() == 6
                )
                rec.so_ngay_cong_chuan = so_ngay - so_chu_nhat
            else:
                rec.so_ngay_cong_chuan = 0

    @api.depends('employee_id', 'thang', 'nam')
    def _compute_cham_cong_data(self):
        """Đếm ngày công từ hr.attendance theo yêu cầu Giai đoạn 1"""
        for rec in self:
            if rec.employee_id and rec.thang and rec.nam:
                ngay_dau = date(rec.nam, rec.thang, 1)
                ngay_cuoi = date(rec.nam, rec.thang,
                                 calendar.monthrange(rec.nam, rec.thang)[1])

                attendances = self.env['hr.attendance'].search([
                    ('employee_id', '=', rec.employee_id.id),
                    ('check_in', '>=', datetime.combine(ngay_dau, datetime.min.time())),
                    ('check_in', '<=', datetime.combine(ngay_cuoi, datetime.max.time())),
                    ('check_out', '!=', False)
                ])

                rec.so_ngay_lam_viec = len(set(att.check_in.date() for att in attendances))
                rec.tong_gio_lam_viec = sum(attendances.mapped('worked_hours'))
            else:
                rec.so_ngay_lam_viec = 0
                rec.tong_gio_lam_viec = 0.0

    @api.model
    def tao_bang_cham_cong_thang(self, thang=None, nam=None, employee_ids=None):
        if not thang:
            thang = fields.Date.today().month
        if not nam:
            nam = fields.Date.today().year
        if not employee_ids:
            employee_ids = self.env['hr.employee'].search([]).ids

        created = self.env['bang.cham.cong.thang']
        for emp_id in employee_ids:
            existing = self.search([
                ('employee_id', '=', emp_id),
                ('thang', '=', thang),
                ('nam', '=', nam)
            ])
            if not existing:
                created |= self.create({
                    'employee_id': emp_id,
                    'thang': thang,
                    'nam': nam
                })
        return created

    def action_confirm(self):
        self.write({'trang_thai': 'confirmed'})

    def action_lock(self):
        self.write({'trang_thai': 'locked'})

    def action_reset_to_draft(self):
        self.write({'trang_thai': 'draft'})

    _sql_constraints = [
        ('unique_employee_thang_nam',
         'unique(employee_id, thang, nam)',
         'Mỗi nhân viên chỉ có một bảng chấm công cho mỗi tháng!')
    ]
