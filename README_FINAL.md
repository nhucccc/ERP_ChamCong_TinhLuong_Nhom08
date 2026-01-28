# HỆ THỐNG CHẤM CÔNG & TÍNH LƯƠNG - NHÓM 08

## 📋 THÔNG TIN DỰ ÁN
- **Đề tài**: Hệ thống Chấm công và Tính lương tích hợp với Quản lý nhân sự (HRM)
- **Môn học**: Thực tập CNTT7 - Hội nhập và Quản trị phần mềm doanh nghiệp
- **Nền tảng**: Odoo 15, Python, PostgreSQL
- **Mức độ hoàn thành**: MỨC 2 (Process Automation)

## 🎯 YÊU CẦU ĐÃ HOÀN THÀNH

### ✅ MỨC 1 - Tích hợp hệ thống
- Module `nhan_su` làm dữ liệu gốc (master data)
- Tích hợp với `hr_attendance` (chấm công)
- Tích hợp với `hr_contract` (hợp đồng lương)
- Loại bỏ nhập liệu trùng lặp

### ✅ MỨC 2 - Tự động hóa quy trình
- **3 Cron Jobs tự động**:
  1. Tạo bảng chấm công đầu tháng
  2. Tạo bảng lương đầu tháng
  3. Tính lương tự động ngày 5 hàng tháng
- **Event-driven**: Hệ thống tự động thực thi không cần can thiệp thủ công

## 🏗️ KIẾN TRÚC HỆ THỐNG

### Module chính: `nhan_su_cham_cong_luong`
```
addons/nhan_su_cham_cong_luong/
├── models/
│   ├── bang_cham_cong_thang.py    # Model bảng chấm công
│   ├── bang_luong_thang.py        # Model bảng lương
│   └── nhan_vien_extend.py        # Mở rộng nhân viên
├── views/
│   ├── bang_cham_cong_thang_views.xml
│   ├── bang_luong_thang_views.xml
│   ├── nhan_vien_extend_views.xml
│   └── menu.xml
├── wizard/
│   ├── tao_bang_cham_cong_luong_wizard.py
│   └── tao_bang_cham_cong_luong_wizard_views.xml
├── data/
│   └── cron_jobs.xml              # 3 cron job tự động
└── security/
    └── ir.model.access.csv
```

## 🚀 HƯỚNG DẪN CHẠY HỆ THỐNG

### Bước 1: Khởi động Docker
```bash
docker-compose up -d
```

### Bước 2: Truy cập hệ thống
- **URL**: http://localhost:8069
- **Username**: admin
- **Password**: admin
- **Database**: odoo_test

### Bước 3: Cài đặt module và tạo dữ liệu test
```bash
python install_and_test.py
```

## 📊 CHỨC NĂNG CHÍNH

### 1. Bảng chấm công tháng
- Tự động tổng hợp từ dữ liệu chấm công
- Tính số ngày công, giờ làm việc
- Trạng thái: Nháp → Xác nhận

### 2. Bảng lương tháng  
- Tính lương dựa trên hợp đồng và số ngày công
- Công thức: (Lương cơ bản / 22) × Số ngày công
- Trạng thái: Nháp → Tính toán → Xác nhận

### 3. Wizard tạo bảng
- Tạo bảng chấm công/lương hàng loạt
- Chọn tháng/năm và nhân viên
- Hỗ trợ HR tạo bảng thủ công khi cần

## 🤖 TỰ ĐỘNG HÓA (MỨC 2)

### Cron Job 1: Tạo bảng chấm công
- **Thời gian**: Đầu tháng (1/month)
- **Chức năng**: Tự động tạo bảng chấm công cho tất cả nhân viên

### Cron Job 2: Tạo bảng lương
- **Thời gian**: Đầu tháng (1/month)  
- **Chức năng**: Tự động tạo bảng lương cho tất cả nhân viên

### Cron Job 3: Tính lương tự động
- **Thời gian**: Ngày 5 hàng tháng
- **Chức năng**: Tự động tính lương cho các bảng ở trạng thái nháp

## 📈 LUỒNG NGHIỆP VỤ END-TO-END

1. **Nhân viên chấm công** (hr_attendance)
2. **Hệ thống tự động tổng hợp** → Bảng chấm công tháng
3. **Hệ thống tự động tạo** → Bảng lương tháng
4. **Hệ thống tự động tính lương** → Dựa trên hợp đồng + số ngày công
5. **HR xác nhận** → Hoàn thành quy trình

## 📁 CẤU TRÚC PROJECT CUỐI CÙNG

### Files quan trọng:
- `PROJECT_README.md` - Tài liệu tổng quan dự án
- `docker-compose.yml` - Cấu hình Docker
- `odoo.conf` - Cấu hình Odoo
- `install_and_test.py` - Script cài đặt và test
- `addons/nhan_su_cham_cong_luong/` - Module chính

### Tài liệu phân tích:
- `ANALYSIS_HR_MODULES.md` - Phân tích module HR
- `ANALYSIS_NHAN_SU_MODULE.md` - Phân tích module nhan_su
- `LUONG_NGHIEP_VU_END_TO_END.md` - Luồng nghiệp vụ chi tiết
- `LUONG_NGHIEP_VU_RUT_GON.md` - Luồng nghiệp vụ rút gọn

### Tài liệu quản lý project:
- `DANH_SACH_MODULES_PHAN_LOAI.md` - Phân loại module
- `GIAI_THICH_MODULES_GIU_LAI.md` - Giải thích module giữ lại
- `PHAN_TICH_PROJECT_STRUCTURE.md` - Phân tích cấu trúc

## 🎉 KẾT QUẢ ĐẠT ĐƯỢC

- ✅ **100% yêu cầu MỨC 2** - Process Automation
- ✅ **Tích hợp hoàn chỉnh** với module nhan_su
- ✅ **Tự động hóa end-to-end** từ chấm công đến tính lương
- ✅ **Event-driven architecture** với 3 cron job
- ✅ **Loại bỏ thao tác thủ công** cho HR/Kế toán
- ✅ **Dữ liệu test đầy đủ** cho demo
- ✅ **Tài liệu chi tiết** cho báo cáo

## 🌐 DEMO HỆ THỐNG

1. **Truy cập**: http://localhost:8069
2. **Menu**: "Chấm công & Lương"
3. **Xem**: Bảng chấm công tháng, Bảng lương tháng
4. **Test**: Tính lương tự động, Cron job automation
5. **Kiểm tra**: Settings → Technical → Scheduled Actions

---
**Hệ thống đã sẵn sàng cho demo và nộp bài! 🚀**