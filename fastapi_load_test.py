#!/usr/bin/env python3
"""
Simple load test for FastAPI service to demonstrate concurrency performance
"""
import asyncio
import aiohttp
import time
import json

BASE_URL = "http://localhost:8000"

async def test_endpoint(session, endpoint, data, test_id):
    """Test a single endpoint call"""
    try:
        start_time = time.time()
        async with session.post(f"{BASE_URL}{endpoint}", json=data) as response:
            end_time = time.time()
            return {
                "test_id": test_id,
                "status": response.status,
                "response_time": end_time - start_time,
                "success": response.status == 200
            }
    except Exception as e:
        return {
            "test_id": test_id,
            "status": 0,
            "response_time": 0,
            "success": False,
            "error": str(e)
        }

async def run_load_test(concurrent_users=50, requests_per_user=10):
    """Run load test with specified concurrent users"""
    print(f"🚀 Starting load test: {concurrent_users} concurrent users, {requests_per_user} requests each")
    print(f"📊 Total requests: {concurrent_users * requests_per_user}")
    
    # Test data for generate-metadata endpoint (lightweight)
    test_data = {"story_title": "Test Story"}
    
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        request_id = 0
        
        for user in range(concurrent_users):
            for req in range(requests_per_user):
                request_id += 1
                task = test_endpoint(session, "/api/v1/generate-metadata", test_data, request_id)
                tasks.append(task)
        
        # Run all requests concurrently
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
    
    return {
        "total_requests": len(results),
        "successful_requests": successful_requests,
        "failed_requests": failed_requests,
        "total_time": total_time,
        "requests_per_second": requests_per_second,
        "avg_response_time": avg_response_time,
        "success_rate": successful_requests/len(results)*100
    }

if __name__ == "__main__":
    print("🔥 FastAPI Concurrency Performance Test")
    print("=" * 50)
    
    # Test with different concurrency levels
    test_configs = [
        (10, 5),   # 50 total requests
        (25, 4),   # 100 total requests  
        (50, 2),   # 100 total requests
    ]
    
    for concurrent_users, requests_per_user in test_configs:
        print(f"\n🧪 Test Configuration: {concurrent_users} users × {requests_per_user} requests")
        try:
            result = asyncio.run(run_load_test(concurrent_users, requests_per_user))
            print(f"🎯 Performance Score: {result['requests_per_second']:.0f} req/sec")
        except Exception as e:
            print(f"❌ Test failed: {e}")
        
        print("-" * 50)
