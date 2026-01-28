#!/bin/bash

# Script setup Git config (chạy 1 lần duy nhất)

echo "⚙️ Thiết lập Git configuration..."

# Thiết lập thông tin cá nhân (thay đổi thông tin cho đúng)
git config --global user.name "Tên Sinh Viên"
git config --global user.email "email@student.dainam.edu.vn"

# Thiết lập editor mặc định
git config --global core.editor "nano"

# Thiết lập branch mặc định
git config --global init.defaultBranch main

# Kiểm tra cấu hình
echo "📋 Cấu hình hiện tại:"
git config --list | grep user

echo "✅ Hoàn thành setup Git!"
echo ""
echo "🔄 Tiếp theo: Chạy script COMMIT_COMMANDS.sh"