/**
 * Mario Trap Avoidance - Frontend JavaScript
 * Handles UI interactions and API communication
 * 
 * Author: Ayush Khelwal
 * GitHub: Ayush-khelwal2003/AI-project
 */

// Global state
let gridData = null;
let pathData = null;
let currentStep = 0;
let animationInterval = null;

/**
 * Generate a new grid with random traps
 */
async function newGrid() {
    showStatus('Generating new grid...', 'info');
    
    try {
        const response = await fetch('/api/new-grid', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                grid_size: 10,
                trap_count: 15
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to generate grid');
        }
        
        gridData = await response.json();
        pathData = null;
        currentStep = 0;
        
        renderGrid();
        resetStats();
        
        document.getElementById('runBtn').disabled = true;
        document.getElementById('findPathBtn').disabled = false;
        
        showStatus('New grid generated! Click "Find Path" to start.', 'success');
    } catch (error) {
        console.error('Error generating grid:', error);
        showStatus('Error generating grid. Please try again.', 'error');
    }
}

/**
 * Find optimal path using A* with logical reasoning
 */
async function findPath() {
    if (!gridData) {
        showStatus('Please generate a grid first!', 'error');
        return;
    }
    
    showStatus('Finding optimal path with A* + Logic...', 'info');
    document.getElementById('findPathBtn').disabled = true;
    
    try {
        const response = await fetch('/api/find-path', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                grid: gridData.grid
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to find path');
        }
        
        pathData = await response.json();
        
        renderGrid(pathData.visited, pathData.path);
        updateStats(pathData.stats);
        
        document.getElementById('runBtn').disabled = false;
        document.getElementById('findPathBtn').disabled = false;
        
        if (pathData.path.length > 0) {
            showStatus(`✅ Path found! Length: ${pathData.path.length} steps. Click "Run Simulation" to animate.`, 'success');
        } else {
            showStatus('❌ No safe path found! Try generating a new grid.', 'error');
        }
    } catch (error) {
        console.error('Error finding path:', error);
        showStatus('Error finding path. Please try again.', 'error');
        document.getElementById('findPathBtn').disabled = false;
    }
}

/**
 * Run animated simulation of Mario following the path
 */
function runSimulation() {
    if (!pathData || pathData.path.length === 0) {
        showStatus('Please find a path first!', 'error');
        return;
    }
    
    currentStep = 0;
    document.getElementById('runBtn').disabled = true;
    document.getElementById('findPathBtn').disabled = true;
    showStatus('🎬 Running simulation...', 'info');
    
    animationInterval = setInterval(() => {
        if (currentStep < pathData.path.length) {
            renderGrid(pathData.visited, pathData.path, currentStep);
            currentStep++;
        } else {
            clearInterval(animationInterval);
            animationInterval = null;
            document.getElementById('runBtn').disabled = false;
            document.getElementById('findPathBtn').disabled = false;
            showStatus('✅ Simulation complete! Mario reached the goal!', 'success');
        }
    }, 300);
}

/**
 * Reset the current visualization
 */
function reset() {
    if (animationInterval) {
        clearInterval(animationInterval);
        animationInterval = null;
    }
    
    currentStep = 0;
    pathData = null;
    
    if (gridData) {
        renderGrid();
        resetStats();
    }
    
    document.getElementById('runBtn').disabled = true;
    document.getElementById('findPathBtn').disabled = false;
    showStatus('Reset complete. Ready for new search.', 'info');
}

/**
 * Render the grid with current state
 */
function renderGrid(visited = [], path = [], marioStep = -1) {
    if (!gridData) return;
    
    const gridEl = document.getElementById('grid');
    const size = gridData.grid.length;
    
    gridEl.style.gridTemplateColumns = `repeat(${size}, 1fr)`;
    gridEl.innerHTML = '';
    
    // Convert arrays to sets for O(1) lookup
    const visitedSet = new Set(visited.map(v => `${v[0]},${v[1]}`));
    const pathSet = new Set(path.map(p => `${p[0]},${p[1]}`));
    
    // Get Mario's current position during animation
    const marioPos = marioStep >= 0 && marioStep < path.length ? path[marioStep] : null;
    
    // Render each cell
    for (let y = 0; y < size; y++) {
        for (let x = 0; x < size; x++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            
            const posKey = `${x},${y}`;
            
            // Determine cell type and content
            if (marioPos && marioPos[0] === x && marioPos[1] === y) {
                // Mario's current position during animation
                cell.classList.add('mario');
                cell.textContent = '🔴';
            } else if (x === gridData.start[0] && y === gridData.start[1]) {
                // Start position
                cell.classList.add('start');
                cell.textContent = '🔴';
            } else if (x === gridData.goal[0] && y === gridData.goal[1]) {
                // Goal position
                cell.classList.add('goal');
                cell.textContent = '🏁';
            } else if (pathSet.has(posKey)) {
                // Part of optimal path
                cell.classList.add('path');
                cell.textContent = '🔵';
            } else if (gridData.grid[y][x] === 1) {
                // Trap
                cell.classList.add('trap');
                cell.textContent = '💣';
            } else if (gridData.grid[y][x] === 2) {
                // Dangerous zone
                cell.classList.add('dangerous');
                cell.textContent = '⚠️';
            } else if (visitedSet.has(posKey)) {
                // Explored during search
                cell.classList.add('visited');
                cell.textContent = '·';
            } else {
                // Empty cell
                cell.classList.add('empty');
            }
            
            gridEl.appendChild(cell);
        }
    }
}

/**
 * Update statistics display
 */
function updateStats(stats) {
    document.getElementById('explored').textContent = stats.explored;
    document.getElementById('pruned').textContent = stats.pruned;
    document.getElementById('pathLength').textContent = stats.path_length;
    
    const total = stats.explored + stats.pruned;
    const efficiency = total > 0 ? ((stats.pruned / total) * 100).toFixed(1) : 0;
    document.getElementById('efficiency').textContent = efficiency + '%';
}

/**
 * Reset statistics display
 */
function resetStats() {
    document.getElementById('explored').textContent = '0';
    document.getElementById('pruned').textContent = '0';
    document.getElementById('pathLength').textContent = '0';
    document.getElementById('efficiency').textContent = '0%';
}

/**
 * Show status message
 */
function showStatus(message, type) {
    const statusEl = document.getElementById('status');
    statusEl.textContent = message;
    statusEl.className = `status ${type}`;
}

/**
 * Initialize application on page load
 */
window.addEventListener('DOMContentLoaded', () => {
    console.log('🎮 Mario Trap Avoidance - Application Started');
    console.log('📡 API Ready');
    
    // Generate initial grid
    newGrid();
});

/**
 * Cleanup on page unload
 */
window.addEventListener('beforeunload', () => {
    if (animationInterval) {
        clearInterval(animationInterval);
    }
});

/**
 * Keyboard shortcuts
 */
document.addEventListener('keydown', (event) => {
    // Spacebar: Run simulation
    if (event.code === 'Space' && !document.getElementById('runBtn').disabled) {
        event.preventDefault();
        runSimulation();
    }
    
    // Enter: Find path
    if (event.code === 'Enter' && !document.getElementById('findPathBtn').disabled) {
        event.preventDefault();
        findPath();
    }
    
    // R: Reset
    if (event.code === 'KeyR' && event.ctrlKey) {
        event.preventDefault();
        reset();
    }
    
    // N: New grid
    if (event.code === 'KeyN' && event.ctrlKey) {
        event.preventDefault();
        newGrid();
    }
});

// Export functions for potential module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        newGrid,
        findPath,
        runSimulation,
        reset
    };
}