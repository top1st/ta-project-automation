import os
import requests
import json

# Add to .env:
# ONEDRIVE_ACCESS_TOKEN=your_token
# ONEDRIVE_FOLDER_ID=root or folder_id

def upload_to_onedrive(filename):
    """Upload Word document to OneDrive"""
    
    access_token = os.getenv("ONEDRIVE_ACCESS_TOKEN")
    folder_id = os.getenv("ONEDRIVE_FOLDER_ID", "root")
    
    if not access_token or access_token == "your_token":
        print("⚠️ OneDrive token not configured - simulating upload")
        return f"https://onedrive.example.com/simulated/{filename}"
    
    # Microsoft Graph API endpoint
    url = f"https://graph.microsoft.com/v1.0/me/drive/items/{folder_id}:/{filename}:/content"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    }
    
    try:
        with open(filename, "rb") as file:
            response = requests.put(url, headers=headers, data=file)
        
        if response.status_code in [200, 201]:
            file_data = response.json()
            web_url = file_data.get("webUrl", "Upload successful")
            print(f"✅ Uploaded to OneDrive: {web_url}")
            return web_url
        else:
            print(f"❌ Upload failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ OneDrive exception: {e}")
        return None

def get_onedrive_link(filename):
    """Get sharing link for uploaded file"""
    
    access_token = os.getenv("ONEDRIVE_ACCESS_TOKEN")
    
    if not access_token:
        return "No token configured"
    
    # This is simplified - full implementation needs file ID
    return f"https://onedrive.live.com/embed?filename={filename}"

if __name__ == "__main__":
    if os.path.exists("last_run.json"):
        with open("last_run.json", "r") as f:
            data = json.load(f)
        
        link = upload_to_onedrive(data["filename"])
        print(f"OneDrive link: {link}")