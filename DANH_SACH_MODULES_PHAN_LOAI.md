# DANH SÁCH MODULES PHÂN LOẠI CHO ĐỀ TÀI

## A. DANH SÁCH MODULES GIỮ LẠI (BẮT BUỘC) - 18 modules

### A1. Core System Modules (6 modules)
**Lý do**: Cần thiết cho hoạt động cơ bản của Odoo
1. `base` - Module cơ bản của Odoo (bắt buộc)
2. `web` - Giao diện web (bắt buộc)
3. `mail` - Hệ thống email/thông báo (cần cho workflow)
4. `resource` - Quản lý tài nguyên, lịch làm việc (cần cho HR)
5. `uom` - Đơn vị đo lường (cần cho tính toán)
6. `bus` - Hệ thống messaging realtime (cần cho web)

### A2. HR Core Modules (3 modules)
**Lý do**: Trực tiếp liên quan đến đề tài chấm công và lương
7. `hr` - Module HR cơ bản (bắt buộc cho hr_attendance, hr_contract)
8. `hr_attendance` - Chấm công (nguồn dữ liệu chính)
9. `hr_contract` - Hợp đồng lao động (cần cho tính lương)

### A3. Supporting Modules (7 modules)
**Lý do**: Hỗ trợ các chức năng cần thiết
10. `portal` - Portal cơ bản (cần cho user interface)
11. `contacts` - Quản lý liên hệ (cần cho hr)
12. `product` - Sản phẩm cơ bản (dependency của nhiều modules)
13. `analytic` - Phân tích (cần cho báo cáo)
14. `barcodes` - Mã vạch (có thể dùng cho chấm công)
15. `base_setup` - Cài đặt cơ bản (cần cho configuration)
16. `http_routing` - Routing HTTP (cần cho web)

### A4. Custom Modules (2 modules)
**Lý do**: Modules chính của đề tài
17. `nhan_su` - Module quản lý nhân sự (master data)
18. `nhan_su_cham_cong_luong` - Module chính của đề tài

**TỔNG: 18 modules**
## B. DANH SÁCH MODULES CÓ THỂ LOẠI BỎ - 380+ modules

### B1. Accounting Modules (50+ modules)
**Lý do**: Không liên quan đến chấm công và lương
- `account`, `account_*` (tất cả modules kế toán)
- `snailmail_account`, `stock_account`, `mrp_account`, v.v.

### B2. Sales & CRM Modules (40+ modules)
**Lý do**: Không liên quan đến HR
- `sale`, `sale_*` (tất cả modules bán hàng)
- `crm`, `crm_*` (tất cả modules CRM)
- `sales_team`

### B3. Purchase Modules (20+ modules)
**Lý do**: Không liên quan đến HR
- `purchase`, `purchase_*` (tất cả modules mua hàng)

### B4. Inventory/Stock Modules (15+ modules)
**Lý do**: Không liên quan đến chấm công lương
- `stock`, `stock_*` (tất cả modules kho)
- `delivery`, `delivery_*`

### B5. Manufacturing Modules (15+ modules)
**Lý do**: Không liên quan đến HR
- `mrp`, `mrp_*` (tất cả modules sản xuất)
- `repair`

### B6. Website Modules (60+ modules)
**Lý do**: Không cần website cho hệ thống nội bộ
- `website`, `website_*` (tất cả modules website)
- `web_editor`, `web_tour`, `web_unsplash`, `web_kanban_gauge`

### B7. Localization Modules (100+ modules)
**Lý do**: Chỉ cần cho Việt Nam (nếu cần)
- `l10n_*` (tất cả trừ `l10n_vn` nếu cần)

### B8. Point of Sale Modules (20+ modules)
**Lý do**: Không liên quan đến HR
- `point_of_sale`, `pos_*` (tất cả modules POS)

### B9. Project Management Modules (10+ modules)
**Lý do**: Không liên quan trực tiếp đến chấm công lương
- `project`, `project_*`
- `pad`, `pad_project`

### B10. Event Management Modules (20+ modules)
**Lý do**: Không liên quan đến HR
- `event`, `event_*` (tất cả modules sự kiện)

### B11. Marketing Modules (15+ modules)
**Lý do**: Không liên quan đến HR
- `mass_mailing`, `mass_mailing_*`
- `utm`, `link_tracker`

### B12. Integration Modules (25+ modules)
**Lý do**: Không cần tích hợp bên ngoài
- `google_*` (Google integration)
- `microsoft_*` (Microsoft integration)
- `auth_*` (External authentication)
- `fetchmail*` (Email integration)
- `social_media`

### B13. Payment Modules (15+ modules)
**Lý do**: Không cần thanh toán online
- `payment`, `payment_*`

### B14. Specialized Modules (30+ modules)
**Lý do**: Không liên quan đến đề tài
- `fleet*` (Quản lý xe)
- `maintenance*` (Bảo trì)
- `lunch*` (Đặt cơm)
- `survey*` (Khảo sát)
- `gamification*` (Gamification)
- `membership` (Thành viên)
- `coupon`, `gift_card`
- `rating`

