# -*- coding: utf-8 -*-
"""
Quản lý người phụ thuộc & Giảm trừ gia cảnh (GTGC)
====================================================
Theo Luật Thuế TNCN Việt Nam (Thông tư 111/2013/TT-BTC, sửa đổi 2020):
  - Giảm trừ bản thân: 11,000,000 VND/tháng
  - Giảm trừ mỗi người phụ thuộc: 4,400,000 VND/tháng
  - Thuế TNCN: lũy tiến 7 bậc (0% → 35%)

Tính năng tâm đắc: Liên kết hr.employee → khai báo NPT → tự động tính
GTGC → tính thuế TNCN lũy tiến → cập nhật vào bang.luong.thang.
"""

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

# ── Hằng số thuế TNCN (VND/tháng) ──────────────────────────────────────────
GTGC_BAN_THAN = 11_000_000       # Giảm trừ bản thân
GTGC_NGUOI_PHU_THUOC = 4_400_000  # Giảm trừ mỗi NPT

# Biểu thuế lũy tiến (thu nhập tính thuế/tháng → thuế suất, thuế cố định)
# Bậc: (ngưỡng_tối_đa, thue_suat, thue_co_dinh_cua_bac_truoc)
BIEU_THUE_TNCN = [
    (5_000_000,   0.05, 0),
    (10_000_000,  0.10, 250_000),
    (18_000_000,  0.15, 750_000),
    (32_000_000,  0.20, 1_950_000),
    (52_000_000,  0.25, 4_750_000),
    (80_000_000,  0.30, 9_750_000),
    (float('inf'), 0.35, 17_550_000),
]

# Ngưỡng thu nhập chịu thuế (nếu thu nhập tính thuế <= 0 thì không đóng)
NGUONG_CHIU_THUE = 0


def tinh_thue_tncn(thu_nhap_tinh_thue: float) -> float:
    """
    Tính thuế TNCN lũy tiến theo biểu thuế Việt Nam.
    thu_nhap_tinh_thue = Thu nhập chịu thuế - GTGC bản thân - GTGC NPT
    """
    if thu_nhap_tinh_thue <= NGUONG_CHIU_THUE:
        return 0.0

    nguong_duoi = 0.0
    for nguong_tren, thue_suat, thue_co_dinh in BIEU_THUE_TNCN:
        if thu_nhap_tinh_thue <= nguong_tren:
            return thue_co_dinh + (thu_nhap_tinh_thue - nguong_duoi) * thue_suat
        nguong_duoi = nguong_tren

    return 0.0  # fallback


class HrFamilyMember(models.Model):
    """Người phụ thuộc của nhân viên."""
    _name = 'hr.family.member'
    _description = 'Người phụ thuộc'
    _order = 'employee_id, loai_quan_he, ho_ten'

    # ── Liên kết nhân viên (bắt buộc theo nguyên tắc "Ai làm việc này?") ───
    employee_id = fields.Many2one(
        'hr.employee',
        string='Nhân viên',
        required=True,
        ondelete='cascade',
        index=True,
    )

    # ── Thông tin cá nhân ────────────────────────────────────────────────────
    ho_ten = fields.Char('Họ và tên', required=True)
    ngay_sinh = fields.Date('Ngày sinh')
    so_cccd = fields.Char('Số CCCD/CMND')
    loai_quan_he = fields.Selection([
        ('con', 'Con'),
        ('bo_me', 'Bố/Mẹ'),
        ('vo_chong', 'Vợ/Chồng'),
        ('anh_chi_em', 'Anh/Chị/Em'),
        ('khac', 'Khác'),
    ], string='Quan hệ', required=True, default='con')

    # ── Trạng thái đăng ký NPT ───────────────────────────────────────────────
    da_dang_ky = fields.Boolean(
        'Đã đăng ký NPT',
        default=True,
        help='Chỉ những NPT đã đăng ký mới được tính giảm trừ'
    )
    ngay_bat_dau = fields.Date(
        'Ngày bắt đầu tính',
        default=fields.Date.today,
        help='Ngày bắt đầu được tính giảm trừ gia cảnh'
    )
    ngay_ket_thuc = fields.Date(
        'Ngày kết thúc',
        help='Để trống nếu vẫn còn hiệu lực'
    )

    # ── Tuổi (compute) ───────────────────────────────────────────────────────
    tuoi = fields.Integer(
        'Tuổi',
        compute='_compute_tuoi',
        store=True,
        help='Tính từ ngày sinh đến hôm nay'
    )

    @api.depends('ngay_sinh')
    def _compute_tuoi(self):
        today = date.today()
        for rec in self:
            if rec.ngay_sinh:
                rec.tuoi = (
                    today.year - rec.ngay_sinh.year
                    - ((today.month, today.day) < (rec.ngay_sinh.month, rec.ngay_sinh.day))
                )
            else:
                rec.tuoi = 0

    @api.constrains('ngay_sinh')
    def _check_ngay_sinh(self):
        for rec in self:
            if rec.ngay_sinh and rec.ngay_sinh > fields.Date.today():
                raise ValidationError("Ngày sinh không được lớn hơn ngày hiện tại!")

    @api.constrains('ngay_bat_dau', 'ngay_ket_thuc')
    def _check_ngay_hieu_luc(self):
        for rec in self:
            if rec.ngay_bat_dau and rec.ngay_ket_thuc:
                if rec.ngay_ket_thuc < rec.ngay_bat_dau:
                    raise ValidationError("Ngày kết thúc phải sau ngày bắt đầu!")

    def is_active_in_month(self, thang: int, nam: int) -> bool:
        """Kiểm tra NPT có hiệu lực trong tháng/năm chỉ định không."""
        self.ensure_one()
        if not self.da_dang_ky:
            return False
        ngay_dau_thang = date(nam, thang, 1)
        import calendar
        ngay_cuoi_thang = date(nam, thang, calendar.monthrange(nam, thang)[1])

        if self.ngay_bat_dau and self.ngay_bat_dau > ngay_cuoi_thang:
            return False
        if self.ngay_ket_thuc and self.ngay_ket_thuc < ngay_dau_thang:
            return False
        return True

    _sql_constraints = [
        ('unique_cccd_employee',
         'unique(employee_id, so_cccd)',
         'Số CCCD này đã được đăng ký cho nhân viên này!'),
    ]
