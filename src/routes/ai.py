from flask import Blueprint, request, jsonify, session
import requests
import os
import logging
import json
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint
ai_bp = Blueprint('ai', __name__)

# Gemini API configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'dummy_key_for_development')
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"

@ai_bp.route('/api/ai/editor/assistant', methods=['POST'])
def editor_assistant():
    """
    Editor's AI Assistant powered by Gemini API.
    Provides assistance with editing tasks, suggestions, and creative input.
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    # Check if user has editor role
    if session.get('role') not in ['editor', 'director']:
        return jsonify({'error': 'Access denied. Editor role required.'}), 403
    
    data = request.json
    
    if 'query' not in data:
        return jsonify({'error': 'Query is required'}), 400
    
    # Prepare context for the AI
    context = data.get('context', {})
    project_context = context.get('project', {})
    
    # Construct prompt with editing-specific instructions
    prompt = f"""You are an AI assistant for video editors. 
    
Project context:
- Title: {project_context.get('title', 'Unknown project')}
- Type: {project_context.get('type', 'Unknown type')}
- Current task: {project_context.get('current_task', 'General editing')}

User query: {data['query']}

Provide helpful, specific advice for video editing. Include technical suggestions when appropriate.
"""
    
    try:
        # In a real implementation, this would call the Gemini API
        # For development, we'll simulate a response
        if GEMINI_API_KEY == 'dummy_key_for_development':
            # Simulated response for development
            response = {
                'response': f"Here's my suggestion for '{data['query']}':\n\n"
                           f"Based on your {project_context.get('type', 'project')}, I recommend considering the following editing techniques:\n\n"
                           f"For scene transitions, try using cross-dissolves for smoother flow between shots. This creates a more professional look and helps maintain visual continuity throughout your project.\n\n"
                           f"Consider adjusting the color temperature to create a more cohesive visual style. Warmer tones (around 3200K) can create an intimate, emotional atmosphere, while cooler tones (5600K+) often convey a more clinical or detached feeling.\n\n"
                           f"For pacing, try trimming 1-2 frames from the end of each clip to create a slightly faster rhythm. This subtle adjustment can significantly improve the overall energy of your sequence without feeling rushed.\n\n"
                           f"Would you like more specific advice on any of these techniques?"
            }
        else:
            # Real Gemini API call
            headers = {
                "Content-Type": "application/json",
                "x-goog-api-key": GEMINI_API_KEY
            }
            
            gemini_data = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 1024
                }
            }
            
            # Add retry logic for API resilience
            max_retries = 3
            retry_delay = 2  # seconds
            
            for attempt in range(max_retries):
                try:
                    gemini_response = requests.post(
                        GEMINI_API_URL,
                        headers=headers,
                        json=gemini_data,
                        timeout=10  # Add timeout to prevent hanging requests
                    )
                    
                    if gemini_response.status_code == 200:
                        response_data = gemini_response.json()
                        if 'candidates' in response_data and len(response_data['candidates']) > 0:
                            response_text = response_data['candidates'][0]['content']['parts'][0]['text']
                            response = {'response': response_text}
                            break
                        else:
                            logger.error(f"Unexpected Gemini API response format: {response_data}")
                            if attempt == max_retries - 1:
                                return jsonify({'error': 'Invalid response from Gemini API'}), 500
                    elif gemini_response.status_code == 429:  # Rate limit
                        logger.warning(f"Gemini API rate limit hit, retrying in {retry_delay} seconds")
                        if attempt < max_retries - 1:
                            time.sleep(retry_delay)
                            retry_delay *= 2  # Exponential backoff
                        else:
                            return jsonify({'error': 'Gemini API rate limit exceeded'}), 429
                    else:
                        logger.error(f"Gemini API error: {gemini_response.status_code} - {gemini_response.text}")
                        if attempt == max_retries - 1:
                            return jsonify({'error': f'Gemini API error: {gemini_response.status_code}'}), 500
                except requests.exceptions.RequestException as e:
                    logger.error(f"Request error in Gemini API call: {str(e)}")
                    if attempt == max_retries - 1:
                        return jsonify({'error': f'Connection error: {str(e)}'}), 503
                    time.sleep(retry_delay)
                    retry_delay *= 2
        
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Error in editor assistant: {str(e)}")
        return jsonify({'error': f'Error processing request: {str(e)}'}), 500

@ai_bp.route('/api/ai/music_director/assistant', methods=['POST'])
def music_director_assistant():
    """
    Music Director's AI Assistant.
    Provides assistance with music composition, sound design, and audio suggestions.
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    # Check if user has music director role
    if session.get('role') not in ['music_director', 'director']:
        return jsonify({'error': 'Access denied. Music Director role required.'}), 403
    
    data = request.json
    
    if 'query' not in data:
        return jsonify({'error': 'Query is required'}), 400
    
    # Prepare context for the AI
    context = data.get('context', {})
    project_context = context.get('project', {})
    
    # Construct prompt with music-specific instructions
    prompt = f"""You are an AI assistant for music directors and sound designers. 
    
Project context:
- Title: {project_context.get('title', 'Unknown project')}
- Type: {project_context.get('type', 'Unknown type')}
- Current task: {project_context.get('current_task', 'General sound design')}
- Mood: {project_context.get('mood', 'Not specified')}

User query: {data['query']}

Provide helpful, specific advice for music composition and sound design. Include technical suggestions when appropriate.
"""
    
    try:
        # In a real implementation, this would call the Gemini API
        if GEMINI_API_KEY == 'dummy_key_for_development':
            # Simulated response for development
            response = {
                'response': f"Here's my suggestion for '{data['query']}':\n\n"
                           f"For your {project_context.get('type', 'project')} with a {project_context.get('mood', 'general')} mood, consider these audio approaches:\n\n"
                           f"The emotional tone would benefit from a minor key composition with string instruments for depth. Minor keys naturally evoke contemplative or melancholic feelings, while strings provide a rich harmonic foundation that can support various emotional nuances throughout your project.\n\n"
                           f"For the background ambience, try layering subtle nature sounds with a low-pass filter. This creates an immersive atmosphere without distracting from the primary audio elements. The low-pass filter (set around 500-800Hz) will help these sounds sit further back in the mix.\n\n"
                           f"The transition points would work well with a gradual volume automation curve rather than abrupt changes. Consider using a 2-3 second fade between scenes to maintain the emotional continuity while still clearly delineating different sections.\n\n"
                           f"Would you like me to elaborate on any specific aspect of the sound design?"
            }
        else:
            # Real Gemini API call
            headers = {
                "Content-Type": "application/json",
                "x-goog-api-key": GEMINI_API_KEY
            }
            
            gemini_data = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 1024
                }
            }
            
            # Add retry logic for API resilience
            max_retries = 3
            retry_delay = 2  # seconds
            
            for attempt in range(max_retries):
                try:
                    gemini_response = requests.post(
                        GEMINI_API_URL,
                        headers=headers,
                        json=gemini_data,
                        timeout=10  # Add timeout to prevent hanging requests
                    )
                    
                    if gemini_response.status_code == 200:
                        response_data = gemini_response.json()
                        if 'candidates' in response_data and len(response_data['candidates']) > 0:
                            response_text = response_data['candidates'][0]['content']['parts'][0]['text']
                            response = {'response': response_text}
                            break
                        else:
                            logger.error(f"Unexpected Gemini API response format: {response_data}")
                            if attempt == max_retries - 1:
                                return jsonify({'error': 'Invalid response from Gemini API'}), 500
                    elif gemini_response.status_code == 429:  # Rate limit
                        logger.warning(f"Gemini API rate limit hit, retrying in {retry_delay} seconds")
                        if attempt < max_retries - 1:
                            time.sleep(retry_delay)
                            retry_delay *= 2  # Exponential backoff
                        else:
                            return jsonify({'error': 'Gemini API rate limit exceeded'}), 429
                    else:
                        logger.error(f"Gemini API error: {gemini_response.status_code} - {gemini_response.text}")
                        if attempt == max_retries - 1:
                            return jsonify({'error': f'Gemini API error: {gemini_response.status_code}'}), 500
                except requests.exceptions.RequestException as e:
                    logger.error(f"Request error in Gemini API call: {str(e)}")
                    if attempt == max_retries - 1:
                        return jsonify({'error': f'Connection error: {str(e)}'}), 503
                    time.sleep(retry_delay)
                    retry_delay *= 2
        
        return jsonify(response), 200
    
    except Exception as e:
        logger.error(f"Error in music director assistant: {str(e)}")
        return jsonify({'error': f'Error processing request: {str(e)}'}), 500

