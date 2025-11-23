import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { ArrowLeft, Clock, CheckCircle, XCircle, Brain, Target } from 'lucide-react';

const StudentQuiz = () => {
  const { quizId } = useParams();
  const navigate = useNavigate();
  const [quiz, setQuiz] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [timeLeft, setTimeLeft] = useState(0);
  const [loading, setLoading] = useState(true);
  const [submitted, setSubmitted] = useState(false);
  const [results, setResults] = useState(null);

  useEffect(() => {
    fetchQuiz();
  }, [quizId]);

  useEffect(() => {
    let timer;
    if (timeLeft > 0 && !submitted) {
      timer = setInterval(() => {
        setTimeLeft(prev => {
          if (prev <= 1) {
            handleSubmit();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }
    return () => clearInterval(timer);
  }, [timeLeft, submitted]);

  const fetchQuiz = async () => {
    try {
      // Mock AI-generated quiz
      const mockQuiz = {
        id: quizId,
        title: 'Linear Equations Practice Quiz',
        description: 'Test your understanding of linear equations',
        timeLimit: 900, // 15 minutes
        questions: [
          {
            id: 1,
            type: 'mcq',
            question: 'Solve for x: 2x + 5 = 13',
            options: ['x = 3', 'x = 4', 'x = 5', 'x = 6'],
            correct: 1,
            explanation: 'Subtract 5 from both sides: 2x = 8, then divide by 2: x = 4'
          },
          {
            id: 2,
            type: 'mcq',
            question: 'What is the slope of the line y = 3x - 2?',
            options: ['3', '-2', '1', '0'],
            correct: 0,
            explanation: 'In the form y = mx + b, the coefficient of x (3) is the slope'
          },
          {
            id: 3,
            type: 'short',
            question: 'Find the y-intercept of the equation y = -2x + 7',
            correct: '7',
            explanation: 'The y-intercept is the constant term when x = 0, which is 7'
          },
          {
            id: 4,
            type: 'mcq',
            question: 'Which point lies on the line y = 2x + 1?',
            options: ['(1, 3)', '(2, 4)', '(0, 2)', '(3, 6)'],
            correct: 0,
            explanation: 'Substitute x = 1: y = 2(1) + 1 = 3, so (1, 3) is correct'
          },
          {
            id: 5,
            type: 'short',
            question: 'Solve for x: 3x - 7 = 2x + 5',
            correct: '12',
            explanation: 'Subtract 2x from both sides: x - 7 = 5, then add 7: x = 12'
          }
        ]
      };
      
      setQuiz(mockQuiz);
      setTimeLeft(mockQuiz.timeLimit);
      toast.success('Quiz loaded successfully!');
    } catch (error) {
      toast.error('Failed to load quiz');
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerChange = (questionId, answer) => {
    setAnswers(prev => ({ ...prev, [questionId]: answer }));
  };

  const handleSubmit = async () => {
    try {
      setSubmitted(true);
      toast.info('Grading your quiz...');
      
      // Auto-grade quiz
      let correct = 0;
      const questionResults = quiz.questions.map(q => {
        const userAnswer = answers[q.id];
        let isCorrect = false;
        
        if (q.type === 'mcq') {
          isCorrect = userAnswer === q.correct;
        } else if (q.type === 'short') {
          isCorrect = userAnswer?.toLowerCase().trim() === q.correct.toLowerCase();
        }
        
        if (isCorrect) correct++;
        
        return {
          questionId: q.id,
          correct: isCorrect,
          userAnswer,
          correctAnswer: q.type === 'mcq' ? q.options[q.correct] : q.correct,
          explanation: q.explanation
        };
      });
      
      const score = Math.round((correct / quiz.questions.length) * 100);
      
      setResults({
        score,
        correct,
        total: quiz.questions.length,
        questions: questionResults
      });
      
      toast.success(`Quiz completed! You scored ${score}%`);
      
    } catch (error) {
      toast.error('Failed to submit quiz');
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (loading) {
    return (
      <div className="min-h-screen animated-gradient flex items-center justify-center">
        <div className="glass-card p-8 text-center">
          <Brain className="h-16 w-16 text-blue-600 mx-auto mb-4 animate-pulse" />
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-gray-700 font-medium">Loading quiz...</p>
        </div>
      </div>
    );
  }

  if (submitted && results) {
    return (
      <div className="min-h-screen animated-gradient">
        <div className="glass-nav sticky top-0 z-50">
          <div className="max-w-4xl mx-auto px-4 py-4">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate('/student/learning-path')}
                className="glass-button p-3 hover-lift"
              >
                <ArrowLeft className="h-5 w-5 text-white" />
              </button>
              <div>
                <h1 className="text-xl font-bold text-white">Quiz Results</h1>
                <p className="text-white/80 text-sm">{quiz.title}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="max-w-4xl mx-auto px-4 py-8">
          {/* Results Summary */}
          <div className="glass-card p-8 mb-8 text-center">
            <div className={`inline-flex items-center justify-center w-20 h-20 rounded-full mb-4 ${
              results.score >= 80 ? 'bg-green-100' : results.score >= 60 ? 'bg-yellow-100' : 'bg-red-100'
            }`}>
              <span className={`text-3xl font-bold ${
                results.score >= 80 ? 'text-green-600' : results.score >= 60 ? 'text-yellow-600' : 'text-red-600'
              }`}>
                {results.score}%
              </span>
            </div>
            
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Quiz Complete!</h2>
            <p className="text-gray-600 mb-4">
              You got {results.correct} out of {results.total} questions correct
            </p>
            
            <div className="flex justify-center space-x-4">
              <button
                onClick={() => navigate('/student/learning-path')}
                className="glass-button bg-gradient-primary text-white"
              >
                Back to Learning Path
              </button>
              <button
                onClick={() => window.location.reload()}
                className="glass-button bg-gradient-secondary text-white"
              >
                Retake Quiz
              </button>
            </div>
          </div>

          {/* Question Review */}
          <div className="space-y-6">
            {quiz.questions.map((question, index) => {
              const result = results.questions.find(r => r.questionId === question.id);
              return (
                <div key={question.id} className="glass-card p-6">
                  <div className="flex items-start space-x-4">
                    <div className={`p-2 rounded-full ${result.correct ? 'bg-green-100' : 'bg-red-100'}`}>
                      {result.correct ? 
                        <CheckCircle className="h-5 w-5 text-green-600" /> : 
                        <XCircle className="h-5 w-5 text-red-600" />
                      }
                    </div>
                    
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-900 mb-2">
                        Question {index + 1}: {question.question}
                      </h3>
                      
                      <div className="space-y-2 mb-4">
                        <div className="text-sm">
                          <span className="font-medium">Your answer: </span>
                          <span className={result.correct ? 'text-green-600' : 'text-red-600'}>
                            {result.userAnswer || 'No answer'}
                          </span>
                        </div>
                        
                        {!result.correct && (
                          <div className="text-sm">
                            <span className="font-medium">Correct answer: </span>
                            <span className="text-green-600">{result.correctAnswer}</span>
                          </div>
                        )}
                      </div>
                      
                      <div className="glass-card p-4 bg-blue-50">
                        <div className="flex items-start space-x-2">
                          <Brain className="h-4 w-4 text-blue-600 mt-0.5" />
                          <div>
                            <div className="font-medium text-blue-900 text-sm">Explanation:</div>
                            <div className="text-blue-800 text-sm">{result.explanation}</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    );
  }

  const currentQ = quiz.questions[currentQuestion];

  return (
    <div className="min-h-screen animated-gradient">
      {/* Header */}
      <div className="glass-nav sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <h1 className="text-xl font-bold text-white">{quiz.title}</h1>
              <span className="px-3 py-1 bg-white/20 text-white rounded-full text-sm">
                Question {currentQuestion + 1} of {quiz.questions.length}
              </span>
            </div>
            
            <div className={`flex items-center space-x-2 px-3 py-1 rounded-full ${
              timeLeft < 300 ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
            }`}>
              <Clock className="h-4 w-4" />
              <span className="font-mono">{formatTime(timeLeft)}</span>
            </div>
          </div>
          
          <div className="mt-4">
            <div className="w-full bg-white/20 rounded-full h-2">
              <div 
                className="bg-white h-2 rounded-full transition-all duration-300" 
                style={{ width: `${((currentQuestion + 1) / quiz.questions.length) * 100}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>

      {/* Question Content */}
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="glass-card p-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">
            {currentQ.question}
          </h2>
          
          {currentQ.type === 'mcq' && (
            <div className="space-y-3">
              {currentQ.options.map((option, index) => (
                <label key={index} className="glass-card p-4 cursor-pointer hover-lift">
                  <input
                    type="radio"
                    name={`question-${currentQ.id}`}
                    value={index}
                    checked={answers[currentQ.id] === index}
                    onChange={() => handleAnswerChange(currentQ.id, index)}
                    className="sr-only"
                  />
                  <div className={`flex items-center space-x-3 ${
                    answers[currentQ.id] === index ? 'text-blue-600' : 'text-gray-700'
                  }`}>
                    <div className={`w-4 h-4 rounded-full border-2 ${
                      answers[currentQ.id] === index ? 'border-blue-600 bg-blue-600' : 'border-gray-300'
                    }`}>
                      {answers[currentQ.id] === index && <div className="w-2 h-2 bg-white rounded-full m-0.5"></div>}
                    </div>
                    <span>{option}</span>
                  </div>
                </label>
              ))}
            </div>
          )}
          
          {currentQ.type === 'short' && (
            <input
              type="text"
              value={answers[currentQ.id] || ''}
              onChange={(e) => handleAnswerChange(currentQ.id, e.target.value)}
              className="glass-input w-full px-4 py-3 text-gray-900"
              placeholder="Enter your answer..."
            />
          )}
        </div>
        
        {/* Navigation */}
        <div className="flex items-center justify-between mt-8">
          <button
            onClick={() => setCurrentQuestion(Math.max(0, currentQuestion - 1))}
            disabled={currentQuestion === 0}
            className="glass-button text-gray-700 disabled:opacity-50"
          >
            Previous
          </button>
          
          <div className="flex space-x-4">
            {currentQuestion === quiz.questions.length - 1 ? (
              <button
                onClick={handleSubmit}
                className="glass-button bg-gradient-success text-white"
              >
                <Target className="h-4 w-4 mr-2" />
                Submit Quiz
              </button>
            ) : (
              <button
                onClick={() => setCurrentQuestion(Math.min(quiz.questions.length - 1, currentQuestion + 1))}
                className="glass-button bg-gradient-primary text-white"
              >
                Next Question
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default StudentQuiz;