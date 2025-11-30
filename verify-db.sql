-- Database Verification Queries
-- Run these queries to verify database setup

-- Check if tables exist
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;

-- Count records in key tables
SELECT 'users' as table_name, COUNT(*) as record_count FROM users
UNION ALL
SELECT 'curricula' as table_name, COUNT(*) as record_count FROM curricula  
UNION ALL
SELECT 'assessments' as table_name, COUNT(*) as record_count FROM assessments;

-- Sample users data
SELECT id, email, name, role, institution, created_at 
FROM users 
ORDER BY created_at 
LIMIT 5;

-- Sample curricula data
SELECT id, title, subject, grade_level, ai_generated, amazon_q_powered, created_at
FROM curricula 
ORDER BY created_at 
LIMIT 5;

-- Sample assessments data
SELECT id, title, curriculum_id, total_points, time_limit, ai_generated, created_at
FROM assessments 
ORDER BY created_at 
LIMIT 5;

-- Verify relationships
SELECT 
    c.title as curriculum_title,
    c.subject,
    COUNT(a.id) as assessment_count
FROM curricula c
LEFT JOIN assessments a ON c.id = a.curriculum_id
GROUP BY c.id, c.title, c.subject
ORDER BY c.title;