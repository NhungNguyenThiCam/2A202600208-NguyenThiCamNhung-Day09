"""
test_components.py — Test từng component độc lập
Chạy script này để verify từng worker hoạt động đúng.

Usage:
    python test_components.py
"""

import sys
import os

def test_retrieval_worker():
    """Test retrieval worker độc lập"""
    print("\n" + "=" * 60)
    print("TEST 1: Retrieval Worker")
    print("=" * 60)
    
    try:
        from workers.retrieval import run as retrieval_run
        
        test_state = {
            "task": "SLA ticket P1 là bao lâu?",
            "history": [],
            "workers_called": [],
        }
        
        result = retrieval_run(test_state)
        
        assert "retrieved_chunks" in result, "Missing retrieved_chunks"
        assert "retrieved_sources" in result, "Missing retrieved_sources"
        assert len(result["retrieved_chunks"]) > 0, "No chunks retrieved"
        
        print(f"✓ Retrieved {len(result['retrieved_chunks'])} chunks")
        print(f"✓ Sources: {result['retrieved_sources']}")
        print(f"✓ Top chunk: {result['retrieved_chunks'][0]['text'][:80]}...")
        print("\n✅ Retrieval Worker: PASS")
        return True
        
    except Exception as e:
        print(f"\n❌ Retrieval Worker: FAIL")
        print(f"   Error: {e}")
        return False

def test_policy_tool_worker():
    """Test policy tool worker độc lập"""
    print("\n" + "=" * 60)
    print("TEST 2: Policy Tool Worker")
    print("=" * 60)
    
    try:
        from workers.policy_tool import run as policy_tool_run
        
        test_state = {
            "task": "Khách hàng Flash Sale yêu cầu hoàn tiền",
            "retrieved_chunks": [
                {
                    "text": "Ngoại lệ: Đơn hàng Flash Sale không được hoàn tiền.",
                    "source": "policy_refund_v4.txt",
                    "score": 0.9
                }
            ],
            "needs_tool": True,
            "history": [],
            "workers_called": [],
            "mcp_tools_used": [],
        }
        
        result = policy_tool_run(test_state)
        
        assert "policy_result" in result, "Missing policy_result"
        assert "mcp_tools_used" in result, "Missing mcp_tools_used"
        
        pr = result["policy_result"]
        assert "policy_applies" in pr, "Missing policy_applies"
        assert "exceptions_found" in pr, "Missing exceptions_found"
        
        print(f"✓ policy_applies: {pr['policy_applies']}")
        print(f"✓ exceptions_found: {len(pr['exceptions_found'])}")
        if pr['exceptions_found']:
            print(f"✓ Exception type: {pr['exceptions_found'][0]['type']}")
        print(f"✓ MCP tools called: {len(result['mcp_tools_used'])}")
        print("\n✅ Policy Tool Worker: PASS")
        return True
        
    except Exception as e:
        print(f"\n❌ Policy Tool Worker: FAIL")
        print(f"   Error: {e}")
        return False

def test_synthesis_worker():
    """Test synthesis worker độc lập"""
    print("\n" + "=" * 60)
    print("TEST 3: Synthesis Worker")
    print("=" * 60)
    
    try:
        from workers.synthesis import run as synthesis_run
        
        test_state = {
            "task": "SLA ticket P1 là bao lâu?",
            "retrieved_chunks": [
                {
                    "text": "Ticket P1: Phản hồi ban đầu 15 phút, xử lý 4 giờ.",
                    "source": "sla_p1_2026.txt",
                    "score": 0.92
                }
            ],
            "policy_result": {},
            "history": [],
            "workers_called": [],
        }
        
        result = synthesis_run(test_state)
        
        assert "final_answer" in result, "Missing final_answer"
        assert "sources" in result, "Missing sources"
        assert "confidence" in result, "Missing confidence"
        
        print(f"✓ Answer: {result['final_answer'][:100]}...")
        print(f"✓ Sources: {result['sources']}")
        print(f"✓ Confidence: {result['confidence']}")
        print("\n✅ Synthesis Worker: PASS")
        return True
        
    except Exception as e:
        print(f"\n❌ Synthesis Worker: FAIL")
        print(f"   Error: {e}")
        return False

