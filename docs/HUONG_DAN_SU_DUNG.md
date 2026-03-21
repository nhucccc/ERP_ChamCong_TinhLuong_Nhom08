# HƯỚNG DẪN SỬ DỤNG HỆ THỐNG CHẤM CÔNG & TÍNH LƯƠNG

> Đọc từ trên xuống theo thứ tự. Mỗi bước đều có lệnh kiểm thử cụ thể.

---

## PHẦN 1: KHỞI ĐỘNG HỆ THỐNG

### Bước 1 - Chạy Docker

```bash
docker-compose up -d
```

Kiểm tra container đã chạy chưa:
```bash
docker ps
```

Kết quả mong đợi - 3 container đang `Up`:
```
erp_chamcong_tinhluong_nhom08-odoo-1      Up  0.0.0.0:8069->8069/tcp
erp_chamcong_tinhluong_nhom08-db-1        Up  0.0.0.0:5432->5432/tcp
erp_chamcong_tinhluong_nhom08-pgadmin-1   Up  0.0.0.0:5050->80/tcp
```

Theo dõi log nếu Odoo chưa sẵn sàng:
```bash
docker logs -f erp_chamcong_tinhluong_nhom08-odoo-1
# Chờ đến khi thấy: "HTTP service (werkzeug) running on 0.0.0.0:8069"
```

### Bước 2 - Đăng nhập

- URL: http://localhost:8069
- Database: `odoo_test`
- Username: `admin`
- Password: `admin`

### Bước 3 - Migrate module (khi vừa pull code mới)

```bash
docker exec erp_chamcong_tinhluong_nhom08-odoo-1 \
  odoo -c /etc/odoo/odoo.conf \
  -u nhan_su_cham_cong_luong \
  -d odoo_test \
  --stop-after-init

docker-compose restart odoo
```

---

## PHẦN 2: CHUẨN BỊ DỮ LIỆU NỀN (làm 1 lần)

### 2.1. Tạo nhân viên

**Đường dẫn:** Menu `Nhân viên` → `Nhân viên` → nút `Mới`

Điền các trường:

| Trường | Giá trị ví dụ |
|---|---|
| Tên nhân viên | Nguyễn Văn Test |
| Chức vụ | Developer |
| Phòng ban | Phòng Kỹ thuật |
| Email công việc | test@techsoft.vn |

Nhấn `Lưu`.

**Kiểm thử:** Danh sách nhân viên phải hiện bản ghi vừa tạo.

### 2.2. Tạo hợp đồng lao động

Không có hợp đồng → không tính được lương.

**Đường dẫn:** Mở form nhân viên → tab `Thông tin công việc` → nút `Hợp đồng` (góc trên phải) → `Mới`

| Trường | Giá trị |
|---|---|
| Mã hợp đồng | HD-2026-001 |
| Ngày bắt đầu | 01/01/2026 |
| Ngày kết thúc | (để trống = không thời hạn) |
| Lương | 15,000,000 |
| Trạng thái hợp đồng | Đang chạy |

Nhấn `Lưu`.

**Kiểm thử:** Quay lại form nhân viên, nút `Hợp đồng` phải hiện số `1`.

### 2.3. Tạo dữ liệu chấm công thủ công (để test)

**Đường dẫn:** Menu `Chấm công` → `Chấm công` → `Mới`

Tạo các bản ghi sau để có đủ kịch bản test:

| Nhân viên | Giờ vào | Giờ ra | Kịch bản |
|---|---|---|---|
| Nguyễn Văn Test | 03/01/2026 09:00 | 03/01/2026 17:30 | Đi muộn 30 phút |
| Nguyễn Văn Test | 03/02/2026 08:20 | 03/02/2026 20:00 | Đúng giờ + tăng ca 2.5h |
| Nguyễn Văn Test | 03/03/2026 08:30 | 03/03/2026 16:00 | Về sớm 90 phút |
| Nguyễn Văn Test | 03/04/2026 08:30 | 03/04/2026 17:30 | Bình thường |
| Nguyễn Văn Test | 03/05/2026 08:30 | 03/05/2026 17:30 | Bình thường |

