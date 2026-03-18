# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

# ── Cấu hình giờ làm việc chuẩn ────────────────────────────────────────────
# Giờ bắt đầu: 08:30, Giờ kết thúc: 17:30 (8 tiếng + 30 phút nghỉ trưa)
GIO_LAM_CHUAN = {
    'bat_dau': (8, 30),   # 08:30
    'ket_thuc': (17, 30), # 17:30
    'so_gio_chuan': 8.0,  # 8 tiếng/ngày
}

# Hệ số tăng ca
HE_SO_TANG_CA = {
    'ngay_thuong': 1.5,  # Ngày thường: x1.5
    'cuoi_tuan': 2.0,    # Thứ 7, Chủ nhật: x2.0
}

# Ngưỡng tối thiểu để tính tăng ca (phút)
TANG_CA_TOI_THIEU_PHUT = 30


def _phut_trong_ngay(dt_local):
    """Trả về số phút kể từ 00:00 của ngày đó."""
    return dt_local.hour * 60 + dt_local.minute


class HrAttendanceInherit(models.Model):
    _inherit = 'hr.attendance'

    # ── Đi muộn ─────────────────────────────────────────────────────────────
    is_late = fields.Boolean(
        string='Đi muộn',
        compute='_compute_ky_luat',
        store=True,
        help='True nếu check-in sau 08:30'
    )
    late_minutes = fields.Integer(
        string='Số phút muộn',
        compute='_compute_ky_luat',
        store=True
    )

    # ── Về sớm ───────────────────────────────────────────────────────────────
    is_early_leave = fields.Boolean(
        string='Về sớm',
        compute='_compute_ky_luat',
        store=True,
        help='True nếu check-out trước 17:30'
    )
    early_leave_minutes = fields.Integer(
        string='Số phút về sớm',
        compute='_compute_ky_luat',
        store=True
    )

    # ── Tăng ca ──────────────────────────────────────────────────────────────
    is_overtime = fields.Boolean(
        string='Có tăng ca',
        compute='_compute_tang_ca',
        store=True,
        help='True nếu làm thêm ít nhất 30 phút sau 17:30'
    )
    overtime_minutes = fields.Integer(
        string='Số phút tăng ca',
        compute='_compute_tang_ca',
        store=True
    )
    overtime_hours = fields.Float(
        string='Giờ tăng ca',
        compute='_compute_tang_ca',
        store=True,
        digits=(5, 2)
    )
    he_so_tang_ca = fields.Float(
        string='Hệ số tăng ca',
        compute='_compute_tang_ca',
        store=True,
        help='1.5 ngày thường, 2.0 cuối tuần'
    )

    # ── Tổng hợp vi phạm ─────────────────────────────────────────────────────
    tong_phut_vi_pham = fields.Integer(
        string='Tổng phút vi phạm',
        compute='_compute_ky_luat',
        store=True,
        help='late_minutes + early_leave_minutes'
    )

    @api.depends('check_in', 'check_out')
    def _compute_ky_luat(self):
        """
        Tính toán vi phạm kỷ luật: đi muộn và về sớm.
        Dùng context_timestamp để chuyển UTC -> giờ địa phương.
        """
        phut_bat_dau = GIO_LAM_CHUAN['bat_dau'][0] * 60 + GIO_LAM_CHUAN['bat_dau'][1]
        phut_ket_thuc = GIO_LAM_CHUAN['ket_thuc'][0] * 60 + GIO_LAM_CHUAN['ket_thuc'][1]

        for rec in self:
            # ── Đi muộn ──
            if rec.check_in:
                ci_local = fields.Datetime.context_timestamp(rec, rec.check_in)
                phut_ci = _phut_trong_ngay(ci_local)
                if phut_ci > phut_bat_dau:
                    rec.is_late = True
                    rec.late_minutes = phut_ci - phut_bat_dau
                else:
                    rec.is_late = False
                    rec.late_minutes = 0
            else:
                rec.is_late = False
                rec.late_minutes = 0

            # ── Về sớm ──
            if rec.check_out:
                co_local = fields.Datetime.context_timestamp(rec, rec.check_out)
                phut_co = _phut_trong_ngay(co_local)
                if phut_co < phut_ket_thuc:
                    rec.is_early_leave = True
                    rec.early_leave_minutes = phut_ket_thuc - phut_co
                else:
                    rec.is_early_leave = False
                    rec.early_leave_minutes = 0
            else:
                rec.is_early_leave = False
                rec.early_leave_minutes = 0

            rec.tong_phut_vi_pham = rec.late_minutes + rec.early_leave_minutes

    @api.depends('check_in', 'check_out')
    def _compute_tang_ca(self):
        """
        Tính tăng ca: số phút làm việc sau giờ kết thúc chuẩn (17:30).
        Áp hệ số 2.0 nếu là cuối tuần (thứ 7=5, chủ nhật=6).
        Chỉ tính nếu tăng ca >= TANG_CA_TOI_THIEU_PHUT (30 phút).
        """
        phut_ket_thuc = GIO_LAM_CHUAN['ket_thuc'][0] * 60 + GIO_LAM_CHUAN['ket_thuc'][1]

        for rec in self:
            if rec.check_in and rec.check_out:
                co_local = fields.Datetime.context_timestamp(rec, rec.check_out)
                phut_co = _phut_trong_ngay(co_local)
                phut_tang_ca = max(0, phut_co - phut_ket_thuc)

                if phut_tang_ca >= TANG_CA_TOI_THIEU_PHUT:
                    rec.is_overtime = True
                    rec.overtime_minutes = phut_tang_ca
                    rec.overtime_hours = round(phut_tang_ca / 60.0, 2)
                    # Cuối tuần: weekday() 5=Thứ 7, 6=Chủ nhật
                    ngay_trong_tuan = co_local.weekday()
                    rec.he_so_tang_ca = (
                        HE_SO_TANG_CA['cuoi_tuan']
                        if ngay_trong_tuan >= 5
                        else HE_SO_TANG_CA['ngay_thuong']
                    )
                else:
                    rec.is_overtime = False
                    rec.overtime_minutes = 0
                    rec.overtime_hours = 0.0
                    rec.he_so_tang_ca = 0.0
            else:
                rec.is_overtime = False
                rec.overtime_minutes = 0
                rec.overtime_hours = 0.0
                rec.he_so_tang_ca = 0.0

    @api.constrains('check_in', 'check_out')
    def _check_checkout_after_checkin(self):
        """Check-out phải sau check-in."""
        for rec in self:
            if rec.check_in and rec.check_out and rec.check_out <= rec.check_in:
                raise ValidationError(
                    f"Check-out ({rec.check_out}) phải sau check-in ({rec.check_in})!"
                )
