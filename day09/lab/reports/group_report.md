# Báo Cáo Nhóm — Lab Day 09: Multi-Agent Orchestration

**Tên nhóm:** Solo Implementation  
**Thành viên:**
| Tên | Vai trò | Email |
|-----|---------|-------|
| Nguyễn Thị Cẩm Nhung | Full-stack (All roles) | 2A202600208 |

**Ngày nộp:** 14/04/2026  
**Repo:** day09/lab  
**Độ dài khuyến nghị:** 600–1000 từ

---

> **Hướng dẫn nộp group report:**
> 
> - File này nộp tại: `reports/group_report.md`
> - Deadline: Được phép commit **sau 18:00** (xem SCORING.md)
> - Tập trung vào **quyết định kỹ thuật cấp nhóm** — không trùng lặp với individual reports
> - Phải có **bằng chứng từ code/trace** — không mô tả chung chung
> - Mỗi mục phải có ít nhất 1 ví dụ cụ thể từ code hoặc trace thực tế của nhóm

---

## 1. Kiến trúc nhóm đã xây dựng (150–200 từ)

> Mô tả ngắn gọn hệ thống nhóm: bao nhiêu workers, routing logic hoạt động thế nào,
> MCP tools nào được tích hợp. Dùng kết quả từ `docs/system_architecture.md`.

**Hệ thống tổng quan:**

Hệ thống multi-agent orchestration với 1 supervisor node và 3 specialized workers:
- **Retrieval Worker**: Xử lý câu hỏi tra cứu thông tin từ knowledge base (ChromaDB với 77 chunks từ 5 documents)
- **Policy Tool Worker**: Xử lý câu hỏi về policy logic phức tạp (refund, access control, SLA exceptions) với MCP tool integration
- **Synthesis Worker**: Tổng hợp kết quả từ nhiều workers và gọi LLM để tạo câu trả lời cuối cùng

Supervisor sử dụng StateGraph từ LangGraph để orchestrate workflow, với conditional routing dựa trên task classification.

**Routing logic cốt lõi:**

Supervisor dùng **keyword-based routing** với pattern matching:
- Nếu task chứa keywords như "SLA", "ticket", "P1", "lỗi", "ERR-" → route đến `retrieval_worker`
- Nếu task chứa keywords như "hoàn tiền", "refund", "cấp quyền", "access", "Level" → route đến `policy_tool_worker`
- Nếu không match → mặc định route đến `retrieval_worker`

Logic này nhanh (~5ms) và đủ chính xác cho 5 categories, tránh overhead của LLM classifier (~800ms).

**MCP tools đã tích hợp:**

- `search_kb`: Tìm kiếm semantic trong knowledge base, được gọi bởi policy_tool_worker khi cần context bổ sung
- `get_ticket_info`: Lấy thông tin chi tiết ticket từ hệ thống ticketing (mock data với ticket ID, priority, timestamps)
- `check_access_permission`: Kiểm tra quyền truy cập dựa trên role, level, và business rules (contractor restrictions, emergency access)
- `check_refund_eligibility`: Kiểm tra điều kiện hoàn tiền với logic phức tạp (purchase date, product type, flash sale exceptions)

Ví dụ trace có gọi MCP: `q13` (contractor cần Level 3 access) → policy_tool_worker gọi `check_access_permission` → trả về `can_grant=False` do contractor không được cấp Level 3.

---

## 2. Quyết định kỹ thuật quan trọng nhất (200–250 từ)

> Chọn **1 quyết định thiết kế** mà nhóm thảo luận và đánh đổi nhiều nhất.
> Phải có: (a) vấn đề gặp phải, (b) các phương án cân nhắc, (c) lý do chọn phương án đã chọn.

**Quyết định:** Keyword-based routing vs LLM-based classifier trong supervisor node

**Bối cảnh vấn đề:**

Supervisor cần classify task để route đến worker phù hợp. Với 15 test questions và 5 document categories, cần balance giữa accuracy và latency. Nếu routing sai, toàn bộ pipeline sẽ trả lời sai hoặc phải retry.

**Các phương án đã cân nhắc:**

