import asyncio
import json
from typing import Dict, Any, List
from agents.ingest_agent import IngestAgent
from agents.curriculum_architect_agent import CurriculumArchitectAgent
from agents.assessment_generator_agent import AssessmentGeneratorAgent
from agents.agent_config import AgentConfig

class AmazonQAgentOrchestrator:
    """Orchestrator for Amazon Q agent pipeline"""
    
    def __init__(self):
        self.ingest_agent = IngestAgent()
        self.curriculum_agent = CurriculumArchitectAgent()
        self.assessment_agent = AssessmentGeneratorAgent()
        self.config = AgentConfig()
    
    async def process_complete_pipeline(self, s3_key: str, teacher_id: int, generation_schema: Dict) -> Dict[str, Any]:
        """Complete pipeline: S3 -> Ingest -> Curriculum -> Assessment"""
        
        pipeline_result = {
            "pipeline_id": f"pipeline_{s3_key}_{teacher_id}",
            "stages": {},
            "success": False,
            "errors": []
        }
        
        try:
            # Stage 1: Ingest
            print("🔄 Stage 1: Content Ingestion")
            ingest_result = await self.ingest_agent.process_s3_object(s3_key, teacher_id)
            pipeline_result["stages"]["ingest"] = ingest_result
            
            if not ingest_result.get("success"):
                raise Exception(f"Ingest failed: {ingest_result.get('error')}")
            
            resource_id = ingest_result["resource_id"]
            
            # Stage 2: Curriculum Generation
            print("🔄 Stage 2: Curriculum Architecture")
            curriculum_result = await self.curriculum_agent.generate_curriculum_from_resource(
                resource_id, generation_schema
            )
            pipeline_result["stages"]["curriculum"] = curriculum_result
            
            if not curriculum_result.get("success"):
                raise Exception(f"Curriculum generation failed: {curriculum_result.get('error')}")
            
            curriculum_id = curriculum_result["curriculum_id"]
            
            # Stage 3: Assessment Generation
            print("🔄 Stage 3: Assessment Generation")
            assessment_results = []
            
            for module_id in curriculum_result.get("module_ids", ["module_0"]):
                assessment_result = await self.assessment_agent.generate_assessment(
                    curriculum_id, module_id, generation_schema.get("difficulty", "intermediate")
                )
                assessment_results.append(assessment_result)
            
            pipeline_result["stages"]["assessments"] = assessment_results
            
            # Pipeline success
            pipeline_result["success"] = True
            pipeline_result["final_outputs"] = {
                "resource_id": resource_id,
                "curriculum_id": curriculum_id,
                "assessment_ids": [a.get("assessment_id") for a in assessment_results if a.get("success")],
                "total_modules": len(curriculum_result.get("module_ids", [])),
                "total_assessments": len([a for a in assessment_results if a.get("success")])
            }
            
        except Exception as e:
            pipeline_result["errors"].append(str(e))
            pipeline_result["success"] = False
        
        return pipeline_result
    
    async def process_batch_content(self, s3_keys: List[str], teacher_id: int, schema: Dict) -> Dict[str, Any]:
        """Process multiple content files in batch"""
        
        batch_results = {
            "batch_id": f"batch_{teacher_id}_{len(s3_keys)}",
            "total_files": len(s3_keys),
            "processed": 0,
            "failed": 0,
            "results": []
        }
        
        for s3_key in s3_keys:
            try:
                result = await self.process_complete_pipeline(s3_key, teacher_id, schema)
                batch_results["results"].append(result)
                
                if result["success"]:
                    batch_results["processed"] += 1
                else:
                    batch_results["failed"] += 1
                    
            except Exception as e:
                batch_results["results"].append({
                    "s3_key": s3_key,
                    "success": False,
                    "error": str(e)
                })
                batch_results["failed"] += 1
        
        return batch_results

# API Integration
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()
orchestrator = AmazonQAgentOrchestrator()

class PipelineRequest(BaseModel):
    s3_key: str
    teacher_id: int
    generation_schema: Dict[str, Any] = {
        "difficulty": "intermediate",
        "duration_weeks": 4,
        "learning_objectives": []
    }

class BatchRequest(BaseModel):
    s3_keys: List[str]
    teacher_id: int
    generation_schema: Dict[str, Any] = {
        "difficulty": "intermediate", 
        "duration_weeks": 4
    }

@router.post("/agents/pipeline")
async def run_agent_pipeline(request: PipelineRequest):
    """Run complete Amazon Q agent pipeline"""
    
    try:
        result = await orchestrator.process_complete_pipeline(
            request.s3_key,
            request.teacher_id,
            request.generation_schema
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/agents/batch")
async def run_batch_processing(request: BatchRequest):
    """Run batch processing with multiple files"""
    
    try:
        result = await orchestrator.process_batch_content(
            request.s3_keys,
            request.teacher_id,
            request.generation_schema
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agents/status/{pipeline_id}")
async def get_pipeline_status(pipeline_id: str):
    """Get status of running pipeline"""
    
    # Mock status for now
    return {
        "pipeline_id": pipeline_id,
        "status": "completed",
        "progress": 100,
        "current_stage": "assessment_generation",
        "estimated_completion": "2024-01-01T12:00:00Z"
    }