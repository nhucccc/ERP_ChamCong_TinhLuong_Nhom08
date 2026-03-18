# GIAI ĐOẠN 0: PHÂN TÍCH NGHIỆP VỤ & THIẾT KẾ KIẾN TRÚC
## Đề tài: Chấm công + Tính lương
### Tự động hóa tính lương: Kết nối hồ sơ nhân sự và dữ liệu công thực tế để tính lương tự động

---

## BƯỚC 1: HỒ SƠ DOANH NGHIỆP GIẢ ĐỊNH

### 1.1. Thông tin công ty

| Hạng mục | Thông tin |
|---|---|
| **Tên công ty** | Công ty TNHH Phần mềm TechSoft Việt Nam |
| **Lĩnh vực** | Công nghệ thông tin - Phát triển phần mềm |
| **Mô hình** | **Mô hình B - Công ty Dịch vụ/Dự án (Service)** |
| **Quy mô** | 50-100 nhân viên |   
| **Địa chỉ** | Hà Nội, Việt Nam |

### 1.2. Lý do chọn Mô hình B

Đề tài **Chấm công + Tính lương** phù hợp nhất với **Mô hình B (Công ty Dịch vụ/Dự án)** vì:
- Nhân viên làm việc theo giờ, tính lương theo ngày công thực tế
- Không bán sản phẩm vật lý, doanh thu từ hợp đồng dịch vụ
- Thách thức cốt lõi là tính lương chính xác từ dữ liệu chấm công

### 1.3. Sơ đồ tổ chức

```
                    BAN GIÁM ĐỐC
                         │
          ┌──────────────┼──────────────┐
          │              │              │
    PHÒNG NHÂN SỰ   PHÒNG KỸ THUẬT   PHÒNG KẾ TOÁN
    (HR Department)  (Tech Dept)      (Accounting)
          │              │              │
    - Quản lý hồ sơ  - Lập trình viên  - Kế toán lương
    - Chấm công      - Tester          - Kế toán thuế
    - Hợp đồng LĐ   - BA/PM           - Báo cáo tài chính
```

---

## BƯỚC 2: PHÂN RÃ CHỨC NĂNG (THE MATRIX)

### 2.1. Bảng phân chia 3 module chính

| Hạng mục | MODULE NHÂN SỰ (`nhan_su`) | MODULE CHẤM CÔNG (`hr_attendance`) | MODULE TÍNH LƯƠNG (`nhan_su_cham_cong_luong`) |
|---|---|---|---|
| **Vai trò** | "Người quản lý hồ sơ" | "Người ghi nhận thời gian" | "Người tính toán tiền lương" |
| **Chức năng chính** | - Quản lý hồ sơ nhân viên | - Ghi nhận check-in/check-out | - Tổng hợp ngày công theo tháng |
| | - Quản lý phòng ban, chức vụ | - Tính giờ làm việc thực tế | - Tính lương theo hợp đồng |
| | - Quản lý hợp đồng lao động | - Quản lý ca làm việc | - Tính phụ cấp, khấu trừ |
| | - Lưu thông tin cá nhân | - Báo cáo chấm công | - Xác nhận và chốt lương |
| **Đầu ra (Output)** | Hồ sơ nhân viên đã duyệt | Bảng chấm công đã xác nhận | Bảng lương đã tính toán |
| **Dữ liệu cung cấp cho module khác** | Thông tin nhân viên (master data) | Số ngày/giờ công thực tế | Phiếu lương để kế toán xử lý |
| **CẤM KỴ** | Không được tự tính lương | Không được tự tính tiền | Không được tự sửa hồ sơ nhân viên |

### 2.2. Nguyên tắc Hard Boundaries của dự án

```
┌─────────────────────────────────────────────────────────────┐
│  MODULE NHÂN SỰ (nhan_su)                                   │
│  ✅ Quản lý: Hồ sơ, phòng ban, hợp đồng, thông tin cá nhân │
│  ❌ CẤM: Tự tính lương, tự ghi chấm công                   │
└─────────────────────────────────────────────────────────────┘
                          │ cung cấp master data
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  MODULE CHẤM CÔNG (hr_attendance)                           │
│  ✅ Quản lý: Check-in/out, giờ làm, ca làm việc             │
│  ❌ CẤM: Tự tính tiền lương, tự sửa hồ sơ nhân viên        │
└─────────────────────────────────────────────────────────────┘
                          │ cung cấp dữ liệu công
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  MODULE TÍNH LƯƠNG (nhan_su_cham_cong_luong)                │
│  ✅ Quản lý: Tổng hợp công, tính lương, phụ cấp, khấu trừ  │
│  ❌ CẤM: Tự sửa hồ sơ nhân viên, tự sửa dữ liệu chấm công │
└─────────────────────────────────────────────────────────────┘
                          │ cung cấp chứng từ lương
                          ▼
                   KẾ TOÁN XỬ LÝ THANH TOÁN
```

---

## BƯỚC 3: THIẾT KẾ LUỒNG DỮ LIỆU (DATA FLOW)

### 3.1. Luồng dữ liệu tổng quan

```
[nhan_su]          [hr_contract]      [hr_attendance]
Hồ sơ nhân viên → Hợp đồng lương  → Dữ liệu chấm công
       │                │                    │
       └────────────────┴────────────────────┘
                        │
                        ▼
            [nhan_su_cham_cong_luong]
            Tổng hợp & Tính lương
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
    Bảng chấm công tháng    Bảng lương tháng
              │                   │
              └─────────┬─────────┘
                        ▼
                 Kế toán xác nhận
                 & Thanh toán lương
```

### 3.2. Luồng nghiệp vụ chi tiết (10 bước)

