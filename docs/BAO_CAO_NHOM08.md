# BÁO CÁO BÀI TẬP LỚN
## HỌC PHẦN: THỰC TẬP CNTT7
### HỘI NHẬP VÀ QUẢN TRỊ PHẦN MỀM DOANH NGHIỆP

---

**TRƯỜNG ĐẠI HỌC ĐẠI NAM**
**KHOA CÔNG NGHỆ THÔNG TIN**

**Đề tài: HỆ THỐNG CHẤM CÔNG & TÍNH LƯƠNG**
*Tích hợp với Quản lý Nhân sự trên nền tảng Odoo 15*

**Nhóm thực hiện: Nhóm 08**
**Giảng viên hướng dẫn: ...**
**Năm học: 2024 - 2025**

---

## MỤC LỤC

- Chương 1: Tổng quan đề tài
- Chương 2: Phân tích nghiệp vụ (Giai đoạn 0)
- Chương 3: Thiết kế và cài đặt hệ thống
- Chương 4: Kết quả thực hiện
- Chương 5: Kết luận và hướng phát triển
- Tài liệu tham khảo
- Phụ lục

---

## BẢNG CÁC TỪ VIẾT TẮT

| STT | Từ viết tắt | Viết đầy đủ |
|---|---|---|
| 1 | CSDL | Cơ sở dữ liệu |
| 2 | ERP | Enterprise Resource Planning - Hoạch định nguồn lực doanh nghiệp |
| 3 | HRM | Human Resource Management - Quản lý nhân sự |
| 4 | HR | Human Resources - Nhân sự |
| 5 | API | Application Programming Interface - Giao diện lập trình ứng dụng |
| 6 | AI | Artificial Intelligence - Trí tuệ nhân tạo |
| 7 | LLM | Large Language Model - Mô hình ngôn ngữ lớn |
| 8 | ORM | Object-Relational Mapping - Ánh xạ đối tượng quan hệ |
| 9 | MVC | Model-View-Controller - Mô hình kiến trúc phần mềm |
| 10 | XML | Extensible Markup Language - Ngôn ngữ đánh dấu mở rộng |
| 11 | XML-RPC | XML Remote Procedure Call - Giao thức gọi thủ tục từ xa qua XML |
| 12 | REST | Representational State Transfer - Kiểu kiến trúc dịch vụ web |
| 13 | HTTP | HyperText Transfer Protocol - Giao thức truyền tải siêu văn bản |
| 14 | BHXH | Bảo hiểm xã hội |
| 15 | BHYT | Bảo hiểm y tế |
| 16 | BHTN | Bảo hiểm thất nghiệp |
| 17 | TNCN | Thu nhập cá nhân |
| 18 | GTGC | Giảm trừ gia cảnh |
| 19 | NPT | Người phụ thuộc |
| 20 | TNCT | Thu nhập chịu thuế |
| 21 | TNTT | Thu nhập tính thuế |
| 22 | NV | Nhân viên |
| 23 | CC | Chấm công |
| 24 | CB | Cơ bản |
| 25 | TC | Tăng ca |
| 26 | BTL | Bài tập lớn |
| 27 | FIT-DNU | Faculty of Information Technology - Đại học Đại Nam |
| 28 | UI | User Interface - Giao diện người dùng |
| 29 | CLI | Command Line Interface - Giao diện dòng lệnh |
| 30 | BPMN | Business Process Model and Notation - Ký hiệu mô hình quy trình nghiệp vụ |

---

## CHƯƠNG 1: TỔNG QUAN ĐỀ TÀI

### 1.1. Lý do chọn đề tài

Trong bối cảnh chuyển đổi số ngày càng phổ biến tại các doanh nghiệp Việt Nam, việc quản lý nhân sự, chấm công và tính lương thủ công đang bộc lộ nhiều hạn chế nghiêm trọng: dễ sai sót, tốn thời gian, thiếu minh bạch và khó kiểm soát. Đặc biệt với các doanh nghiệp vừa và nhỏ, bộ phận HR thường phải xử lý hàng chục đến hàng trăm phiếu lương mỗi tháng bằng Excel, dẫn đến nguy cơ nhầm lẫn cao và không đảm bảo tuân thủ quy định pháp luật về thuế thu nhập cá nhân (TNCN) và bảo hiểm xã hội (BHXH).

Theo khảo sát của Hiệp hội Doanh nghiệp Việt Nam năm 2023, hơn 60% doanh nghiệp vừa và nhỏ vẫn đang sử dụng bảng tính Excel để quản lý lương, dẫn đến tỷ lệ sai sót lên đến 15-20% mỗi kỳ lương. Điều này không chỉ gây thiệt hại tài chính mà còn ảnh hưởng đến niềm tin của nhân viên và uy tín doanh nghiệp.

Xuất phát từ thực tế đó, nhóm 08 lựa chọn đề tài **"Hệ thống Chấm công & Tính lương"** với mục tiêu xây dựng một giải pháp ERP hoàn chỉnh trên nền tảng Odoo 15, tích hợp chặt chẽ với module Quản lý Nhân sự (HRM), tự động hóa toàn bộ quy trình từ khi nhân viên chấm công đến khi nhận lương, đồng thời ứng dụng trí tuệ nhân tạo (AI) để hỗ trợ phân tích và ra quyết định nhân sự.

### 1.2. Mục tiêu đề tài

**Mục tiêu tổng quát:**
Xây dựng hệ thống quản lý chấm công và tính lương tự động, tích hợp với module Quản lý Nhân sự có sẵn của Khoa FIT-DNU, vận hành trên nền tảng Odoo 15, đáp ứng đầy đủ 3 mức yêu cầu của bài tập lớn.

**Mục tiêu cụ thể:**
- Tích hợp dữ liệu nhân sự từ module `nhan_su` (master data) với hệ thống chấm công và tính lương, đảm bảo tính nhất quán và không trùng lặp dữ liệu (Mức 1).
- Tự động phát hiện vi phạm kỷ luật (đi muộn, về sớm) và tăng ca từ dữ liệu chấm công thực tế.
- Tự động tính lương theo ngày công, bao gồm: BHXH/BHYT/BHTN, thuế TNCN lũy tiến 7 bậc theo Luật Thuế Việt Nam, tiền phạt kỷ luật và tiền tăng ca (Mức 2).
- Tự động hóa quy trình bằng 3 cron job event-driven, giảm thiểu thao tác thủ công của bộ phận HR (Mức 2).
- Tích hợp Google Gemini AI để phân tích xu hướng nhân viên và hỗ trợ ra quyết định nhân sự (Mức 3).
- Kết nối hệ thống với máy chấm công vật lý qua External API (XML-RPC) (Mức 3).

### 1.3. Phạm vi thực hiện

| Hạng mục | Nội dung |
|---|---|
| Nền tảng | Odoo 15 Community Edition |
| Ngôn ngữ | Python 3.9, XML, JavaScript |
| Cơ sở dữ liệu | PostgreSQL 13 |
| Triển khai | Docker Compose (Windows/Ubuntu) |
| Module kế thừa | `nhan_su` từ kho GitHub FIT-DNU |
| Mức độ hoàn thành | Mức 1 + Mức 2 + Mức 3 (đầy đủ) |

**Phạm vi nghiệp vụ:**
- Quản lý hồ sơ nhân viên mở rộng (thêm CCCD, quê quán, người phụ thuộc)
- Chấm công theo giờ thực tế (check-in/check-out)
- Phát hiện vi phạm kỷ luật và tăng ca tự động
- Tính lương tháng đầy đủ theo quy định pháp luật Việt Nam
- Phân tích AI hỗ trợ quyết định nhân sự
- Kết nối máy chấm công vật lý qua API

**Ngoài phạm vi:**
- Quản lý nghỉ phép (leave management) - chưa tích hợp vào tính lương
- Chuyển khoản ngân hàng tự động
- App di động cho nhân viên

### 1.4. Công nghệ sử dụng

| Công nghệ | Phiên bản | Mục đích sử dụng |
|---|---|---|
| Odoo | 15 Community | Framework ERP, ORM, Web UI |
| Python | 3.9 | Backend, business logic |
| PostgreSQL | 13 | Cơ sở dữ liệu quan hệ |
| Docker & Docker Compose | Latest | Đóng gói và triển khai |
| Google Gemini API | 2.5 Flash | Phân tích AI nhân sự |
| XML-RPC | - | Giao thức External API |
| Git & GitHub | - | Quản lý phiên bản |

### 1.5. Tổng quan về nền tảng Odoo 15

Odoo là một bộ ứng dụng quản trị doanh nghiệp (ERP) mã nguồn mở, được phát triển bởi Odoo S.A. (Bỉ). Phiên bản 15 được phát hành năm 2021 với nhiều cải tiến về hiệu năng và giao diện người dùng.

**Kiến trúc kỹ thuật của Odoo 15:**

