# LUỒNG NGHIỆP VỤ RÚT GỌN: HỆ THỐNG CHẤM CÔNG VÀ TÍNH LƯƠNG

## ACTORS
- **HR**: Bộ phận nhân sự
- **Nhân viên**: Người lao động  
- **Hệ thống**: Odoo 15 (Cron jobs)
- **Kế toán**: Bộ phận tài chính

## LUỒNG NGHIỆP VỤ CHÍNH (10 BƯỚC)

**1. HR thiết lập master data nhân viên**
- **Actor**: HR
- **Mô tả**: Tạo thông tin nhân viên trong module `nhan_su` (master data)
- **Kết quả**: Dữ liệu nhân viên gốc được lưu trữ

**2. HR tạo hợp đồng lao động**
- **Actor**: HR  
- **Mô tả**: Tạo `hr.contract` với thông tin lương cơ bản và thời hạn
- **Kết quả**: Có cơ sở để tính lương cho nhân viên

**3. Nhân viên thực hiện chấm công hàng ngày**
- **Actor**: Nhân viên
- **Mô tả**: Check-in/check-out tạo dữ liệu trong `hr.attendance`
- **Kết quả**: Dữ liệu chấm công được ghi nhận liên tục

**4. Hệ thống tự động tạo bảng chấm công tháng**
- **Actor**: Hệ thống (Cron job - ngày 1 hàng tháng)
- **Mô tả**: Tổng hợp dữ liệu từ `hr.attendance` tạo `bang.cham.cong.thang`
- **Kết quả**: Bảng chấm công tháng với số ngày công và giờ làm việc

**5. Hệ thống tự động tạo bảng lương tháng**
- **Actor**: Hệ thống (Cron job - sau bước 4)
- **Mô tả**: Tạo `bang.luong.thang` liên kết với chấm công và hợp đồng
- **Kết quả**: Bảng lương tháng ở trạng thái "Nháp"

**6. Hệ thống tự động tính lương**
- **Actor**: Hệ thống (Cron job - ngày 5 hàng tháng)
- **Mô tả**: Tính lương = Lương cơ bản × (Ngày làm việc / Ngày công chuẩn)
- **Kết quả**: Lương được tính toán tự động, trạng thái "Đã tính"

**7. HR xác nhận chấm công**
- **Actor**: HR
- **Mô tả**: Kiểm tra và xác nhận tính chính xác của bảng chấm công
- **Kết quả**: Bảng chấm công được khóa, trạng thái "Đã xác nhận"

**8. HR điều chỉnh lương (nếu cần)**
- **Actor**: HR
- **Mô tả**: Thêm phụ cấp hoặc khấu trừ đặc biệt vào bảng lương
- **Kết quả**: Bảng lương được điều chỉnh phù hợp thực tế

**9. Kế toán xác nhận lương**
- **Actor**: Kế toán
- **Mô tả**: Kiểm tra và xác nhận bảng lương cuối cùng
- **Kết quả**: Bảng lương trạng thái "Đã xác nhận", sẵn sàng thanh toán

**10. Kế toán thanh toán lương**
- **Actor**: Kế toán
- **Mô tả**: Thực hiện chuyển khoản lương cho nhân viên
- **Kết quả**: Lương được thanh toán, trạng thái "Đã thanh toán"

## ĐIỂM QUAN TRỌNG

### Master Data:
- **nhan_su**: Nguồn dữ liệu nhân viên chính (master data)

### Tự động hóa:
- **Ngày 1**: Tạo bảng chấm công và lương tháng
- **Ngày 5**: Tính lương tự động

### Workflow:
- Nháp → Đã tính → Đã xác nhận → Đã thanh toán

### Data Flow:
- nhan_su → hr.contract → hr.attendance → bang.cham.cong.thang → bang.luong.thang