| Bước | Actor | Hành động | Module | Output |
|---|---|---|---|---|
| 1 | HR | Tạo hồ sơ nhân viên | `nhan_su` | Hồ sơ nhân viên |
| 2 | HR | Ký hợp đồng lao động | `hr_contract` | Hợp đồng với mức lương |
| 3 | Nhân viên | Check-in đầu ngày | `hr_attendance` | Bản ghi check-in |
| 4 | Nhân viên | Check-out cuối ngày | `hr_attendance` | Bản ghi check-out + giờ công |
| 5 | **Hệ thống** | **Tự động tổng hợp chấm công** | `nhan_su_cham_cong_luong` | Bảng chấm công tháng |
| 6 | **Hệ thống** | **Tự động tạo bảng lương** | `nhan_su_cham_cong_luong` | Bảng lương nháp |
| 7 | **Hệ thống** | **Tự động tính lương** (ngày 5) | `nhan_su_cham_cong_luong` | Lương = (CB ÷ 22) × Ngày công |
| 8 | HR | Kiểm tra và xác nhận bảng lương | `nhan_su_cham_cong_luong` | Bảng lương đã duyệt |
| 9 | Kế toán | Nhận chứng từ lương đã duyệt | Kế toán | Phiếu chi lương |
| 10 | Kế toán | Thanh toán lương cho nhân viên | Kế toán | Lương được chuyển khoản |

> **Bước 5, 6, 7 là tự động hóa (MỨC 2)** - Không cần can thiệp thủ công

### 3.3. Công thức tính lương

```
Lương thực nhận = Lương theo ngày công + Phụ cấp - Khấu trừ

Trong đó:
  Lương theo ngày công = (Lương cơ bản ÷ 22 ngày chuẩn) × Số ngày công thực tế
  Phụ cấp             = Phụ cấp ăn trưa + Phụ cấp đi lại + ...
  Khấu trừ            = Bảo hiểm xã hội (8%) + Thuế TNCN + ...
```

---

## BƯỚC 4: KỊCH BẢN NGHIỆP VỤ (USER SCENARIO)

### Câu chuyện: "Tháng lương tháng 1/2026 tại TechSoft"

> **Thứ 2, ngày 02/01/2026 - Đầu tháng mới:**
> Hệ thống tự động kích hoạt **Cron Job 1** lúc 00:00, tạo bảng chấm công tháng 1 cho toàn bộ 50 nhân viên. Đồng thời **Cron Job 2** tạo bảng lương tháng 1 ở trạng thái "Nháp".
>
> **Từ 02/01 đến 31/01/2026 - Trong tháng:**
> Mỗi sáng, **anh Nguyễn Văn An** (Lập trình viên, lương cơ bản 15 triệu) check-in lúc 8:00 và check-out lúc 17:30. Hệ thống `hr_attendance` ghi nhận 9.5 giờ/ngày.
>
> **Thứ 5, ngày 05/01/2026 - Ngày 5 hàng tháng:**
> **Cron Job 3** tự động chạy, tính lương cho tất cả bảng lương đang ở trạng thái "Nháp":
> - Số ngày công của anh An: 3 ngày (02, 03, 04/01)
> - Lương tạm tính: 15,000,000 ÷ 22 × 3 = 2,045,454 VND
>
> **Thứ 2, ngày 03/02/2026 - Đầu tháng 2:**
> **Chị Trần Thị HR** vào hệ thống, kiểm tra bảng chấm công tháng 1 (22 ngày công của anh An), xác nhận bảng lương:
> - Lương theo ngày công: 15,000,000 ÷ 22 × 22 = 15,000,000 VND
> - Phụ cấp ăn trưa: 800,000 VND
> - Khấu trừ BHXH (8%): 1,200,000 VND
> - **Lương thực nhận: 14,600,000 VND**
>
> Chị HR nhấn **"Xác nhận"**, bảng lương chuyển sang trạng thái "Đã duyệt".
>
> **Kế toán** nhận được thông báo, xuất phiếu chi lương và chuyển khoản cho anh An.
>
> **Toàn bộ quy trình hoàn thành mà HR chỉ cần 1 thao tác "Xác nhận" cuối cùng.**

---

## TỔNG KẾT GIAI ĐOẠN 0

### ✅ Checklist hoàn thành

| Yêu cầu | Trạng thái | File tham chiếu |
|---|---|---|
| Chọn mô hình doanh nghiệp (Mô hình B) | ✅ | File này |
| Hồ sơ doanh nghiệp giả định | ✅ | File này |
| Sơ đồ tổ chức phòng ban | ✅ | File này |
| Bảng phân rã chức năng (Matrix) | ✅ | File này |
| Nguyên tắc Hard Boundaries | ✅ | File này |
| Thiết kế luồng dữ liệu | ✅ | File này |
| Kịch bản nghiệp vụ (User Scenario) | ✅ | File này |
| Luồng nghiệp vụ End-to-End (10 bước) | ✅ | `LUONG_NGHIEP_VU_RUT_GON.md` |
| Sơ đồ Swimlane/BPMN | ✅ | `docs/businessflow/` (poster) |

### 🎯 Cam kết nghiệp vụ

- **Module `nhan_su`**: Chỉ quản lý hồ sơ, KHÔNG tính lương
- **Module `hr_attendance`**: Chỉ ghi nhận thời gian, KHÔNG tính tiền
- **Module `nhan_su_cham_cong_luong`**: Chỉ tổng hợp và tính lương, KHÔNG sửa hồ sơ gốc
- **Kế toán**: Chỉ xử lý khi có chứng từ lương đã được HR duyệt

---

*Tài liệu này là đầu ra bắt buộc của Giai đoạn 0 trước khi bắt đầu lập trình.*
*Nhóm 08 - Học phần Thực tập CNTT7 - Trường Đại học Đại Nam*