> Odoo lưu giờ theo UTC. Nếu server đặt timezone UTC+7, nhập giờ bình thường, Odoo tự chuyển đổi.
  
**Kiểm thử:** Mở từng bản ghi, kéo xuống phần `Phân tích kỷ luật & Tăng ca`:
- Bản ghi vào 09:00 → `Đi muộn = True`, `Phút muộn = 30`
- Bản ghi ra 20:00 → `Có tăng ca = True`, `Giờ tăng ca = 2.5`
- Bản ghi ra 16:00 → `Về sớm = True`, `Phút về sớm = 90`

---

## PHẦN 3: CHỨC NĂNG CHẤM CÔNG

### 3.1. Xem chi tiết một ngày chấm công

**Đường dẫn:** `Chấm công` → `Chấm công` → click vào bản ghi bất kỳ

Các trường tự động tính trong phần `Phân tích kỷ luật & Tăng ca`:

| Trường hiển thị | Ý nghĩa | Điều kiện |
|---|---|---|
| Đi muộn | Check-in sau 08:30 | True/False |
| Phút muộn | Số phút trễ | Khi đi muộn |
| Về sớm | Check-out trước 17:30 | True/False |
| Phút về sớm | Số phút thiếu | Khi về sớm |
| Có tăng ca | Làm thêm ≥30 phút sau 17:30 | True/False |
| Giờ tăng ca | Số giờ làm thêm | Khi có tăng ca |
| Hệ số tăng ca | 1.5 ngày thường / 2.0 cuối tuần | Khi có tăng ca |
| Tổng phút vi phạm | Phút muộn + phút về sớm | Luôn hiển thị |

### 3.2. Tạo bảng chấm công tháng

**Cách 1 - Thủ công qua Wizard:**

`Chấm công & Lương` → `Cấu hình` → `Tạo bảng chấm công & lương`

- Chọn tháng: `3`, năm: `2026`
- Nhấn `Tạo`

**Cách 2 - Tự động qua Cron Job** (xem Phần 6)

**Kiểm thử:** Vào `Chấm công & Lương` → `Chấm công` → `Bảng chấm công theo tháng` → phải thấy bản ghi tháng 3/2026 với:
- `Số ngày làm việc` = số ngày có bản ghi chấm công
- `Số ngày công chuẩn` = số ngày trong tháng trừ Chủ nhật
- Trạng thái = `Nháp`

---

## PHẦN 4: CHỨC NĂNG TÍNH LƯƠNG

### 4.1. Tạo bảng lương tháng

**Đường dẫn:** `Chấm công & Lương` → `Lương` → `Bảng lương theo tháng` → `Mới`

| Trường | Giá trị |
|---|---|
| Nhân viên | Nguyễn Văn Test |
| Tháng | 3 |
| Năm | 2026 |

Nhấn `Lưu`. Hệ thống tự động điền:
- `Bảng chấm công` → liên kết bảng CC tháng 3/2026
- `Hợp đồng lao động` → hợp đồng đang active
- `Lương cơ bản/tháng` → lấy từ hợp đồng (15,000,000đ)

### 4.2. Tính lương

Nhấn nút `Tính lương` trên thanh header.

Hệ thống tính toán và điền đầy đủ các nhóm:

**Nhóm "Dữ liệu chấm công":**

| Trường | Ý nghĩa |
|---|---|
| Số ngày công chuẩn | Ngày chuẩn của tháng (trừ CN) |
| Tổng ngày công | Số bản ghi attendance trong tháng |
| Số ngày làm việc | Từ bảng chấm công |
| Tỷ lệ công | Ngày làm / Ngày chuẩn × 100% |

**Nhóm "Tính lương":**

