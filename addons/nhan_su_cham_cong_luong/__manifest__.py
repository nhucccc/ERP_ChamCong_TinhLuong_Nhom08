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
    'author': "Thực tập CNTT7",
    'website': "http://www.yourcompany.com",
    'category': 'Human Resources',
    'version': '15.0.1.0.0',
    
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