Odoo sử dụng kiến trúc MVC (Model-View-Controller) ba tầng:
- **Model (Python):** Định nghĩa cấu trúc dữ liệu và business logic thông qua ORM (Object-Relational Mapping). Mỗi model tương ứng với một bảng trong PostgreSQL.
- **View (XML):** Định nghĩa giao diện người dùng dưới dạng XML, bao gồm form view, tree view, kanban view, search view.
- **Controller (Python):** Xử lý HTTP request, điều phối luồng dữ liệu giữa Model và View.

**Cơ chế kế thừa (Inheritance) trong Odoo:**

Odoo hỗ trợ 3 loại kế thừa:
1. **Classical Inheritance (`_inherit`):** Mở rộng model hiện có, thêm trường và method mới mà không tạo bảng mới.
2. **Prototype Inheritance (`_inherits`):** Tạo model mới kế thừa từ model cha, dùng delegation.
3. **View Inheritance:** Mở rộng view XML hiện có bằng cách thêm/sửa/xóa phần tử.

Trong đề tài này, nhóm sử dụng chủ yếu Classical Inheritance để mở rộng `hr.employee` và `hr.attendance` mà không phá vỡ cấu trúc gốc.

**Hệ thống Cron Job trong Odoo:**

Odoo cung cấp cơ chế Scheduled Actions (ir.cron) cho phép lập lịch chạy tự động các tác vụ. Cron job được định nghĩa trong file XML và có thể cấu hình tần suất (hàng ngày, hàng tuần, hàng tháng) và thời điểm chạy cụ thể.

### 1.6. Tổng quan về hệ thống ERP và bài toán nhân sự

**ERP (Enterprise Resource Planning)** là hệ thống phần mềm tích hợp quản lý toàn bộ hoạt động của doanh nghiệp trên một nền tảng duy nhất, chia sẻ cơ sở dữ liệu chung. Các module ERP điển hình bao gồm: Kế toán, Nhân sự, Kho hàng, Mua hàng, Bán hàng, Sản xuất.

**Bài toán Chấm công & Tính lương trong ERP:**

Trong một hệ thống ERP hoàn chỉnh, module Chấm công & Tính lương đóng vai trò trung tâm kết nối nhiều module khác:
- Nhận dữ liệu nhân viên từ module HRM (Human Resource Management)
- Nhận dữ liệu hợp đồng từ module Contract
- Ghi nhận thời gian làm việc từ thiết bị chấm công hoặc ứng dụng
- Tính toán lương và chuyển dữ liệu sang module Kế toán
- Cung cấp báo cáo cho Ban lãnh đạo

**Lợi ích của hệ thống tự động hóa:**
- Giảm 90% thời gian xử lý lương thủ công
- Loại bỏ sai sót do nhập liệu tay
- Đảm bảo tuân thủ pháp luật (thuế TNCN, BHXH)
- Minh bạch hóa quy trình, tăng niềm tin nhân viên
- Dữ liệu thời gian thực hỗ trợ ra quyết định nhanh

---

## CHƯƠNG 2: PHÂN TÍCH NGHIỆP VỤ (GIAI ĐOẠN 0)

### 2.1. Hồ sơ doanh nghiệp giả định

Để phân tích nghiệp vụ một cách thực tế, nhóm xây dựng kịch bản doanh nghiệp giả định như sau:

| Hạng mục | Thông tin |
|---|---|
| Tên công ty | Công ty TNHH Phần mềm TechSoft Việt Nam |
| Lĩnh vực | Công nghệ thông tin - Phát triển phần mềm |
| Mô hình | Mô hình B - Công ty Dịch vụ/Dự án (Service) |
| Quy mô | 50-100 nhân viên |
| Địa chỉ | Hà Nội, Việt Nam |
| Cơ cấu tổ chức | Ban Giám đốc → Phòng Kỹ thuật, Phòng HR, Phòng Kế toán, Phòng Kinh doanh |

**Lý do chọn Mô hình B (Dịch vụ):**
Đề tài Chấm công & Tính lương phù hợp nhất với mô hình dịch vụ vì:
- Nhân viên làm việc theo giờ, tính lương theo ngày công thực tế
- Không bán sản phẩm vật lý, không cần module kho hàng
- Tăng ca phổ biến trong ngành IT (deadline dự án)
- Cần theo dõi chặt chẽ giờ làm việc để tính chi phí dự án

### 2.2. Sơ đồ tổ chức doanh nghiệp

```
                    BAN GIÁM ĐỐC
                         │
          ┌──────────────┼──────────────┐
          │              │              │
    PHÒNG KỸ THUẬT  PHÒNG HR      PHÒNG KẾ TOÁN
    (Dev, QA, BA)   (Tuyển dụng,  (Lương, Thuế,
                     Đào tạo,      Báo cáo tài
                     Chấm công)    chính)
          │
    PHÒNG KINH DOANH
    (Sales, Marketing)
```

**Vai trò trong hệ thống chấm công - tính lương:**

| Vai trò | Trách nhiệm trong hệ thống |
|---|---|
| Nhân viên | Check-in/check-out hàng ngày, xem phiếu lương |
| Quản lý phòng | Xác nhận bảng chấm công, duyệt tăng ca |
| HR | Quản lý hồ sơ, xác nhận bảng lương, phân tích AI |
| Kế toán | Xác nhận thanh toán, xuất báo cáo thuế |
| Hệ thống | Tự động tạo bảng CC, tính lương, gửi thông báo |

### 2.3. Phân rã chức năng (The Matrix)

Hệ thống được phân chia thành 3 module với ranh giới trách nhiệm rõ ràng, tuân thủ nguyên tắc Single Responsibility:

| Module | Vai trò | Chức năng chính | CẤM KỴ |
|---|---|---|---|
| `nhan_su` | Quản lý hồ sơ | Hồ sơ NV, phòng ban, hợp đồng | Không tự tính lương |
| `hr_attendance` | Ghi nhận thời gian | Check-in/out, giờ công | Không tự tính tiền |
| `nhan_su_cham_cong_luong` | Tính toán lương | Tổng hợp công, tính lương, phụ cấp | Không sửa hồ sơ gốc |

**Nguyên tắc Master Data:**
Module `nhan_su` là nguồn dữ liệu gốc (master data) duy nhất cho thông tin nhân viên. Tất cả các module khác chỉ được đọc (read) dữ liệu từ đây, không được phép tạo bản ghi nhân viên mới hoặc sửa thông tin cơ bản.

### 2.4. Luồng dữ liệu tổng quan

```
[nhan_su]          [hr_contract]      [hr_attendance]
Hồ sơ nhân viên → Hợp đồng lương  → Dữ liệu chấm công
       │                │                    │
       └────────────────┴────────────────────┘
                        ↓
            [nhan_su_cham_cong_luong]
            Tổng hợp & Tính lương
                        │
              ┌─────────┴──────────┐
              ↓                    ↓
    Bảng chấm công tháng    Bảng lương tháng
                                   │
                        ┌──────────┴──────────┐
                        ↓                     ↓
                  Gemini AI              Kế toán xác nhận
                  Phân tích              & Thanh toán
```

### 2.5. Luồng nghiệp vụ End-to-End (10 bước)

Luồng nghiệp vụ chính (happy path) từ khi nhân viên bắt đầu làm việc đến khi nhận lương:

| Bước | Actor | Hành động | Module | Output |
|---|---|---|---|---|
| 1 | HR | Tạo hồ sơ nhân viên | `nhan_su` | Hồ sơ nhân viên |
| 2 | HR | Ký hợp đồng lao động | `hr_contract` | Hợp đồng + mức lương |
| 3 | NV/Máy CC | Check-in đầu ngày (XML-RPC) | `hr_attendance` | Bản ghi check-in |
| 4 | NV/Máy CC | Check-out cuối ngày (XML-RPC) | `hr_attendance` | Giờ công + vi phạm |
| 5 | **Hệ thống** | **Cron Job 1: Tạo bảng chấm công** | Module chính | Bảng CC tháng |
| 6 | **Hệ thống** | **Cron Job 2: Tạo bảng lương** | Module chính | Bảng lương nháp |
| 7 | **Hệ thống** | **Cron Job 3: Tính lương tự động** | Module chính | Lương đã tính |
| 8 | HR | Phân tích AI (Gemini) | Gemini API | Báo cáo phân tích |
| 9 | HR | Xác nhận bảng lương | Module chính | Lương đã duyệt |
| 10 | Kế toán | Thanh toán lương | Module chính | Lương đã trả |

**Ghi chú ngoại lệ:**
- Nếu nhân viên quên check-out: HR có thể nhập thủ công check-out
- Nếu hợp đồng hết hạn: Cron Job bỏ qua nhân viên đó
- Nếu Gemini API lỗi: Hệ thống thông báo lỗi, không ảnh hưởng tính lương

### 2.6. Kịch bản nghiệp vụ chi tiết

