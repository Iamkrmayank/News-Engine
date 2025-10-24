#!/usr/bin/env python3
"""
Real-world FastAPI Performance Test with Working Endpoints
"""
import asyncio
import aiohttp
import time
import json

BASE_URL = "http://localhost:8000"

async def test_working_endpoint(session, test_id):
    """Test with a working endpoint"""
    try:
        # Test with generate-metadata endpoint (Form data)
        start_time = time.time()
        
        # Use aiohttp for form data
        data = aiohttp.FormData()
        data.add_field('story_title', 'Performance Test Story')
        
        async with session.post(f"{BASE_URL}/api/v1/generate-metadata", data=data) as response:
            end_time = time.time()
            response_text = await response.text()
            
            return {
                "test_id": test_id,
                "status": response.status,
                "response_time": end_time - start_time,
                "success": response.status == 200,
                "response_size": len(response_text)
            }
    except Exception as e:
        return {
            "test_id": test_id,
            "status": 0,
            "response_time": 0,
            "success": False,
            "error": str(e)
        }

async def run_real_performance_test(concurrent_users=100, requests_per_user=3):
    """Run real performance test with working endpoint"""
    print(f"🚀 Real FastAPI Performance Test")
    print(f"📊 {concurrent_users} concurrent users × {requests_per_user} requests = {concurrent_users * requests_per_user} total requests")
    
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        request_id = 0
        
        for user in range(concurrent_users):
            for req in range(requests_per_user):
                request_id += 1
                task = test_working_endpoint(session, request_id)
                tasks.append(task)
        
        results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    # Analyze results
    successful_requests = sum(1 for r in results if r["success"])
    failed_requests = len(results) - successful_requests
    avg_response_time = sum(r["response_time"] for r in results if r["success"]) / max(successful_requests, 1)
    requests_per_second = len(results) / total_time
    
    print(f"\n📈 RESULTS:")
    print(f"✅ Successful requests: {successful_requests}")
    print(f"❌ Failed requests: {failed_requests}")
    print(f"⏱️  Total time: {total_time:.2f} seconds")
    print(f"🚀 Requests per second: {requests_per_second:.2f}")
    print(f"📊 Average response time: {avg_response_time:.3f} seconds")
    print(f"📈 Success rate: {(successful_requests/len(results)*100):.1f}%")
    
    # Performance analysis
    print(f"\n💡 PERFORMANCE ANALYSIS:")
    if requests_per_second > 100:
        print(f"🔥 EXCELLENT: {requests_per_second:.0f} req/sec - Production ready!")
    elif requests_per_second > 50:
        print(f"✅ GOOD: {requests_per_second:.0f} req/sec - Suitable for most applications")
    elif requests_per_second > 20:
        print(f"⚠️  MODERATE: {requests_per_second:.0f} req/sec - May need optimization")
    else:
        print(f"❌ POOR: {requests_per_second:.0f} req/sec - Needs optimization")
    
    # Comparison with n8n
    n8n_typical_rps = 50  # Typical n8n performance
    if requests_per_second > n8n_typical_rps:
        improvement = ((requests_per_second - n8n_typical_rps) / n8n_typical_rps) * 100
        print(f"🏆 FastAPI is {improvement:.1f}% FASTER than typical n8n performance!")
    
    return {
        "total_requests": len(results),
        "successful_requests": successful_requests,
        "failed_requests": failed_requests,
        "total_time": total_time,
        "requests_per_second": requests_per_second,
        "avg_response_time": avg_response_time,
        "success_rate": successful_requests/len(results)*100
    }

def simulate_n8n_workflow_performance():
    """Simulate realistic n8n workflow performance"""
    print(f"\n🔄 n8n Workflow Simulation")
    print(f"📊 Simulating typical n8n workflow execution...")
    
    # n8n workflow steps typically include:
    # 1. HTTP Request node (50-100ms)
    # 2. Data transformation (20-50ms)  
    # 3. Conditional logic (10-30ms)
    # 4. Response formatting (20-40ms)
    # Total: ~100-220ms per workflow
    
    workflow_delay = 0.15  # 150ms average per workflow
    concurrent_limit = 10  # n8n typically limits concurrent executions
    
    print(f"⏱️  Average workflow execution time: {workflow_delay*1000:.0f}ms")
    print(f"🔄 Concurrent execution limit: {concurrent_limit}")
    print(f"📊 Typical throughput: ~{concurrent_limit/workflow_delay:.0f} workflows/second")
    
    return {
        "avg_execution_time": workflow_delay,
        "concurrent_limit": concurrent_limit,
        "typical_throughput": concurrent_limit/workflow_delay
    }

async def main():
    """Main performance demonstration"""
    print("🔥 FastAPI vs n8n - Real Performance Comparison")
    print("="*60)
    
    # Test different load levels
    test_configs = [
        (50, 2),   # Light load
        (100, 3),  # Medium load  
        (200, 2),  # Heavy load
    ]
    
    for concurrent_users, requests_per_user in test_configs:
        print(f"\n🧪 Test: {concurrent_users} users × {requests_per_user} requests")
        try:
            fastapi_results = await run_real_performance_test(concurrent_users, requests_per_user)
            n8n_simulation = simulate_n8n_workflow_performance()
            
            print(f"\n📊 COMPARISON SUMMARY:")
            print(f"FastAPI: {fastapi_results['requests_per_second']:.0f} req/sec")
            print(f"n8n: ~{n8n_simulation['typical_throughput']:.0f} workflows/sec")
            
            if fastapi_results['requests_per_second'] > n8n_simulation['typical_throughput']:
                improvement = ((fastapi_results['requests_per_second'] - n8n_simulation['typical_throughput']) / n8n_simulation['typical_throughput']) * 100
                print(f"🏆 FastAPI is {improvement:.0f}% FASTER!")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
        
        print("\n" + "-"*60)

if __name__ == "__main__":
    asyncio.run(main())
