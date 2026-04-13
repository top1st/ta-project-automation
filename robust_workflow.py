import time
import json
from datetime import datetime

class TAWorkflowEngine:
    """Production-ready workflow with error handling"""
    
    def __init__(self):
        self.state = "initialized"
        self.errors = []
        self.retry_count = 0
        self.max_retries = 3
    
    def run_with_retry(self, function, step_name):
        """Retry failed operations"""
        for attempt in range(self.max_retries):
            try:
                result = function()
                self.log_success(step_name)
                return result
            except Exception as e:
                self.log_error(step_name, e, attempt)
                time.sleep(2 ** attempt)  # Exponential backoff
        
        self.state = "failed"
        return None
    
    def validate_brief(self, brief_text):
        """Check for common data quality issues"""
        issues = []
        
        if len(brief_text) < 100:
            issues.append("Brief is very short - AI output may be limited")
        
        if "urgent" in brief_text.lower() and not "timeline" in brief_text.lower():
            issues.append("Urgency mentioned but no timeline provided")
        
        missing_keywords = []
        required = ["scope", "deliverable", "risk"]
        for keyword in required:
            if keyword not in brief_text.lower():
                missing_keywords.append(keyword)
        
        if missing_keywords:
            issues.append(f"Missing keywords: {', '.join(missing_keywords)}")
        
        return issues
    
    def log_success(self, step):
        print(f"✅ {step} - {datetime.now().strftime('%H:%M:%S')}")
    
    def log_error(self, step, error, attempt):
        print(f"❌ {step} failed (attempt {attempt+1}): {str(error)[:100]}")
        self.errors.append({
            "step": step,
            "error": str(error),
            "attempt": attempt,
            "timestamp": datetime.now().isoformat()
        })
    
    def generate_fallback_output(self, brief_text):
        """If AI fails, produce structured output from rules"""
        print("⚠️ Using fallback rule-based generation")
        
        return {
            "executive_summary": f"Project requires planning. Brief received: {brief_text[:100]}...",
            "project_scope": ["To be defined during discovery"],
            "key_deliverables": ["1. Complete project documentation", "2. Stakeholder approval"],
            "risks": ["Scope creep", "Resource availability"],
            "next_actions": ["1. Review this AI-generated draft", "2. Add specific requirements"]
        }
    
    def run(self, brief_text, project_name):
        """Main orchestration with full error handling"""
        
        print("\n🔍 Validating input...")
        issues = self.validate_brief(brief_text)
        if issues:
            print("⚠️ Data quality warnings:")
            for issue in issues:
                print(f"   - {issue}")
        
        print("🤖 Processing with AI...")
        ai_result = self.run_with_retry(
            lambda: call_ai_to_generate_document(brief_text),
            "AI Generation"
        )
        
        if not ai_result:
            print("Using fallback mechanism")
            ai_result = self.generate_fallback_output(brief_text)
        
        print("📄 Creating document...")
        filename = create_word_document(ai_result, project_name)
        
        # Save workflow state for debugging
        with open(f"workflow_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
            json.dump({
                "project": project_name,
                "state": self.state,
                "errors": self.errors,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)
        
        return filename

# Quick test
if __name__ == "__main__":
    engine = TAWorkflowEngine()
    
    test_brief = "Build a bridge. Need it fast. Budget unknown."
    result = engine.run(test_brief, "Test Project")
    print(f"\n✅ Completed with result: {result}")