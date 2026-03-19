# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date, datetime
import calendar

from .hr_family import tinh_thue_tncn, GTGC_BAN_THAN, GTGC_NGUOI_PHU_THUOC

# Mức phạt mỗi phút vi phạm kỷ luật (VND)
PHAT_MOI_PHUT_VI_PHAM = 5_000

# Tỷ lệ BHXH/BHYT/BHTN nhân viên đóng (% lương cơ bản)
# BHXH 8% + BHYT 1.5% + BHTN 1% = 10.5%
TY_LE_BAO_HIEM_NV = 0.105


class BangLuongThang(models.Model):
    _name = 'bang.luong.thang'
    _description = 'Bảng lương theo tháng'
    _rec_name = 'ten_bang_luong'
    _order = 'nam desc, thang desc, employee_id'

    # ── Thông tin cơ bản ─────────────────────────────────────────────────────
    # Trỏ thẳng tới hr.employee - yêu cầu bắt buộc Giai đoạn 1
    employee_id = fields.Many2one(
        'hr.employee', string='Nhân viên',
        required=True, ondelete='cascade',
    )
    thang = fields.Integer('Tháng', required=True)
    nam = fields.Integer('Năm', required=True)
    ten_bang_luong = fields.Char(
        'Tên phiếu lương', compute='_compute_ten_bang_luong', store=True
    )

    # ── Liên kết ─────────────────────────────────────────────────────────────
    bang_cham_cong_id = fields.Many2one(
        'bang.cham.cong.thang', string='Bảng chấm công',
        compute='_compute_bang_cham_cong_id', store=True
    )
    hr_contract_id = fields.Many2one(
        'hr.contract', string='Hợp đồng lao động',
        compute='_compute_hr_contract_id', store=True
    )

    # ── Lương từ hợp đồng ────────────────────────────────────────────────────
    luong_co_ban = fields.Monetary(
        'Lương cơ bản/tháng', currency_field='currency_id',
        compute='_compute_luong_co_ban', store=True
    )
    luong_theo_gio = fields.Monetary(
        'Lương theo giờ', currency_field='currency_id',
        compute='_compute_luong_co_ban', store=True,
        help='Lương cơ bản / (số ngày chuẩn × 8 giờ)'
    )

    # ── Dữ liệu chấm công ────────────────────────────────────────────────────
    so_ngay_lam_viec = fields.Integer(
        'Số ngày làm việc', related='bang_cham_cong_id.so_ngay_lam_viec', store=True
    )
    so_ngay_cong_chuan = fields.Integer(
        'Số ngày công chuẩn', related='bang_cham_cong_id.so_ngay_cong_chuan', store=True
    )
    tong_gio_lam_viec = fields.Float(
        'Tổng giờ làm việc', related='bang_cham_cong_id.tong_gio_lam_viec', store=True
    )
    # Đếm trực tiếp từ hr.attendance - yêu cầu Giai đoạn 1
    tong_ngay_cong = fields.Float(
        'Tổng ngày công', compute='_compute_tong_ngay_cong', store=True,
        help='Đếm số bản ghi hr.attendance trong tháng'
    )
    ty_le_cong = fields.Float(
        'Tỷ lệ công (%)', compute='_compute_ty_le_cong', store=True
    )
    luong_theo_ngay_cong = fields.Monetary(
        'Lương theo ngày công', currency_field='currency_id',
        compute='_compute_luong_theo_ngay_cong', store=True
    )

    # ── Kỷ luật: phạt đi muộn / về sớm - Giai đoạn 2 ───────────────────────
    so_lan_vi_pham = fields.Integer(
        'Số lần vi phạm', compute='_compute_ky_luat_thang', store=True,
        help='Số lần đi muộn hoặc về sớm trong tháng'
    )
    tong_phut_vi_pham = fields.Integer(
        'Tổng phút vi phạm', compute='_compute_ky_luat_thang', store=True
    )
    tien_phat_ky_luat = fields.Monetary(
        'Tiền phạt kỷ luật', currency_field='currency_id',
        compute='_compute_ky_luat_thang', store=True,
        help=f'Tổng phút vi phạm × {PHAT_MOI_PHUT_VI_PHAM:,} VND/phút'
    )

    # ── Tăng ca - Giai đoạn 2 ────────────────────────────────────────────────
    tong_gio_tang_ca_thuong = fields.Float(
        'Giờ tăng ca ngày thường', compute='_compute_tang_ca_thang', store=True
    )
    tong_gio_tang_ca_cuoi_tuan = fields.Float(
        'Giờ tăng ca cuối tuần', compute='_compute_tang_ca_thang', store=True
    )
    tien_tang_ca = fields.Monetary(
        'Tiền tăng ca', currency_field='currency_id',
        compute='_compute_tang_ca_thang', store=True,
        help='(Giờ TC thường × 1.5 + Giờ TC cuối tuần × 2.0) × lương/giờ'
    )

    # ── Thủ công ─────────────────────────────────────────────────────────────
    phu_cap_khac = fields.Monetary(
        'Phụ cấp khác', currency_field='currency_id', default=0.0
    )
    khau_tru_khac = fields.Monetary(
        'Khấu trừ khác', currency_field='currency_id', default=0.0
    )

    # ── Bảo hiểm xã hội ──────────────────────────────────────────────────────
    tien_bao_hiem = fields.Monetary(
        'BHXH/BHYT/BHTN (NV đóng)', currency_field='currency_id',
        compute='_compute_thue_tncn', store=True,
        help=f'Lương cơ bản × {TY_LE_BAO_HIEM_NV*100:.1f}% (BHXH 8% + BHYT 1.5% + BHTN 1%)'
    )

    # ── Giảm trừ gia cảnh & Thuế TNCN - Tính năng tâm đắc ──────────────────
    so_nguoi_phu_thuoc = fields.Integer(
        'Số người phụ thuộc', compute='_compute_thue_tncn', store=True,
        help='Số NPT đã đăng ký và còn hiệu lực trong tháng'
    )
    tong_giam_tru_gia_canh = fields.Monetary(
        'Tổng giảm trừ gia cảnh', currency_field='currency_id',
        compute='_compute_thue_tncn', store=True,
        help='GTGC bản thân (11tr) + GTGC NPT (4.4tr × số NPT)'
    )
    thu_nhap_chiu_thue = fields.Monetary(
        'Thu nhập chịu thuế', currency_field='currency_id',
        compute='_compute_thue_tncn', store=True,
        help='Lương thực nhận trước thuế - Bảo hiểm'
    )
    thu_nhap_tinh_thue = fields.Monetary(
        'Thu nhập tính thuế', currency_field='currency_id',
        compute='_compute_thue_tncn', store=True,
        help='Thu nhập chịu thuế - Tổng giảm trừ gia cảnh'
    )
    thue_tncn = fields.Monetary(
        'Thuế TNCN', currency_field='currency_id',
        compute='_compute_thue_tncn', store=True,
        help='Thuế thu nhập cá nhân lũy tiến 7 bậc'
    )

    # ── Lương thực lãnh ──────────────────────────────────────────────────────
    luong_thuc_lanh = fields.Monetary(
        'Lương thực lãnh', currency_field='currency_id',
        compute='_compute_luong_thuc_lanh', store=True,
        help='Lương ngày công + Tăng ca + Phụ cấp - Phạt - BHXH - Thuế TNCN - Khấu trừ'
    )

    # ── Chi tiết phiếu lương (One2many) ──────────────────────────────────────
    line_ids = fields.One2many(
        'bang.luong.line', 'bang_luong_id', string='Chi tiết phiếu lương'
    )
    thuc_lanh_chi_tiet = fields.Monetary(
        'Thực lãnh (từ chi tiết)', currency_field='currency_id',
        compute='_compute_thuc_lanh_chi_tiet', store=True
    )

    # ── Meta ─────────────────────────────────────────────────────────────────
    trang_thai = fields.Selection([
        ('draft', 'Nháp'),
        ('calculated', 'Đã tính'),
        ('confirmed', 'Đã xác nhận'),
        ('paid', 'Đã thanh toán'),
    ], string='Trạng thái', default='draft')
    currency_id = fields.Many2one(
        'res.currency', default=lambda self: self.env.company.currency_id
    )
    ghi_chu = fields.Text('Ghi chú')

    # ── Helpers ──────────────────────────────────────────────────────────────

    def _get_attendance_domain(self):
        """Domain tìm hr.attendance trong tháng của phiếu lương này."""
        self.ensure_one()
        ngay_dau = date(self.nam, self.thang, 1)
        ngay_cuoi = date(self.nam, self.thang,
                         calendar.monthrange(self.nam, self.thang)[1])
        return [
            ('employee_id', '=', self.employee_id.id),
            ('check_in', '>=', datetime.combine(ngay_dau, datetime.min.time())),
            ('check_in', '<=', datetime.combine(ngay_cuoi, datetime.max.time())),
        ]

    # ── Compute methods ──────────────────────────────────────────────────────

    @api.depends('employee_id', 'thang', 'nam')
    def _compute_ten_bang_luong(self):
        for rec in self:
            if rec.employee_id and rec.thang and rec.nam:
                rec.ten_bang_luong = f"Lương {rec.employee_id.name} - {rec.thang:02d}/{rec.nam}"
            else:
                rec.ten_bang_luong = "Phiếu lương"

    @api.depends('employee_id', 'thang', 'nam')
    def _compute_bang_cham_cong_id(self):
        for rec in self:
            if rec.employee_id and rec.thang and rec.nam:
                bcc = self.env['bang.cham.cong.thang'].search([
                    ('employee_id', '=', rec.employee_id.id),
                    ('thang', '=', rec.thang),
                    ('nam', '=', rec.nam),
                ], limit=1)
                rec.bang_cham_cong_id = bcc
            else:
                rec.bang_cham_cong_id = False

    @api.depends('employee_id', 'thang', 'nam')
    def _compute_hr_contract_id(self):
        for rec in self:
            if rec.employee_id and rec.thang and rec.nam:
                ngay_dau = date(rec.nam, rec.thang, 1)
                ngay_cuoi = date(rec.nam, rec.thang,
                                 calendar.monthrange(rec.nam, rec.thang)[1])
                contract = self.env['hr.contract'].search([
                    ('employee_id', '=', rec.employee_id.id),
                    ('state', '=', 'open'),
                    ('date_start', '<=', ngay_cuoi),
                    '|',
                    ('date_end', '=', False),
                    ('date_end', '>=', ngay_dau),
                ], limit=1)
                rec.hr_contract_id = contract
            else:
                rec.hr_contract_id = False

    @api.depends('hr_contract_id', 'so_ngay_cong_chuan')
    def _compute_luong_co_ban(self):
        for rec in self:
            if rec.hr_contract_id:
                rec.luong_co_ban = rec.hr_contract_id.wage
                so_gio_chuan = (rec.so_ngay_cong_chuan or 26) * 8
                rec.luong_theo_gio = rec.hr_contract_id.wage / so_gio_chuan
            else:
                rec.luong_co_ban = 0.0
                rec.luong_theo_gio = 0.0

    @api.depends('employee_id', 'thang', 'nam')
    def _compute_tong_ngay_cong(self):
        """Đếm số ngày công từ hr.attendance - yêu cầu Giai đoạn 1."""
        for rec in self:
            if rec.employee_id and rec.thang and rec.nam:
                rec.tong_ngay_cong = float(
                    self.env['hr.attendance'].search_count(rec._get_attendance_domain())
                )
            else:
                rec.tong_ngay_cong = 0.0

    @api.depends('so_ngay_lam_viec', 'so_ngay_cong_chuan')
    def _compute_ty_le_cong(self):
        for rec in self:
            rec.ty_le_cong = (
                rec.so_ngay_lam_viec / rec.so_ngay_cong_chuan * 100
                if rec.so_ngay_cong_chuan > 0 else 0.0
            )

    @api.depends('luong_co_ban', 'ty_le_cong')
    def _compute_luong_theo_ngay_cong(self):
        for rec in self:
            rec.luong_theo_ngay_cong = rec.luong_co_ban * (rec.ty_le_cong / 100)

    @api.depends('employee_id', 'thang', 'nam')
    def _compute_ky_luat_thang(self):
        """Tổng hợp vi phạm kỷ luật trong tháng từ hr.attendance."""
        for rec in self:
            if rec.employee_id and rec.thang and rec.nam:
                attendances = self.env['hr.attendance'].search(
                    rec._get_attendance_domain() + [
                        '|', ('is_late', '=', True), ('is_early_leave', '=', True)
                    ]
                )
                rec.so_lan_vi_pham = len(attendances)
                rec.tong_phut_vi_pham = sum(att.tong_phut_vi_pham for att in attendances)
                rec.tien_phat_ky_luat = rec.tong_phut_vi_pham * PHAT_MOI_PHUT_VI_PHAM
            else:
                rec.so_lan_vi_pham = 0
                rec.tong_phut_vi_pham = 0
                rec.tien_phat_ky_luat = 0.0

    @api.depends('employee_id', 'thang', 'nam', 'luong_theo_gio')
    def _compute_tang_ca_thang(self):
        """Tổng hợp tăng ca trong tháng, tính tiền theo hệ số."""
        for rec in self:
            if rec.employee_id and rec.thang and rec.nam:
                attendances = self.env['hr.attendance'].search(
                    rec._get_attendance_domain() + [('is_overtime', '=', True)]
                )
                gio_thuong = sum(
                    att.overtime_hours for att in attendances if att.he_so_tang_ca == 1.5
                )
                gio_cuoi_tuan = sum(
                    att.overtime_hours for att in attendances if att.he_so_tang_ca == 2.0
                )
                rec.tong_gio_tang_ca_thuong = round(gio_thuong, 2)
                rec.tong_gio_tang_ca_cuoi_tuan = round(gio_cuoi_tuan, 2)
                rec.tien_tang_ca = (
                    (gio_thuong * 1.5 + gio_cuoi_tuan * 2.0) * rec.luong_theo_gio
                )
            else:
                rec.tong_gio_tang_ca_thuong = 0.0
                rec.tong_gio_tang_ca_cuoi_tuan = 0.0
                rec.tien_tang_ca = 0.0

    @api.depends(
        'employee_id', 'thang', 'nam',
        'luong_theo_ngay_cong', 'tien_tang_ca', 'phu_cap_khac',
        'tien_phat_ky_luat', 'luong_co_ban'
    )
    def _compute_thue_tncn(self):
        """
        Tính thuế TNCN lũy tiến và giảm trừ gia cảnh.
        Quy trình:
          1. Đếm NPT còn hiệu lực trong tháng từ hr.family.member
          2. GTGC = 11tr (bản thân) + 4.4tr × số NPT
          3. BHXH/BHYT/BHTN = lương CB × 10.5%
          4. Thu nhập chịu thuế = tổng thu nhập - BHXH
          5. Thu nhập tính thuế = TNCT - GTGC (min 0)
          6. Thuế TNCN = lũy tiến 7 bậc
        """
        for rec in self:
            if not (rec.employee_id and rec.thang and rec.nam):
                rec.so_nguoi_phu_thuoc = 0
                rec.tong_giam_tru_gia_canh = 0.0
                rec.tien_bao_hiem = 0.0
                rec.thu_nhap_chiu_thue = 0.0
                rec.thu_nhap_tinh_thue = 0.0
                rec.thue_tncn = 0.0
                continue

            # 1. Đếm NPT hiệu lực trong tháng
            npt_records = self.env['hr.family.member'].search([
                ('employee_id', '=', rec.employee_id.id),
                ('da_dang_ky', '=', True),
            ])
            so_npt = sum(
                1 for npt in npt_records
                if npt.is_active_in_month(rec.thang, rec.nam)
            )
            rec.so_nguoi_phu_thuoc = so_npt

            # 2. Giảm trừ gia cảnh
            rec.tong_giam_tru_gia_canh = GTGC_BAN_THAN + so_npt * GTGC_NGUOI_PHU_THUOC

            # 3. BHXH/BHYT/BHTN (tính trên lương cơ bản hợp đồng)
            rec.tien_bao_hiem = rec.luong_co_ban * TY_LE_BAO_HIEM_NV

            # 4. Thu nhập chịu thuế
            tong_thu_nhap = (
                rec.luong_theo_ngay_cong
                + rec.tien_tang_ca
                + rec.phu_cap_khac
                - rec.tien_phat_ky_luat
            )
            rec.thu_nhap_chiu_thue = max(0.0, tong_thu_nhap - rec.tien_bao_hiem)

            # 5. Thu nhập tính thuế
            rec.thu_nhap_tinh_thue = max(
                0.0, rec.thu_nhap_chiu_thue - rec.tong_giam_tru_gia_canh
            )

            # 6. Thuế TNCN lũy tiến
            rec.thue_tncn = tinh_thue_tncn(rec.thu_nhap_tinh_thue)

    @api.depends(
        'luong_theo_ngay_cong', 'tien_tang_ca',
        'phu_cap_khac', 'tien_phat_ky_luat',
        'tien_bao_hiem', 'thue_tncn', 'khau_tru_khac'
    )
    def _compute_luong_thuc_lanh(self):
        for rec in self:
            rec.luong_thuc_lanh = (
                rec.luong_theo_ngay_cong
                + rec.tien_tang_ca
                + rec.phu_cap_khac
                - rec.tien_phat_ky_luat
                - rec.tien_bao_hiem
                - rec.thue_tncn
                - rec.khau_tru_khac
            )

    @api.depends('line_ids.so_tien', 'line_ids.loai')
    def _compute_thuc_lanh_chi_tiet(self):
        for rec in self:
            tong_cong = sum(l.so_tien for l in rec.line_ids if l.loai == 'cong')
            tong_tru = sum(l.so_tien for l in rec.line_ids if l.loai == 'tru')
            rec.thuc_lanh_chi_tiet = tong_cong - tong_tru

    # ── Actions ──────────────────────────────────────────────────────────────

    def action_calculate(self):
        """Tính lương và tự động sinh các dòng chi tiết minh bạch."""
        for rec in self:
            rec.line_ids.unlink()
            lines = []

            if rec.luong_theo_ngay_cong:
                lines.append({
                    'name': (
                        f'Lương cơ bản theo ngày công '
                        f'({rec.so_ngay_lam_viec}/{rec.so_ngay_cong_chuan} ngày'
                        f' = {rec.ty_le_cong:.1f}%)'
                    ),
                    'loai': 'cong', 'sequence': 10,
                    'so_tien': rec.luong_theo_ngay_cong,
                })
            if rec.tong_gio_tang_ca_thuong > 0:
                lines.append({
                    'name': (
                        f'Tăng ca ngày thường '
                        f'({rec.tong_gio_tang_ca_thuong:.2f}h × 1.5 × '
                        f'{rec.luong_theo_gio:,.0f}đ/h)'
                    ),
                    'loai': 'cong', 'sequence': 20,
                    'so_tien': rec.tong_gio_tang_ca_thuong * 1.5 * rec.luong_theo_gio,
                })
            if rec.tong_gio_tang_ca_cuoi_tuan > 0:
                lines.append({
                    'name': (
                        f'Tăng ca cuối tuần '
                        f'({rec.tong_gio_tang_ca_cuoi_tuan:.2f}h × 2.0 × '
                        f'{rec.luong_theo_gio:,.0f}đ/h)'
                    ),
                    'loai': 'cong', 'sequence': 30,
                    'so_tien': rec.tong_gio_tang_ca_cuoi_tuan * 2.0 * rec.luong_theo_gio,
                })
            if rec.phu_cap_khac:
                lines.append({
                    'name': 'Phụ cấp khác',
                    'loai': 'cong', 'sequence': 40,
                    'so_tien': rec.phu_cap_khac,
                })
            if rec.tien_phat_ky_luat:
                lines.append({
                    'name': (
                        f'Phạt kỷ luật '
                        f'({rec.so_lan_vi_pham} lần, '
                        f'{rec.tong_phut_vi_pham} phút × '
                        f'{PHAT_MOI_PHUT_VI_PHAM:,}đ/phút)'
                    ),
                    'loai': 'tru', 'sequence': 50,
                    'so_tien': rec.tien_phat_ky_luat,
                })
            if rec.tien_bao_hiem:
                lines.append({
                    'name': (
                        f'BHXH/BHYT/BHTN ({TY_LE_BAO_HIEM_NV*100:.1f}% × '
                        f'{rec.luong_co_ban:,.0f}đ)'
                    ),
                    'loai': 'tru', 'sequence': 55,
                    'so_tien': rec.tien_bao_hiem,
                })
            if rec.thue_tncn:
                lines.append({
                    'name': (
                        f'Thuế TNCN lũy tiến '
                        f'(TNTT: {rec.thu_nhap_tinh_thue:,.0f}đ, '
                        f'GTGC: {rec.tong_giam_tru_gia_canh:,.0f}đ, '
                        f'{rec.so_nguoi_phu_thuoc} NPT)'
                    ),
                    'loai': 'tru', 'sequence': 57,
                    'so_tien': rec.thue_tncn,
                })
            if rec.khau_tru_khac:
                lines.append({
                    'name': 'Khấu trừ khác',
                    'loai': 'tru', 'sequence': 60,
                    'so_tien': rec.khau_tru_khac,
                })

            for vals in lines:
                vals['bang_luong_id'] = rec.id
                self.env['bang.luong.line'].create(vals)

        self.write({'trang_thai': 'calculated'})

    def action_confirm(self):
        self.write({'trang_thai': 'confirmed'})

    def action_mark_paid(self):
        self.write({'trang_thai': 'paid'})

    def action_reset_to_draft(self):
        self.line_ids.unlink()
        self.write({'trang_thai': 'draft'})

    @api.model
    def tao_bang_luong_thang(self, thang=None, nam=None, employee_ids=None):
        if not thang:
            thang = fields.Date.today().month
        if not nam:
            nam = fields.Date.today().year
        if not employee_ids:
            employee_ids = self.env['hr.employee'].search([]).ids

        created = self.env['bang.luong.thang']
        for emp_id in employee_ids:
            if not self.search([
                ('employee_id', '=', emp_id),
                ('thang', '=', thang), ('nam', '=', nam)
            ]):
                self.env['bang.cham.cong.thang'].tao_bang_cham_cong_thang(
                    thang=thang, nam=nam, employee_ids=[emp_id]
                )
                created |= self.create({
                    'employee_id': emp_id, 'thang': thang, 'nam': nam
                })
        return created

    # ── AI Analysis ──────────────────────────────────────────────────────────
    ai_phan_tich = fields.Text(
        string='Phân tích AI', readonly=True,
        help='Kết quả phân tích từ Google Gemini AI'
    )

    def action_phan_tich_ai(self):
        """Gọi Gemini AI phân tích bảng lương và xu hướng nhân viên."""
        self.ensure_one()

        api_key = self.env['ir.config_parameter'].sudo().get_param(
            'nhan_su_cham_cong_luong.gemini_api_key'
        )
        if not api_key:
            raise UserError(
                "Chưa cấu hình Gemini API Key!\n"
                "Vào Settings → Technical → System Parameters\n"
                "Tạo key: 'nhan_su_cham_cong_luong.gemini_api_key'\n"
                "Lấy API key miễn phí tại: https://aistudio.google.com/app/apikey"
            )

        try:
            import google.generativeai as genai
        except ImportError:
            raise UserError(
                "Thiếu thư viện google-generativeai!\n"
                "Chạy: pip install google-generativeai"
            )

        # Lịch sử 3 tháng gần nhất
        lich_su = self.env['bang.luong.thang'].search([
            ('employee_id', '=', self.employee_id.id),
            ('trang_thai', 'in', ['calculated', 'confirmed', 'paid']),
            ('id', '!=', self.id),
        ], order='nam desc, thang desc', limit=3)

        lich_su_str = ""
        if lich_su:
            lich_su_str = "\nLỊCH SỬ 3 THÁNG GẦN NHẤT:\n"
            for bl in lich_su:
                lich_su_str += (
                    f"- Tháng {bl.thang:02d}/{bl.nam}: "
                    f"Công={bl.so_ngay_lam_viec}ngày, "
                    f"Vi phạm={bl.so_lan_vi_pham}lần/{bl.tong_phut_vi_pham}phút, "
                    f"Tăng ca={bl.tong_gio_tang_ca_thuong + bl.tong_gio_tang_ca_cuoi_tuan:.1f}h, "
                    f"Thực lãnh={bl.luong_thuc_lanh:,.0f}VND\n"
                )

        prompt = f"""Bạn là chuyên gia phân tích nhân sự. Phân tích dữ liệu lương sau bằng tiếng Việt, ngắn gọn.

BẢNG LƯƠNG THÁNG {self.thang:02d}/{self.nam} - {self.employee_id.name}
Phòng ban: {self.employee_id.department_id.name if self.employee_id.department_id else 'N/A'}

CHẤM CÔNG: {self.so_ngay_lam_viec}/{self.so_ngay_cong_chuan} ngày ({self.ty_le_cong:.1f}%)
KỶ LUẬT: {self.so_lan_vi_pham} lần vi phạm, {self.tong_phut_vi_pham} phút, phạt {self.tien_phat_ky_luat:,.0f}đ
TĂNG CA: {self.tong_gio_tang_ca_thuong:.1f}h thường + {self.tong_gio_tang_ca_cuoi_tuan:.1f}h cuối tuần = {self.tien_tang_ca:,.0f}đ
LƯƠNG: CB={self.luong_co_ban:,.0f}đ | BHXH={self.tien_bao_hiem:,.0f}đ | Thuế={self.thue_tncn:,.0f}đ | THỰC LÃNH={self.luong_thuc_lanh:,.0f}đ
{lich_su_str}
Phân tích theo 4 mục (mỗi mục 2-3 câu):
1. ĐÁNH GIÁ CHUYÊN CẦN
2. ĐÁNH GIÁ HIỆU SUẤT
3. XU HƯỚNG SO SÁNH (nếu có lịch sử)
4. ĐỀ XUẤT CHO HR"""

        try:
            genai.configure(api_key=api_key)
            model_ai = genai.GenerativeModel('gemini-1.5-flash')
            response = model_ai.generate_content(prompt)
            self.write({'ai_phan_tich': response.text})
        except Exception as e:
            raise UserError(f"Lỗi Gemini API: {str(e)}")

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Phân tích AI hoàn tất',
                'message': 'Xem kết quả bên dưới form',
                'type': 'success',
            }
        }

    _sql_constraints = [
        ('unique_employee_thang_nam',
         'unique(employee_id, thang, nam)',
         'Mỗi nhân viên chỉ có một phiếu lương cho mỗi tháng!')
    ]
