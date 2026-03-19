# -*- coding: utf-8 -*-
"""
Tích hợp AI (Google Gemini) để phân tích bảng lương và xu hướng nhân viên.
Yêu cầu: pip install google-generativeai
API Key: Lấy tại https://aistudio.google.com/app/apikey
"""

from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

# Tên param lưu API key trong Odoo System Parameters
GEMINI_API_KEY_PARAM = 'nhan_su_cham_cong_luong.gemini_api_key'


class BangLuongThangAI(models.Model):
    _inherit = 'bang.luong.thang'

    ai_phan_tich = fields.Text(
        string='Phân tích AI',
        readonly=True,
        help='Kết quả phân tích từ Google Gemini AI'
    )
    ai_dang_xu_ly = fields.Boolean(
        string='Đang phân tích...', default=False
    )

    def action_phan_tich_ai(self):
        """Gọi Gemini AI phân tích bảng lương và xu hướng nhân viên."""
        self.ensure_one()

        # Lấy API key từ System Parameters
        api_key = self.env['ir.config_parameter'].sudo().get_param(GEMINI_API_KEY_PARAM)
        if not api_key:
            raise UserError(
                "Chưa cấu hình Gemini API Key!\n"
                "Vào Settings → Technical → System Parameters\n"
                f"Tạo key: '{GEMINI_API_KEY_PARAM}' với giá trị là API key của bạn.\n"
                "Lấy API key miễn phí tại: https://aistudio.google.com/app/apikey"
            )

        try:
            import google.generativeai as genai
        except ImportError:
            raise UserError(
                "Thiếu thư viện google-generativeai!\n"
                "Chạy lệnh: pip install google-generativeai"
            )

        # Lấy lịch sử 3 tháng gần nhất để so sánh
        lich_su = self.env['bang.luong.thang'].search([
            ('employee_id', '=', self.employee_id.id),
            ('trang_thai', 'in', ['calculated', 'confirmed', 'paid']),
            ('id', '!=', self.id),
        ], order='nam desc, thang desc', limit=3)

        # Xây dựng prompt
        prompt = self._build_ai_prompt(lich_su)

        self.write({'ai_dang_xu_ly': True, 'ai_phan_tich': 'Đang phân tích...'})

        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            ket_qua = response.text
        except Exception as e:
            _logger.error("Lỗi gọi Gemini API: %s", str(e))
            self.write({'ai_dang_xu_ly': False, 'ai_phan_tich': f'Lỗi: {str(e)}'})
            raise UserError(f"Lỗi khi gọi Gemini API: {str(e)}")

        self.write({
            'ai_phan_tich': ket_qua,
            'ai_dang_xu_ly': False,
        })

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Phân tích AI hoàn tất',
                'message': 'Xem kết quả trong tab "Phân tích AI"',
                'type': 'success',
            }
        }

    def _build_ai_prompt(self, lich_su):
        """Xây dựng prompt gửi cho Gemini."""
        self.ensure_one()

        # Dữ liệu tháng hiện tại
        thong_tin_hien_tai = f"""
THÔNG TIN BẢNG LƯƠNG THÁNG {self.thang:02d}/{self.nam}
Nhân viên: {self.employee_id.name}
Chức vụ: {self.employee_id.job_title or 'N/A'}
Phòng ban: {self.employee_id.department_id.name if self.employee_id.department_id else 'N/A'}

DỮ LIỆU CHẤM CÔNG:
- Số ngày công chuẩn: {self.so_ngay_cong_chuan} ngày
- Số ngày làm việc thực tế: {self.so_ngay_lam_viec} ngày
- Tỷ lệ công: {self.ty_le_cong:.1f}%
- Tổng giờ làm việc: {self.tong_gio_lam_viec:.1f} giờ

KỶ LUẬT:
- Số lần vi phạm (đi muộn/về sớm): {self.so_lan_vi_pham} lần
- Tổng phút vi phạm: {self.tong_phut_vi_pham} phút
- Tiền phạt: {self.tien_phat_ky_luat:,.0f} VND

TĂNG CA:
- Giờ tăng ca ngày thường: {self.tong_gio_tang_ca_thuong:.1f} giờ
- Giờ tăng ca cuối tuần: {self.tong_gio_tang_ca_cuoi_tuan:.1f} giờ
- Tiền tăng ca: {self.tien_tang_ca:,.0f} VND

LƯƠNG:
- Lương cơ bản: {self.luong_co_ban:,.0f} VND
- Lương theo ngày công: {self.luong_theo_ngay_cong:,.0f} VND
- BHXH/BHYT/BHTN: {self.tien_bao_hiem:,.0f} VND
- Số người phụ thuộc: {self.so_nguoi_phu_thuoc}
- Giảm trừ gia cảnh: {self.tong_giam_tru_gia_canh:,.0f} VND
- Thuế TNCN: {self.thue_tncn:,.0f} VND
- LƯƠNG THỰC LÃNH: {self.luong_thuc_lanh:,.0f} VND
"""

        # Lịch sử so sánh
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

        prompt = f"""Bạn là chuyên gia phân tích nhân sự và lương thưởng. 
Hãy phân tích dữ liệu lương sau và đưa ra nhận xét ngắn gọn, thực tế bằng tiếng Việt.

{thong_tin_hien_tai}
{lich_su_str}

Hãy phân tích theo 4 mục sau (mỗi mục 2-3 câu ngắn gọn):

1. ĐÁNH GIÁ CHUYÊN CẦN: Nhận xét về tỷ lệ đi làm, vi phạm kỷ luật.
2. ĐÁNH GIÁ HIỆU SUẤT: Nhận xét về tăng ca, mức độ cống hiến.
3. XU HƯỚNG SO SÁNH: So sánh với các tháng trước (nếu có dữ liệu).
4. ĐỀ XUẤT CHO HR: 1-2 hành động cụ thể HR nên thực hiện.

Trả lời ngắn gọn, súc tích, không dùng markdown phức tạp."""

        return prompt
