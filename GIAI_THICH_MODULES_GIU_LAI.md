# GIẢI THÍCH CÁC MODULES ĐƯỢC GIỮ LẠI TRONG ĐỀ TÀI

## DANH SÁCH 18 MODULES VÀ LÝ DO GIỮ LẠI

### A. CORE SYSTEM MODULES (6 modules)

**1. `base`**
- **Lý do giữ**: Module cơ bản bắt buộc của Odoo, không thể thiếu
- **Vai trò**: Cung cấp framework cơ bản, models, fields, và các chức năng nền tảng

**2. `web`**
- **Lý do giữ**: Cần thiết cho giao diện web của hệ thống
- **Vai trò**: Cung cấp giao diện người dùng, views, controllers cho việc truy cập hệ thống

**3. `mail`**
- **Lý do giữ**: Hỗ trợ hệ thống thông báo và workflow trong quản lý lương
- **Vai trò**: Gửi thông báo về lương, chấm công và các hoạt động liên quan đến nhân sự

**4. `resource`**
- **Lý do giữ**: Quản lý lịch làm việc, ca làm việc cần thiết cho tính lương
- **Vai trò**: Định nghĩa giờ làm việc chuẩn, lịch nghỉ để tính toán ngày công chính xác

**5. `uom`**
- **Lý do giữ**: Đơn vị đo lường cần thiết cho tính toán giờ, ngày công
- **Vai trò**: Cung cấp các đơn vị đo như giờ, ngày để tính toán lương và thời gian làm việc

**6. `bus`**
- **Lý do giữ**: Hỗ trợ messaging realtime cho giao diện web
- **Vai trò**: Đảm bảo giao diện web hoạt động mượt mà, cập nhật dữ liệu realtime

### B. HR CORE MODULES (3 modules)

**7. `hr`**
- **Lý do giữ**: Module HR cơ bản, là dependency bắt buộc của hr_attendance và hr_contract
- **Vai trò**: Cung cấp model hr.employee và các chức năng HR cơ bản để tích hợp với module nhan_su

**8. `hr_attendance`**
- **Lý do giữ**: Nguồn dữ liệu chấm công chính của hệ thống
- **Vai trò**: Cung cấp dữ liệu check-in/check-out để tính toán số ngày công và giờ làm việc

**9. `hr_contract`**
- **Lý do giữ**: Cung cấp thông tin hợp đồng và lương cơ bản để tính lương
- **Vai trò**: Lưu trữ mức lương cơ bản, thời hạn hợp đồng làm cơ sở tính lương hàng tháng

### C. SUPPORTING MODULES (7 modules)

**10. `portal`**
- **Lý do giữ**: Cung cấp chức năng portal cơ bản cho giao diện người dùng
- **Vai trò**: Hỗ trợ phân quyền và giao diện cho nhân viên xem thông tin lương của mình

**11. `contacts`**
- **Lý do giữ**: Quản lý thông tin liên hệ, là dependency của module hr
- **Vai trò**: Lưu trữ thông tin liên hệ của nhân viên, hỗ trợ tích hợp với hr.employee

**12. `product`**
- **Lý do giữ**: Dependency cơ bản của nhiều modules khác trong hệ thống
- **Vai trò**: Cung cấp cấu trúc dữ liệu cơ bản, hỗ trợ các tính năng mở rộng sau này

**13. `analytic`**
- **Lý do giữ**: Hỗ trợ phân tích và báo cáo về lương, chấm công
- **Vai trò**: Cung cấp framework để tạo báo cáo thống kê lương theo phòng ban, thời gian

**14. `barcodes`**
- **Lý do giữ**: Hỗ trợ chấm công bằng mã vạch hoặc QR code
- **Vai trò**: Cho phép nhân viên chấm công bằng cách quét mã vạch, nâng cao trải nghiệm người dùng

**15. `base_setup`**
- **Lý do giữ**: Cung cấp các cài đặt cơ bản cho hệ thống
- **Vai trò**: Hỗ trợ cấu hình các tham số hệ thống liên quan đến tính lương và chấm công

**16. `http_routing`**
- **Lý do giữ**: Cần thiết cho routing HTTP của giao diện web
- **Vai trò**: Đảm bảo các URL và routing hoạt động chính xác cho giao diện web

### D. CUSTOM MODULES (2 modules)

**17. `nhan_su`**
- **Lý do giữ**: Module master data nhân viên theo yêu cầu đề tài
- **Vai trò**: Cung cấp dữ liệu nhân viên gốc, thông tin chức vụ, đơn vị để tích hợp với hệ thống lương

**18. `nhan_su_cham_cong_luong`**
- **Lý do giữ**: Module chính của đề tài, chứa toàn bộ logic nghiệp vụ
- **Vai trò**: Thực hiện tổng hợp chấm công, tính lương, và các chức năng chính của hệ thống

## TÓM TẮT KIẾN TRÚC HỆ THỐNG

**Luồng dữ liệu chính:**
1. **nhan_su** → Cung cấp thông tin nhân viên master data
2. **hr_attendance** → Cung cấp dữ liệu chấm công thực tế  
3. **hr_contract** → Cung cấp thông tin lương cơ bản
4. **nhan_su_cham_cong_luong** → Tổng hợp và tính toán lương cuối cùng

**Các modules còn lại** đóng vai trò hỗ trợ framework, giao diện, và các chức năng phụ trợ cần thiết cho hoạt động của hệ thống.