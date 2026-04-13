import os
import sys
import json
from ai_document_generator import main as generate_doc
from asana_integration import create_asana_task, add_internal_comment
from onedrive_integration import upload_to_onedrive

def run_complete_workflow():
    """Orchestrate entire process"""
    
    print("\n" + "🚀" * 20)
    print("TA PROJECT SERVICES - COMPLETE AI WORKFLOW")
    print("🚀" * 20 + "\n")
    
    # Step 1: Generate document
    print("[1/4] Generating AI document...")
    generate_doc()  # This creates document and last_run.json
    
    # Step 2: Load results
    if not os.path.exists("last_run.json"):
        print("❌ No document generated")
        return
    
    with open("last_run.json", "r") as f:
        data = json.load(f)
    
    # Step 3: Upload to OneDrive
    print("\n[2/4] Uploading to OneDrive...")
    onedrive_link = upload_to_onedrive(data["filename"])
    
    # Step 4: Create Asana task
    print("\n[3/4] Creating Asana task...")
    task = create_asana_task(
        data["project_name"],
        data["filename"],
        data["ai_data"]["executive_summary"]
    )
    
    # Step 5: Add comment with OneDrive link
    print("\n[4/4] Adding document link...")
    if task and onedrive_link:
        add_internal_comment(
            task["gid"],
            f"📁 Document available: {onedrive_link}\n\nReady for review and next steps."
        )
    
    # Summary
    print("\n" + "✅" * 20)
    print("WORKFLOW COMPLETE")
    print("✅" * 20)
    print(f"📄 Document: {data['filename']}")
    if onedrive_link:
        print(f"☁️ OneDrive: {onedrive_link}")
    if task:
        print(f"📋 Asana: {task.get('permalink_url', 'Created')}")
    print("✅" * 20)

if __name__ == "__main__":
    run_complete_workflow()