### B15. Hardware Modules (5+ modules)
**Lý do**: Không cần hardware đặc biệt
- `hw_*` (Hardware drivers)

### B16. Test Modules (10+ modules)
**Lý do**: Chỉ dùng cho testing
- `test_*` (tất cả modules test)

### B17. Theme Modules (5+ modules)
**Lý do**: Không cần theme đặc biệt
- `theme_*`
- `muk_web_theme`

### B18. Other HR Modules (15+ modules)
**Lý do**: Không cần thiết cho đề tài cơ bản
- `hr_expense` (Chi phí)
- `hr_holidays` (Nghỉ phép)
- `hr_recruitment` (Tuyển dụng)
- `hr_skills` (Kỹ năng)
- `hr_timesheet` (Timesheet)
- `hr_work_entry*` (Work entries)
- `hr_presence`, `hr_org_chart`, `hr_gamification`
- `hr_fleet`, `hr_maintenance`

### B19. Other Custom Modules (1 module)
**Lý do**: Không liên quan đến đề tài chấm công lương
- `quan_ly_van_ban` (Quản lý văn bản)
## C. DANH SÁCH MODULES KHÔNG SỬA - CHỈ ĐỂ THAM CHIẾU

### C1. Core Framework (Không được sửa)
**Lý do**: Core system của Odoo, sửa sẽ gây lỗi hệ thống
- `base` - Module cơ bản
- `web` - Giao diện web
- `mail` - Hệ thống mail
- `bus` - Messaging system
- `http_routing` - HTTP routing

### C2. Standard HR Modules (Không được sửa)
**Lý do**: Standard modules của Odoo, chỉ sử dụng API
- `hr` - HR cơ bản
- `hr_attendance` - Chấm công (chỉ đọc dữ liệu)
- `hr_contract` - Hợp đồng (chỉ đọc dữ liệu)

### C3. Supporting Modules (Không được sửa)
**Lý do**: Standard modules, chỉ sử dụng chức năng có sẵn
- `resource` - Quản lý tài nguyên
- `uom` - Đơn vị đo lường
- `portal` - Portal
- `contacts` - Liên hệ
- `product` - Sản phẩm
- `analytic` - Phân tích
- `barcodes` - Mã vạch
- `base_setup` - Cài đặt cơ bản

**NGUYÊN TẮC**: Chỉ sử dụng API và extend, KHÔNG sửa đổi code gốc

### C4. Custom Modules (Có thể sửa/mở rộng)
**Lý do**: Modules do sinh viên phát triển
- `nhan_su` - Có thể mở rộng nếu cần
- `nhan_su_cham_cong_luong` - Module chính, được phép sửa đổi

## D. CẤU TRÚC THU MỤC ADDONS/ CUỐI CÙNG

```
addons/
├── # === CORE SYSTEM (6 modules) ===
├── base/                           # Module cơ bản Odoo
├── web/                            # Giao diện web
├── mail/                           # Hệ thống email/thông báo
├── resource/                       # Quản lý tài nguyên, lịch làm việc
├── uom/                           # Đơn vị đo lường
├── bus/                           # Messaging realtime
├── 
├── # === HR CORE (3 modules) ===
├── hr/                            # HR cơ bản
├── hr_attendance/                 # Chấm công (nguồn dữ liệu)
├── hr_contract/                   # Hợp đồng lao động
├── 
├── # === SUPPORTING (7 modules) ===
├── portal/                        # Portal cơ bản
├── contacts/                      # Quản lý liên hệ
├── product/                       # Sản phẩm cơ bản
├── analytic/                      # Phân tích
├── barcodes/                      # Mã vạch
├── base_setup/                    # Cài đặt cơ bản
├── http_routing/                  # HTTP routing
├── 
├── # === CUSTOM MODULES (2 modules) ===
├── nhan_su/                       # Quản lý nhân sự (master data)
└── nhan_su_cham_cong_luong/       # Module chính của đề tài
```

**TỔNG CỘNG: 18 modules (thay vì 400+ modules)**

## E. LỢI ÍCH CỦA VIỆC TỐI GIẢN

### E1. Kỹ thuật
- **Kích thước**: Giảm từ ~2GB xuống ~200MB
- **Tốc độ**: Khởi động nhanh hơn 5-10 lần
- **Memory**: Sử dụng ít RAM hơn
- **Dependencies**: Ít conflict, dễ quản lý

### E2. Học thuật
- **Focus**: Tập trung vào đề tài chính
- **Hiểu rõ**: Dễ nắm bắt toàn bộ hệ thống
- **Đánh giá**: Giảng viên dễ đánh giá năng lực thực tế
- **Demo**: Dễ demo và giải thích

### E3. Quản lý
- **Git**: Repository nhỏ gọn, clone nhanh
- **Backup**: Dễ backup và restore
- **Deploy**: Triển khai đơn giản
- **Maintenance**: Ít modules cần maintain

**KẾT LUẬN**: Cấu trúc 18 modules này đủ để thực hiện đầy đủ chức năng của đề tài "Quản lý chấm công và tính lương dựa trên dữ liệu nhân sự" mà vẫn giữ được tính đơn giản và tập trung.