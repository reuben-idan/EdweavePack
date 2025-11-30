import boto3
import json
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import asyncio
import aiohttp

logger = logging.getLogger(__name__)

class AWSAIService:
    """Comprehensive AWS AI service integration"""
    
    def __init__(self, region: str = "us-east-1"):
        self.region = region
        
        # Initialize AWS clients
        self.bedrock = boto3.client('bedrock-runtime', region_name=region)
        self.textract = boto3.client('textract', region_name=region)
        self.comprehend = boto3.client('comprehend', region_name=region)
        self.polly = boto3.client('polly', region_name=region)
        self.transcribe = boto3.client('transcribe', region_name=region)
        self.translate = boto3.client('translate', region_name=region)
        self.rekognition = boto3.client('rekognition', region_name=region)
        self.personalize = boto3.client('personalize-runtime', region_name=region)
        self.forecast = boto3.client('forecast', region_name=region)
        self.kendra = boto3.client('kendra', region_name=region)
        
    async def analyze_document_content(self, s3_bucket: str, s3_key: str) -> Dict[str, Any]:
        """Extract and analyze document content using Textract + Comprehend"""
        
        try:
            # Extract text with Textract
            textract_response = self.textract.detect_document_text(
                Document={'S3Object': {'Bucket': s3_bucket, 'Name': s3_key}}
            )
            
            # Combine extracted text
            extracted_text = ""
            for block in textract_response['Blocks']:
                if block['BlockType'] == 'LINE':
                    extracted_text += block['Text'] + " "
            
            # Analyze with Comprehend
            entities = self.comprehend.detect_entities(
                Text=extracted_text[:5000],  # Comprehend limit
                LanguageCode='en'
            )
            
            key_phrases = self.comprehend.detect_key_phrases(
                Text=extracted_text[:5000],
                LanguageCode='en'
            )
            
            sentiment = self.comprehend.detect_sentiment(
                Text=extracted_text[:5000],
                LanguageCode='en'
            )
            
            return {
                "extracted_text": extracted_text,
                "entities": entities['Entities'],
                "key_phrases": [kp['Text'] for kp in key_phrases['KeyPhrases']],
                "sentiment": sentiment['Sentiment'],
                "confidence": sentiment['SentimentScore']
            }
            
        except Exception as e:
            logger.error(f"Document analysis failed: {e}")
            return {"error": str(e)}
    
    async def generate_curriculum_with_bedrock(self, content: str, subject: str, grade_level: str) -> Dict[str, Any]:
        """Generate curriculum using Bedrock Claude"""
        
        prompt = f"""
        Create a comprehensive 4-week curriculum for {subject} at {grade_level} level.
        
        Source Content: {content[:2000]}
        
        Generate a detailed curriculum with:
        1. Learning objectives aligned with Bloom's taxonomy
        2. Weekly modules with specific activities
        3. Assessment strategies
        4. Differentiation for diverse learners
        5. Technology integration opportunities
        
        Return as structured JSON with modules, objectives, and assessments.
        """
        
        try:
            response = self.bedrock.invoke_model(
                modelId="anthropic.claude-3-sonnet-20240229-v1:0",
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 4000,
                    "messages": [{"role": "user", "content": prompt}]
                })
            )
            
            result = json.loads(response['body'].read())
            content_text = result['content'][0]['text']
            
            # Parse JSON from Claude response
            try:
                curriculum_data = json.loads(content_text)
            except:
                # Fallback if Claude doesn't return valid JSON
                curriculum_data = {
                    "title": f"{subject} Curriculum - {grade_level}",
                    "description": content_text[:500],
                    "modules": self._create_fallback_modules(subject, grade_level)
                }
            
            return curriculum_data
            
        except Exception as e:
            logger.error(f"Bedrock curriculum generation failed: {e}")
            return self._create_fallback_curriculum(subject, grade_level)
    
    async def generate_assessment_questions(self, curriculum_data: Dict, difficulty: str = "medium") -> List[Dict]:
        """Generate assessment questions using Bedrock"""
        
        prompt = f"""
        Generate 10 assessment questions based on this curriculum:
        
        Curriculum: {json.dumps(curriculum_data, indent=2)[:1500]}
        Difficulty: {difficulty}
        
        Create a mix of:
        - 5 multiple choice questions
        - 3 short answer questions  
        - 2 essay questions
        
        Each question should include:
        - question_text
        - question_type
        - bloom_level
        - points
        - correct_answer or sample_answer
        - explanation
        
        Return as JSON array.
        """
        
        try:
            response = self.bedrock.invoke_model(
                modelId="anthropic.claude-3-sonnet-20240229-v1:0",
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 3000,
                    "messages": [{"role": "user", "content": prompt}]
                })
            )
            
            result = json.loads(response['body'].read())
            content_text = result['content'][0]['text']
            
            try:
                questions = json.loads(content_text)
                return questions if isinstance(questions, list) else []
            except:
                return self._create_fallback_questions()
                
        except Exception as e:
            logger.error(f"Assessment generation failed: {e}")
            return self._create_fallback_questions()
    
    async def auto_grade_response(self, question: Dict, student_answer: str) -> Dict[str, Any]:
        """Auto-grade student responses using Bedrock"""
        
        if question.get('question_type') == 'multiple_choice':
            is_correct = student_answer.strip().lower() == question.get('correct_answer', '').strip().lower()
            return {
                "score": question.get('points', 5) if is_correct else 0,
                "max_score": question.get('points', 5),
                "is_correct": is_correct,
                "feedback": "Correct!" if is_correct else f"Incorrect. The correct answer is {question.get('correct_answer')}"
            }
        
        # Use Bedrock for open-ended responses
        prompt = f"""
        Grade this student response:
        
        Question: {question.get('question_text')}
        Student Answer: {student_answer}
        Sample Answer: {question.get('sample_answer', 'Not provided')}
        Max Points: {question.get('points', 10)}
        
        Provide:
        1. Score (0 to {question.get('points', 10)})
        2. Constructive feedback
        3. Strengths identified
        4. Areas for improvement
        
        Return as JSON with score, feedback, strengths, improvements.
        """
        
        try:
            response = self.bedrock.invoke_model(
                modelId="anthropic.claude-3-sonnet-20240229-v1:0",
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1000,
                    "messages": [{"role": "user", "content": prompt}]
                })
            )
            
            result = json.loads(response['body'].read())
            content_text = result['content'][0]['text']
            
            try:
                grading_result = json.loads(content_text)
                return grading_result
            except:
                # Fallback grading
                return {
                    "score": question.get('points', 10) * 0.8,
                    "feedback": "Good response with room for improvement",
                    "strengths": ["Clear understanding shown"],
                    "improvements": ["Add more specific examples"]
                }
                
        except Exception as e:
            logger.error(f"Auto-grading failed: {e}")
            return {"score": 0, "feedback": "Unable to grade response"}
    
    async def generate_learning_insights(self, student_data: List[Dict]) -> Dict[str, Any]:
        """Generate learning analytics using Comprehend + Bedrock"""
        
        # Analyze student performance patterns
        performance_text = " ".join([
            f"Student {data.get('student_id')} scored {data.get('score', 0)} on {data.get('assessment', 'unknown')}"
            for data in student_data[:50]  # Limit for processing
        ])
        
        try:
            # Use Comprehend for sentiment analysis of performance
            sentiment = self.comprehend.detect_sentiment(
                Text=performance_text[:5000],
                LanguageCode='en'
            )
            
            # Use Bedrock for deeper insights
            prompt = f"""
            Analyze this student performance data and provide educational insights:
            
            Performance Data: {json.dumps(student_data[:10], indent=2)}
            Overall Sentiment: {sentiment['Sentiment']}
            
            Provide:
            1. Learning patterns identified
            2. Common misconceptions
            3. Recommended interventions
            4. Differentiation strategies
            5. Progress predictions
            
            Return as structured JSON.
            """
            
            response = self.bedrock.invoke_model(
                modelId="anthropic.claude-3-sonnet-20240229-v1:0",
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 2000,
                    "messages": [{"role": "user", "content": prompt}]
                })
            )
            
            result = json.loads(response['body'].read())
            insights_text = result['content'][0]['text']
            
            try:
                insights = json.loads(insights_text)
                insights['sentiment_analysis'] = sentiment
                return insights
            except:
                return {
                    "learning_patterns": "Mixed performance levels observed",
                    "sentiment_analysis": sentiment,
                    "recommendations": ["Provide additional support", "Use varied teaching methods"]
                }
                
        except Exception as e:
            logger.error(f"Learning insights generation failed: {e}")
            return {"error": str(e)}
    
    async def text_to_speech(self, text: str, voice_id: str = "Joanna") -> bytes:
        """Convert text to speech using Polly"""
        
        try:
            response = self.polly.synthesize_speech(
                Text=text[:3000],  # Polly limit
                OutputFormat='mp3',
                VoiceId=voice_id,
                Engine='neural'
            )
            
            return response['AudioStream'].read()
            
        except Exception as e:
            logger.error(f"Text-to-speech failed: {e}")
            return b""
    
    async def translate_content(self, text: str, target_language: str = "es") -> str:
        """Translate content using AWS Translate"""
        
        try:
            response = self.translate.translate_text(
                Text=text[:5000],  # Translate limit
                SourceLanguageCode='en',
                TargetLanguageCode=target_language
            )
            
            return response['TranslatedText']
            
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            return text
    
    def _create_fallback_modules(self, subject: str, grade_level: str) -> List[Dict]:
        """Create fallback curriculum modules"""
        return [
            {
                "week": 1,
                "title": f"Introduction to {subject}",
                "objectives": [f"Understand basic {subject} concepts"],
                "activities": ["Reading", "Discussion", "Practice"],
                "assessment": "Quiz"
            },
            {
                "week": 2,
                "title": f"Applied {subject}",
                "objectives": [f"Apply {subject} knowledge"],
                "activities": ["Problem solving", "Projects"],
                "assessment": "Assignment"
            }
        ]
    
    def _create_fallback_curriculum(self, subject: str, grade_level: str) -> Dict[str, Any]:
        """Create fallback curriculum structure"""
        return {
            "title": f"{subject} Curriculum - {grade_level}",
            "description": f"Comprehensive {subject} curriculum for {grade_level} students",
            "modules": self._create_fallback_modules(subject, grade_level),
            "duration_weeks": 4,
            "ai_generated": True
        }
    
    def _create_fallback_questions(self) -> List[Dict]:
        """Create fallback assessment questions"""
        return [
            {
                "question_text": "What are the main concepts covered in this unit?",
                "question_type": "multiple_choice",
                "bloom_level": "Remember",
                "points": 5,
                "options": ["Concept A", "Concept B", "Concept C", "All of the above"],
                "correct_answer": "All of the above",
                "explanation": "This unit covers multiple key concepts"
            },
            {
                "question_text": "Explain how you would apply these concepts in practice.",
                "question_type": "short_answer",
                "bloom_level": "Apply",
                "points": 10,
                "sample_answer": "Students should demonstrate practical application",
                "explanation": "This tests application of learned concepts"
            }
        ]