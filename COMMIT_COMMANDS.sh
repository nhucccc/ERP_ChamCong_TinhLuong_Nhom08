#!/bin/bash

# Script tự động commit và push code lên GitHub
# Chạy từng lệnh theo thứ tự

echo "🚀 Bắt đầu commit code lên GitHub..."

# Commit 1: Thêm module chính
git add addons/nhan_su_cham_cong_luong/
git commit -m "feat: Add nhan_su_cham_cong_luong module - Core attendance and payroll system

✨ New Features:
- Implement bang_cham_cong_thang model for monthly attendance summary
- Implement bang_luong_thang model for monthly payroll calculation  
- Add wizard for batch creation of attendance/payroll records
- Add comprehensive views and user interface
- Add cron jobs for end-of-month automation
- Integrate with existing nhan_su module (master data)

🔧 Technical Details:
- Models: attendance summary, payroll calculation, employee extension
- Views: tree, form, search views with proper workflow states
- Automation: 3 cron jobs (create attendance, create payroll, calculate salary)
- Integration: Bridge pattern to connect nhan_su ↔ hr.employee
- Business Logic: Salary = Base salary × (Work days / Standard days)

📋 Business Process:
- Master data from nhan_su module
- Daily attendance from hr_attendance  
- Monthly automation on day 1 and day 5
- HR approval workflow
- Accounting confirmation and payment

Ref: CNTT7 Assignment - Attendance & Payroll Management System"

# Commit 2: Thêm documentation
git add docs/ *.md ANALYSIS_*.md DANH_SACH_*.md GIAI_THICH_*.md LUONG_*.md PHAN_TICH_*.md
git commit -m "docs: Add comprehensive project documentation and analysis

📚 Documentation Added:
- Business flow analysis (end-to-end and simplified)
- System architecture and module structure analysis  
- Gap analysis from existing modules
- Module classification and justification
- Integration strategy documentation

📊 Analysis Files:
- LUONG_NGHIEP_VU_END_TO_END.md: Complete business process (12 steps)
- LUONG_NGHIEP_VU_RUT_GON.md: Simplified flow for BPMN (10 steps)
- ANALYSIS_NHAN_SU_MODULE.md: Deep dive into nhan_su module
- DANH_SACH_MODULES_PHAN_LOAI.md: Module classification (keep/remove)
- PHAN_TICH_PROJECT_STRUCTURE.md: Project structure optimization

🎯 Purpose:
- Demonstrate understanding of business requirements
- Show integration points between modules
- Provide clear development roadmap
- Support academic evaluation process"

# Commit 3: Cập nhật README chính
cp PROJECT_README.md README.md
git add README.md
git commit -m "docs: Update main README with project information

📝 Updates:
- Add CNTT7 assignment information
- Document system features and architecture
- Add installation and usage instructions
- Include team member information
- Reference original repository and improvements
- Add technical documentation links

🎓 Academic Requirements:
- Clear project description for evaluation
- Demonstrate improvements over original version
- Proper attribution to source repository
- Professional documentation standards"

# Push tất cả lên GitHub
echo "📤 Pushing to GitHub..."
git push origin feature/nhan-su-cham-cong-luong

echo "✅ Hoàn thành! Kiểm tra GitHub repository của bạn."
echo "🔗 Link: https://github.com/YOUR_USERNAME/Business-Internship"

# Tạo Pull Request (optional)
echo ""
echo "🔄 Tùy chọn: Tạo Pull Request để merge vào main branch"
echo "1. Vào GitHub repository"
echo "2. Click 'Compare & pull request'"  
echo "3. Merge pull request"