| Trường | Công thức |
|---|---|
| Lương cơ bản/tháng | Từ hợp đồng |
| Lương theo giờ | Lương CB / (Ngày chuẩn × 8h) |
| Lương theo ngày công | Lương CB × Tỷ lệ công |

**Nhóm "Tăng ca"** (chỉ hiện khi có tăng ca):

| Trường | Công thức |
|---|---|
| Giờ tăng ca ngày thường | Tổng từ attendance |
| Giờ tăng ca cuối tuần | Tổng từ attendance |
| Tiền tăng ca | (TC thường × 1.5 + TC CT × 2.0) × lương/giờ |

**Nhóm "Kỷ luật"** (chỉ hiện khi có vi phạm):

| Trường | Công thức |
|---|---|
| Số lần vi phạm | Đếm bản ghi có đi muộn hoặc về sớm |
| Tổng phút vi phạm | Tổng phút muộn + phút về sớm |
| Tiền phạt kỷ luật | Tổng phút × 5.000đ |

**Nhóm "Giảm trừ gia cảnh (GTGC)":**

| Trường | Công thức |
|---|---|
| Số người phụ thuộc | Đếm NPT đã đăng ký còn hiệu lực |
| Tổng giảm trừ gia cảnh | 11.000.000 + NPT × 4.400.000 |
| BHXH/BHYT/BHTN (NV đóng) | Lương CB × 10.5% |
| Thu nhập chịu thuế | Tổng thu nhập - BHXH |
| Thu nhập tính thuế | TNCT - GTGC (tối thiểu 0) |
| Thuế TNCN | Lũy tiến 7 bậc |

**Nhóm "Tổng kết":**
- `Lương thực lãnh` = Lương ngày công + Tăng ca + Phụ cấp - Phạt - BHXH - Thuế - Khấu trừ

**Kiểm thử với dữ liệu mẫu (5 ngày công, 1 lần muộn 30 phút, 2.5h tăng ca, 0 NPT):**
```
Lương/giờ = 15,000,000 / (26 × 8) = 72,115đ/h
Lương ngày công = 15,000,000 × (5/26)  =  2,884,615đ  [+]
Tăng ca = 2.5h × 1.5 × 72,115         =    270,433đ  [+]
Phạt = 30 phút × 5,000                =    150,000đ  [-]
BHXH = 15,000,000 × 10.5%             =  1,575,000đ  [-]
GTGC = 11,000,000 (0 NPT) → TNTT = âm → Thuế = 0đ
─────────────────────────────────────────────────────
THỰC LÃNH                              =  1,430,048đ
```

### 4.3. Xem chi tiết phiếu lương

Tab `Chi tiết phiếu lương` hiện danh sách các dòng màu xanh (cộng) / đỏ (trừ):

| Tên dòng | Loại |
|---|---|
| Lương cơ bản theo ngày công (5/26 ngày = 19.2%) | Cộng |
| Tăng ca ngày thường (2.50h × 1.5 × 72,115đ/h) | Cộng |
| Phạt kỷ luật (1 lần, 30 phút × 5,000đ/phút) | Trừ |
| BHXH/BHYT/BHTN (10.5% × 15,000,000đ) | Trừ |

### 4.4. Thêm người phụ thuộc (NPT)

NPT làm tăng giảm trừ gia cảnh → giảm thuế TNCN.

**Đường dẫn:** Form nhân viên → tab `Người phụ thuộc (GTGC)` → thêm dòng mới

| Trường | Giá trị |
|---|---|
| Họ tên | Nguyễn Thị Con |
| Quan hệ | Con |
| Ngày sinh | 15/06/2020 |
| Đã đăng ký | ✅ bật toggle |
| Ngày bắt đầu | 01/01/2026 |

Nhấn `Lưu`, sau đó quay lại bảng lương → nhấn `Đưa về nháp` → nhấn `Tính lương` lại.

**Kiểm thử:** `Số người phụ thuộc` = 1, `Tổng giảm trừ gia cảnh` = 15,400,000đ.

### 4.5. Luồng trạng thái bảng lương

