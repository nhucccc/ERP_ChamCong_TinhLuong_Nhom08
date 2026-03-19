# Audit Code & Gap Analysis
## Module tham chiếu: `nhan_su` (FIT-DNU/Business-Internship)

---

## PHẦN 1: AUDIT CODE – Kiểm thử mã nguồn cũ

### 1.1 Chức năng hiện có (kế thừa)
| Chức năng | Trạng thái | Ghi chú |
|---|---|---|
| Quản lý hồ sơ nhân viên (họ tên, CCCD, ngày sinh) | ✅ Ổn định | Dùng làm master data |
| Đơn vị công tác, chức vụ, phòng ban | ✅ Ổn định | Kế thừa qua `nhan_vien_extend.py` |
| Lịch sử công tác, chứng chỉ | ✅ Ổn định | Giữ nguyên |
| Quan hệ gia đình | ⚠️ Thiếu | Chưa có người phụ thuộc giảm trừ gia cảnh |

### 1.2 Lỗi tồn đọng phát hiện
| Lỗi | Mức độ | Cách xử lý |
|---|---|---|
| Không kế thừa `hr.employee` Odoo native | Nghiêm trọng | Tạo `hr_employee_inherit.py` bridge |
| Không có liên kết với `hr.attendance` | Nghiêm trọng | Thêm compute fields từ attendance |
| Không có liên kết với `hr.contract` | Nghiêm trọng | Thêm `_compute_hr_contract_id` |
| Không có logic tính lương | Nghiêm trọng | Xây mới `bang_luong_thang.py` |
| Không phát hiện đi muộn/về sớm/tăng ca | Trung bình | Thêm `hr_attendance_inherit.py` |
| Không có thuế TNCN, BHXH | Trung bình | Xây mới `hr_family.py` + logic lũy tiến |

---

## PHẦN 2: GAP ANALYSIS – Phân tích sự khác biệt

### 2.1 Phần kế thừa từ `nhan_su`
- Model `nhan_vien` → kế thừa qua `nhan_vien_extend.py` (giữ nguyên master data)
- Cấu trúc phòng ban, chức vụ → dùng trực tiếp
- Docker + odoo.conf setup → tái sử dụng

### 2.2 Phần phát triển mới hoàn toàn

| Module mới | Mục đích | Lý do cần thiết |
|---|---|---|
| `hr_employee_inherit.py` | Bridge `nhan_vien` ↔ `hr.employee` | Odoo attendance/contract yêu cầu `hr.employee` |
| `hr_attendance_inherit.py` | Phát hiện đi muộn, về sớm, tăng ca | Không có trong `nhan_su` gốc |
| `hr_family.py` | Người phụ thuộc + giảm trừ gia cảnh | Yêu cầu Luật Thuế TNCN VN |
| `bang_cham_cong_thang.py` | Tổng hợp chấm công theo tháng | Không có trong `nhan_su` gốc |
| `bang_luong_thang.py` | Tính lương lũy tiến 7 bậc + BHXH | Không có trong `nhan_su` gốc |
| `bang_luong_line.py` | Chi tiết minh bạch từng khoản lương | Không có trong `nhan_su` gốc |
| `cron_jobs.xml` | 3 cron job tự động hóa end-to-end | Mức 2 - Process Automation |
| `bang_luong_thang.action_phan_tich_ai` | Gemini AI phân tích xu hướng nhân viên | Mức 3 - AI/LLM |
| `external_api/cham_cong_client.py` | XML-RPC client giả lập máy chấm công | Mức 3 - External API |

### 2.3 Cải tiến so với bản gốc
1. **Tích hợp native Odoo**: Dùng `hr.employee`, `hr.attendance`, `hr.contract` thay vì model độc lập
2. **Tính lương lũy tiến**: Thuế TNCN 7 bậc theo Luật số 04/2007/QH12 (sửa đổi 2012)
3. **Kỷ luật tự động**: Phát hiện đi muộn/về sớm, tính tiền phạt theo phút
4. **Tăng ca**: Hệ số 1.5 ngày thường, 2.0 cuối tuần
5. **Người phụ thuộc**: Giảm trừ gia cảnh 11tr/tháng + 4.4tr/NPT
6. **AI phân tích**: Gemini 2.5 Flash đánh giá chuyên cần, hiệu suất, xu hướng
7. **External API**: XML-RPC client kết nối từ máy chấm công vật lý

---

## PHẦN 3: IMPLEMENTATION – Tích hợp và đồng bộ

### 3.1 Xử lý xung đột dữ liệu
- `nhan_vien` (nhan_su) và `hr.employee` (Odoo) là 2 model khác nhau → giải quyết bằng `nhan_vien_extend.py` kế thừa `nhan_vien`, `hr_employee_inherit.py` kế thừa `hr.employee`, hai model cùng tồn tại không xung đột
- Timezone: `hr.attendance` lưu UTC → dùng `context_timestamp()` để chuyển sang giờ VN khi tính đi muộn/về sớm

### 3.2 Chuẩn hóa quy trình nghiệp vụ
```
[Nhân viên chấm công] → hr.attendance (check_in/check_out)
        ↓ (compute tự động)
[Phát hiện vi phạm] → is_late, is_early_leave, is_overtime
        ↓ (Cron Job ngày 1)
[Tạo bảng chấm công] → bang.cham.cong.thang
        ↓ (Cron Job ngày 1)
[Tạo bảng lương] → bang.luong.thang (trạng thái: draft)
        ↓ (Cron Job ngày 5)
[Tính lương tự động] → action_calculate() → bang.luong.line
        ↓ (HR xác nhận)
[Xác nhận & Thanh toán] → trạng thái: confirmed → paid
        ↓ (tùy chọn)
[AI phân tích] → Gemini 2.5 Flash → ai_phan_tich field
```