def test_mcp_server():
    """Test MCP server"""
    print("\n" + "=" * 60)
    print("TEST 4: MCP Server")
    print("=" * 60)
    
    try:
        from mcp_server import dispatch_tool, list_tools
        
        # Test list_tools
        tools = list_tools()
        assert len(tools) >= 2, "Should have at least 2 tools"
        print(f"✓ Found {len(tools)} tools")
        
        # Test search_kb
        result = dispatch_tool("search_kb", {"query": "SLA P1", "top_k": 2})
        assert "chunks" in result or "error" in result, "Invalid search_kb response"
        if "chunks" in result:
            print(f"✓ search_kb returned {len(result['chunks'])} chunks")
        else:
            print(f"⚠ search_kb returned error (expected if ChromaDB not ready)")
        
        # Test get_ticket_info
        result = dispatch_tool("get_ticket_info", {"ticket_id": "P1-LATEST"})
        assert "ticket_id" in result or "error" in result, "Invalid get_ticket_info response"
        if "ticket_id" in result:
            print(f"✓ get_ticket_info returned ticket {result['ticket_id']}")
        
        # Test check_access_permission
        result = dispatch_tool("check_access_permission", {
            "access_level": 2,
            "requester_role": "contractor",
            "is_emergency": True
        })
        assert "can_grant" in result or "error" in result, "Invalid check_access_permission response"
        if "can_grant" in result:
            print(f"✓ check_access_permission: can_grant={result['can_grant']}")
        
        print("\n✅ MCP Server: PASS")
        return True
        
    except Exception as e:
        print(f"\n❌ MCP Server: FAIL")
        print(f"   Error: {e}")
        return False

def test_graph():
    """Test full graph"""
    print("\n" + "=" * 60)
    print("TEST 5: Full Graph")
    print("=" * 60)
    
    try:
        from graph import run_graph
        
        test_query = "SLA xử lý ticket P1 là bao lâu?"
        result = run_graph(test_query)
        
        assert "supervisor_route" in result, "Missing supervisor_route"
        assert "route_reason" in result, "Missing route_reason"
        assert "workers_called" in result, "Missing workers_called"
        assert "final_answer" in result, "Missing final_answer"
        assert "confidence" in result, "Missing confidence"
        
        print(f"✓ Route: {result['supervisor_route']}")
        print(f"✓ Reason: {result['route_reason']}")
        print(f"✓ Workers: {result['workers_called']}")
        print(f"✓ Answer: {result['final_answer'][:100]}...")
        print(f"✓ Confidence: {result['confidence']}")
        print("\n✅ Full Graph: PASS")
        return True
        
    except Exception as e:
        print(f"\n❌ Full Graph: FAIL")
        print(f"   Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║   Lab Day 09 — Component Tests                          ║
╚══════════════════════════════════════════════════════════╝
""")
    
    results = []
    
    # Test each component
    results.append(("Retrieval Worker", test_retrieval_worker()))
    results.append(("Policy Tool Worker", test_policy_tool_worker()))
    results.append(("Synthesis Worker", test_synthesis_worker()))
    results.append(("MCP Server", test_mcp_server()))
    results.append(("Full Graph", test_graph()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} — {name}")
    
    print("\n" + "=" * 60)
    print(f"Total: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready.")
        print("\nNext steps:")
        print("  1. Run: python eval_trace.py")
        print("  2. Run: python fill_docs.py")
        print("  3. At 17:00, run: python eval_trace.py --grading")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check errors above.")
        print("\nCommon issues:")
        print("  - ChromaDB not built: run python build_index.py")
        print("  - API key missing: check .env file")
        print("  - Dependencies missing: run pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
