# Hệ thống Chấm công và Tính lương - Bài tập lớn CNTT7

## 📋 Thông tin đề tài
- **Đề tài**: Chấm công + Tính lương  
- **Môn học**: Thực tập CNTT7 - Hội nhập và Quản trị phần mềm doanh nghiệp
- **Platform**: Odoo 15 Community Edition
- **Nhóm**: [Nhập tên nhóm]
- **Thành viên**: 
  - [Tên sinh viên 1] - [MSSV]
  - [Tên sinh viên 2] - [MSSV]

## 🎯 Mô tả hệ thống
Hệ thống tích hợp quản lý nhân sự, chấm công và tính lương với các tính năng chính:

### Tính năng đã phát triển:
- ✅ **Quản lý nhân sự**: Sử dụng module `nhan_su` làm master data
- ✅ **Chấm công tự động**: Tích hợp với `hr_attendance` của Odoo
- ✅ **Tính lương**: Dựa trên ngày công thực tế và hợp đồng lao động
- ✅ **Tự động hóa**: Cron jobs tự động tạo bảng lương cuối tháng
- ✅ **Workflow**: Quy trình duyệt và thanh toán lương
- ✅ **Báo cáo**: Thống kê chấm công và lương theo tháng

### Công nghệ sử dụng:
- **Backend**: Python, Odoo 15 Framework
- **Database**: PostgreSQL
- **Frontend**: XML Views, JavaScript
- **Automation**: Cron Jobs, Event-driven

## 🏗️ Cấu trúc project

```
├── addons/
│   ├── nhan_su/                           # Module HRM gốc (master data)
│   │   ├── models/                        # Models nhân viên, chức vụ, đơn vị
│   │   ├── views/                         # Giao diện quản lý nhân sự
│   │   └── security/                      # Phân quyền
│   │
│   └── nhan_su_cham_cong_luong/          # Module chính (phát triển mới)
│       ├── models/                        # Logic nghiệp vụ
│       │   ├── bang_cham_cong_thang.py   # Tổng hợp chấm công
│       │   ├── bang_luong_thang.py       # Tính lương
│       │   └── nhan_vien_extend.py       # Mở rộng nhân viên
│       ├── views/                         # Giao diện người dùng
│       ├── wizard/                        # Wizard tạo hàng loạt
│       ├── data/                          # Cron jobs tự động
│       └── security/                      # Phân quyền
│
├── docs/                                  # Tài liệu dự án
│   ├── businessflow/                      # Sơ đồ luồng nghiệp vụ
│   └── analysis/                          # Phân tích hệ thống
│
└── README.md                              # File này
```

## 🔄 Luồng nghiệp vụ chính

1. **HR thiết lập master data** trong module `nhan_su`
2. **HR tạo hợp đồng** lao động với mức lương cơ bản
3. **Nhân viên chấm công** hàng ngày qua `hr_attendance`
4. **Hệ thống tự động** tạo bảng chấm công cuối tháng (Cron)
5. **Hệ thống tự động** tính lương dựa trên ngày công (Cron)
6. **HR xem xét** và điều chỉnh lương nếu cần
7. **Kế toán xác nhận** và thanh toán lương

## 🚀 Cài đặt và chạy

### Yêu cầu hệ thống:
- Python 3.8+
- PostgreSQL 12+
- Odoo 15 Community

### Cài đặt:
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/Business-Internship.git
cd Business-Internship

# Cài đặt dependencies
pip install -r requirements.txt

# Setup database
sudo docker-compose up -d

# Chạy Odoo
python3 odoo-bin.py -c odoo.conf -u nhan_su,nhan_su_cham_cong_luong
```

### Sử dụng:
1. Truy cập: http://localhost:8069
2. Cài đặt modules: `nhan_su`, `nhan_su_cham_cong_luong`
3. Thiết lập dữ liệu nhân viên và hợp đồng
4. Bắt đầu sử dụng chức năng chấm công và tính lương

## 📊 Kết quả đạt được

### Mức độ hoàn thành:
- ✅ **MỨC 1 - Tích hợp hệ thống**: Hoàn thành 100%
  - Dữ liệu nhân sự thống nhất từ module `nhan_su`
  - Tích hợp với `hr_attendance` và `hr_contract`
  - Loại bỏ nhập liệu trùng lặp

- ✅ **MỨC 2 - Tự động hóa**: Hoàn thành 100%
  - Cron jobs tự động tạo bảng chấm công/lương
  - Event-driven: tự động tính lương dựa trên chấm công
  - Giảm thiểu thao tác thủ công

### Cải tiến so với phiên bản cũ:
- 🔄 **Tái cấu trúc**: Tối ưu hóa cấu trúc dữ liệu và performance
- 🤖 **Tự động hóa**: Thêm quy trình tự động cuối tháng
- 🔗 **Tích hợp**: Kết nối chặt chẽ với hệ sinh thái HR của Odoo
- 📱 **UX/UI**: Cải thiện giao diện và trải nghiệm người dùng

## 📚 Tài liệu tham khảo

### Nguồn gốc:
- **Repository gốc**: https://github.com/FIT-DNU/Business-Internship
- **Module nhan_su**: Kế thừa và mở rộng từ phiên bản K15

### Tài liệu kỹ thuật:
- **Odoo 15 Documentation**: https://www.odoo.com/documentation/15.0/
- **Python ORM**: https://www.odoo.com/documentation/15.0/developer/reference/backend/orm.html
- **Odoo Views**: https://www.odoo.com/documentation/15.0/developer/reference/backend/views.html

## 🏆 Đóng góp

Dự án này được phát triển như một phần của bài tập lớn môn Thực tập CNTT7, đóng góp vào cộng đồng học tập của FIT-DNU.

### Liên hệ:
- **Email**: [email sinh viên]
- **GitHub**: [link profile GitHub]

---
© 2024 - Bài tập lớn CNTT7, Khoa Công nghệ Thông tin, Đại học Đại Nam