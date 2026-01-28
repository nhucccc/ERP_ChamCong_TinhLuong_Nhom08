#!/usr/bin/env python3
"""
Script tự động cài đặt module và tạo dữ liệu test
Chạy: python3 install_and_test.py
"""

import xmlrpc.client
import time
from datetime import datetime, timedelta

# Cấu hình kết nối
url = 'http://localhost:8069'
db = 'odoo_test'
username = 'admin'
password = 'admin'

print("🔄 Đang kết nối Odoo...")

# Chờ Odoo khởi động hoàn toàn
time.sleep(5)

try:
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})

    if not uid:
        print("❌ Không thể đăng nhập! Kiểm tra lại database/username/password")
        print("💡 Hướng dẫn:")
        print("   1. Truy cập http://localhost:8069")
        print("   2. Tạo database 'odoo_test' với admin/admin")
        print("   3. Chạy lại script này")
        exit(1)

    print(f"✅ Đăng nhập thành công! UID: {uid}")

    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

    # 1. Cài đặt module nhan_su_cham_cong_luong
    print("\n📦 Cài đặt module nhan_su_cham_cong_luong...")
    
    # Kiểm tra module đã cài chưa
    module_ids = models.execute_kw(db, uid, password,
        'ir.module.module', 'search', 
        [[('name', '=', 'nhan_su_cham_cong_luong')]])
    
    if module_ids:
        module_info = models.execute_kw(db, uid, password,
            'ir.module.module', 'read', [module_ids], {'fields': ['state']})
        
        if module_info[0]['state'] == 'installed':
            print("✅ Module đã được cài đặt")
        else:
            print("🔄 Đang cài đặt module...")
            models.execute_kw(db, uid, password,
                'ir.module.module', 'button_immediate_install', [module_ids])
            print("✅ Cài đặt module thành công")
    else:
        print("❌ Không tìm thấy module nhan_su_cham_cong_luong")
        print("💡 Kiểm tra lại đường dẫn addons trong docker-compose.yml")
        exit(1)

    # 2. Tạo nhân viên trong nhan_su
    print("\n👤 Tạo nhân viên test...")
    
    # Kiểm tra nhân viên đã tồn tại chưa
    existing_nv = models.execute_kw(db, uid, password,
        'nhan_vien', 'search', [[('ma_dinh_danh', '=', 'TEST001')]])
    
    if not existing_nv:
        nhan_vien_data = {
            'ho_ten_dem': 'Nguyễn Văn',
            'ten': 'Test',
            'ma_dinh_danh': 'TEST001',
            'email': 'test@company.com',
            'ngay_sinh': '1990-01-01',
            'que_quan': 'Hà Nội',
            'so_dien_thoai': '0123456789'
        }
        
        nhan_vien_id = models.execute_kw(db, uid, password,
            'nhan_vien', 'create', [nhan_vien_data])
        print(f"✅ Tạo nhân viên: ID {nhan_vien_id}")
    else:
        nhan_vien_id = existing_nv[0]
        print(f"✅ Sử dụng nhân viên có sẵn: ID {nhan_vien_id}")

    # 3. Tạo hr.employee
    print("\n👔 Tạo HR Employee...")
    
    existing_emp = models.execute_kw(db, uid, password,
        'hr.employee', 'search', [[('work_email', '=', 'test@company.com')]])
    
    if not existing_emp:
        hr_employee_data = {
            'name': 'Nguyễn Văn Test',
            'work_email': 'test@company.com',
            'work_phone': '0123456789',
        }
        
        hr_employee_id = models.execute_kw(db, uid, password,
            'hr.employee', 'create', [hr_employee_data])
        print(f"✅ Tạo HR Employee: ID {hr_employee_id}")
    else:
        hr_employee_id = existing_emp[0]
        print(f"✅ Sử dụng HR Employee có sẵn: ID {hr_employee_id}")

    # 4. Tạo hợp đồng
    print("\n📄 Tạo hợp đồng...")
    
    existing_contract = models.execute_kw(db, uid, password,
        'hr.contract', 'search', [[('employee_id', '=', hr_employee_id)]])
    
    if not existing_contract:
        contract_data = {
            'name': 'HD-TEST001',
            'employee_id': hr_employee_id,
            'wage': 15000000,  # 15 triệu
            'date_start': '2024-01-01',
            'state': 'open'
        }
        
        contract_id = models.execute_kw(db, uid, password,
            'hr.contract', 'create', [contract_data])
        print(f"✅ Tạo hợp đồng: ID {contract_id}")
    else:
        contract_id = existing_contract[0]
        print(f"✅ Sử dụng hợp đồng có sẵn: ID {contract_id}")

    # 5. Tạo dữ liệu chấm công
    print("\n⏰ Tạo dữ liệu chấm công...")
    
    today = datetime.now()
    created_count = 0
    
    for i in range(10):  # Tạo 10 ngày chấm công
        work_date = today - timedelta(days=i)
        if work_date.weekday() < 5:  # Chỉ tạo cho thứ 2-6
            # Kiểm tra đã có chấm công ngày này chưa
            existing_att = models.execute_kw(db, uid, password,
                'hr.attendance', 'search', [[
                    ('employee_id', '=', hr_employee_id),
                    ('check_in', '>=', work_date.strftime('%Y-%m-%d 00:00:00')),
                    ('check_in', '<=', work_date.strftime('%Y-%m-%d 23:59:59'))
                ]])
            
            if not existing_att:
                attendance_data = {
                    'employee_id': hr_employee_id,
                    'check_in': work_date.replace(hour=8, minute=0, second=0).strftime('%Y-%m-%d %H:%M:%S'),
                    'check_out': work_date.replace(hour=17, minute=30, second=0).strftime('%Y-%m-%d %H:%M:%S'),
                }
                
                attendance_id = models.execute_kw(db, uid, password,
                    'hr.attendance', 'create', [attendance_data])
                created_count += 1
                print(f"   ✅ {work_date.strftime('%Y-%m-%d')}: ID {attendance_id}")
    
    print(f"✅ Tạo {created_count} bản ghi chấm công mới")

    # 6. Test tạo bảng chấm công
    print("\n📊 Test tạo bảng chấm công...")
    try:
        bang_cham_cong = models.execute_kw(db, uid, password,
            'bang.cham.cong.thang', 'tao_bang_cham_cong_thang', [])
        print(f"✅ Tạo bảng chấm công: {len(bang_cham_cong)} bảng")
    except Exception as e:
        print(f"❌ Lỗi tạo bảng chấm công: {e}")

    # 7. Test tạo bảng lương
    print("\n💰 Test tạo bảng lương...")
    try:
        bang_luong = models.execute_kw(db, uid, password,
            'bang.luong.thang', 'tao_bang_luong_thang', [])
        print(f"✅ Tạo bảng lương: {len(bang_luong)} bảng")
        
        # 8. Test tính lương
        if bang_luong:
            print("\n🧮 Test tính lương...")
            for bl_id in bang_luong:
                try:
                    models.execute_kw(db, uid, password,
                        'bang.luong.thang', 'action_calculate', [bl_id])
                    print(f"   ✅ Tính lương cho bảng ID {bl_id}")
                except Exception as e:
                    print(f"   ❌ Lỗi tính lương cho bảng ID {bl_id}: {e}")
            
            print(f"✅ Hoàn thành tính lương cho {len(bang_luong)} bảng")
    except Exception as e:
        print(f"❌ Lỗi tạo bảng lương: {e}")

    print("\n🎉 HOÀN THÀNH SETUP VÀ TEST!")
    print("\n📋 Dữ liệu đã tạo:")
    print(f"   - 1 nhân viên: Nguyễn Văn Test (TEST001)")
    print(f"   - 1 hợp đồng: 15,000,000 VND")
    print(f"   - {created_count} ngày chấm công")
    print(f"   - Bảng chấm công và lương tháng hiện tại")
    
    print("\n🌐 Truy cập hệ thống:")
    print("   URL: http://localhost:8069")
    print("   Database: odoo_test")
    print("   Username: admin")
    print("   Password: admin")
    print("   Menu: Chấm công & Lương")

except Exception as e:
    print(f"❌ Lỗi: {e}")
    import traceback
    traceback.print_exc()