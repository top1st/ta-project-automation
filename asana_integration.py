import os
import requests
import json
from datetime import datetime

# Add to .env:
# ASANA_TOKEN=your_personal_access_token
# ASANA_PROJECT_ID=your_project_id

def create_asana_task(project_name, filename, ai_summary):
    """Create task in Asana with document link"""
    
    asana_token = os.getenv("ASANA_TOKEN")
    project_id = os.getenv("ASANA_PROJECT_ID")
    
    if not asana_token or asana_token == "your_personal_access_token":
        print("⚠️ Asana token not configured - skipping")
        return None
    
    url = "https://app.asana.com/api/1.0/tasks"
    
    headers = {
        "Authorization": f"Bearer {asana_token}",
        "Content-Type": "application/json"
    }
    
    # Task description
    description = f"""**AI-Generated Project Document**

**Project:** {project_name}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

**Executive Summary:**
{ai_summary[:300]}

**Document:** {filename}

---
*This task was auto-created by TA AI Automation System*
"""
    
    payload = {
        "data": {
            "name": f"📄 AI Document: {project_name}",
            "notes": description,
            "projects": [project_id],
            "tags": ["AI Generated", "Ready for Review"]
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201:
            task_data = response.json()
            print(f"✅ Asana task created: {task_data['data']['permalink_url']}")
            return task_data['data']
        else:
            print(f"❌ Asana error: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Asana exception: {e}")
        return None

def add_internal_comment(task_gid, message):
    """Add internal comment to Asana task"""
    
    asana_token = os.getenv("ASANA_TOKEN")
    
    if not asana_token:
        return
    
    url = f"https://app.asana.com/api/1.0/tasks/{task_gid}/stories"
    
    headers = {
        "Authorization": f"Bearer {asana_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "data": {
            "text": f"💬 {message}",
            "is_pinned": False
        }
    }
    
    try:
        requests.post(url, headers=headers, json=payload)
        print(f"✅ Comment added to task")
    except Exception as e:
        print(f"⚠️ Could not add comment: {e}")

if __name__ == "__main__":
    # Test with last run data
    if os.path.exists("last_run.json"):
        with open("last_run.json", "r") as f:
            data = json.load(f)
        
        task = create_asana_task(
            data["project_name"],
            data["filename"],
            data["ai_data"]["executive_summary"]
        )
        
        if task:
            add_internal_comment(
                task["gid"],
                "AI document ready for review. Please verify against original brief."
            )
            