@ai_bp.route('/api/ai/music_director/generate', methods=['POST'])
def generate_music():
    """
    Generate music based on parameters.
    In a real implementation, this would connect to a music generation AI.
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    # Check if user has music director role
    if session.get('role') not in ['music_director', 'director']:
        return jsonify({'error': 'Access denied. Music Director role required.'}), 403
    
    data = request.json
    
    # Validate required fields
    required_fields = ['style', 'mood', 'duration']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    try:
        # In a real implementation, this would call a music generation AI
        # For development, we'll simulate a response
        response = {
            'message': 'Music generation request received',
            'status': 'processing',
            'estimated_completion': '30 seconds',
            'request_id': 'music_gen_12345'
        }
        
        return jsonify(response), 202
    
    except Exception as e:
        logger.error(f"Error in music generation: {str(e)}")
        return jsonify({'error': f'Error processing request: {str(e)}'}), 500

@ai_bp.route('/api/ai/editor/analyze', methods=['POST'])
def analyze_video():
    """
    Analyze video content and provide editing suggestions.
    In a real implementation, this would connect to a video analysis AI.
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    # Check if user has editor role
    if session.get('role') not in ['editor', 'director']:
        return jsonify({'error': 'Access denied. Editor role required.'}), 403
    
    # This would typically process a video file
    # For development, we'll simulate a response
    response = {
        'message': 'Video analysis complete',
        'suggestions': [
            {
                'timestamp': '00:01:23',
                'issue': 'Lighting inconsistency',
                'suggestion': 'Consider color grading to match the previous scene'
            },
            {
                'timestamp': '00:02:45',
                'issue': 'Pacing',
                'suggestion': 'This sequence feels too long, consider trimming by 5-10 seconds'
            },
            {
                'timestamp': '00:04:12',
                'issue': 'Audio levels',
                'suggestion': 'Background music is competing with dialogue, reduce by 3-4dB'
            }
        ]
    }
    
    return jsonify(response), 200

@ai_bp.route('/api/ai/status', methods=['GET'])
def ai_status():
    """
    Check the status of the AI integration.
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    # Check if Gemini API is configured
    if GEMINI_API_KEY == 'dummy_key_for_development':
        status = 'development'
        message = 'Running in development mode with simulated AI responses'
    else:
        # Test connection to Gemini API
        try:
            headers = {
                "Content-Type": "application/json",
                "x-goog-api-key": GEMINI_API_KEY
            }
            
            test_data = {
                "contents": [{"parts": [{"text": "Hello, this is a test."}]}],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 10
                }
            }
            
            response = requests.post(
                GEMINI_API_URL,
                headers=headers,
                json=test_data,
                timeout=5
            )
            
            if response.status_code == 200:
                status = 'connected'
                message = 'Successfully connected to Gemini API'
            else:
                status = 'error'
                message = f'Error connecting to Gemini API: {response.status_code}'
        except Exception as e:
            status = 'error'
            message = f'Error testing Gemini API connection: {str(e)}'
    
    return jsonify({
        'status': status,
        'message': message,
        'api_url': GEMINI_API_URL,
        'api_configured': GEMINI_API_KEY != 'dummy_key_for_development'
    }), 200
