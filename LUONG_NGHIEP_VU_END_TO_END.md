# LUỒNG NGHIỆP VỤ END-TO-END: HỆ THỐNG CHẤM CÔNG VÀ TÍNH LƯƠNG

## ACTORS (Các bên tham gia)
- **Nhân viên**: Người lao động thực hiện chấm công
- **HR**: Bộ phận nhân sự quản lý thông tin nhân viên và chấm công
- **Kế toán**: Bộ phận tài chính xử lý lương và thanh toán
- **Hệ thống**: Odoo 15 với các modules tự động hóa

## LUỒNG NGHIỆP VỤ CHÍNH (HAPPY PATH)

### GIAI ĐOẠN 1: THIẾT LẬP MASTER DATA

**Bước 1: HR thiết lập thông tin nhân viên trong HRM (nhan_su)**
- HR tạo hồ sơ nhân viên trong module `nhan_su` (master data)
- Nhập thông tin: họ tên, mã định danh, chức vụ, đơn vị, ngày sinh
- Thiết lập lịch sử công tác và chứng chỉ bằng cấp
- **Kết quả**: Dữ liệu nhân viên master được lưu trong `nhan_vien`

**Bước 2: HR tạo hồ sơ nhân viên trong HR System**
- HR tạo tương ứng `hr.employee` trong module `hr`
- Liên kết với thông tin từ `nhan_su` (mapping qua tên/email)
- **Kết quả**: Nhân viên có thể sử dụng chức năng chấm công

**Bước 3: HR thiết lập hợp đồng lao động**
- HR tạo `hr.contract` trong module `hr_contract`
- Nhập thông tin: lương cơ bản, ngày bắt đầu, ngày kết thúc, loại hợp đồng
- **Kết quả**: Có cơ sở để tính lương cho nhân viên

### GIAI ĐOẠN 2: CHẤM CÔNG HÀNG NGÀY

**Bước 4: Nhân viên thực hiện chấm công**
- Nhân viên check-in khi đến công ty (tạo record trong `hr.attendance`)
- Nhân viên check-out khi về (cập nhật record với thời gian ra)
- **Kết quả**: Dữ liệu chấm công được lưu với thời gian vào/ra và tổng giờ làm việc

### GIAI ĐOẠN 3: XỬ LÝ CUỐI THÁNG (TỰ ĐỘNG)

**Bước 5: Hệ thống tự động tạo bảng chấm công tháng**
- **Trigger**: Cron job chạy vào ngày 1 hàng tháng
- Hệ thống tạo `bang.cham.cong.thang` cho tất cả nhân viên
- Tổng hợp dữ liệu từ `hr.attendance` của tháng trước
- Tính toán: số ngày làm việc, tổng giờ làm việc, số ngày công chuẩn
- **Kết quả**: Bảng chấm công tháng với trạng thái "Nháp"

**Bước 6: Hệ thống tự động tạo bảng lương tháng**
- **Trigger**: Cron job chạy sau khi tạo bảng chấm công
- Hệ thống tạo `bang.luong.thang` cho tất cả nhân viên
- Liên kết với bảng chấm công và hợp đồng tương ứng
- Lấy lương cơ bản từ `hr.contract`
- **Kết quả**: Bảng lương tháng với trạng thái "Nháp"

### GIAI ĐOẠN 4: TÍNH LƯƠNG TỰ ĐỘNG

**Bước 7: Hệ thống tự động tính lương**
- **Trigger**: Cron job chạy vào ngày 5 hàng tháng
- Hệ thống tính toán cho từng nhân viên:
  - Tỷ lệ công = Số ngày làm việc / Số ngày công chuẩn
  - Lương theo ngày công = Lương cơ bản × Tỷ lệ công
  - Tổng lương = Lương theo ngày công + Phụ cấp - Khấu trừ
- Cập nhật trạng thái bảng lương thành "Đã tính"
- **Kết quả**: Lương được tính toán tự động cho tất cả nhân viên

### GIAI ĐOẠN 5: KIỂM DUYỆT VÀ THANH TOÁN

**Bước 8: HR xem xét và xác nhận chấm công**
- HR truy cập danh sách bảng chấm công tháng
- Kiểm tra tính chính xác của dữ liệu chấm công
- Xác nhận bảng chấm công (chuyển trạng thái thành "Đã xác nhận")
- **Kết quả**: Dữ liệu chấm công được khóa, không thể sửa đổi

**Bước 9: HR điều chỉnh lương (nếu cần)**
- HR xem xét bảng lương đã được tính tự động
- Điều chỉnh phụ cấp hoặc khấu trừ đặc biệt (làm thêm giờ, phạt, thưởng)
- Thêm ghi chú giải thích các khoản điều chỉnh
- **Kết quả**: Bảng lương được điều chỉnh phù hợp với thực tế

**Bước 10: Kế toán xác nhận và thanh toán lương**
- Kế toán truy cập danh sách bảng lương đã tính
- Kiểm tra tính chính xác của các khoản lương
- Xác nhận bảng lương (chuyển trạng thái thành "Đã xác nhận")
- Thực hiện thanh toán lương cho nhân viên
- Đánh dấu "Đã thanh toán" sau khi chuyển khoản
- **Kết quả**: Lương được thanh toán và ghi nhận hoàn tất

### GIAI ĐOẠN 6: BÁO CÁO VÀ THEO DÕI

**Bước 11: Nhân viên xem thông tin lương cá nhân**
- Nhân viên đăng nhập hệ thống
- Xem bảng lương của mình (chỉ đọc)
- Kiểm tra chi tiết chấm công và cách tính lương
- **Kết quả**: Nhân viên nắm được thông tin lương minh bạch

**Bước 12: HR/Kế toán tạo báo cáo tổng hợp**
- Tạo báo cáo lương theo phòng ban, tháng, quý
- Phân tích xu hướng chấm công và chi phí lương
- Xuất báo cáo để báo cáo lãnh đạo
- **Kết quả**: Có dữ liệu để ra quyết định quản lý

## ĐIỂM QUAN TRỌNG TRONG LUỒNG

### Master Data Flow:
- **nhan_su** → Nguồn thông tin nhân viên gốc
- **hr.employee** → Bridge để sử dụng chức năng HR của Odoo
- **hr.contract** → Cung cấp thông tin lương cơ bản

### Data Integration:
- **hr.attendance** → Dữ liệu chấm công thực tế
- **bang.cham.cong.thang** → Tổng hợp chấm công theo tháng
- **bang.luong.thang** → Kết quả tính lương cuối cùng

### Automation Triggers:
- **Ngày 1**: Tạo bảng chấm công và lương tháng mới
- **Ngày 5**: Tính lương tự động
- **Realtime**: Cập nhật dữ liệu chấm công khi nhân viên check-in/out

### Business Rules:
- Tỷ lệ công = Ngày làm việc thực tế / Ngày công chuẩn (trừ chủ nhật)
- Lương = Lương cơ bản × Tỷ lệ công + Phụ cấp - Khấu trừ
- Workflow: Nháp → Đã tính → Đã xác nhận → Đã thanh toán