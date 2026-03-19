# External API - Máy chấm công Client

Kết nối Odoo qua XML-RPC theo tài liệu chính thức:
https://www.odoo.com/documentation/15.0/ro/developer/reference/external_api.html

## Cài đặt
```bash
# Không cần cài thêm thư viện - xmlrpc.client có sẵn trong Python 3
python --version  # Python 3.6+
```

## Cách dùng
```bash
# Demo tự động (liệt kê NV + chấm công + bảng lương)
python cham_cong_client.py

# Liệt kê nhân viên
python cham_cong_client.py --list

# Check-in nhân viên ID=3
python cham_cong_client.py --checkin 3

# Check-out nhân viên ID=3
python cham_cong_client.py --checkout 3

# Kết nối server khác
python cham_cong_client.py --url http://192.168.1.100:8069 --db mydb --user admin --password admin
```

## Luồng hoạt động
```
Máy chấm công (script) → XML-RPC → Odoo Server → hr.attendance
                                                 → bang.cham.cong.thang (cron)
                                                 → bang.luong.thang (cron)
```
