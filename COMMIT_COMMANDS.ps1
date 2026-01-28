# PowerShell script cho Windows
# Chạy: .\COMMIT_COMMANDS.ps1

Write-Host "🚀 Bắt đầu commit code lên GitHub..." -ForegroundColor Green

# Tạo branch mới
Write-Host "📝 Tạo branch mới..." -ForegroundColor Yellow
git checkout -b feature/nhan-su-cham-cong-luong

# Tạo thư mục docs
Write-Host "📁 Tạo thư mục docs..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path "docs\businessflow" -Force | Out-Null

# Copy README
Write-Host "📄 Cập nhật README..." -ForegroundColor Yellow
Copy-Item "PROJECT_README.md" "README.md" -Force

# Commit 1: Module chính
Write-Host "💾 Commit 1: Module chính..." -ForegroundColor Yellow
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

Ref: CNTT7 Assignment - Attendance & Payroll Management System"

# Commit 2: Documentation
Write-Host "💾 Commit 2: Documentation..." -ForegroundColor Yellow
git add docs/ *.md
git commit -m "docs: Add comprehensive project documentation and analysis

📚 Documentation Added:
- Business flow analysis (end-to-end and simplified)
- System architecture and module structure analysis  
- Gap analysis from existing modules
- Module classification and justification
- Integration strategy documentation

🎯 Purpose:
- Demonstrate understanding of business requirements
- Show integration points between modules
- Provide clear development roadmap
- Support academic evaluation process"

# Commit 3: README chính
Write-Host "💾 Commit 3: README chính..." -ForegroundColor Yellow
git add README.md
git commit -m "docs: Update main README with project information

📝 Updates:
- Add CNTT7 assignment information
- Document system features and architecture
- Add installation and usage instructions
- Include team member information
- Reference original repository and improvements

🎓 Academic Requirements:
- Clear project description for evaluation
- Demonstrate improvements over original version
- Proper attribution to source repository"

# Push lên GitHub
Write-Host "📤 Pushing to GitHub..." -ForegroundColor Green
git push origin feature/nhan-su-cham-cong-luong

Write-Host "✅ Hoàn thành! Kiểm tra GitHub repository của bạn." -ForegroundColor Green
Write-Host "🔗 Link: https://github.com/YOUR_USERNAME/Business-Internship" -ForegroundColor Cyan

Write-Host ""
Write-Host "🔄 Tùy chọn: Tạo Pull Request để merge vào main branch" -ForegroundColor Yellow
Write-Host "1. Vào GitHub repository" -ForegroundColor White
Write-Host "2. Click 'Compare & pull request'" -ForegroundColor White
Write-Host "3. Merge pull request" -ForegroundColor White