| Phương án | Ưu điểm | Nhược điểm |
|-----------|---------|-----------|
| LLM classifier (gọi GPT-4 để classify) | Accuracy cao (~95%), hiểu context phức tạp | Latency cao (~800ms), cost cao, phụ thuộc API |
| Keyword matching (regex patterns) | Latency thấp (~5ms), không cost, deterministic | Accuracy thấp hơn (~85%), không hiểu context |
| Hybrid (keyword first, LLM fallback) | Balance tốt | Phức tạp implement, edge cases nhiều |

**Phương án đã chọn và lý do:**

Chọn **keyword matching** vì:
1. Test questions có pattern rõ ràng (SLA/ticket vs policy/access)
2. Latency quan trọng hơn accuracy 5-10% trong lab setting
3. Deterministic behavior dễ debug hơn LLM non-deterministic
4. Không phụ thuộc API key/quota

Trade-off chấp nhận: Có thể miss edge cases như "Ticket P1 cần cấp quyền Level 3" (ambiguous giữa retrieval và policy) → giải quyết bằng cách ưu tiên policy keywords.

**Bằng chứng từ trace/code:**

```python
# graph.py - supervisor_node
def classify_task(task: str) -> str:
    task_lower = task.lower()
    
    # Policy keywords have higher priority
    policy_keywords = ['hoàn tiền', 'refund', 'cấp quyền', 'access', 'level', 'phê duyệt']
    if any(kw in task_lower for kw in policy_keywords):
        return 'policy_tool_worker'
    
    # Retrieval keywords
    retrieval_keywords = ['sla', 'ticket', 'p1', 'lỗi', 'err-', 'quy trình']
    if any(kw in task_lower for kw in retrieval_keywords):
        return 'retrieval_worker'
    
    return 'retrieval_worker'  # default
```

Trace evidence: `q01` route_reason="task contains SLA/ticket keywords", latency=22ms (fast routing)

---

## 3. Kết quả grading questions (150–200 từ)

> Sau khi chạy pipeline với grading_questions.json (public lúc 17:00):
> - Nhóm đạt bao nhiêu điểm raw?
> - Câu nào pipeline xử lý tốt nhất?
> - Câu nào pipeline fail hoặc gặp khó khăn?

**Tổng điểm raw ước tính:** Chưa chạy grading_questions.json (sẽ public lúc 17:00)

**Câu pipeline xử lý tốt nhất (từ test_questions.json):**
- ID: q06 — "Ticket P1 không được phản hồi sau 10 phút. Hệ thống tự động làm gì?"
- Lý do tốt: Confidence 0.77 (cao nhất), routing chính xác đến retrieval_worker, latency 6344ms (acceptable), answer chính xác về auto-escalation policy

**Câu pipeline fail hoặc partial (từ test_questions.json):**
- ID: q09 — "ERR-403-AUTH là lỗi gì và cách xử lý?"
- Fail ở đâu: Confidence thấp nhất (0.44), trigger HITL vì unknown error code
- Root cause: Knowledge base không có document về error code ERR-403-AUTH cụ thể, chỉ có general IT helpdesk FAQ. Retrieval worker không tìm được relevant chunks → synthesis worker phải abstain hoặc give generic answer.

**Câu gq07 (abstain):** Chưa test với grading questions, nhưng pipeline có logic abstain khi confidence < 0.3 hoặc không tìm được relevant sources. Synthesis worker sẽ trả về "[ABSTAIN] Không đủ thông tin để trả lời" thay vì hallucinate.

**Câu gq09 (multi-hop khó nhất):** Chưa test với grading questions. Với test_questions.json, câu q15 (multi-hop: ticket P1 + Level 2 access + contractor + 2am) đã route qua policy_tool_worker → gọi MCP tools (check_access_permission + get_ticket_info) → synthesis_worker tổng hợp → confidence 0.65, acceptable.

---

## 4. So sánh Day 08 vs Day 09 — Điều nhóm quan sát được (150–200 từ)

> Dựa vào `docs/single_vs_multi_comparison.md` — trích kết quả thực tế.

**Metric thay đổi rõ nhất (có số liệu):**

