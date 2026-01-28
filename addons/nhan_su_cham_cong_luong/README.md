# Module Nhân sự - Chấm công và Tính lương

## Mô tả
Module tích hợp chấm công và tính lương với hệ thống quản lý nhân sự Odoo 15.

## Tính năng chính
1. **Tổng hợp chấm công theo tháng**: Tự động tính toán từ dữ liệu hr.attendance
2. **Tính lương theo ngày công**: Dựa trên hợp đồng và số ngày làm việc thực tế
3. **Tích hợp với module nhan_su**: Sử dụng dữ liệu nhân viên làm master data
4. **Tự động hóa**: Cron job tự động tạo bảng và tính lương

## Cài đặt
1. Đảm bảo các module dependencies đã được cài đặt: `nhan_su`, `hr_attendance`, `hr_contract`
2. Cài đặt module: `nhan_su_cham_cong_luong`
3. Cập nhật danh sách ứng dụng và cài đặt

## Sử dụng
### Tạo bảng chấm công và lương
- Sử dụng wizard: Menu > Chấm công & Lương > Cấu hình > Tạo bảng chấm công & lương
- Hoặc tự động qua cron job (chạy đầu mỗi tháng)

### Quy trình tính lương
1. Tạo bảng chấm công (tự động từ hr.attendance)
2. Tạo bảng lương (liên kết với chấm công và hợp đồng)
3. Tính lương (nút "Tính lương" hoặc tự động ngày 5 hàng tháng)
4. Xác nhận và thanh toán

## Cấu trúc dữ liệu
- `bang.cham.cong.thang`: Tổng hợp chấm công theo tháng
- `bang.luong.thang`: Tính lương dựa trên chấm công và hợp đồng