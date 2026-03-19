# BÁO CÁO BÀI TẬP LỚN
## HỌC PHẦN: THỰC TẬP CNTT7 - HỘI NHẬP VÀ QUẢN TRỊ PHẦN MỀM DOANH NGHIỆP

<div align="center">

**TRƯỜNG ĐẠI HỌC ĐẠI NAM - KHOA CÔNG NGHỆ THÔNG TIN**

**ĐỀ TÀI: HỆ THỐNG CHẤM CÔNG & TÍNH LƯƠNG**

**Nhóm 08**

</div>

---

## 1. THÔNG TIN DỰ ÁN

| Hạng mục | Nội dung |
|---|---|
| Đề tài | Chấm công + Tính lương (tự động hóa) |
| Nền tảng | Python Odoo 15, PostgreSQL, Docker |
| Repository | https://github.com/nhucccc/ERP_ChamCong_TinhLuong_Nhom08 |
| Nguồn tham khảo | https://github.com/FIT-DNU/Business-Internship (module `nhan_su`) |

---

## 2. KẾT QUẢ THEO THANG ĐÁNH GIÁ

### ✅ MỨC 1 - TÍCH HỢP HỆ THỐNG

- Module `nhan_su` (Khoa) là master data, không trùng lặp dữ liệu
- `bang.cham.cong.thang` và `bang.luong.thang` đều dùng `hr.employee` làm khóa ngoại
- Liên kết `hr.contract` lấy lương cơ bản, `hr.attendance` lấy ngày công thực tế
- `nhan_vien_extend.py` kế thừa model `nhan_vien` gốc của Khoa

### ✅ MỨC 2 - TỰ ĐỘNG HÓA QUY TRÌNH

3 Cron Job event-driven (`data/cron_jobs.xml`):
- **Cron 1** (ngày 1/tháng): Tự động tạo bảng chấm công cho tất cả nhân viên
- **Cron 2** (ngày 1/tháng): Tự động tạo bảng lương trạng thái Nháp
- **Cron 3** (ngày 5/tháng): Tự động tính lương - phát hiện đi muộn/về sớm/tăng ca, tính BHXH 10.5%, thuế TNCN lũy tiến 7 bậc

### ✅ MỨC 3 - AI & EXTERNAL API

- **AI/LLM**: Tích hợp Google Gemini 2.5 Flash qua REST API - phân tích chuyên cần, hiệu suất, xu hướng 3 tháng, đề xuất cho HR. Nút "🤖 Phân tích AI" trên form bảng lương.
- **External API**: `external_api/cham_cong_client.py` dùng `xmlrpc.client` giả lập máy chấm công vật lý kết nối Odoo, hỗ trợ check-in/check-out/đọc bảng lương qua CLI.

---

## 3. KIẾN TRÚC MODULE

```
addons/nhan_su_cham_cong_luong/
├── models/
│   ├── hr_employee_inherit.py     # Mở rộng hr.employee (CCCD, NPT, liên kết)
│   ├── hr_attendance_inherit.py   # Phát hiện đi muộn, về sớm, tăng ca
│   ├── hr_family.py               # Người phụ thuộc + thuế TNCN lũy tiến 7 bậc
│   ├── bang_cham_cong_thang.py    # Tổng hợp chấm công theo tháng
│   ├── bang_luong_thang.py        # Tính lương + Gemini AI phân tích
│   ├── bang_luong_line.py         # Chi tiết minh bạch từng khoản lương
│   └── nhan_vien_extend.py        # Kế thừa model nhan_vien của Khoa
├── views/                         # 6 file XML + menu
├── wizard/                        # Tạo bảng hàng loạt
├── data/cron_jobs.xml             # 3 cron job tự động hóa
└── security/ir.model.access.csv
```

---

## 4. LUỒNG NGHIỆP VỤ (10 BƯỚC)

| Bước | Actor | Hành động | Module |
|---|---|---|---|
| 1 | HR | Tạo hồ sơ nhân viên, ký hợp đồng | `nhan_su`, `hr_contract` |
| 2 | Nhân viên / Máy CC | Check-in đầu ngày (XML-RPC) | `hr_attendance` |
| 3 | Nhân viên / Máy CC | Check-out cuối ngày (XML-RPC) | `hr_attendance` |
| 4 | **Hệ thống** | Auto compute: đi muộn, về sớm, tăng ca | `hr_attendance_inherit` |
| 5 | **Cron Job 1** | Tạo bảng chấm công tháng (ngày 1) | `bang.cham.cong.thang` |
| 6 | **Cron Job 2** | Tạo bảng lương nháp (ngày 1) | `bang.luong.thang` |
| 7 | **Cron Job 3** | Tính lương tự động (ngày 5) | `bang.luong.thang` |
| 8 | HR | Nhấn "🤖 Phân tích AI" → Gemini phân tích | Gemini 2.5 Flash API |
| 9 | HR | Xác nhận bảng lương | `bang.luong.thang` |
| 10 | Kế toán | Thanh toán lương | `bang.luong.thang` |

---

## 5. TÀI LIỆU KỸ THUẬT

- [`docs/GIAI_DOAN_0_PHAN_TICH_NGHIEP_VU.md`](docs/GIAI_DOAN_0_PHAN_TICH_NGHIEP_VU.md) - Phân tích nghiệp vụ Giai đoạn 0
- [`docs/Audit_Gap_Analysis.md`](docs/Audit_Gap_Analysis.md) - Audit Code & Gap Analysis
- [`docs/businessflow/Nhom08_BusinessFlow_ChamCong_TinhLuong.pdf`](docs/businessflow/Nhom08_BusinessFlow_ChamCong_TinhLuong.pdf) - Sơ đồ Swimlane End-to-End
- [`external_api/README.md`](external_api/README.md) - Hướng dẫn External API

---

**© 2025 Nhóm 08 - Khoa CNTT - Trường Đại học Đại Nam**
