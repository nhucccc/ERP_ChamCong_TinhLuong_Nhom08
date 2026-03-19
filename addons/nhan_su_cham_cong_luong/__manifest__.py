# -*- coding: utf-8 -*-
{
    'name': "Nhân sự - Chấm công và Tính lương",
    'summary': """
        Hệ thống tổng hợp chấm công và tính lương tích hợp với quản lý nhân sự
    """,
    'description': """
        Module tích hợp chấm công và tính lương:
        - Tổng hợp dữ liệu chấm công theo tháng
        - Tính lương dựa trên hợp đồng và số ngày công
        - Tích hợp với module nhan_su (master data)
        - Tự động hóa quy trình tính lương
    """,
    'author': "Nhóm 08 - Thực tập CNTT7 - FIT-DNU",
    'website': "https://github.com/nhucccc/ERP_ChamCong_TinhLuong_Nhom08",
    'category': 'Human Resources',
    'version': '15.0.2.0.0',
    # Nguồn tham khảo: module nhan_su từ kho GitHub học phần FIT-DNU
    # https://github.com/FIT-DNU/Business-Internship
    # Cải tiến: tích hợp hr.employee/hr.attendance/hr.contract Odoo native,
    # tính lương lũy tiến Thuế TNCN 7 bậc, phát hiện đi muộn/về sớm/tăng ca,
    # quản lý người phụ thuộc giảm trừ gia cảnh, tích hợp Gemini AI phân tích lương,
    # kết nối External API XML-RPC giả lập máy chấm công.
    
    # Dependencies - các module cần thiết
    'depends': [
        'base',
        'nhan_su',           # Module master data nhân sự
        'hr_attendance',     # Module chấm công
        'hr_contract',       # Module hợp đồng
        'hr',               # Module HR cơ bản
    ],
    
    # Data files
    'data': [
        'security/ir.model.access.csv',
        'data/cron_jobs.xml',
        'views/bang_cham_cong_thang_views.xml',
        'views/bang_luong_thang_views.xml',
        'views/hr_employee_inherit_views.xml',
        'views/hr_attendance_inherit_views.xml',
        'views/hr_family_views.xml',
        'views/nhan_vien_extend_views.xml',
        'wizard/tao_bang_cham_cong_luong_wizard_views.xml',
        'views/menu.xml',
    ],
    
    # Demo data
    'demo': [],
    
    'installable': True,
    'auto_install': False,
    'application': True,
}