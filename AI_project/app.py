"""
Mario Trap Avoidance - Flask Backend
AI Hybrid Search: A* Algorithm + Logical Reasoning
Author: Ayush Khelwal
GitHub: Ayush-khelwal2003/AI-project
"""

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from mario_engine import MarioTrapAvoidance

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')

@app.route('/api/new-grid', methods=['POST'])
def new_grid():
    """
    Generate a new grid with random traps
    
    Request JSON:
        {
            "grid_size": int (default: 10),
            "trap_count": int (default: 15)
        }
    
    Response JSON:
        {
            "grid": 2D array,
            "start": [x, y],
            "goal": [x, y]
        }
    """
    data = request.json
    grid_size = data.get('grid_size', 10)
    trap_count = data.get('trap_count', 15)
    
    game = MarioTrapAvoidance(grid_size)
    game.initialize_grid(trap_count)
    
    return jsonify({
        'grid': game.grid,
        'start': game.start,
        'goal': game.goal
    })

@app.route('/api/find-path', methods=['POST'])
def find_path():
    """
    Find optimal path using A* with logical reasoning
    
    Request JSON:
        {
            "grid": 2D array
        }
    
    Response JSON:
        {
            "path": [[x, y], ...],
            "visited": [[x, y], ...],
            "stats": {
                "explored": int,
                "pruned": int,
                "path_length": int
            }
        }
    """
    data = request.json
    grid = data.get('grid')
    
    if not grid:
        return jsonify({'error': 'Grid data required'}), 400
    
    game = MarioTrapAvoidance(len(grid))
    game.grid = grid
    result = game.a_star_search()
    
    return jsonify(result)

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Mario Trap Avoidance API is running'})

if __name__ == '__main__':
    print("=" * 70)
    print("🎮 MARIO TRAP AVOIDANCE - Full Stack Application")
    print("=" * 70)
    print("🚀 Server starting...")
    print("📡 Backend: Flask REST API")
    print("🎨 Frontend: Interactive HTML/CSS/JS")
    print("🧠 AI: A* Search + Logical Reasoning")
    print("=" * 70)
    print("\n🌐 Open your browser and navigate to:")
    print("   👉 http://localhost:5000")
    print("\n💡 Press CTRL+C to stop the server")
    print("=" * 70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)