**Kịch bản 1: Nhân viên đi làm bình thường**
- 08:25 - Nhân viên check-in → `is_late = False`
- 17:35 - Nhân viên check-out → `is_early_leave = False`, `overtime_minutes = 5` (< 30 phút → không tính tăng ca)
- Kết quả: 1 ngày công đầy đủ, không vi phạm, không tăng ca

**Kịch bản 2: Nhân viên đi muộn và tăng ca**
- 09:00 - Nhân viên check-in → `is_late = True`, `late_minutes = 30`
- 20:00 - Nhân viên check-out → `is_overtime = True`, `overtime_hours = 2.5`
- Kết quả: 1 ngày công, phạt 30 phút × 5.000đ = 150.000đ, tăng ca 2.5h × 1.5 × lương/giờ

**Kịch bản 3: Nhân viên làm cuối tuần**
- Thứ 7, 08:30 check-in, 17:30 check-out → `he_so_tang_ca = 2.0`
- Kết quả: Tăng ca cuối tuần với hệ số 2.0

### 2.7. Audit Code - Kiểm thử module nhan_su gốc (FIT-DNU)

Trước khi phát triển, nhóm tiến hành kiểm thử toàn diện module `nhan_su` từ kho GitHub của Khoa FIT-DNU để xác định những gì có thể kế thừa và những gì cần phát triển mới.

#### 2.7.1. Kết quả Audit Code

| Chức năng | Trạng thái | Ghi chú |
|---|---|---|
| Quản lý hồ sơ nhân viên cơ bản | ✅ Ổn định | Dùng làm master data |
| Phòng ban, chức vụ | ✅ Ổn định | Kế thừa nguyên vẹn |
| Danh sách nhân viên (tree view) | ✅ Ổn định | Giao diện đầy đủ |
| Form nhân viên cơ bản | ✅ Ổn định | Có thể mở rộng |
| Người phụ thuộc giảm trừ gia cảnh | ❌ Thiếu hoàn toàn | Cần xây mới |
| Liên kết hr.attendance | ❌ Thiếu | Cần bridge |
| Liên kết hr.contract | ❌ Thiếu | Cần bridge |
| Logic tính lương | ❌ Không có | Cần xây mới hoàn toàn |
| Phát hiện đi muộn/về sớm | ❌ Không có | Cần xây mới |
| Tăng ca và hệ số | ❌ Không có | Cần xây mới |
| Cron job tự động hóa | ❌ Không có | Cần xây mới |
| Tích hợp AI | ❌ Không có | Cần xây mới |
| External API | ❌ Không có | Cần xây mới |

#### 2.7.2. Gap Analysis - Phân tích sự khác biệt

| Module mới | Mục đích | Loại công việc |
|---|---|---|
| `hr_employee_inherit.py` | Bridge nhan_vien ↔ hr.employee, thêm CCCD, quê quán | Phát triển mới |
| `hr_attendance_inherit.py` | Phát hiện đi muộn, về sớm, tăng ca | Phát triển mới |
| `hr_family.py` | Người phụ thuộc + thuế TNCN lũy tiến 7 bậc | Phát triển mới |
| `bang_cham_cong_thang.py` | Tổng hợp chấm công theo tháng | Phát triển mới |
| `bang_luong_thang.py` | Tính lương + Gemini AI | Phát triển mới |
| `bang_luong_line.py` | Chi tiết minh bạch từng khoản | Phát triển mới |
| `cron_jobs.xml` | 3 cron job tự động hóa | Phát triển mới |
| `cham_cong_client.py` | XML-RPC External API | Phát triển mới |

**Kết luận Gap Analysis:**
Module `nhan_su` gốc chỉ cung cấp nền tảng quản lý hồ sơ cơ bản. Toàn bộ logic nghiệp vụ chấm công, tính lương, tự động hóa và AI đều phải phát triển mới hoàn toàn. Đây là cải tiến thực chất, không phải sao chép thụ động.

---

## CHƯƠNG 3: THIẾT KẾ VÀ CÀI ĐẶT HỆ THỐNG

### 3.1. Kiến trúc hệ thống

Hệ thống được xây dựng theo kiến trúc phân tầng 4 lớp của Odoo 15:

```
┌─────────────────────────────────────────────────────┐
│  TẦNG NGƯỜI DÙNG (User Layer)                       │
│  HR / Kế toán / Nhân viên / Máy chấm công (XML-RPC) │
└──────────────────────┬──────────────────────────────┘
                       ↕ HTTP / XML-RPC / REST
┌──────────────────────────────────────────────────────┐
│  TẦNG FRONTEND (Presentation Layer)                  │
│  Odoo Web UI - JavaScript/XML Views                  │
│  Form View | Tree View | Kanban | Search             │
└──────────────────────┬───────────────────────────────┘
                       ↕ ORM / Python RPC
┌──────────────────────────────────────────────────────┐
│  TẦNG BACKEND (Business Logic Layer)                 │
│  ┌─────────────────┐    ┌──────────────────────────┐ │
│  │ HRM (nhan_su)   │←──→│ nhan_su_cham_cong_luong  │ │
│  │ master data     │    │ + Gemini AI REST API      │ │
│  └─────────────────┘    └──────────────────────────┘ │
│  ┌─────────────────┐    ┌──────────────────────────┐ │
│  │ hr_attendance   │←──→│ hr_contract              │ │
│  │ check-in/out    │    │ wage, date_start/end      │ │
│  └─────────────────┘    └──────────────────────────┘ │
└──────────────────────┬───────────────────────────────┘
                       ↕ SQL / ORM
┌──────────────────────────────────────────────────────┐
│  TẦNG DỮ LIỆU (Data Layer)                          │
│  PostgreSQL 13 - Database: odoo_test                 │
└──────────────────────────────────────────────────────┘
                       ↕ Docker Network
┌──────────────────────────────────────────────────────┐
│  TẦNG TRIỂN KHAI (Infrastructure Layer)              │
│  Docker Compose: odoo-1 | postgres-1 | pgadmin-1     │
└──────────────────────────────────────────────────────┘
```

> 📸 [Hình 3.1: Sơ đồ kiến trúc hệ thống tổng quan]

### 3.2. Cấu trúc module

```
addons/nhan_su_cham_cong_luong/
├── models/
│   ├── __init__.py
│   ├── hr_employee_inherit.py      # Mở rộng hr.employee
│   ├── hr_attendance_inherit.py    # Phát hiện vi phạm & tăng ca
│   ├── hr_family.py                # NPT + thuế TNCN lũy tiến
│   ├── bang_cham_cong_thang.py     # Bảng chấm công tháng
│   ├── bang_luong_thang.py         # Bảng lương + Gemini AI
│   ├── bang_luong_line.py          # Chi tiết phiếu lương
│   └── nhan_vien_extend.py         # Kế thừa model nhan_vien
├── views/
│   ├── hr_employee_inherit_views.xml
│   ├── hr_attendance_inherit_views.xml
│   ├── hr_family_views.xml
│   ├── bang_cham_cong_thang_views.xml
│   ├── bang_luong_thang_views.xml
│   ├── nhan_vien_extend_views.xml
│   └── menu.xml
├── wizard/
│   ├── tao_bang_cham_cong_luong_wizard.py
│   └── tao_bang_cham_cong_luong_wizard_views.xml
├── data/
│   └── cron_jobs.xml
├── security/
│   └── ir.model.access.csv
├── external_api/
│   └── cham_cong_client.py
├── docs/
│   └── businessflow/
├── __init__.py
└── __manifest__.py
```

### 3.3. Thiết kế cơ sở dữ liệu

#### 3.3.1. Sơ đồ quan hệ thực thể (ERD)

```
hr.employee (nhan_su)
    │ id, name, department_id, job_id, ...
    │
    ├──[1:N]── hr.attendance
    │           id, employee_id, check_in, check_out
    │           is_late, late_minutes, is_early_leave
    │           is_overtime, overtime_hours, he_so_tang_ca
    │
    ├──[1:N]── hr.contract
    │           id, employee_id, wage, date_start, date_end, state
    │
    ├──[1:N]── hr.family.member
    │           id, employee_id, ho_ten, quan_he, ngay_sinh
    │           da_dang_ky, ngay_bat_dau, ngay_ket_thuc
    │
    ├──[1:N]── bang.cham.cong.thang
    │           id, employee_id, thang, nam
    │           so_ngay_lam_viec, tong_gio_lam_viec
    │           so_ngay_cong_chuan, trang_thai
    │
    └──[1:N]── bang.luong.thang
                id, employee_id, thang, nam
                bang_cham_cong_id, hr_contract_id
                luong_co_ban, luong_thuc_lanh
                thue_tncn, tien_bao_hiem
                ai_phan_tich, trang_thai
                    │
                    └──[1:N]── bang.luong.line
                                id, bang_luong_id
                                name, loai, so_tien, sequence
```

#### 3.3.2. Model bang.cham.cong.thang

