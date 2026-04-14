# Quick Start Guide — Lab Day 09

Hướng dẫn nhanh để chạy toàn bộ lab trong 10 phút.

## Bước 1: Setup môi trường (2 phút)

```bash
# 1. Cài dependencies
pip install -r requirements.txt

# 2. Tạo file .env và điền API key
cp .env.example .env
# Mở .env và điền OPENAI_API_KEY của bạn
```

## Bước 2: Build ChromaDB index (2 phút)

```bash
python build_index.py
```

Output mong đợi:
```
✓ Created collection 'day09_docs'
✓ Model loaded
✓ Indexed 5 documents
✅ Index built successfully!
```

## Bước 3: Test graph (1 phút)

```bash
python graph.py
```

Output mong đợi:
```
▶ Query: SLA xử lý ticket P1 là bao lâu?
  Route   : retrieval_worker
  Reason  : task contains SLA/ticket keywords
  Workers : ['retrieval_worker', 'synthesis_worker']
  Answer  : Ticket P1 có SLA phản hồi ban đầu 15 phút...
  Confidence: 0.92
  Latency : 1234ms
  Trace saved → artifacts/traces/run_20260414_143211.json
```

## Bước 4: Chạy evaluation với 15 test questions (3 phút)

```bash
python eval_trace.py
```

Output mong đợi:
```
📋 Running 15 test questions from data/test_questions.json
[01/15] q01: SLA xử lý ticket P1 là bao lâu?...
  ✓ route=retrieval_worker, conf=0.92, 1234ms
[02/15] q02: Khách hàng có thể yêu cầu hoàn tiền trong bao nhiêu ngày?...
  ✓ route=retrieval_worker, conf=0.88, 1456ms
...
✅ Done. 15 / 15 succeeded.

📊 Trace Analysis:
  total_traces: 15
  routing_distribution:
    retrieval_worker: 9/15 (60%)
    policy_tool_worker: 6/15 (40%)
  avg_confidence: 0.82
  avg_latency_ms: 1850
```

## Bước 5: Fill documentation templates (1 phút)

```bash
python fill_docs.py
```

Output:
```
✓ Filled: docs/system_architecture.md
✓ Filled: docs/routing_decisions.md
✓ Filled: docs/single_vs_multi_comparison.md
✅ All documentation templates filled!
```

## Bước 6: Review kết quả (1 phút)

```bash
# Xem traces
ls artifacts/traces/

# Xem eval report
cat artifacts/eval_report.json

# Xem docs đã fill
cat docs/system_architecture.md
```

---

## Chạy grading questions (sau 17:00)

Khi file `data/grading_questions.json` được public lúc 17:00:

```bash
python eval_trace.py --grading
```

Output:
```
🎯 Running GRADING questions — 10 câu
   Output → artifacts/grading_run.jsonl
[01/10] gq01: Ticket P1 được tạo lúc 22:47...
  ✓ route=retrieval_worker, conf=0.91
...
✅ Grading log saved → artifacts/grading_run.jsonl
```

**Deadline nộp:** 18:00 — commit `artifacts/grading_run.jsonl` trước giờ này!

---

## Chạy tất cả trong 1 lệnh

```bash
python run_all.py
```

Script này sẽ chạy:
1. Build index
2. Test graph
3. Run evaluation
4. Analyze traces
5. Compare single vs multi

---

## Troubleshooting

### Lỗi: "No module named 'sentence_transformers'"
```bash
pip install sentence-transformers
```

### Lỗi: "No module named 'openai'"
```bash
pip install openai
```

### Lỗi: "OPENAI_API_KEY not found"
Mở file `.env` và điền API key:
```
OPENAI_API_KEY=sk-...
```

### Lỗi: "Collection 'day09_docs' not found"
Chạy lại:
```bash
python build_index.py
```

### Graph chạy nhưng answer là "[SYNTHESIS ERROR]"
Kiểm tra API key trong `.env` có đúng không.

---

## Checklist nộp bài

- [ ] Code chạy được: `python graph.py`
- [ ] Evaluation chạy được: `python eval_trace.py`
- [ ] Có traces trong `artifacts/traces/`
- [ ] Có `artifacts/grading_run.jsonl` (sau 17:00)
- [ ] Docs đã fill: `docs/*.md`
- [ ] Group report: `reports/group_report.md`
- [ ] Individual reports: `reports/individual/[ten].md`

**Deadline code:** 18:00  
**Deadline reports:** Sau 18:00 được phép

---

## Điểm thưởng (Bonus)

- [ ] Implement real MCP HTTP server (+2 điểm)
- [ ] Confidence score thực tế không hard-code (+1 điểm)
- [ ] Câu gq09 đạt Full marks + trace đúng (+2 điểm)

---

Chúc các bạn làm bài tốt! 🚀