- **Latency**: Day 09 multi-agent có latency trung bình 7533ms, cao hơn Day 08 single-agent (ước tính ~3000-4000ms) do overhead của orchestration và multiple worker calls. Tuy nhiên, latency này acceptable cho complex queries cần multi-hop reasoning.
- **MCP usage**: Day 09 có 46% traces gọi MCP tools, cho phép extend capability mà không cần sửa core code. Day 08 không có MCP integration.
- **Routing visibility**: Day 09 có `route_reason` trong mỗi trace, giúp debug dễ hơn. Day 08 là black box.

**Điều nhóm bất ngờ nhất khi chuyển từ single sang multi-agent:**

HITL (Human-in-the-Loop) trigger rate chỉ 6% (2/30 traces), thấp hơn expected. Ban đầu nghĩ rằng multi-agent sẽ trigger HITL nhiều hơn do complexity, nhưng thực tế keyword routing + specialized workers giảm uncertainty. HITL chỉ trigger khi gặp unknown error codes hoặc edge cases thực sự ambiguous.

**Trường hợp multi-agent KHÔNG giúp ích hoặc làm chậm hệ thống:**

Câu hỏi đơn giản như "SLA xử lý ticket P1 là bao lâu?" (q01) không cần multi-agent complexity. Single-agent với simple retrieval đủ nhanh và chính xác. Multi-agent overhead (supervisor routing + worker coordination) tăng latency từ ~3000ms lên 22060ms (lần đầu chạy, có cold start) hoặc ~6000ms (subsequent runs). Trade-off này chỉ worth it cho complex multi-hop queries.

---

## 5. Phân công và đánh giá nhóm (100–150 từ)

> Đánh giá trung thực về quá trình làm việc nhóm.

**Phân công thực tế:**

| Thành viên | Phần đã làm | Sprint |
|------------|-------------|--------|
| Nguyễn Thị Cẩm Nhung | Supervisor node (graph.py) | Sprint 1 |
| Nguyễn Thị Cẩm Nhung | 3 Workers (retrieval, policy_tool, synthesis) | Sprint 2 |
| Nguyễn Thị Cẩm Nhung | MCP server (4 tools) | Sprint 3 |
| Nguyễn Thị Cẩm Nhung | Trace evaluation + docs | Sprint 4 |

**Điều nhóm làm tốt:**

Làm việc solo nên không có conflict về design decisions. Tất cả components được implement consistent với nhau (naming conventions, error handling, logging format). Documentation được auto-fill đầy đủ. Testing được thực hiện systematic với test_components.py trước khi chạy full pipeline.

**Điều nhóm làm chưa tốt hoặc gặp vấn đề về phối hợp:**

Làm solo nên không có peer review, có thể miss edge cases hoặc best practices. Không có thảo luận nhóm để brainstorm alternative approaches. Time management khó hơn vì phải handle tất cả sprints một mình.

**Nếu làm lại, nhóm sẽ thay đổi gì trong cách tổ chức?**

Nếu có team, sẽ phân công parallel: 1 người làm supervisor + routing logic, 2 người làm workers (mỗi người 1-2 workers), 1 người làm MCP + trace. Như vậy có thể finish nhanh hơn và có peer review để improve code quality.

---

## 6. Nếu có thêm 1 ngày, nhóm sẽ làm gì? (50–100 từ)

> 1–2 cải tiến cụ thể với lý do có bằng chứng từ trace/scorecard.

**Cải tiến 1: Hybrid search (keyword + semantic) cho retrieval worker**

Lý do: Trace q09 (ERR-403-AUTH) có confidence thấp (0.44) vì pure semantic search không match được error code cụ thể. Nếu thêm keyword search cho error codes (ERR-XXX pattern) trước khi semantic search, có thể improve accuracy cho technical queries.

**Cải tiến 2: LLM fallback cho ambiguous routing**

Lý do: Một số câu hỏi ambiguous giữa retrieval và policy (VD: "Ticket P1 cần cấp quyền Level 3") có thể route sai với pure keyword matching. Thêm confidence threshold: nếu keyword matching không confident (match cả 2 categories), fallback sang LLM classifier. Trade-off: tăng latency cho edge cases nhưng improve accuracy.

Bằng chứng: Eval report cho thấy avg_confidence 0.648 (acceptable nhưng có room for improvement). Nếu improve routing cho ambiguous cases, có thể đạt 0.75+.
