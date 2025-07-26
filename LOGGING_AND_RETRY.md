# Logging and Retry Mechanisms

## Overview
The Medical Diagnosis AI System implements comprehensive logging and retry mechanisms to ensure reliability, observability, and graceful handling of failures.

## Logging System

### Configuration
Logging is configured in `main.py` and `src/api.py` with the following setup:

```python
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),  # INFO by default
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.LOG_FILE),  # ./logs/medical_ai.log
        logging.Logging.StreamHandler()          # Console output
    ]
)
```

### Log Levels
- **DEBUG**: Detailed diagnostic information
- **INFO**: General information about program execution
- **WARNING**: Warning messages for potentially problematic situations
- **ERROR**: Error messages for serious problems
- **CRITICAL**: Critical errors that may prevent the program from running

### Log File Location
- **Path**: `./logs/medical_ai.log`
- **Auto-creation**: Directory is automatically created if it doesn't exist
- **Rotation**: Currently no automatic rotation (consider adding logrotate)

### What Gets Logged

#### 1. Application Lifecycle
```python
logger.info("Starting Medical Diagnosis AI System")
logger.info("Completed diagnosis session {session_id}")
logger.error("Application error: {str(e)}")
```

#### 2. Agent Operations
```python
logger.info(f"Agent {agent_id} completed analysis for patient {patient_id}")
logger.error(f"Error in agent {agent_id} analysis: {str(e)}")
logger.warning(f"Attempt {attempt} failed for {func.__name__}: {str(e)}")
```

#### 3. API Operations
```python
logger.error(f"Error in diagnosis endpoint: {str(e)}")
logger.info(f"API request received for patient {patient_id}")
```

#### 4. Retry Operations
```python
logger.warning(f"Attempt {attempt} failed for {func.__name__}: {str(e)}. Retrying in {delay:.2f} seconds...")
logger.error(f"All {max_retries + 1} attempts failed for {func.__name__}. Last error: {str(e)}")
```

## Retry System

### Overview
The retry system implements exponential backoff with jitter to handle transient failures gracefully.

### Retry Configuration

#### 1. RetryConfig Class
```python
class RetryConfig:
    def __init__(
        self,
        max_retries: int = 3,           # Maximum number of retry attempts
        base_delay: float = 1.0,        # Initial delay in seconds
        max_delay: float = 60.0,        # Maximum delay between retries
        exponential_base: float = 2.0,  # Exponential backoff multiplier
        jitter: bool = True,            # Add random jitter to prevent thundering herd
        retry_on_exceptions: tuple = (Exception,)  # Exceptions to retry on
    )
```

#### 2. Pre-configured Configurations

**GEMINI_API_RETRY_CONFIG** (Default for AI calls):
```python
RetryConfig(
    max_retries=3,
    base_delay=2.0,
    max_delay=30.0,
    exponential_base=2.0,
    jitter=True,
    retry_on_exceptions=(Exception,)
)
```

**NETWORK_RETRY_CONFIG** (For network operations):
```python
RetryConfig(
    max_retries=5,
    base_delay=1.0,
    max_delay=60.0,
    exponential_base=2.0,
    jitter=True,
    retry_on_exceptions=(ConnectionError, TimeoutError, Exception)
)
```

**QUICK_RETRY_CONFIG** (For fast operations):
```python
RetryConfig(
    max_retries=2,
    base_delay=0.5,
    max_delay=5.0,
    exponential_base=2.0,
    jitter=False,
    retry_on_exceptions=(Exception,)
)
```

### Retry Algorithm

#### 1. Exponential Backoff
```
Delay = base_delay × (exponential_base ^ (attempt - 1))
Delay = min(Delay, max_delay)
```

#### 2. Jitter Addition
```python
if jitter:
    jitter = random.uniform(0, 0.1 * delay)
    delay += jitter
```

#### 3. Example Retry Sequence
For `GEMINI_API_RETRY_CONFIG`:
- **Attempt 1**: Immediate (no delay)
- **Attempt 2**: ~2.2 seconds (2.0 + jitter)
- **Attempt 3**: ~4.4 seconds (4.0 + jitter)
- **Attempt 4**: ~8.8 seconds (8.0 + jitter)
- **Final failure**: Error logged and raised

### Usage Examples

#### 1. Direct Function Call
```python
response = await async_retry(
    my_function,
    arg1, arg2,
    config=GEMINI_API_RETRY_CONFIG
)
```

#### 2. Decorator Usage
```python
@retry_decorator(GEMINI_API_RETRY_CONFIG)
async def my_function():
    pass
```

#### 3. In Base Agent
```python
async def _get_ai_response(self, prompt: str) -> str:
    async def _call_gemini():
        return await asyncio.to_thread(
            self.model.generate_content,
            prompt
        )
    
    response = await async_retry(
        _call_gemini,
        config=GEMINI_API_RETRY_CONFIG
    )
    return response.text
```

## Error Handling Strategy

### 1. Graceful Degradation
- Individual agent failures don't stop the entire diagnosis
- System continues with available agent responses
- Error responses are created with 0.0 confidence

### 2. Error Response Creation
```python
def _create_error_response(self, diagnosis_request: DiagnosisRequest) -> AgentResponse:
    return AgentResponse(
        agent_id=self.agent_id,
        specialty=self.specialty,
        analysis="I apologize, but I encountered an error while analyzing your symptoms. Please try again or consult with a healthcare provider.",
        recommendations=["Consult with a healthcare provider for proper evaluation"],
        confidence=0.0,
        additional_questions=[],
        suggested_tests=[]
    )
```

### 3. Coordinator Error Handling
```python
# Execute all analyses concurrently
responses = await asyncio.gather(*tasks, return_exceptions=True)

# Filter out exceptions and return valid responses
valid_responses = []
for response in responses:
    if isinstance(response, Exception):
        logger.error(f"Agent analysis failed: {str(response)}")
    else:
        valid_responses.append(response)
```

## Monitoring and Observability

### 1. Log Analysis
Monitor these key metrics:
- **Error rates**: Frequency of retry failures
- **Response times**: Time taken for successful vs failed requests
- **Agent performance**: Success rates per specialist agent
- **API usage**: Number of requests and rate limiting

### 2. Health Checks
The system includes health check endpoints:
- `/health`: Basic API health
- `/agents`: Agent status information
- `/specialties`: Available medical specialties

### 3. Session Tracking
All diagnosis sessions are logged with:
- Session ID and patient ID
- Start/end times
- Agent responses
- Final diagnosis results

## Best Practices

### 1. Logging
- Use appropriate log levels
- Include context in log messages
- Avoid logging sensitive patient information
- Consider log rotation for production

### 2. Retry Logic
- Don't retry on client errors (4xx)
- Retry on server errors (5xx) and network issues
- Use exponential backoff with jitter
- Set reasonable timeouts

### 3. Error Handling
- Always provide fallback responses
- Log errors with sufficient context
- Don't expose internal errors to users
- Maintain system stability during failures

## Configuration

### Environment Variables
```bash
# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/medical_ai.log

# Retry (can be added to config)
MAX_RETRIES=3
BASE_DELAY=2.0
MAX_DELAY=30.0
```

### Future Enhancements
1. **Structured Logging**: Use JSON format for better parsing
2. **Log Aggregation**: Integrate with ELK stack or similar
3. **Metrics Collection**: Add Prometheus metrics
4. **Circuit Breaker**: Implement circuit breaker pattern
5. **Rate Limiting**: Add rate limiting for API calls 