```
Nháp  ──[Tính lương]──▶  Đã tính  ──[Xác nhận]──▶  Đã xác nhận  ──[Đánh dấu đã trả]──▶  Đã thanh toán
  ◀──────────────────────────────────[Đưa về nháp]──────────────────────────────────────────
```

---

## PHẦN 5: TÍNH NĂNG AI - GOOGLE GEMINI

### 5.1. Cấu hình API Key (làm 1 lần)

**Đường dẫn:** `Cài đặt` → `Kỹ thuật` → `Thông số` → `Thông số hệ thống` → `Mới`

| Trường | Giá trị |
|---|---|
| Khóa | `nhan_su_cham_cong_luong.gemini_api_key` |
| Giá trị | `[API Key của bạn]` |

Lấy API Key miễn phí: https://aistudio.google.com/app/apikey

### 5.2. Sử dụng phân tích AI

**Điều kiện:** Bảng lương phải ở trạng thái `Đã tính` hoặc `Đã xác nhận`.

**Đường dẫn:** Mở form bảng lương → nhấn nút `🤖 Phân tích AI` trên header

Hệ thống gửi dữ liệu lên Gemini 2.5 Flash và trả về phân tích 4 chiều trong phần `🤖 Kết quả phân tích AI` ở cuối form:

```
1. ĐÁNH GIÁ CHUYÊN CẦN
Nhân viên đạt 84.6% ngày công, có 1 lần đi muộn 30 phút.
Mức độ chuyên cần ở ngưỡng chấp nhận được, cần nhắc nhở nhẹ.

2. ĐÁNH GIÁ HIỆU SUẤT
Có 2.5 giờ tăng ca cho thấy tinh thần trách nhiệm với công việc.

3. XU HƯỚNG SO SÁNH
Chưa đủ dữ liệu lịch sử để so sánh xu hướng.

4. ĐỀ XUẤT CHO HR
Theo dõi thêm 2-3 tháng. Xem xét khen thưởng nếu duy trì hiệu suất.
```

**Kiểm thử lỗi:** Nếu chưa cấu hình API Key → hệ thống hiện thông báo lỗi hướng dẫn cụ thể.

---

## PHẦN 6: TỰ ĐỘNG HÓA - CRON JOB

### 6.1. Xem danh sách Cron Job

**Đường dẫn:** `Cài đặt` → `Kỹ thuật` → `Tự động hóa` → `Hành động theo lịch`

Tìm 3 job của module:
- `Tạo bảng chấm công tháng mới`
- `Tạo bảng lương tháng mới`
- `Tính lương tự động ngày 5`

### 6.2. Chạy thủ công để test

Click vào từng Cron Job → nhấn nút `Chạy thủ công` (góc trên).

**Thứ tự bắt buộc:**
1. `Tạo bảng chấm công tháng mới`
2. `Tạo bảng lương tháng mới`
3. `Tính lương tự động ngày 5`

**Kiểm thử:** Vào `Lương` → `Bảng lương theo tháng` → phải thấy bảng lương mới trạng thái `Đã tính`.

### 6.3. Điều chỉnh lịch chạy

Click vào Cron Job → sửa trường `Lần thực thi tiếp theo` để test với ngày cụ thể.

---

## PHẦN 7: EXTERNAL API - GIẢ LẬP MÁY CHẤM CÔNG

Script `external_api/cham_cong_client.py` kết nối Odoo qua XML-RPC, giả lập máy chấm công vật lý.

### 7.1. Liệt kê nhân viên

```bash
python external_api/cham_cong_client.py --list
```

Kết quả mẫu:
```
✅ Kết nối thành công! UID=2
ID     Tên                            Chức vụ              Phòng ban
----------------------------------------------------------------------
3      Nguyễn Văn Test                Developer            Phòng Kỹ thuật
```

### 7.2. Check-in

```bash
python external_api/cham_cong_client.py --checkin 3
```

