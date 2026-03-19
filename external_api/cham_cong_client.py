#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Giả lập máy chấm công gửi dữ liệu vào Odoo qua XML-RPC External API.
Tài liệu: https://www.odoo.com/documentation/15.0/ro/developer/reference/external_api.html

Cách dùng:
    python cham_cong_client.py                  # Chạy demo tự động
    python cham_cong_client.py --list           # Liệt kê nhân viên
    python cham_cong_client.py --checkin 3      # Check-in nhân viên ID=3
    python cham_cong_client.py --checkout 3     # Check-out nhân viên ID=3
"""

import xmlrpc.client
import argparse
from datetime import datetime, timezone

# ── Cấu hình kết nối Odoo ────────────────────────────────────────────────────
ODOO_URL = "http://localhost:8069"
ODOO_DB  = "odoo_test"
ODOO_USER = "admin"
ODOO_PASS = "admin"


class OdooClient:
    """Client kết nối Odoo qua XML-RPC."""

    def __init__(self, url, db, username, password):
        self.url = url
        self.db = db

        # Endpoint common: dùng để authenticate
        common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
        self.uid = common.authenticate(db, username, password, {})
        if not self.uid:
            raise ConnectionError(
                f"Xác thực thất bại! Kiểm tra lại user/pass và database '{db}'."
            )
        print(f"✅ Kết nối thành công! UID={self.uid}")

        # Endpoint object: dùng để gọi model methods
        self.models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
        self._password = password

    def execute(self, model, method, *args, **kwargs):
        """Gọi method trên model Odoo."""
        return self.models.execute_kw(
            self.db, self.uid, self._password,
            model, method, list(args), kwargs
        )

    # ── Nhân viên ────────────────────────────────────────────────────────────

    def lay_danh_sach_nhan_vien(self):
        """Lấy danh sách nhân viên đang hoạt động."""
        employees = self.execute(
            'hr.employee', 'search_read',
            [[('active', '=', True)]],
            fields=['id', 'name', 'job_title', 'department_id'],
            limit=50,
        )
        return employees

    # ── Chấm công ────────────────────────────────────────────────────────────

    def check_in(self, employee_id: int):
        """Ghi nhận check-in cho nhân viên."""
        now_utc = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

        # Kiểm tra xem đã có bản ghi check-in chưa check-out chưa
        existing = self.execute(
            'hr.attendance', 'search_read',
            [[
                ('employee_id', '=', employee_id),
                ('check_out', '=', False),
            ]],
            fields=['id', 'check_in'],
            limit=1,
        )
        if existing:
            print(f"⚠️  Nhân viên ID={employee_id} đã check-in lúc {existing[0]['check_in']}, chưa check-out.")
            return None

        record_id = self.execute(
            'hr.attendance', 'create',
            [{'employee_id': employee_id, 'check_in': now_utc}]
        )
        print(f"✅ Check-in thành công! Bản ghi ID={record_id}, thời gian={now_utc}")
        return record_id

    def check_out(self, employee_id: int):
        """Ghi nhận check-out cho nhân viên."""
        now_utc = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

        # Tìm bản ghi check-in chưa check-out
        existing = self.execute(
            'hr.attendance', 'search_read',
            [[
                ('employee_id', '=', employee_id),
                ('check_out', '=', False),
            ]],
            fields=['id', 'check_in'],
            limit=1,
        )
        if not existing:
            print(f"⚠️  Nhân viên ID={employee_id} chưa check-in hoặc đã check-out rồi.")
            return None

        record_id = existing[0]['id']
        self.execute(
            'hr.attendance', 'write',
            [[record_id], {'check_out': now_utc}]
        )
        print(f"✅ Check-out thành công! Bản ghi ID={record_id}, thời gian={now_utc}")
        return record_id

    def lay_cham_cong_thang(self, employee_id: int, thang: int, nam: int):
        """Lấy dữ liệu chấm công của nhân viên trong tháng."""
        ngay_dau = f"{nam}-{thang:02d}-01 00:00:00"
        import calendar
        ngay_cuoi_so = calendar.monthrange(nam, thang)[1]
        ngay_cuoi = f"{nam}-{thang:02d}-{ngay_cuoi_so} 23:59:59"

        records = self.execute(
            'hr.attendance', 'search_read',
            [[
                ('employee_id', '=', employee_id),
                ('check_in', '>=', ngay_dau),
                ('check_in', '<=', ngay_cuoi),
            ]],
            fields=['check_in', 'check_out', 'worked_hours', 'is_late', 'late_minutes', 'is_overtime'],
            order='check_in asc',
        )
        return records

    # ── Bảng lương ───────────────────────────────────────────────────────────

    def lay_bang_luong(self, employee_id: int, thang: int, nam: int):
        """Lấy thông tin bảng lương của nhân viên."""
        records = self.execute(
            'bang.luong.thang', 'search_read',
            [[
                ('employee_id', '=', employee_id),
                ('thang', '=', thang),
                ('nam', '=', nam),
            ]],
            fields=[
                'ten_bang_luong', 'luong_co_ban', 'tong_ngay_cong',
                'tien_phat_ky_luat', 'tien_tang_ca', 'thue_tncn',
                'tien_bao_hiem', 'luong_thuc_lanh', 'trang_thai',
            ],
            limit=1,
        )
        return records[0] if records else None


def demo_chay_tu_dong(client: OdooClient):
    """Demo: liệt kê nhân viên và hiển thị chấm công tháng hiện tại."""
    print("\n" + "="*60)
    print("  DEMO MÁY CHẤM CÔNG - KẾT NỐI ODOO XML-RPC")
    print("="*60)

    # 1. Lấy danh sách nhân viên
    print("\n📋 DANH SÁCH NHÂN VIÊN:")
    employees = client.lay_danh_sach_nhan_vien()
    if not employees:
        print("  (Không có nhân viên nào)")
        return

    for emp in employees[:5]:  # Hiển thị tối đa 5
        dept = emp['department_id'][1] if emp['department_id'] else 'N/A'
        print(f"  [{emp['id']}] {emp['name']} - {emp['job_title'] or 'N/A'} - {dept}")

    # 2. Lấy chấm công tháng hiện tại của nhân viên đầu tiên
    emp = employees[0]
    now = datetime.now()
    print(f"\n📅 CHẤM CÔNG THÁNG {now.month}/{now.year} - {emp['name']}:")
    records = client.lay_cham_cong_thang(emp['id'], now.month, now.year)

    if not records:
        print("  (Chưa có dữ liệu chấm công)")
    else:
        for r in records[:5]:
            late_str = f" ⚠️ Muộn {r['late_minutes']} phút" if r.get('is_late') else ""
            ot_str = " 🕐 Tăng ca" if r.get('is_overtime') else ""
            print(f"  {r['check_in'][:10]} | {r['worked_hours']:.1f}h{late_str}{ot_str}")
        print(f"  Tổng: {len(records)} ngày công")

    # 3. Lấy bảng lương
    print(f"\n💰 BẢNG LƯƠNG THÁNG {now.month}/{now.year} - {emp['name']}:")
    bang_luong = client.lay_bang_luong(emp['id'], now.month, now.year)
    if not bang_luong:
        print("  (Chưa có bảng lương)")
    else:
        print(f"  Lương cơ bản  : {bang_luong['luong_co_ban']:>15,.0f} VND")
        print(f"  Ngày công     : {bang_luong['tong_ngay_cong']:>15.1f} ngày")
        print(f"  Tăng ca       : {bang_luong['tien_tang_ca']:>15,.0f} VND")
        print(f"  Phạt kỷ luật  : {bang_luong['tien_phat_ky_luat']:>15,.0f} VND")
        print(f"  BHXH/BHYT/BHTN: {bang_luong['tien_bao_hiem']:>15,.0f} VND")
        print(f"  Thuế TNCN     : {bang_luong['thue_tncn']:>15,.0f} VND")
        print(f"  {'─'*35}")
        print(f"  THỰC LÃNH     : {bang_luong['luong_thuc_lanh']:>15,.0f} VND")
        print(f"  Trạng thái    : {bang_luong['trang_thai']}")

    print("\n" + "="*60)


def main():
    parser = argparse.ArgumentParser(description='Client máy chấm công Odoo')
    parser.add_argument('--url',      default=ODOO_URL,  help='URL Odoo server')
    parser.add_argument('--db',       default=ODOO_DB,   help='Tên database')
    parser.add_argument('--user',     default=ODOO_USER, help='Username')
    parser.add_argument('--password', default=ODOO_PASS, help='Password')
    parser.add_argument('--list',     action='store_true', help='Liệt kê nhân viên')
    parser.add_argument('--checkin',  type=int, metavar='EMP_ID', help='Check-in nhân viên')
    parser.add_argument('--checkout', type=int, metavar='EMP_ID', help='Check-out nhân viên')
    args = parser.parse_args()

    try:
        client = OdooClient(args.url, args.db, args.user, args.password)

        if args.list:
            employees = client.lay_danh_sach_nhan_vien()
            print(f"\n{'ID':<6} {'Tên':<30} {'Chức vụ':<20} {'Phòng ban'}")
            print("-" * 70)
            for emp in employees:
                dept = emp['department_id'][1] if emp['department_id'] else 'N/A'
                print(f"{emp['id']:<6} {emp['name']:<30} {emp['job_title'] or 'N/A':<20} {dept}")
        elif args.checkin:
            client.check_in(args.checkin)
        elif args.checkout:
            client.check_out(args.checkout)
        else:
            demo_chay_tu_dong(client)

    except ConnectionError as e:
        print(f"❌ Lỗi kết nối: {e}")
    except Exception as e:
        print(f"❌ Lỗi: {e}")


if __name__ == '__main__':
    main()