| Trường | Kiểu dữ liệu | Ràng buộc | Mô tả |
|---|---|---|---|
| employee_id | Many2one(hr.employee) | required, ondelete=cascade | Nhân viên |
| thang | Integer | required | Tháng (1-12) |
| nam | Integer | required | Năm |
| so_ngay_lam_viec | Integer | computed | Số ngày có chấm công thực tế |
| tong_gio_lam_viec | Float | computed | Tổng giờ làm việc |
| so_ngay_cong_chuan | Integer | computed | Số ngày chuẩn (trừ Chủ nhật) |
| trang_thai | Selection | default=draft | draft/confirmed/locked |

**Ràng buộc duy nhất:** `unique(employee_id, thang, nam)` - Mỗi nhân viên chỉ có 1 bảng CC/tháng.

#### 3.3.3. Model bang.luong.thang

| Trường | Kiểu dữ liệu | Mô tả |
|---|---|---|
| employee_id | Many2one(hr.employee) | Nhân viên |
| hr_contract_id | Many2one(hr.contract) | Hợp đồng lao động (tự động tìm) |
| luong_co_ban | Monetary | Lương cơ bản từ hợp đồng |
| luong_theo_gio | Monetary | Lương CB / (ngày chuẩn × 8h) |
| so_lan_vi_pham | Integer | Số lần đi muộn/về sớm |
| tong_phut_vi_pham | Integer | Tổng phút vi phạm |
| tien_phat_ky_luat | Monetary | Phút vi phạm × 5.000đ/phút |
| tong_gio_tang_ca_thuong | Float | Giờ tăng ca ngày thường |
| tong_gio_tang_ca_cuoi_tuan | Float | Giờ tăng ca cuối tuần |
| tien_tang_ca | Monetary | (TC thường×1.5 + TC CT×2.0) × lương/giờ |
| tien_bao_hiem | Monetary | Lương CB × 10.5% |
| so_nguoi_phu_thuoc | Integer | Số NPT đã đăng ký còn hiệu lực |
| tong_giam_tru_gia_canh | Monetary | 11tr + NPT × 4.4tr |
| thu_nhap_tinh_thue | Monetary | TNCT - GTGC |
| thue_tncn | Monetary | Thuế TNCN lũy tiến 7 bậc |
| luong_thuc_lanh | Monetary | Tổng thu nhập - Khấu trừ |
| ai_phan_tich | Text | Kết quả phân tích từ Gemini AI |
| trang_thai | Selection | draft/calculated/confirmed/paid |

#### 3.3.4. Model hr.attendance (mở rộng)

| Trường mới | Kiểu | Mô tả |
|---|---|---|
| is_late | Boolean | Đi muộn (check-in sau 08:30) |
| late_minutes | Integer | Số phút đi muộn |
| is_early_leave | Boolean | Về sớm (check-out trước 17:30) |
| early_leave_minutes | Integer | Số phút về sớm |
| is_overtime | Boolean | Có tăng ca (≥30 phút sau 17:30) |
| overtime_hours | Float | Số giờ tăng ca |
| he_so_tang_ca | Float | 1.5 ngày thường / 2.0 cuối tuần |
| tong_phut_vi_pham | Integer | late_minutes + early_leave_minutes |

### 3.4. Mô tả chi tiết các Model chính

#### 3.4.1. Model hr_attendance_inherit.py - Phát hiện vi phạm kỷ luật

Đây là model quan trọng nhất trong giai đoạn 1, chịu trách nhiệm phát hiện tự động các vi phạm kỷ luật và tăng ca từ dữ liệu check-in/check-out thô.

**Cấu hình giờ làm việc chuẩn:**
```python
GIO_LAM_CHUAN = {
    'bat_dau': (8, 30),   # 08:30 - giờ bắt đầu
    'ket_thuc': (17, 30), # 17:30 - giờ kết thúc
    'so_gio_chuan': 8.0,  # 8 tiếng/ngày
}
TANG_CA_TOI_THIEU_PHUT = 30  # Tối thiểu 30 phút mới tính tăng ca
```

**Method `_compute_ky_luat` - Tính vi phạm kỷ luật:**
```python
@api.depends('check_in', 'check_out')
def _compute_ky_luat(self):
    for rec in self:
        # Chuyển UTC -> giờ địa phương (quan trọng!)
        ci_local = fields.Datetime.context_timestamp(rec, rec.check_in)
        phut_ci = ci_local.hour * 60 + ci_local.minute

        # Đi muộn: check-in sau 08:30
        if phut_ci > 8 * 60 + 30:
            rec.is_late = True
            rec.late_minutes = phut_ci - (8 * 60 + 30)

        # Về sớm: check-out trước 17:30
        co_local = fields.Datetime.context_timestamp(rec, rec.check_out)
        phut_co = co_local.hour * 60 + co_local.minute
        if phut_co < 17 * 60 + 30:
            rec.is_early_leave = True
            rec.early_leave_minutes = (17 * 60 + 30) - phut_co
```

**Lưu ý kỹ thuật quan trọng:** Odoo lưu tất cả datetime trong database theo UTC. Khi so sánh giờ làm việc, bắt buộc phải dùng `context_timestamp()` để chuyển về giờ địa phương (UTC+7 tại Việt Nam), tránh sai lệch 7 tiếng.

**Method `_compute_tang_ca` - Tính tăng ca:**
```python
@api.depends('check_in', 'check_out')
def _compute_tang_ca(self):
    for rec in self:
        co_local = fields.Datetime.context_timestamp(rec, rec.check_out)
        phut_co = co_local.hour * 60 + co_local.minute
        phut_tang_ca = max(0, phut_co - (17 * 60 + 30))

        if phut_tang_ca >= 30:  # Tối thiểu 30 phút
            rec.is_overtime = True
            rec.overtime_hours = round(phut_tang_ca / 60.0, 2)
            # Cuối tuần: weekday() >= 5 (Thứ 7=5, CN=6)
            rec.he_so_tang_ca = 2.0 if co_local.weekday() >= 5 else 1.5
```

#### 3.4.2. Model hr_family.py - Người phụ thuộc và thuế TNCN

Model này quản lý danh sách người phụ thuộc (NPT) của nhân viên để tính giảm trừ gia cảnh, đồng thời cung cấp hàm tính thuế TNCN lũy tiến 7 bậc.

**Hằng số giảm trừ gia cảnh (theo Nghị quyết 954/2020/UBTVQH14):**
```python
GTGC_BAN_THAN = 11_000_000       # 11 triệu/tháng
GTGC_NGUOI_PHU_THUOC = 4_400_000 # 4.4 triệu/NPT/tháng
```

**Hàm tính thuế TNCN lũy tiến 7 bậc:**
```python
BIEU_THUE_TNCN = [
    (5_000_000,  0.05),   # Bậc 1: đến 5tr - 5%
    (10_000_000, 0.10),   # Bậc 2: 5-10tr - 10%
    (18_000_000, 0.15),   # Bậc 3: 10-18tr - 15%
    (32_000_000, 0.20),   # Bậc 4: 18-32tr - 20%
    (52_000_000, 0.25),   # Bậc 5: 32-52tr - 25%
    (80_000_000, 0.30),   # Bậc 6: 52-80tr - 30%
    (float('inf'), 0.35), # Bậc 7: trên 80tr - 35%
]

def tinh_thue_tncn(thu_nhap_tinh_thue):
    thue = 0.0
    nguong_truoc = 0
    for nguong, ty_le in BIEU_THUE_TNCN:
        if thu_nhap_tinh_thue <= nguong_truoc:
            break
        phan_chiu_thue = min(thu_nhap_tinh_thue, nguong) - nguong_truoc
        thue += phan_chiu_thue * ty_le
        nguong_truoc = nguong
    return thue
```

**Ví dụ tính thuế TNCN:**
- Thu nhập tính thuế: 20.000.000đ
- Bậc 1: 5.000.000 × 5% = 250.000đ
- Bậc 2: 5.000.000 × 10% = 500.000đ
- Bậc 3: 8.000.000 × 15% = 1.200.000đ (10tr → 18tr, chỉ lấy đến 20tr)
- **Tổng thuế: 1.950.000đ**

#### 3.4.3. Model bang_luong_thang.py - Tính lương tổng hợp

Đây là model trung tâm của toàn bộ hệ thống, tổng hợp dữ liệu từ tất cả các model khác để tính lương thực lãnh.

