# -*- coding: utf-8 -*-

from odoo import models, fields, api

# Giờ quy định bắt đầu làm việc: 08:30
GIO_BAT_DAU = 8
PHUT_BAT_DAU = 30

# Giờ quy định kết thúc làm việc: 17:30
GIO_KET_THUC = 17
PHUT_KET_THUC = 30


class HrAttendanceInherit(models.Model):
    _inherit = 'hr.attendance'

    # Đi muộn
    is_late = fields.Boolean(
        string='Đi muộn',
        compute='_compute_late_info',
        store=True
    )
    late_minutes = fields.Integer(
        string='Số phút muộn',
        compute='_compute_late_info',
        store=True
    )

    # Về sớm
    is_early_leave = fields.Boolean(
        string='Về sớm',
        compute='_compute_early_leave',
        store=True
    )
    early_leave_minutes = fields.Integer(
        string='Số phút về sớm',
        compute='_compute_early_leave',
        store=True
    )

    @api.depends('check_in')
    def _compute_late_info(self):
        for rec in self:
            if rec.check_in:
                # Chuyển về giờ địa phương (UTC+7)
                check_in_local = fields.Datetime.context_timestamp(rec, rec.check_in)
                gio = check_in_local.hour
                phut = check_in_local.minute

                # Tính số phút từ đầu ngày
                phut_check_in = gio * 60 + phut
                phut_bat_dau = GIO_BAT_DAU * 60 + PHUT_BAT_DAU

                if phut_check_in > phut_bat_dau:
                    rec.is_late = True
                    rec.late_minutes = phut_check_in - phut_bat_dau
                else:
                    rec.is_late = False
                    rec.late_minutes = 0
            else:
                rec.is_late = False
                rec.late_minutes = 0

    @api.depends('check_out')
    def _compute_early_leave(self):
        for rec in self:
            if rec.check_out:
                check_out_local = fields.Datetime.context_timestamp(rec, rec.check_out)
                gio = check_out_local.hour
                phut = check_out_local.minute

                phut_check_out = gio * 60 + phut
                phut_ket_thuc = GIO_KET_THUC * 60 + PHUT_KET_THUC

                if phut_check_out < phut_ket_thuc:
                    rec.is_early_leave = True
                    rec.early_leave_minutes = phut_ket_thuc - phut_check_out
                else:
                    rec.is_early_leave = False
                    rec.early_leave_minutes = 0
            else:
                rec.is_early_leave = False
                rec.early_leave_minutes = 0
