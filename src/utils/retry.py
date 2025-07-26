"""
Retry utilities for the Medical Diagnosis AI System
"""

import asyncio
import logging
import random
from typing import Callable, Any, Optional
from functools import wraps

logger = logging.getLogger(__name__)

class RetryConfig:
    """Configuration for retry behavior"""
    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True,
        retry_on_exceptions: tuple = (Exception,)
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter
        self.retry_on_exceptions = retry_on_exceptions

def calculate_delay(attempt: int, config: RetryConfig) -> float:
    """Calculate delay for retry attempt with exponential backoff and jitter"""
    delay = config.base_delay * (config.exponential_base ** (attempt - 1))
    delay = min(delay, config.max_delay)
    
    if config.jitter:
        # Add random jitter to prevent thundering herd
        jitter = random.uniform(0, 0.1 * delay)
        delay += jitter
    
    return delay

async def async_retry(
    func: Callable,
    *args,
    config: Optional[RetryConfig] = None,
    **kwargs
) -> Any:
    """
    Retry an async function with exponential backoff
    
    Args:
        func: Async function to retry
        *args: Function arguments
        config: Retry configuration
        **kwargs: Function keyword arguments
    
    Returns:
        Function result
    
    Raises:
        Last exception if all retries fail
    """
    if config is None:
        config = RetryConfig()
    
    last_exception = None
    
    for attempt in range(1, config.max_retries + 2):  # +2 because we start at 1 and want max_retries + 1 total attempts
        try:
            return await func(*args, **kwargs)
        
        except config.retry_on_exceptions as e:
            last_exception = e
            
            if attempt <= config.max_retries:
                delay = calculate_delay(attempt, config)
                logger.warning(
                    f"Attempt {attempt} failed for {func.__name__}: {str(e)}. "
                    f"Retrying in {delay:.2f} seconds..."
                )
                await asyncio.sleep(delay)
            else:
                logger.error(
                    f"All {config.max_retries + 1} attempts failed for {func.__name__}. "
                    f"Last error: {str(e)}"
                )
                raise last_exception
    
    # This should never be reached, but just in case
    raise last_exception

def retry_decorator(config: Optional[RetryConfig] = None):
    """
    Decorator for adding retry logic to async functions
    
    Usage:
        @retry_decorator(RetryConfig(max_retries=3))
        async def my_function():
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await async_retry(func, *args, config=config, **kwargs)
        return wrapper
    return decorator

# Pre-configured retry configs for different use cases
GEMINI_API_RETRY_CONFIG = RetryConfig(
    max_retries=3,
    base_delay=2.0,
    max_delay=30.0,
    exponential_base=2.0,
    jitter=True,
    retry_on_exceptions=(Exception,)
)

NETWORK_RETRY_CONFIG = RetryConfig(
    max_retries=5,
    base_delay=1.0,
    max_delay=60.0,
    exponential_base=2.0,
    jitter=True,
    retry_on_exceptions=(ConnectionError, TimeoutError, Exception)
)

QUICK_RETRY_CONFIG = RetryConfig(
    max_retries=2,
    base_delay=0.5,
    max_delay=5.0,
    exponential_base=2.0,
    jitter=False,
    retry_on_exceptions=(Exception,)
) 