**Công thức tính lương đầy đủ:**
```
Lương thực lãnh =
    Lương theo ngày công          [+]
  + Tiền tăng ca                  [+]
  + Phụ cấp khác                  [+]
  - Tiền phạt kỷ luật             [-]
  - BHXH/BHYT/BHTN (10.5%)        [-]
  - Thuế TNCN lũy tiến            [-]
  - Khấu trừ khác                 [-]

Trong đó:
  Lương theo ngày công = Lương CB × (Ngày làm / Ngày chuẩn)
  Tiền tăng ca = (TC thường × 1.5 + TC cuối tuần × 2.0) × Lương/giờ
  Lương/giờ = Lương CB / (Ngày chuẩn × 8 giờ)
  Tiền phạt = Tổng phút vi phạm × 5.000 VND/phút
  BHXH/BHYT/BHTN = Lương CB × 10.5%
  GTGC = 11.000.000 + NPT × 4.400.000
  Thu nhập tính thuế = (Tổng thu nhập - BHXH) - GTGC
```

**Method `action_calculate` - Tính lương và sinh chi tiết:**

Khi HR hoặc Cron Job gọi `action_calculate()`, hệ thống:
1. Xóa toàn bộ dòng chi tiết cũ (`line_ids.unlink()`)
2. Tính toán lại tất cả các khoản
3. Tạo các dòng chi tiết minh bạch (One2many `bang.luong.line`)
4. Chuyển trạng thái sang `calculated`

Mỗi dòng chi tiết ghi rõ công thức tính, ví dụ:
- `"Lương cơ bản theo ngày công (22/26 ngày = 84.6%)"`
- `"Tăng ca ngày thường (5.00h × 1.5 × 72,115đ/h)"`
- `"Thuế TNCN lũy tiến (TNTT: 8,500,000đ, GTGC: 11,000,000đ, 0 NPT)"`

### 3.5. Công thức tính lương chi tiết

**Bảng thuế TNCN lũy tiến 7 bậc (theo Luật số 04/2007/QH12, sửa đổi 2012):**

| Bậc | Thu nhập tính thuế/tháng | Thuế suất | Thuế tối đa bậc này |
|---|---|---|---|
| 1 | Đến 5 triệu | 5% | 250.000đ |
| 2 | 5 - 10 triệu | 10% | 500.000đ |
| 3 | 10 - 18 triệu | 15% | 1.200.000đ |
| 4 | 18 - 32 triệu | 20% | 2.800.000đ |
| 5 | 32 - 52 triệu | 25% | 5.000.000đ |
| 6 | 52 - 80 triệu | 30% | 8.400.000đ |
| 7 | Trên 80 triệu | 35% | Không giới hạn |

**Tỷ lệ đóng BHXH/BHYT/BHTN (phần nhân viên đóng):**

| Loại bảo hiểm | Tỷ lệ NV đóng | Căn cứ pháp lý |
|---|---|---|
| BHXH | 8% | Nghị định 58/2020/NĐ-CP |
| BHYT | 1.5% | Luật BHYT 2008 |
| BHTN | 1% | Luật Việc làm 2013 |
| **Tổng** | **10.5%** | |

### 3.6. Tự động hóa quy trình - 3 Cron Job (Mức 2)

Hệ thống triển khai 3 Scheduled Actions (ir.cron) trong file `data/cron_jobs.xml`:

#### Cron Job 1: Tạo bảng chấm công tháng mới
```xml
<record id="cron_tao_bang_cham_cong" model="ir.cron">
    <field name="name">Tạo bảng chấm công tháng mới</field>
    <field name="model_id" ref="model_bang_cham_cong_thang"/>
    <field name="code">model.tao_bang_cham_cong_thang()</field>
    <field name="interval_number">1</field>
    <field name="interval_type">months</field>
    <field name="nextcall">2026-01-01 00:00:00</field>
</record>
```
- **Thời gian:** Ngày 1 hàng tháng lúc 00:00
- **Chức năng:** Tự động tạo bản ghi `bang.cham.cong.thang` cho tất cả nhân viên đang có hợp đồng active

#### Cron Job 2: Tạo bảng lương tháng mới
- **Thời gian:** Ngày 1 hàng tháng lúc 00:00
- **Chức năng:** Tự động tạo bản ghi `bang.luong.thang` cho tất cả nhân viên, liên kết với bảng chấm công và hợp đồng tương ứng

#### Cron Job 3: Tính lương tự động ngày 5
- **Thời gian:** Ngày 5 hàng tháng lúc 01:00
- **Chức năng:** Tự động gọi `action_calculate()` cho tất cả bảng lương đang ở trạng thái "Nháp" trong tháng hiện tại
- **Lý do chọn ngày 5:** Đảm bảo đủ dữ liệu chấm công tháng trước (nhân viên có thể check-out muộn ngày cuối tháng)

**Luồng tự động hóa hoàn chỉnh:**
```
Ngày 1/tháng 00:00
    → Cron 1: Tạo bang.cham.cong.thang (trạng thái: draft)
    → Cron 2: Tạo bang.luong.thang (trạng thái: draft)

Ngày 1-4/tháng
    → Nhân viên tiếp tục check-in/out
    → Dữ liệu hr.attendance cập nhật liên tục

Ngày 5/tháng 01:00
    → Cron 3: Tính lương tự động (trạng thái: calculated)

Ngày 5-10/tháng
    → HR xem xét, phân tích AI
    → HR xác nhận (trạng thái: confirmed)

Ngày 10-15/tháng
    → Kế toán thanh toán (trạng thái: paid)
```

### 3.7. Tích hợp AI - Google Gemini (Mức 3)

#### 3.7.1. Tổng quan tính năng

Tính năng "🤖 Phân tích AI" được tích hợp trực tiếp vào form bảng lương tháng. Khi HR nhấn nút, hệ thống gọi Google Gemini 2.5 Flash API để phân tích dữ liệu lương và trả về báo cáo phân tích nhân sự 4 chiều.

**Lý do chọn Gemini 2.5 Flash:**
- Miễn phí với quota hợp lý cho môi trường học thuật
- Hỗ trợ tiếng Việt tốt
- Tốc độ phản hồi nhanh (Flash model)
- Không cần cài thư viện ngoài, dùng `requests` có sẵn trong Odoo

#### 3.7.2. Luồng xử lý AI

```
[HR nhấn nút "🤖 Phân tích AI"]
        ↓
[Kiểm tra API Key trong System Parameters]
        ↓
[Thu thập dữ liệu bảng lương hiện tại]
  - Tên nhân viên, phòng ban
  - Số ngày công, tỷ lệ công
  - Vi phạm kỷ luật (số lần, số phút, tiền phạt)
  - Tăng ca (giờ thường, giờ cuối tuần, tiền)
  - Lương cơ bản, BHXH, thuế, thực lãnh
        ↓
[Truy vấn lịch sử 3 tháng gần nhất]
        ↓
[Tạo prompt tiếng Việt có cấu trúc]
        ↓
[POST đến Gemini REST API]
  URL: /v1beta/models/gemini-2.5-flash:generateContent
  Timeout: 30 giây
        ↓
[Nhận và parse JSON response]
  data['candidates'][0]['content']['parts'][0]['text']
        ↓
[Lưu vào field ai_phan_tich]
[Hiển thị trên form view]
```

> 📸 [Hình 3.2: Giao diện nút Phân tích AI và kết quả hiển thị trên form bảng lương]

#### 3.7.3. Cấu trúc Prompt

```python
prompt = f"""Bạn là chuyên gia phân tích nhân sự. Phân tích dữ liệu lương
sau bằng tiếng Việt, ngắn gọn.

BẢNG LƯƠNG THÁNG {thang:02d}/{nam} - {employee_name}
Phòng ban: {department}

CHẤM CÔNG: {so_ngay_lam_viec}/{so_ngay_cong_chuan} ngày ({ty_le_cong:.1f}%)
KỶ LUẬT: {so_lan_vi_pham} lần vi phạm, {tong_phut_vi_pham} phút
TĂNG CA: {gio_thuong:.1f}h thường + {gio_cuoi_tuan:.1f}h cuối tuần
LƯƠNG: CB={luong_co_ban:,.0f}đ | BHXH={tien_bao_hiem:,.0f}đ
       Thuế={thue_tncn:,.0f}đ | THỰC LÃNH={luong_thuc_lanh:,.0f}đ

{lich_su_3_thang}

Phân tích theo 4 mục (mỗi mục 2-3 câu):
1. ĐÁNH GIÁ CHUYÊN CẦN
2. ĐÁNH GIÁ HIỆU SUẤT
3. XU HƯỚNG SO SÁNH (nếu có lịch sử)
4. ĐỀ XUẤT CHO HR"""
```

#### 3.7.4. Cấu hình bảo mật API Key

API Key được lưu an toàn trong System Parameters của Odoo, không hardcode trong source code:
- **Key:** `nhan_su_cham_cong_luong.gemini_api_key`
- **Truy cập:** Settings → Technical → Parameters → System Parameters
- **Lấy API Key miễn phí:** https://aistudio.google.com/app/apikey

### 3.8. External API - Kết nối máy chấm công (Mức 3)

#### 3.8.1. Tổng quan

File `external_api/cham_cong_client.py` là script Python giả lập máy chấm công vật lý, kết nối với Odoo qua giao thức XML-RPC theo tài liệu chính thức của Odoo 15. Đây là minh chứng cho khả năng tích hợp hệ thống với thiết bị phần cứng thực tế.

