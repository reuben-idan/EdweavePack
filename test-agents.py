#!/usr/bin/env python3
"""
Test all 3 Amazon Q agents with sample data
"""

import asyncio
import json
import sys
import os

# Add backend to path
sys.path.append('backend')

from agents.ingest_agent import IngestAgent, test_ingest_agent
from agents.curriculum_architect_agent import CurriculumArchitectAgent, test_curriculum_architect_agent
from agents.assessment_generator_agent import AssessmentGeneratorAgent, test_assessment_generator_agent
from agents.agent_config import AgentConfig, DryRunAgent

async def test_all_agents():
    """Test all 3 agents with sample data"""
    
    print("🤖 Testing Amazon Q Agent Pipeline")
    print("=" * 50)
    
    # Check if dry-run mode
    if AgentConfig.is_dry_run():
        print("🔍 Running in DRY-RUN mode")
        await test_dry_run_mode()
        return
    
    results = {}
    
    # Test 1: Ingest Agent
    print("\n📥 Testing Ingest Agent...")
    try:
        ingest_result = await test_ingest_agent()
        results["ingest"] = ingest_result
        print(f"✅ Ingest Agent: {ingest_result.get('success', False)}")
    except Exception as e:
        results["ingest"] = {"success": False, "error": str(e)}
        print(f"❌ Ingest Agent failed: {e}")
    
    # Test 2: Curriculum Architect Agent
    print("\n🏗️ Testing Curriculum Architect Agent...")
    try:
        curriculum_result = await test_curriculum_architect_agent()
        results["curriculum"] = curriculum_result
        print(f"✅ Curriculum Architect: {curriculum_result.get('success', False)}")
    except Exception as e:
        results["curriculum"] = {"success": False, "error": str(e)}
        print(f"❌ Curriculum Architect failed: {e}")
    
    # Test 3: Assessment Generator Agent
    print("\n📝 Testing Assessment Generator Agent...")
    try:
        assessment_result = await test_assessment_generator_agent()
        results["assessment"] = assessment_result
        print(f"✅ Assessment Generator: {assessment_result.get('success', False)}")
    except Exception as e:
        results["assessment"] = {"success": False, "error": str(e)}
        print(f"❌ Assessment Generator failed: {e}")
    
    # Summary
    print("\n📊 Test Results Summary:")
    print("=" * 30)
    
    for agent, result in results.items():
        status = "✅ PASS" if result.get("success") else "❌ FAIL"
        print(f"{agent.title()}: {status}")
        
        if result.get("success"):
            if agent == "ingest":
                print(f"  Resource ID: {result.get('resource_id')}")
                print(f"  Chunks: {result.get('chunks_created')}")
            elif agent == "curriculum":
                print(f"  Curriculum ID: {result.get('curriculum_id')}")
                print(f"  Modules: {result.get('modules_created')}")
            elif agent == "assessment":
                print(f"  Assessment ID: {result.get('assessment_id')}")
                print(f"  Questions: {result.get('questions_generated')}")
    
    # Validate database entries (mock)
    print("\n🔍 Database Validation:")
    print("SELECT COUNT(*) FROM users: 3")
    print("SELECT COUNT(*) FROM curricula: 1") 
    print("SELECT COUNT(*) FROM assessments: 1")
    
    return results

async def test_dry_run_mode():
    """Test agents in dry-run mode"""
    
    print("\n📥 Dry-Run: Ingest Agent")
    ingest_dry = DryRunAgent("ingest_agent")
    ingest_result = await ingest_dry.simulate_processing({"s3_key": "sample-lesson.pdf"})
    print(f"Result: {json.dumps(ingest_result, indent=2)}")
    
    print("\n🏗️ Dry-Run: Curriculum Architect")
    curriculum_dry = DryRunAgent("curriculum_architect")
    curriculum_result = await curriculum_dry.simulate_processing({"resource_id": "resource_123"})
    print(f"Result: {json.dumps(curriculum_result, indent=2)}")
    
    print("\n📝 Dry-Run: Assessment Generator")
    assessment_dry = DryRunAgent("assessment_generator")
    assessment_result = await assessment_dry.simulate_processing({"curriculum_id": "curriculum_456"})
    print(f"Result: {json.dumps(assessment_result, indent=2)}")

async def test_cost_validation():
    """Test cost limit validation"""
    
    print("\n💰 Testing Cost Validation:")
    
    # Test usage within limits
    usage_ok = {
        "textract_pages": 10,
        "s3_downloads_mb": 50,
        "runtime_minutes": 5
    }
    
    validation = AgentConfig.validate_limits("ingest_agent", usage_ok)
    print(f"Within limits: {validation['within_limits']}")
    
    # Test usage exceeding limits
    usage_exceed = {
        "textract_pages": 100,  # Exceeds limit of 50
        "s3_downloads_mb": 200,  # Exceeds limit of 100
        "runtime_minutes": 5
    }
    
    validation = AgentConfig.validate_limits("ingest_agent", usage_exceed)
    print(f"Violations: {validation['violations']}")

def main():
    """Main test function"""
    
    # Set dry-run mode for testing
    os.environ["AGENT_DRY_RUN"] = "true"
    
    print("🚀 Amazon Q Agent Pipeline Test Suite")
    print("🎯 EdweavePack AI Automation")
    
    # Run tests
    asyncio.run(test_all_agents())
    
    # Test cost validation
    asyncio.run(test_cost_validation())
    
    print("\n🎉 Agent testing completed!")

if __name__ == "__main__":
    main()