```
✅ Check-in thành công! Bản ghi ID=42, thời gian=2026-03-21 02:30:00
```

**Kiểm thử:** Vào `Chấm công` → `Chấm công` → phải thấy bản ghi mới, cột `Giờ ra` trống.

### 7.3. Check-out

```bash
python external_api/cham_cong_client.py --checkout 3
```

**Kiểm thử:** Bản ghi được cập nhật `Giờ ra`, các trường `Đi muộn`, `Có tăng ca` tự động tính.

### 7.4. Demo đầy đủ tự động

```bash
python external_api/cham_cong_client.py
```

Tự động: liệt kê nhân viên → hiển thị chấm công tháng → hiển thị bảng lương.

### 7.5. Kết nối server khác

```bash
python external_api/cham_cong_client.py \
  --url http://192.168.1.100:8069 \
  --db odoo_test \
  --user admin \
  --password admin \
  --list
```

---

## PHẦN 8: KIỂM THỬ TOÀN BỘ LUỒNG END-TO-END

### Bước 1 - Chuẩn bị
```
✅ Tạo nhân viên "Nguyễn Văn Test"
✅ Tạo hợp đồng 15,000,000đ/tháng (trạng thái "Đang chạy")
✅ Thêm 1 NPT trong tab "Người phụ thuộc (GTGC)"
```

### Bước 2 - Chấm công qua External API
```bash
python external_api/cham_cong_client.py --checkin 3
python external_api/cham_cong_client.py --checkout 3
```

### Bước 3 - Tạo bảng chấm công
```
Chấm công & Lương → Cấu hình → Tạo bảng chấm công & lương → Tháng 3/2026 → Tạo
```

### Bước 4 - Tạo và tính bảng lương
```
Lương → Bảng lương theo tháng → Mới → Chọn nhân viên + tháng 3/2026 → Lưu → Tính lương
```

### Bước 5 - Kiểm tra kết quả
```
✅ Số lần vi phạm = 1, Tổng phút vi phạm = 30, Tiền phạt = 150,000đ
✅ Giờ tăng ca ngày thường > 0, Tiền tăng ca > 0
✅ Số người phụ thuộc = 1, Tổng GTGC = 15,400,000đ
✅ Tab "Chi tiết phiếu lương" có đủ các dòng cộng/trừ
```

### Bước 6 - Phân tích AI
```
Nhấn nút "🤖 Phân tích AI" → Xem kết quả trong phần "🤖 Kết quả phân tích AI"
```

### Bước 7 - Xác nhận và thanh toán
```
Nhấn "Xác nhận" → trạng thái = Đã xác nhận
Nhấn "Đánh dấu đã trả" → trạng thái = Đã thanh toán
```

---

## PHẦN 9: CÁC LỖI THƯỜNG GẶP

| Lỗi | Nguyên nhân | Cách xử lý |
|---|---|---|
| Lương cơ bản = 0 | Chưa có hợp đồng trạng thái "Đang chạy" | Tạo hợp đồng, đặt trạng thái `Đang chạy` |
| Không phát hiện đi muộn dù vào 09:00 | Timezone server sai | Kiểm tra timezone Odoo, phải là UTC+7 |
| Bảng chấm công không tạo được | Nhân viên không có hợp đồng active | Kiểm tra hợp đồng |
| Gemini API lỗi 404 | Sai tên model | Đảm bảo dùng `gemini-2.5-flash` |
| Gemini API lỗi 403 | API Key sai hoặc hết quota | Kiểm tra lại key tại aistudio.google.com |
| XML-RPC `ConnectionRefused` | Odoo chưa chạy | Kiểm tra `docker ps` |
| Cron Job không tự chạy | `Đang hoạt động = False` | Vào `Hành động theo lịch` → bật `Đang hoạt động` |
| Module không tìm thấy sau pull code | Chưa migrate | Chạy lệnh migrate ở Bước 3 Phần 1 |

---

*Hệ thống Chấm công & Tính lương - Nhóm 08 - FIT-DNU*
