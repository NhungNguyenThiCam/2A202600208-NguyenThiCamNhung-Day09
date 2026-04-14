# Báo Cáo Cá Nhân — Lab Day 09: Multi-Agent Orchestration

**Họ và tên:** [Tên của bạn]  
**Vai trò trong nhóm:** [Supervisor Owner / Worker Owner / MCP Owner / Trace & Docs Owner]  
**Ngày nộp:** [YYYY-MM-DD]  
**Độ dài:** [số từ] từ

---

## 1. Tôi phụ trách phần nào? (100-150 từ)

**Module/file tôi chịu trách nhiệm:**
- **File chính:** [tên file, ví dụ: graph.py, workers/policy_tool.py]
- **Functions tôi implement:** [tên functions, lines]

**Mô tả chi tiết:**
[Viết 2-3 câu mô tả cụ thể bạn làm gì trong file đó]

**Cách công việc của tôi kết nối với phần của thành viên khác:**
[Giải thích phần của bạn phụ thuộc vào ai, và ai phụ thuộc vào phần của bạn]

**Bằng chứng:**
- Code comments: [dòng nào có tên bạn]
- Trace files: [file nào chứng minh phần bạn làm]
- Test: [command test nào chạy được]

---

## 2. Tôi đã ra một quyết định kỹ thuật gì? (150-200 từ)

**Quyết định:** [Tên quyết định ngắn gọn]

**Các lựa chọn thay thế:**
1. **Option A (đã chọn):** [Mô tả]
2. **Option B:** [Mô tả]
3. **Option C:** [Mô tả]

**Tại sao tôi chọn cách này:**

**Lý do chính:**
- [Lý do 1: performance, cost, accuracy, etc.]
- [Lý do 2]
- [Lý do 3]

**Trade-off đã chấp nhận:**
- [Nhược điểm của quyết định này]
- [Tại sao chấp nhận được]

**Bằng chứng từ trace:**

```json
// Paste trace từ artifacts/traces/
{
  "task": "...",
  "supervisor_route": "...",
  "route_reason": "...",
  "latency_ms": ...
}
```

**Code evidence:**

```python
# Paste đoạn code liên quan
```

---

## 3. Tôi đã sửa một lỗi gì? (150-200 từ)

**Lỗi:** [Mô tả ngắn gọn lỗi gì]

**Symptom:**
[Pipeline làm gì sai? Error message là gì?]

```
[Paste error message nếu có]
```

**Root cause:**
[Lỗi nằm ở đâu? Tại sao xảy ra?]

**Cách sửa:**

```python
# Before
[code cũ]

# After
[code mới]
```

**Bằng chứng trước/sau:**

**Trước khi sửa:**
```
[Output hoặc error trước khi sửa]
```

**Sau khi sửa:**
```
[Output thành công sau khi sửa]
```

**Impact:** [Ảnh hưởng của fix này đến hệ thống]

---

## 4. Tôi tự đánh giá đóng góp của mình (100-150 từ)

**Tôi làm tốt nhất ở điểm nào?**
- [Điểm mạnh 1]
- [Điểm mạnh 2]

**Tôi làm chưa tốt hoặc còn yếu ở điểm nào?**
- [Điểm yếu 1]
- [Điểm yếu 2]

**Nhóm phụ thuộc vào tôi ở đâu?**
[Phần nào của hệ thống bị block nếu bạn chưa xong?]

**Phần tôi phụ thuộc vào thành viên khác:**
[Bạn cần gì từ ai để tiếp tục được?]

---

## 5. Nếu có thêm 2 giờ, tôi sẽ làm gì? (50-100 từ)

**Cải tiến:** [Tên cải tiến cụ thể]

**Lý do từ trace:**
[Dẫn chứng từ trace hoặc metrics cụ thể]

```json
// Trace evidence
{
  "question_id": "q04",
  "confidence": 0.78,
  "issue": "..."
}
```

**Cách implement:**
1. [Bước 1]
2. [Bước 2]
3. [Bước 3]

**Expected impact:** [Kết quả mong đợi với số liệu cụ thể]

---

*File này lưu tại: `reports/individual/[ten_ban].md`*  
*Commit sau 18:00 được phép theo SCORING.md*
