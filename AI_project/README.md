# 🎮 MARIO TRAP AVOIDANCE

An AI-powered pathfinding game that combines **A* Search Algorithm** with **Logical Reasoning** to navigate Mario through a trap-filled grid.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

- **A* Search Algorithm**: Optimal pathfinding with Manhattan distance heuristic
- **Logical Reasoning**: Intelligent path pruning to avoid dangerous areas
- **Interactive UI**: Real-time visualization of algorithm execution
- **Statistics Dashboard**: Track explored nodes, pruned paths, and efficiency
- **Animated Simulation**: Watch Mario navigate the optimal path
- **REST API**: Clean API endpoints for integration

## 🎯 Demo

Watch Mario navigate through traps using AI!

```
🔴 Mario (Start)  →  🔵 Optimal Path  →  🏁 Goal
      ↓                    ↓                 ↓
   Avoids 💣           Smart AI          Success! ✅
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ayush-khelwal2003/AI-project.git
   cd AI-project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open in browser**
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
AI-project/
├── app.py                 # Flask backend server
├── mario_engine.py        # AI engine (A* + Logic)
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/
│   └── index.html        # Frontend interface
└── static/
    ├── css/
    │   └── style.css     # Styling
    └── js/
        └── main.js       # Frontend logic
```

## 🧠 How It Works

### 1. A* Search Algorithm

The A* algorithm finds the optimal path using:
- **G-score**: Actual cost from start to current node
- **H-score**: Heuristic (Manhattan distance to goal)
- **F-score**: G + H (total estimated cost)

```python
f(n) = g(n) + h(n)
```

### 2. Logical Reasoning

Before exploring a path, the AI checks:
- ❌ Is it a trap? (Immediate rejection)
- ⚠️ Is it surrounded by 3+ dangerous cells? (Heuristic pruning)
- 💰 Is there a safer alternative? (Cost comparison)

### 3. Cost Function

Different terrains have different costs:
- **Empty cells**: Cost = 1
- **Dangerous zones**: Cost = 2 (adjacent to traps)
- **Traps**: Cost = ∞ (avoided completely)

## 🎮 How to Use

1. **Generate Grid**: Click "New Grid" to create a random maze
2. **Find Path**: Click "Find Path" to run the AI algorithm
3. **Watch**: Click "Run Simulation" to see Mario move
4. **Analyze**: Check the statistics panel for performance metrics

## 📊 Algorithm Performance

Typical results:
- **Nodes Explored**: ~40-60 (out of 100 cells)
- **Paths Pruned**: ~20-30 (40-50% reduction)
- **Path Length**: ~15-20 steps
- **Success Rate**: ~95%

## 🛠️ API Endpoints

### POST `/api/new-grid`
Generate a new grid with traps

**Request:**
```json
{
  "grid_size": 10,
  "trap_count": 15
}
```

**Response:**
```json
{
  "grid": [[0, 0, 1, ...], ...],
  "start": [0, 0],
  "goal": [9, 9]
}
```

### POST `/api/find-path`
Find optimal path using A* + Logic

**Request:**
```json
{
  "grid": [[0, 0, 1, ...], ...]
}
```

**Response:**
```json
{
  "path": [[0,0], [0,1], ...],
  "visited": [[0,0], [1,0], ...],
  "stats": {
    "explored": 45,
    "pruned": 23,
    "path_length": 18
  }
}
```

## 🎨 Legend

| Symbol | Meaning |
|--------|---------|
| 🔴 | Mario / Start Position |
| 🏁 | Goal Position |
| 💣 | Trap (Instant Fail) |
| ⚠️ | Dangerous Zone |
| 🔵 | Optimal Path |
| · | Explored Node |

## 🔬 Algorithm Complexity

- **Time Complexity**: O(b^d) where b = branching factor, d = depth
- **Space Complexity**: O(b^d)
- **Optimization**: Logical pruning reduces effective b by ~40%

## 🎓 Educational Value

This project demonstrates:
- Graph search algorithms (A*)
- Heuristic functions
- Priority queues (heaps)
- Logical reasoning in AI
- Full-stack web development
- REST API design

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Ayush Khelwal**
- GitHub: [@Ayush-khelwal2003](https://github.com/Ayush-khelwal2003)

## 🙏 Acknowledgments

- Inspired by classic Mario games
- A* algorithm by Peter Hart, Nils Nilsson, and Bertram Raphael
- Built with Flask and modern web technologies

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

⭐ Star this repo if you find it helpful!