#### 3.8.2. Cơ chế xác thực XML-RPC

```python
import xmlrpc.client

# Bước 1: Kết nối endpoint xác thực
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

# Bước 2: Kết nối endpoint thực thi
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# Bước 3: Gọi method của model
result = models.execute_kw(
    db, uid, password,
    'hr.attendance',    # model name
    'create',           # method name
    [{'employee_id': emp_id, 'check_in': datetime_str}]
)
```

#### 3.8.3. Các chức năng CLI

| Lệnh | Chức năng | Ví dụ |
|---|---|---|
| `--list` | Liệt kê nhân viên từ Odoo | `python cham_cong_client.py --list` |
| `--checkin [ID]` | Tạo bản ghi check-in | `python cham_cong_client.py --checkin 3` |
| `--checkout [ID]` | Cập nhật check-out | `python cham_cong_client.py --checkout 3` |
| (mặc định) | Demo đầy đủ tự động | `python cham_cong_client.py` |

#### 3.8.4. Ứng dụng thực tế

Trong môi trường doanh nghiệp thực tế, script này có thể được tích hợp vào:
- Máy chấm công vân tay (fingerprint scanner)
- Máy chấm công thẻ từ (RFID card reader)
- Ứng dụng di động check-in bằng QR code
- Hệ thống camera nhận diện khuôn mặt

### 3.9. Giao diện người dùng

#### 3.9.1. Menu hệ thống

Hệ thống cung cấp menu đầy đủ trong Odoo:
```
Chấm Công & Lương
├── Chấm Công
│   ├── Bảng Chấm Công Tháng
│   └── Chi Tiết Chấm Công (hr.attendance)
├── Bảng Lương
│   ├── Bảng Lương Tháng
│   └── Tạo Bảng Lương (Wizard)
├── Nhân Viên
│   ├── Danh Sách Nhân Viên
│   └── Người Phụ Thuộc
└── Cấu Hình
    └── System Parameters (API Key)
```

> 📸 [Hình 3.3: Giao diện menu hệ thống Chấm Công & Lương trong Odoo]

#### 3.9.2. Giao diện bảng lương tháng

Form view bảng lương được thiết kế theo nhóm thông tin rõ ràng:
- **Nhóm 1:** Thông tin cơ bản (nhân viên, tháng, năm, trạng thái)
- **Nhóm 2:** Dữ liệu chấm công (ngày công, tỷ lệ, giờ làm)
- **Nhóm 3:** Kỷ luật và tăng ca (vi phạm, tiền phạt, tăng ca)
- **Nhóm 4:** Tính lương (lương CB, BHXH, thuế, thực lãnh)
- **Nhóm 5:** Chi tiết phiếu lương (One2many lines)
- **Nhóm 6:** Phân tích AI (kết quả Gemini)

> 📸 [Hình 3.4: Form view bảng lương tháng với đầy đủ các khoản tính toán]

> 📸 [Hình 3.5: Tab chi tiết phiếu lương - hiển thị từng khoản cộng/trừ minh bạch]

---

## CHƯƠNG 4: KẾT QUẢ THỰC HIỆN

### 4.1. Kết quả theo thang đánh giá BTL

#### 4.1.1. Mức 1 - Tích hợp hệ thống ✅

**Yêu cầu:** Đảm bảo tính nhất quán dữ liệu, module HRM là master data.

**Kết quả đạt được:**
- Module `nhan_su` của Khoa FIT-DNU là master data duy nhất, không có nhập liệu trùng lặp
- `bang.cham.cong.thang` và `bang.luong.thang` đều dùng `hr.employee` làm khóa ngoại bắt buộc (`required=True`)
- `hr.contract` cung cấp lương cơ bản, `hr.attendance` cung cấp ngày công thực tế
- `nhan_vien_extend.py` kế thừa model `nhan_vien` gốc bằng `_inherit`, bổ sung thống kê chấm công/lương mà không phá vỡ cấu trúc gốc
- Không có bất kỳ dữ liệu hardcode nào - tất cả đều truy xuất từ database

**Minh chứng kỹ thuật:**
```python
# bang_luong_thang.py - Dữ liệu lấy từ hr.contract, không hardcode
@api.depends('employee_id', 'thang', 'nam')
def _compute_hr_contract_id(self):
    for rec in self:
        contract = self.env['hr.contract'].search([
            ('employee_id', '=', rec.employee_id.id),
            ('state', '=', 'open'),
            ('date_start', '<=', ngay_cuoi),
        ], limit=1)
        rec.hr_contract_id = contract
```

#### 4.1.2. Mức 2 - Tự động hóa quy trình ✅

**Yêu cầu:** Hệ thống tự động thực thi tác vụ dựa trên sự kiện (event-driven).

**Kết quả đạt được:**
- 3 Cron Job hoạt động hoàn toàn tự động, không cần can thiệp thủ công
- **Cron 1 & 2** (ngày 1/tháng): Tạo bảng chấm công và bảng lương cho toàn bộ nhân viên có hợp đồng active
- **Cron 3** (ngày 5/tháng): Tính lương tự động với đầy đủ các khoản: ngày công, tăng ca, phạt kỷ luật, BHXH, thuế TNCN lũy tiến 7 bậc, giảm trừ gia cảnh theo số NPT
- Phát hiện tự động đi muộn (sau 08:30), về sớm (trước 17:30), tăng ca (≥30 phút sau 17:30) với hệ số 1.5/2.0

**So sánh trước và sau khi có hệ thống:**

| Công việc | Trước (thủ công) | Sau (tự động) | Tiết kiệm |
|---|---|---|---|
| Tạo bảng chấm công | 30 phút/tháng | 0 phút (tự động) | 100% |
| Tính lương 50 NV | 8 giờ/tháng | 5 phút (tự động) | 97% |
| Kiểm tra vi phạm | 2 giờ/tháng | 0 phút (tự động) | 100% |
| Tính thuế TNCN | 3 giờ/tháng | 0 phút (tự động) | 100% |
| **Tổng** | **~13 giờ/tháng** | **~5 phút/tháng** | **~96%** |

#### 4.1.3. Mức 3 - AI & External API ✅

**Yêu cầu:** Tích hợp AI/LLM và kết nối External API.

**Kết quả đạt được:**

*Google Gemini AI:*
- Tích hợp thành công Gemini 2.5 Flash qua REST API
- Phân tích 4 chiều: chuyên cần, hiệu suất, xu hướng 3 tháng, đề xuất HR
- Không cần cài thư viện ngoài, dùng `requests` có sẵn trong Odoo
- API Key lưu an toàn trong System Parameters, không hardcode

*External API XML-RPC:*
- Script `cham_cong_client.py` kết nối thành công với Odoo
- Hỗ trợ check-in/check-out/đọc bảng lương qua CLI
- Giả lập đầy đủ luồng máy chấm công vật lý

### 4.2. Danh sách chức năng hoàn thành

| STT | Chức năng | Mức | Trạng thái |
|---|---|---|---|
| 1 | Quản lý hồ sơ nhân viên mở rộng (CCCD, quê quán) | 1 | ✅ |
| 2 | Quản lý người phụ thuộc giảm trừ gia cảnh | 1 | ✅ |
| 3 | Phát hiện đi muộn, về sớm từ hr.attendance | 1 | ✅ |
| 4 | Phát hiện và tính tiền tăng ca (hệ số 1.5/2.0) | 2 | ✅ |
| 5 | Bảng chấm công tháng tự động tổng hợp | 1 | ✅ |
| 6 | Bảng lương tháng với đầy đủ các khoản | 1 | ✅ |
| 7 | Tính BHXH/BHYT/BHTN (10.5% lương CB) | 1 | ✅ |
| 8 | Tính thuế TNCN lũy tiến 7 bậc | 1 | ✅ |
| 9 | Giảm trừ gia cảnh theo số NPT | 1 | ✅ |
| 10 | Chi tiết phiếu lương minh bạch (One2many lines) | 1 | ✅ |
| 11 | Wizard tạo bảng hàng loạt theo tháng | 2 | ✅ |
| 12 | Cron Job 1: Tạo bảng chấm công tự động | 2 | ✅ |
| 13 | Cron Job 2: Tạo bảng lương tự động | 2 | ✅ |
| 14 | Cron Job 3: Tính lương tự động ngày 5 | 2 | ✅ |
| 15 | Phân tích AI bằng Google Gemini 2.5 Flash | 3 | ✅ |
| 16 | External API XML-RPC giả lập máy chấm công | 3 | ✅ |
| 17 | Giao diện đầy đủ: tree, form, search, menu | 1 | ✅ |
| 18 | Phân quyền truy cập (ir.model.access.csv) | 1 | ✅ |
| 19 | BusinessFlow sơ đồ BPMN/Swimlane (PlantUML) | - | ✅ |
| 20 | Audit Code & Gap Analysis documentation | - | ✅ |

