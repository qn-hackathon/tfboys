"""
测试重试装饰器
"""
import pytest
import asyncio
from unittest.mock import AsyncMock
from app.utils.retry import retry_on_failure, retry_on_failure_sync


@pytest.mark.unit
class TestRetryOnFailure:
    @pytest.mark.asyncio
    async def test_retry_success_on_first_attempt(self):
        """测试第一次尝试成功"""
        mock_func = AsyncMock(return_value="success")
        decorated_func = retry_on_failure(max_retries=3, delay=0.01, backoff=1.0)(mock_func)
        
        result = await decorated_func()
        
        assert result == "success"
        assert mock_func.call_count == 1
    
    @pytest.mark.asyncio
    async def test_retry_success_after_failures(self):
        """测试重试后成功"""
        mock_func = AsyncMock(side_effect=[
            Exception("Error 1"),
            Exception("Error 2"),
            "success"
        ])
        decorated_func = retry_on_failure(max_retries=3, delay=0.01, backoff=1.0)(mock_func)
        
        result = await decorated_func()
        
        assert result == "success"
        assert mock_func.call_count == 3
    
    @pytest.mark.asyncio
    async def test_retry_all_attempts_fail(self):
        """测试所有重试都失败"""
        mock_func = AsyncMock(side_effect=Exception("Always fails"))
        decorated_func = retry_on_failure(max_retries=2, delay=0.01, backoff=1.0)(mock_func)
        
        with pytest.raises(Exception, match="Always fails"):
            await decorated_func()
        
        assert mock_func.call_count == 3
    
    @pytest.mark.asyncio
    async def test_retry_with_backoff(self):
        """测试指数退避"""
        mock_func = AsyncMock(side_effect=[
            Exception("Error 1"),
            Exception("Error 2"),
            "success"
        ])
        decorated_func = retry_on_failure(max_retries=3, delay=0.01, backoff=2.0)(mock_func)
        
        start_time = asyncio.get_event_loop().time()
        result = await decorated_func()
        elapsed_time = asyncio.get_event_loop().time() - start_time
        
        assert result == "success"
        assert elapsed_time >= 0.03


@pytest.mark.unit
class TestRetryOnFailureSync:
    def test_sync_retry_success(self):
        """测试同步重试成功"""
        counter = {"count": 0}
        
        def mock_func():
            counter["count"] += 1
            if counter["count"] < 3:
                raise Exception("Error")
            return "success"
        
        decorated_func = retry_on_failure_sync(max_retries=3, delay=0.01, backoff=1.0)(mock_func)
        
        result = decorated_func()
        
        assert result == "success"
        assert counter["count"] == 3
    
    def test_sync_retry_all_fail(self):
        """测试同步重试全部失败"""
        def mock_func():
            raise Exception("Always fails")
        
        decorated_func = retry_on_failure_sync(max_retries=2, delay=0.01, backoff=1.0)(mock_func)
        
        with pytest.raises(Exception, match="Always fails"):
            decorated_func()
