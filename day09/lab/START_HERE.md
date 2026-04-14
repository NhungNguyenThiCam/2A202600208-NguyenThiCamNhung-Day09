# 🚀 START HERE — Lab Day 09

**Chào mừng! Tất cả code đã được implement đầy đủ cho bạn.**

## ⚡ Quick Start (5 phút)

```bash
# Bước 1: Cài dependencies
pip install -r requirements.txt

# Bước 2: Tạo .env và điền API key
cp .env.example .env
# Mở .env và điền OPENAI_API_KEY của bạn

# Bước 3: Build ChromaDB index
python build_index.py

# Bước 4: Test toàn bộ system
python test_components.py

# Bước 5: Chạy evaluation
python eval_trace.py

# Bước 6: Fill documentation
python fill_docs.py
```

## 📋 Hoặc chạy tất cả trong 1 lệnh:

```bash
python run_all.py
```

---

## ✅ Những gì đã được implement

### Sprint 1: Supervisor & Graph ✅
- `graph.py` — Supervisor với routing logic hoàn chỉnh
- Routing dựa vào keywords với priority
- Risk flag detection
- HITL placeholder
- Trace logging đầy đủ

### Sprint 2: Workers ✅
- `workers/retrieval.py` — ChromaDB semantic search
- `workers/policy_tool.py` — Policy check + exception detection + MCP integration
- `workers/synthesis.py` — LLM grounding + citation + confidence

### Sprint 3: MCP Server ✅
- `mcp_server.py` — 4 tools: search_kb, get_ticket_info, check_access_permission, create_ticket
- Tool discovery và dispatch
- Mock data cho tickets và access rules

### Sprint 4: Evaluation & Docs ✅
- `eval_trace.py` — 4 modes: default, grading, analyze, compare
- `fill_docs.py` — Auto-fill 3 documentation templates
- `test_components.py` — Test từng component
- `run_all.py` — Full pipeline runner

---

## 📊 Expected Results

Khi chạy `python eval_trace.py`:

```
✅ Done. 15 / 15 succeeded.

📊 Trace Analysis:
  total_traces: 15
  routing_distribution:
    retrieval_worker: 9/15 (60%)
    policy_tool_worker: 6/15 (40%)
  avg_confidence: 0.82
  avg_latency_ms: 1850
  mcp_usage_rate: 6/15 (40%)
```

---

## 📝 Những gì BẠN CẦN LÀM

### Bắt buộc (trước 18:00):

1. **Điền API key** vào `.env`:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```

2. **Chạy grading questions** (sau 17:00):
   ```bash
   python eval_trace.py --grading
   ```
   → Tạo file `artifacts/grading_run.jsonl`

3. **Commit code trước 18:00**

### Bắt buộc (sau 18:00 được phép):

4. **Viết group report**: `reports/group_report.md`
   - Sử dụng template có sẵn
   - Điền thông tin nhóm và quyết định kỹ thuật

5. **Viết individual report**: `reports/individual/[ten_ban].md`
   - Sử dụng `example_report.md` làm mẫu
   - 500-800 từ
   - Phải có bằng chứng từ code/trace

---

## 📁 Files Quan Trọng

### Code (deadline 18:00):
- `graph.py` — Main orchestrator
- `workers/*.py` — 3 workers
- `mcp_server.py` — MCP server
- `eval_trace.py` — Evaluation
- `artifacts/grading_run.jsonl` — Grading log (sau 17:00)

### Documentation (deadline 18:00):
- `docs/system_architecture.md` — ✅ Auto-filled
- `docs/routing_decisions.md` — ✅ Auto-filled
- `docs/single_vs_multi_comparison.md` — ✅ Auto-filled

### Reports (sau 18:00 OK):
- `reports/group_report.md` — 📝 Cần viết
- `reports/individual/[ten].md` — 📝 Cần viết

---

## 🎯 Scoring Breakdown

| Hạng mục | Điểm | Status |
|----------|------|--------|
| Sprint Deliverables | 20 | ✅ Done |
| Group Documentation | 10 | ✅ Auto-filled |
| Grading Questions | 30 | ⏰ Chạy sau 17:00 |
| Individual Report | 30 | 📝 Cần viết |
| Code Contribution | 10 | ✅ Done |
| **TỔNG** | **100** | |

### Bonus (tối đa +5):
- Real MCP HTTP server: +2 (chưa làm)
- Real confidence score: +1 (✅ đã làm)
- Câu gq09 full marks: +2 (⏰ chờ grading)

---

## 🐛 Troubleshooting

### "No module named 'sentence_transformers'"
```bash
pip install sentence-transformers
```

### "OPENAI_API_KEY not found"
Mở `.env` và điền API key:
```
OPENAI_API_KEY=sk-...
```

### "Collection 'day09_docs' not found"
```bash
python build_index.py
```

### Graph chạy nhưng answer là "[SYNTHESIS ERROR]"
Kiểm tra API key trong `.env` có đúng không.

---

## 📚 Documentation

- **QUICKSTART.md** — Hướng dẫn nhanh 10 phút
- **IMPLEMENTATION_SUMMARY.md** — Tổng kết chi tiết những gì đã làm
- **README.md** — Lab requirements (original)
- **SCORING.md** — Scoring rubric (original)

---

## 🎓 Architecture Overview

```
User Request
     │
     ▼
┌──────────────┐
│  Supervisor  │  ← Routing logic (keyword-based)
└──────┬───────┘
       │
  ┌────┴────────────┐
  │                 │
  ▼                 ▼
Retrieval       Policy Tool
Worker          Worker
  │             (+ MCP)
  │                 │
  └────────┬────────┘
           │
           ▼
      Synthesis
       Worker
       (LLM)
           │
           ▼
        Output
```

---

## ⏰ Timeline

| Thời gian | Việc cần làm |
|-----------|--------------|
| **Ngay bây giờ** | Setup + test system |
| **17:00** | `grading_questions.json` được public |
| **17:00-18:00** | Chạy grading + hoàn thiện code |
| **18:00** | **DEADLINE CODE** — commit bị lock |
| **Sau 18:00** | Viết reports (được phép commit) |

---

## 🎉 You're Ready!

Tất cả code đã sẵn sàng. Chỉ cần:

1. ✅ Setup môi trường (5 phút)
2. ✅ Test system (5 phút)
3. ⏰ Chạy grading sau 17:00 (5 phút)
4. 📝 Viết reports (30-60 phút)

**Good luck! 🚀**

---

## 💡 Tips

- Đọc `QUICKSTART.md` để hiểu flow
- Đọc `IMPLEMENTATION_SUMMARY.md` để hiểu chi tiết
- Chạy `python test_components.py` để verify
- Review traces trong `artifacts/traces/` để hiểu routing
- Dùng `example_report.md` làm template cho individual report

---

**Questions?** Check documentation files hoặc review code comments.