### 4.3. Kịch bản demo thực tế

**Kịch bản: Tháng lương tháng 3/2026 tại TechSoft**

*Dữ liệu nhân viên:*
- Nhân viên: Nguyễn Văn An, Phòng Kỹ thuật
- Lương cơ bản: 15.000.000đ/tháng
- Số NPT: 1 người (con nhỏ dưới 18 tuổi)
- Tháng 3/2026: 26 ngày chuẩn (trừ Chủ nhật)

*Diễn biến tháng 3:*
- 22 ngày làm việc thực tế (nghỉ 4 ngày phép)
- 2 lần đi muộn: 15 phút + 15 phút = 30 phút vi phạm
- 5 giờ tăng ca ngày thường (deadline dự án)
- 0 giờ tăng ca cuối tuần

*Tính lương tự động (Cron Job 3, ngày 05/03/2026):*

| Khoản mục | Tính toán | Số tiền |
|---|---|---|
| Lương theo ngày công | 15.000.000 × (22/26) | +12.692.308đ |
| Tiền tăng ca | 5h × 1.5 × (15.000.000/208h) | +541.827đ |
| Tiền phạt kỷ luật | 30 phút × 5.000đ | -150.000đ |
| BHXH/BHYT/BHTN | 15.000.000 × 10.5% | -1.575.000đ |
| Giảm trừ gia cảnh | 11.000.000 + 1 × 4.400.000 | 15.400.000đ |
| Thu nhập tính thuế | (12.692.308 + 541.827 - 150.000 - 1.575.000) - 15.400.000 | 0đ (âm → 0) |
| Thuế TNCN | 0đ (dưới ngưỡng chịu thuế) | 0đ |
| **Lương thực lãnh** | | **11.509.135đ** |

*Phân tích AI (Gemini 2.5 Flash):*
```
1. ĐÁNH GIÁ CHUYÊN CẦN: Nhân viên đạt 84.6% ngày công tháng này,
   có 2 lần đi muộn nhưng tổng thời gian vi phạm chỉ 30 phút - mức
   chấp nhận được. Cần nhắc nhở nhẹ về giờ giấc.

2. ĐÁNH GIÁ HIỆU SUẤT: Có 5 giờ tăng ca cho thấy tinh thần trách
   nhiệm với công việc. Tuy nhiên cần theo dõi xem tăng ca có phải
   do quản lý thời gian kém hay do khối lượng công việc quá tải.

3. XU HƯỚNG: Đây là tháng đầu tiên có dữ liệu, chưa đủ để so sánh
   xu hướng. Cần theo dõi thêm 2-3 tháng tiếp theo.

4. ĐỀ XUẤT CHO HR: Xem xét điều chỉnh deadline dự án để giảm tăng
   ca. Ghi nhận tinh thần làm việc tốt, có thể xem xét khen thưởng
   cuối quý nếu duy trì hiệu suất.
```

### 4.4. Môi trường triển khai

**Cấu hình Docker Compose:**
```yaml
version: '3.8'
services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: odoo_test
      POSTGRES_USER: odoo
      POSTGRES_PASSWORD: odoo
    ports: ["5432:5432"]

  odoo:
    image: odoo:15
    depends_on: [db]
    ports: ["8069:8069"]
    volumes:
      - ./addons:/mnt/extra-addons
      - odoo-data:/var/lib/odoo
    environment:
      HOST: db
      USER: odoo
      PASSWORD: odoo

  pgadmin:
    image: dpage/pgadmin4
    ports: ["5050:80"]
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.com
      PGADMIN_DEFAULT_PASSWORD: admin
```

**Thông tin truy cập:**
- Odoo Web: http://localhost:8069
- pgAdmin: http://localhost:5050
- Database: `odoo_test` | User: `admin` | Password: `admin`
- Container Odoo: `erp_chamcong_tinhluong_nhom08-odoo-1`

**Lệnh migrate module:**
```bash
docker exec erp_chamcong_tinhluong_nhom08-odoo-1 \
  odoo -c /etc/odoo/odoo.conf \
  -u nhan_su_cham_cong_luong \
  -d odoo_test \
  --stop-after-init
```

> 📸 [Hình 4.1: Giao diện danh sách bảng lương tháng (tree view) với trạng thái các phiếu]

> 📸 [Hình 4.2: Màn hình chấm công - danh sách check-in/check-out với cột đi muộn/tăng ca]

> 📸 [Hình 4.3: Kết quả phân tích AI Gemini hiển thị trên form bảng lương]

### 4.5. Kiểm thử hệ thống

#### 4.5.1. Kiểm thử tính năng cốt lõi

| Test Case | Input | Expected Output | Kết quả |
|---|---|---|---|
| Đi muộn 30 phút | Check-in 09:00 | is_late=True, late_minutes=30 | ✅ Pass |
| Về sớm 60 phút | Check-out 16:30 | is_early_leave=True, early_leave_minutes=60 | ✅ Pass |
| Tăng ca 2h ngày thường | Check-out 19:30 | is_overtime=True, overtime_hours=2.0, he_so=1.5 | ✅ Pass |
| Tăng ca cuối tuần | Check-out 19:30 Thứ 7 | he_so_tang_ca=2.0 | ✅ Pass |
| Tăng ca < 30 phút | Check-out 17:50 | is_overtime=False | ✅ Pass |
| Thuế TNCN bậc 1 | TNTT = 3.000.000đ | Thuế = 150.000đ | ✅ Pass |
| Thuế TNCN nhiều bậc | TNTT = 20.000.000đ | Thuế = 1.950.000đ | ✅ Pass |
| Dưới ngưỡng chịu thuế | TNTT ≤ 0 | Thuế = 0đ | ✅ Pass |
| Cron Job tạo bảng | Chạy ngày 1 | Tạo bảng cho tất cả NV | ✅ Pass |
| Gemini API | Nhấn nút AI | Trả về phân tích tiếng Việt | ✅ Pass |

#### 4.5.2. Kiểm thử tích hợp

| Kịch bản | Mô tả | Kết quả |
|---|---|---|
| End-to-end tháng lương | Từ check-in đến lương thực lãnh | ✅ Pass |
| XML-RPC check-in | Script gọi API tạo attendance | ✅ Pass |
| Nhiều NPT | 3 NPT → GTGC = 11tr + 3×4.4tr = 24.2tr | ✅ Pass |
| Hợp đồng hết hạn | Không tạo bảng lương cho NV hết HĐ | ✅ Pass |
| Unique constraint | Không tạo 2 bảng lương cùng tháng/NV | ✅ Pass |

---

## CHƯƠNG 5: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

### 5.1. Kết luận

Sau quá trình nghiên cứu, phân tích và triển khai, nhóm 08 đã hoàn thành đầy đủ hệ thống Chấm công & Tính lương trên nền tảng Odoo 15 với các kết quả nổi bật:

**Về mặt kỹ thuật:**
- Xây dựng thành công module `nhan_su_cham_cong_luong` tích hợp chặt chẽ với module `nhan_su` của Khoa FIT-DNU, đảm bảo nguyên tắc master data và không trùng lặp dữ liệu.
- Triển khai đầy đủ 3 mức yêu cầu: Tích hợp hệ thống (Mức 1), Tự động hóa quy trình (Mức 2), AI & External API (Mức 3).
- Áp dụng đúng quy định pháp luật Việt Nam về thuế TNCN lũy tiến 7 bậc và BHXH/BHYT/BHTN.
- Sử dụng đúng cơ chế kế thừa Odoo (`_inherit`) để mở rộng model mà không phá vỡ cấu trúc gốc.
- Xử lý đúng múi giờ UTC → UTC+7 khi tính vi phạm kỷ luật.

**Về mặt nghiệp vụ:**
- Hệ thống giảm thiểu ~96% thao tác thủ công trong quy trình tính lương hàng tháng.
- HR chỉ cần thực hiện 1 thao tác duy nhất là "Xác nhận" sau khi hệ thống tự động tính toán.
- Tính năng AI phân tích giúp HR có cái nhìn tổng quan về xu hướng nhân viên mà không cần phân tích thủ công.
- Phiếu lương minh bạch với từng dòng chi tiết giải thích rõ công thức tính.

**Về mặt học thuật:**
- Tuân thủ đầy đủ yêu cầu liêm chính: không hardcoding, có commit history rõ ràng trên GitHub, ghi nguồn tham khảo FIT-DNU.
- Có cải tiến thực chất so với module gốc: thêm 8 tính năng mới hoàn toàn không có trong bản gốc.
- Có đầy đủ tài liệu: Audit Code, Gap Analysis, BusinessFlow BPMN, README.

### 5.2. Những điểm nổi bật của đề tài

**Điểm kỹ thuật đáng chú ý:**

