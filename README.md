<h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>
<h2 align="center">
    HỆ THỐNG CHẤM CÔNG & TÍNH LƯƠNG - NHÓM 08
</h2>
<div align="center">
    <p align="center">
        <img src="docs/logo/aiotlab_logo.png" alt="AIoTLab Logo" width="170"/>
        <img src="docs/logo/fitdnu_logo.png" alt="AIoTLab Logo" width="180"/>
        <img src="docs/logo/dnu_logo.png" alt="DaiNam University Logo" width="200"/>
    </p>

[![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Faculty of Information Technology](https://img.shields.io/badge/Faculty%20of%20Information%20Technology-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)

</div>

## 📖 1. Giới thiệu
Hệ thống **Chấm công & Tính lương** tích hợp với **Quản lý nhân sự (HRM)** được phát triển trên nền tảng Odoo 15 cho học phần **Thực tập CNTT7 - Hội nhập và Quản trị phần mềm doanh nghiệp**.

### 🎯 Mục tiêu dự án
- **Tích hợp hệ thống**: Module `nhan_su` làm dữ liệu gốc (master data)
- **Tự động hóa quy trình**: Loại bỏ thao tác thủ công từ chấm công đến tính lương
- **Event-driven**: Hệ thống tự động thực thi dựa trên sự kiện và lịch trình

### ✅ Yêu cầu đã hoàn thành
- **MỨC 1**: Tích hợp hệ thống - Đảm bảo tính nhất quán dữ liệu
- **MỨC 2**: Tự động hóa quy trình - 3 cron job event-driven 

## 🔧 2. Các công nghệ được sử dụng
<div align="center">

### Hệ điều hành
[![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com/)
[![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://www.microsoft.com/windows/)
### Công nghệ chính
[![Odoo](https://img.shields.io/badge/Odoo-714B67?style=for-the-badge&logo=odoo&logoColor=white)](https://www.odoo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![XML](https://img.shields.io/badge/XML-FF6600?style=for-the-badge&logo=codeforces&logoColor=white)](https://www.w3.org/XML/)
### Cơ sở dữ liệu & DevOps
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
</div>

## 🏗️ 3. Kiến trúc hệ thống

### 3.1. Module chính: `nhan_su_cham_cong_luong`
```
addons/nhan_su_cham_cong_luong/
├── models/
│   ├── bang_cham_cong_thang.py    # Model bảng chấm công tháng
│   ├── bang_luong_thang.py        # Model bảng lương tháng
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
│   └── cron_jobs.xml              # 3 cron job tự động hóa
└── security/
    └── ir.model.access.csv
```

### 3.2. Tích hợp với các module có sẵn
- **`nhan_su`**: Module master data nhân sự
- **`hr_attendance`**: Module chấm công Odoo
- **`hr_contract`**: Module hợp đồng lao động
- **`hr`**: Module HR cơ bản

### 3.3. Luồng nghiệp vụ tự động hóa
```
Nhân viên chấm công → Tổng hợp tự động → Tạo bảng lương → Tính lương tự động
     (hr_attendance)    (Cron Job 1)      (Cron Job 2)     (Cron Job 3)
```
## ⚙️ 4. Cài đặt và chạy hệ thống

### 4.1. Yêu cầu hệ thống
- **Docker & Docker Compose**
- **Python 3.9+**
- **Git**

### 4.2. Cài đặt nhanh với Docker (Khuyến nghị)

#### 4.2.1. Clone project
```bash
git clone https://github.com/nhucccc/ERP_ChamCong_TinhLuong_Nhom08.git
cd ERP_ChamCong_TinhLuong_Nhom08
```

#### 4.2.2. Khởi động hệ thống
```bash
# Khởi động Docker containers
docker-compose up -d

# Chờ hệ thống khởi động (30 giây)
# Truy cập: http://localhost:8069
```

#### 4.2.3. Tạo database và cài đặt module
```bash
# Tạo database 'odoo_test' tại http://localhost:8069
# Username: admin, Password: admin

# Chạy script cài đặt module và tạo dữ liệu test
python install_and_test.py
```

### 4.3. Cài đặt thủ công (Ubuntu/Linux)

#### 4.3.1. Cài đặt các thư viện cần thiết
```bash
sudo apt-get install libxml2-dev libxslt-dev libldap2-dev libsasl2-dev libssl-dev python3.10-distutils python3.10-dev build-essential libssl-dev libffi-dev zlib1g-dev python3.10-venv libpq-dev
```

#### 4.3.2. Khởi tạo môi trường ảo
```bash
# Khởi tạo môi trường ảo
python3.10 -m venv ./venv

# Kích hoạt môi trường ảo
source venv/bin/activate

# Cài đặt dependencies
pip3 install -r requirements.txt
```

#### 4.3.3. Setup database
```bash
# Khởi động PostgreSQL với Docker
sudo docker-compose up -d db
```

#### 4.3.4. Cấu hình Odoo
Sử dụng file **odoo.conf** có sẵn hoặc tạo mới:
```ini
[options]
addons_path = addons
db_host = localhost
db_password = odoo
db_user = odoo
db_port = 5432
xmlrpc_port = 8069
```

#### 4.3.5. Chạy hệ thống
```bash
python3 odoo-bin.py -c odoo.conf -u all
```

### 4.4. Truy cập hệ thống
- **URL**: http://localhost:8069
- **Database**: odoo_test
- **Username**: admin
- **Password**: admin
- **Menu chính**: "Chấm công & Lương"

## 🎯 5. Chức năng chính

### 5.1. Bảng chấm công tháng
- **Tự động tổng hợp** từ dữ liệu chấm công (hr_attendance)
- **Tính toán**: Số ngày công, tổng giờ làm việc
- **Trạng thái**: Nháp → Xác nhận
- **Báo cáo**: Chi tiết chấm công theo nhân viên

### 5.2. Bảng lương tháng
- **Tính lương tự động** dựa trên hợp đồng và số ngày công
- **Công thức**: (Lương cơ bản ÷ 22 ngày) × Số ngày công thực tế
- **Trạng thái**: Nháp → Tính toán → Xác nhận
- **Quản lý**: Phụ cấp, khấu trừ, thuế

### 5.3. Wizard tạo bảng hàng loạt
- **Tạo bảng chấm công/lương** cho nhiều nhân viên
- **Chọn tháng/năm** linh hoạt
- **Lọc nhân viên** theo phòng ban, vị trí

### 5.4. Tự động hóa (MỨC 2)
#### 🤖 Cron Job 1: Tạo bảng chấm công
- **Thời gian**: Đầu tháng (1/month)
- **Chức năng**: Tự động tạo bảng chấm công cho tất cả nhân viên có hợp đồng

#### 🤖 Cron Job 2: Tạo bảng lương
- **Thời gian**: Đầu tháng (1/month)
- **Chức năng**: Tự động tạo bảng lương cho tất cả nhân viên

#### 🤖 Cron Job 3: Tính lương tự động
- **Thời gian**: Ngày 5 hàng tháng
- **Chức năng**: Tự động tính lương cho các bảng ở trạng thái nháp

## 📊 6. Demo hệ thống

### 6.1. Dữ liệu test có sẵn
- **Nhân viên**: Nguyễn Văn Test (TEST001)
- **Hợp đồng**: 15,000,000 VND/tháng
- **Chấm công**: 8 ngày làm việc (8:00-17:30)
- **Bảng lương**: Tự động tính toán

### 6.2. Các bước demo
1. **Truy cập hệ thống**: http://localhost:8069
2. **Xem dữ liệu gốc**: Menu "Nhân sự" → "Nhân viên"
3. **Xem chấm công**: Menu "HR" → "Attendances"
4. **Demo module chính**: Menu "Chấm công & Lương"
5. **Test automation**: Settings → Technical → Scheduled Actions

## 📚 7. Tài liệu kỹ thuật

### 7.1. Tài liệu phân tích
- [`ANALYSIS_HR_MODULES.md`](ANALYSIS_HR_MODULES.md) - Phân tích module HR
- [`ANALYSIS_NHAN_SU_MODULE.md`](ANALYSIS_NHAN_SU_MODULE.md) - Phân tích module nhan_su
- [`LUONG_NGHIEP_VU_END_TO_END.md`](LUONG_NGHIEP_VU_END_TO_END.md) - Luồng nghiệp vụ chi tiết

### 7.2. Tài liệu quản lý dự án
- [`PROJECT_README.md`](PROJECT_README.md) - Tổng quan dự án
- [`DANH_SACH_MODULES_PHAN_LOAI.md`](DANH_SACH_MODULES_PHAN_LOAI.md) - Phân loại module
- [`PHAN_TICH_PROJECT_STRUCTURE.md`](PHAN_TICH_PROJECT_STRUCTURE.md) - Phân tích cấu trúc

### 7.3. Hướng dẫn sử dụng
- [`README_FINAL.md`](README_FINAL.md) - Tài liệu tổng kết cuối cùng
- [`addons/nhan_su_cham_cong_luong/README.md`](addons/nhan_su_cham_cong_luong/README.md) - Hướng dẫn module

## 🔧 8. Troubleshooting

### 8.1. Lỗi thường gặp
```bash
# Lỗi kết nối database
docker logs erp_chamcong_tinhluong_nhom08-odoo-1

# Lỗi module không tìm thấy
docker exec -it erp_chamcong_tinhluong_nhom08-odoo-1 ls -la /mnt/extra-addons

# Restart containers
docker-compose restart
```

### 8.2. Liên hệ hỗ trợ
- **GitHub Issues**: [Tạo issue mới](https://github.com/nhucccc/ERP_ChamCong_TinhLuong_Nhom08/issues)
- **Email**: [Liên hệ nhóm phát triển]

## 📝 9. License

© 2024 AIoTLab, Faculty of Information Technology, DaiNam University. All rights reserved.

---

    
