# ✅ JSON URL Support Added - `/api/v1/generate-amp`

## 🎯 **What Was Implemented**

Successfully modified the `/api/v1/generate-amp` endpoint to accept either JSON data directly OR a URL to fetch JSON data from.

## 📋 **Changes Made**

### 1. **Updated Request Schema** (`app/models/schemas.py`)
```python
class AMPGenerationRequest(BaseModel):
    """Request model for AMP generation (Tab 4)"""
    amp_template_html: Optional[str] = Field(None, description="AMP template HTML")
    amp_template_url: Optional[HttpUrl] = Field(None, description="URL to fetch AMP template from")
    output_json: Optional[Dict[str, Any]] = Field(None, description="Output JSON data")
    output_json_url: Optional[HttpUrl] = Field(None, description="URL to fetch output JSON data from")
    
    @model_validator(mode='after')
    def validate_template_source(self):
        """Ensure at least one template source is provided"""
        if not self.amp_template_html and not self.amp_template_url:
            raise ValueError("Either amp_template_html or amp_template_url must be provided")
        return self
    
    @model_validator(mode='after')
    def validate_output_data(self):
        """Ensure at least one output data source is provided"""
        if not self.output_json and not self.output_json_url:
            raise ValueError("Either output_json or output_json_url must be provided")
        return self
```

### 2. **Added JSON Fetch Method** (`app/services/html_service.py`)
```python
async def fetch_json_from_url(self, json_url: str) -> Dict[str, Any]:
    """Fetch JSON data from URL"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(json_url)
            response.raise_for_status()
            
            # Check if content type is JSON
            content_type = response.headers.get('content-type', '').lower()
            if 'application/json' not in content_type and 'text/json' not in content_type:
                raise ValueError(f"URL does not return JSON content. Content-Type: {content_type}")
            
            return response.json()
            
    except httpx.TimeoutException:
        raise ValueError("Timeout while fetching JSON from URL")
    except httpx.HTTPStatusError as e:
        raise ValueError(f"HTTP error {e.response.status_code} while fetching JSON from URL")
    except httpx.RequestError as e:
        raise ValueError(f"Network error while fetching JSON from URL: {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error while fetching JSON from URL: {str(e)}")
```

### 3. **Updated API Endpoints** (`app/api/routes.py`)

Both `/api/v1/generate-amp` and `/api/v1/generate-amp-download` now support:

```python
# Determine output JSON data source
output_json_data = {}

if request.output_json_url:
    # Fetch JSON data from URL
    output_json_data = await html_service.fetch_json_from_url(str(request.output_json_url))
elif request.output_json:
    # Use provided JSON data
    output_json_data = request.output_json
else:
    # Use empty JSON if neither provided
    output_json_data = {}

# Process AMP template
final_html = html_service.process_amp_template(amp_template_html, output_json_data)
```

## 🚀 **How It Works Now**

### **Option 1: Direct JSON Data (Backward Compatible)**
```json
{
  "amp_template_html": "<html>...</html>",
  "output_json": {
    "slide3": {
      "s3paragraph1": "Content",
      "audio_url3": "https://example.com/audio.mp3"
    }
  }
}
```

### **Option 2: JSON URL (New Feature)**
```json
{
  "amp_template_html": "<html>...</html>",
  "output_json_url": "https://cdn.suvichaar.org/media/processed_data.json"
}
```

## 📊 **Test Results**

✅ **Both Methods Working:**
- **JSON URL**: ✅ Successfully fetches JSON from URL
- **Direct JSON**: ✅ Backward compatibility maintained
- **Error Handling**: ✅ Proper validation and error messages
- **Content Type Validation**: ✅ Ensures URL returns JSON content

## 🔧 **Features**

### **Flexible Input**
- Accept JSON data directly OR JSON URL
- Automatic content type validation
- Proper error handling for network issues

### **Backward Compatibility**
- Existing workflows continue to work
- No breaking changes to current API usage

### **Error Handling**
- Timeout handling (30 seconds)
- HTTP error handling
- Content type validation
- Network error handling

## 🎯 **Usage Examples**

### **For n8n Workflow with JSON URL:**
```json
{
  "amp_template_html": "your_template_html",
  "output_json_url": "https://your-s3-bucket.com/processed_data.json"
}
```

### **For Direct JSON Data:**
```json
{
  "amp_template_html": "your_template_html", 
  "output_json": {
    "slide1": {"s1paragraph1": "Content", "audio_url1": "url"},
    "slide2": {"s2paragraph1": "Content", "audio_url2": "url"}
  }
}
```

## ✅ **Ready for Production**

The endpoint now supports both methods:
1. **Direct JSON data** (existing functionality)
2. **JSON URL** (new feature for your n8n workflow)

Your n8n workflow can now pass a URL to the JSON data instead of the actual data! 🚀