1. **Xử lý múi giờ chính xác:** Dùng `context_timestamp()` thay vì so sánh trực tiếp UTC, tránh sai lệch 7 tiếng khi tính vi phạm kỷ luật.

2. **Thuế TNCN lũy tiến đúng luật:** Implement đúng thuật toán lũy tiến 7 bậc theo Luật Thuế TNCN Việt Nam, không dùng công thức rút gọn sai.

3. **Gemini AI không cần thư viện ngoài:** Gọi REST API trực tiếp bằng `requests` có sẵn trong Odoo, tránh xung đột dependency (đã từng gặp lỗi `cryptography 46.0.5` + `cffi 2.0.0`).

4. **Cron Job monthly thay vì daily:** Dùng `interval_type=months` + `nextcall` ngày 5 thay vì `daily` + `if today.day==5`, đảm bảo chạy đúng ngày.

5. **Unique constraint database:** Ràng buộc `unique(employee_id, thang, nam)` ở cấp database, không chỉ ở cấp Python, đảm bảo toàn vẹn dữ liệu.

### 5.3. Hạn chế

- Chưa có giao diện mobile app cho nhân viên tự check-in/out bằng GPS hoặc QR code.
- Chưa tích hợp trực tiếp với ngân hàng để tự động chuyển khoản lương.
- Báo cáo xuất file Excel/PDF chưa theo mẫu chuẩn của cơ quan thuế Việt Nam (mẫu 05/QTT-TNCN).
- Chưa có tính năng quản lý nghỉ phép (leave management) tích hợp vào tính lương.
- Chưa có thông báo tự động qua email/Zalo khi lương được xác nhận.
- Gemini AI phân tích theo từng nhân viên, chưa có phân tích tổng hợp toàn công ty.

### 5.4. Hướng phát triển

**Ngắn hạn (3-6 tháng):**
- **Tích hợp nghỉ phép:** Kết nối với module `hr_holidays` để tự động trừ lương ngày nghỉ không phép, cộng lương ngày nghỉ phép có lương.
- **Thông báo tự động:** Gửi thông báo qua Zalo OA hoặc Email khi lương được xác nhận hoặc khi có vi phạm kỷ luật.
- **Xuất báo cáo thuế:** Xuất tờ khai thuế TNCN theo mẫu 05/QTT-TNCN của Tổng cục Thuế dưới dạng Excel.

**Trung hạn (6-12 tháng):**
- **App di động:** Xây dựng ứng dụng React Native cho nhân viên tự check-in/out bằng GPS hoặc QR code, tích hợp với Odoo qua REST API.
- **Kết nối ngân hàng:** Tích hợp API ngân hàng (VietcomBank, Techcombank) để tự động chuyển khoản lương hàng tháng sau khi HR xác nhận.
- **Dashboard phân tích:** Xây dựng dashboard tổng hợp xu hướng nhân sự toàn công ty bằng Odoo BI hoặc Metabase.

**Dài hạn (1-2 năm):**
- **AI nâng cao:** Mở rộng AI phân tích dự báo nguy cơ nghỉ việc (turnover prediction), đề xuất điều chỉnh lương theo thị trường dựa trên dữ liệu lương ngành.
- **Chấm công thông minh:** Tích hợp camera nhận diện khuôn mặt (Face Recognition) với OpenCV hoặc AWS Rekognition để chấm công không cần thẻ.
- **Mở rộng sang module khác:** Kết nối với module Dự án (project.task) để tính lương theo hiệu suất dự án, không chỉ theo ngày công.
- **Multi-company:** Hỗ trợ quản lý lương cho nhiều công ty con trong cùng một hệ thống Odoo.

---

## TÀI LIỆU THAM KHẢO

1. Odoo S.A. (2023). *Odoo 15 Developer Documentation*. https://www.odoo.com/documentation/15.0/
2. Odoo S.A. (2023). *External API - XML-RPC*. https://www.odoo.com/documentation/15.0/developer/reference/external_api.html
3. Odoo S.A. (2023). *ORM API - Models and Fields*. https://www.odoo.com/documentation/15.0/developer/reference/backend/orm.html
4. FIT-DNU. (2024). *Kho module học phần Business Internship*. https://github.com/FIT-DNU/Business-Internship
5. Google. (2024). *Gemini API Documentation - REST API*. https://ai.google.dev/docs
6. Google. (2024). *Gemini API - Generate Content*. https://ai.google.dev/api/generate-content
7. Quốc hội Việt Nam. (2007). *Luật Thuế Thu nhập cá nhân số 04/2007/QH12*. Hà Nội.
8. Quốc hội Việt Nam. (2012). *Luật sửa đổi Luật Thuế TNCN số 26/2012/QH13*. Hà Nội.
9. Ủy ban Thường vụ Quốc hội. (2020). *Nghị quyết 954/2020/UBTVQH14 về mức giảm trừ gia cảnh*. Hà Nội.
10. Chính phủ Việt Nam. (2020). *Nghị định 58/2020/NĐ-CP về mức đóng BHXH bắt buộc*. Hà Nội.
11. PostgreSQL Global Development Group. (2023). *PostgreSQL 13 Documentation*. https://www.postgresql.org/docs/13/
12. Docker Inc. (2023). *Docker Compose Documentation*. https://docs.docker.com/compose/
13. Python Software Foundation. (2023). *xmlrpc.client — XML-RPC client access*. https://docs.python.org/3/library/xmlrpc.client.html

---

## PHỤ LỤC

### Phụ lục A: Hướng dẫn cài đặt và triển khai

**Bước 1: Clone repository**
```bash
git clone https://github.com/nhucccc/ERP_ChamCong_TinhLuong_Nhom08.git
cd ERP_ChamCong_TinhLuong_Nhom08
```

**Bước 2: Khởi động Docker**
```bash
docker-compose up -d
# Chờ khoảng 30-60 giây để Odoo khởi động hoàn toàn
docker-compose logs -f odoo  # Theo dõi log
```

**Bước 3: Tạo database và cài module**
- Truy cập http://localhost:8069
- Tạo database: `odoo_test`, master password: `admin`
- Vào Apps → Tìm `nhan_su_cham_cong_luong` → Install

**Bước 4: Cấu hình Gemini API Key**
```
Settings → Technical → Parameters → System Parameters
→ Tạo mới:
  Key: nhan_su_cham_cong_luong.gemini_api_key
  Value: [API Key lấy từ https://aistudio.google.com/app/apikey]
```

**Bước 5: Migrate module (khi có thay đổi code)**
```bash
docker exec erp_chamcong_tinhluong_nhom08-odoo-1 \
  odoo -c /etc/odoo/odoo.conf \
  -u nhan_su_cham_cong_luong \
  -d odoo_test \
  --stop-after-init
```

### Phụ lục B: Hướng dẫn sử dụng External API

```bash
cd external_api

# Liệt kê nhân viên
python cham_cong_client.py --list

# Check-in nhân viên ID=3
python cham_cong_client.py --checkin 3

# Check-out nhân viên ID=3
python cham_cong_client.py --checkout 3

# Chạy demo đầy đủ (liệt kê + chấm công + xem lương)
python cham_cong_client.py
```

**Cấu hình kết nối** (trong file `cham_cong_client.py`):
```python
ODOO_URL = "http://localhost:8069"
ODOO_DB = "odoo_test"
ODOO_USER = "admin"
ODOO_PASSWORD = "admin"
```

### Phụ lục C: Cấu trúc commit history

Nhóm duy trì commit history minh bạch trên GitHub với các milestone chính:
- `feat: Giai đoạn 1 - Models cơ bản (hr_employee, hr_attendance, hr_family)`
- `feat: Giai đoạn 1 - Models tính lương (bang_cham_cong, bang_luong, bang_luong_line)`
- `feat: Giai đoạn 2 - Views và giao diện đầy đủ`
- `feat: Giai đoạn 2 - Cron jobs tự động hóa`
- `feat: Giai đoạn 3 - Tích hợp Gemini AI`
- `feat: Giai đoạn 3 - External API XML-RPC`
- `docs: Thêm BusinessFlow BPMN PlantUML`
- `docs: Thêm Audit Code & Gap Analysis`
- `fix: Sửa lỗi OpenSSL cryptography conflict`
- `fix: Cập nhật Gemini model sang gemini-2.5-flash`

### Phụ lục D: Thông tin nhóm

| Họ tên | Mã SV | Vai trò |
|---|---|---|
| [Thành viên 1] | [MSSV] | Nhóm trưởng - Backend Models |
| [Thành viên 2] | [MSSV] | Backend - Tính lương & Thuế |
| [Thành viên 3] | [MSSV] | Frontend - Views & UI |
| [Thành viên 4] | [MSSV] | AI & External API |

**Repository:** https://github.com/nhucccc/ERP_ChamCong_TinhLuong_Nhom08

---

*© 2025 Nhóm 08 - AIoTLab, Khoa Công nghệ Thông tin, Trường Đại học Đại Nam*
