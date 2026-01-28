Audit Code – Module nhan_su
Module nhan_su cung cấp các chức năng quản lý thông tin nhân viên như hồ sơ cá nhân, đơn vị công tác, chức vụ, lịch sử công tác và chứng chỉ. Module được thiết kế độc lập, không kế thừa trực tiếp từ hr.employee, đóng vai trò dữ liệu gốc (master data) theo yêu cầu học phần.

Gap Analysis
Module nhan_su hiện chưa tích hợp với các module HR chuẩn của Odoo như hr_attendance và hr_contract. Do đó, để triển khai bài toán Chấm công – Tính lương, cần xây dựng một module trung gian để liên kết dữ liệu nhân sự với dữ liệu chấm công và hợp đồng, đảm bảo tính nhất quán và tự động hóa quy trình.