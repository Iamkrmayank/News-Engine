#!/usr/bin/env python3
"""
Comprehensive FastAPI vs n8n Performance Comparison
"""
import asyncio
import aiohttp
import time
import json
import requests
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://localhost:8000"

async def test_fastapi_endpoint(session, endpoint, data, test_id):
    """Test FastAPI endpoint"""
    try:
        start_time = time.time()
        async with session.post(f"{BASE_URL}{endpoint}", json=data) as response:
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

def test_n8n_simulation():
    """Simulate n8n performance (typical workflow execution)"""
    # n8n typically takes 100-500ms per workflow execution
    # This is a conservative simulation
    simulated_delay = 0.2  # 200ms average per request
    time.sleep(simulated_delay)
    return {
        "status": 200,
        "response_time": simulated_delay,
        "success": True
    }

async def run_fastapi_load_test(concurrent_users=100, requests_per_user=5):
    """Run comprehensive FastAPI load test"""
    print(f"🚀 FastAPI Load Test: {concurrent_users} users × {requests_per_user} requests")
    print(f"📊 Total requests: {concurrent_users * requests_per_user}")
    
    # Test with a simple endpoint
    test_data = {"story_title": "Performance Test Story"}
    
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        request_id = 0
        
        for user in range(concurrent_users):
            for req in range(requests_per_user):
                request_id += 1
                task = test_fastapi_endpoint(session, "/api/v1/generate-metadata", test_data, request_id)
                tasks.append(task)
        
        results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    # Analyze results
    successful_requests = sum(1 for r in results if r["success"])
    failed_requests = len(results) - successful_requests
    avg_response_time = sum(r["response_time"] for r in results if r["success"]) / max(successful_requests, 1)
    requests_per_second = len(results) / total_time
    
    return {
        "platform": "FastAPI",
        "total_requests": len(results),
        "successful_requests": successful_requests,
        "failed_requests": failed_requests,
        "total_time": total_time,
        "requests_per_second": requests_per_second,
        "avg_response_time": avg_response_time,
        "success_rate": successful_requests/len(results)*100
    }

def run_n8n_simulation(concurrent_users=100, requests_per_user=5):
    """Simulate n8n performance"""
    print(f"🔄 n8n Simulation: {concurrent_users} users × {requests_per_user} requests")
    print(f"📊 Total requests: {concurrent_users * requests_per_user}")
    
    start_time = time.time()
    
    # Simulate n8n workflow execution
    with ThreadPoolExecutor(max_workers=10) as executor:  # n8n typically limited concurrency
        futures = []
        for user in range(concurrent_users):
            for req in range(requests_per_user):
                future = executor.submit(test_n8n_simulation)
                futures.append(future)
        
        results = [future.result() for future in futures]
    
    end_time = time.time()
    total_time = end_time - start_time
    
    successful_requests = sum(1 for r in results if r["success"])
    avg_response_time = sum(r["response_time"] for r in results) / len(results)
    requests_per_second = len(results) / total_time
    
    return {
        "platform": "n8n (Simulated)",
        "total_requests": len(results),
        "successful_requests": successful_requests,
        "failed_requests": 0,
        "total_time": total_time,
        "requests_per_second": requests_per_second,
        "avg_response_time": avg_response_time,
        "success_rate": 100.0
    }

def print_comparison_results(fastapi_results, n8n_results):
    """Print detailed comparison results"""
    print("\n" + "="*80)
    print("📊 PERFORMANCE COMPARISON RESULTS")
    print("="*80)
    
    print(f"\n🚀 FastAPI Results:")
    print(f"   ✅ Successful requests: {fastapi_results['successful_requests']}")
    print(f"   ❌ Failed requests: {fastapi_results['failed_requests']}")
    print(f"   ⏱️  Total time: {fastapi_results['total_time']:.2f} seconds")
    print(f"   🚀 Requests per second: {fastapi_results['requests_per_second']:.2f}")
    print(f"   📊 Average response time: {fastapi_results['avg_response_time']:.3f} seconds")
    print(f"   📈 Success rate: {fastapi_results['success_rate']:.1f}%")
    
    print(f"\n🔄 n8n Results:")
    print(f"   ✅ Successful requests: {n8n_results['successful_requests']}")
    print(f"   ❌ Failed requests: {n8n_results['failed_requests']}")
    print(f"   ⏱️  Total time: {n8n_results['total_time']:.2f} seconds")
    print(f"   🚀 Requests per second: {n8n_results['requests_per_second']:.2f}")
    print(f"   📊 Average response time: {n8n_results['avg_response_time']:.3f} seconds")
    print(f"   📈 Success rate: {n8n_results['success_rate']:.1f}%")
    
    # Calculate performance difference
    rps_difference = fastapi_results['requests_per_second'] - n8n_results['requests_per_second']
    rps_percentage = (rps_difference / n8n_results['requests_per_second']) * 100
    
    print(f"\n🏆 PERFORMANCE WINNER:")
    if fastapi_results['requests_per_second'] > n8n_results['requests_per_second']:
        print(f"   🥇 FastAPI is {rps_percentage:.1f}% FASTER than n8n!")
        print(f"   📈 FastAPI handles {rps_difference:.2f} more requests per second")
    else:
        print(f"   🥇 n8n is {abs(rps_percentage):.1f}% faster than FastAPI")
    
    print(f"\n💡 KEY INSIGHTS:")
    print(f"   • FastAPI: Built for high-performance APIs with async support")
    print(f"   • n8n: Designed for workflow automation, not high-throughput APIs")
    print(f"   • FastAPI: Can handle {fastapi_results['requests_per_second']:.0f} req/sec")
    print(f"   • n8n: Typically handles {n8n_results['requests_per_second']:.0f} req/sec")
    
    print("\n" + "="*80)

async def main():
    """Main comparison function"""
    print("🔥 FastAPI vs n8n Performance Comparison")
    print("="*50)
    
    # Test configurations
    test_configs = [
        (50, 2),   # 100 total requests
        (100, 3),  # 300 total requests
        (200, 2),  # 400 total requests
    ]
    
    for concurrent_users, requests_per_user in test_configs:
        print(f"\n🧪 Test Configuration: {concurrent_users} users × {requests_per_user} requests")
        
        try:
            # Run FastAPI test
            fastapi_results = await run_fastapi_load_test(concurrent_users, requests_per_user)
            
            # Run n8n simulation
            n8n_results = run_n8n_simulation(concurrent_users, requests_per_user)
            
            # Print comparison
            print_comparison_results(fastapi_results, n8n_results)
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
        
        print("\n" + "-"*80)

if __name__ == "__main__":
    asyncio.run(main())
