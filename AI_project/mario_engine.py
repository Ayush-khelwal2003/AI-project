"""
Mario Trap Avoidance - AI Engine
Implements A* Search Algorithm with Logical Reasoning

Algorithm Components:
1. A* Search: Optimal pathfinding with Manhattan distance heuristic
2. Logical Reasoning: Prunes unsafe paths before exploration
3. Cost Function: Penalizes dangerous zones

Author: Ayush Khelwal
GitHub: Ayush-khelwal2003/AI-project
"""

import heapq
import random
from collections import defaultdict
from typing import List, Tuple, Dict, Set

class MarioTrapAvoidance:
    """
    AI Engine for Mario Trap Avoidance Game
    Combines A* pathfinding with logical reasoning to navigate safely
    """
    
    # Cell type constants
    EMPTY = 0
    TRAP = 1
    DANGEROUS = 2
    
    def __init__(self, grid_size: int = 10):
        """
        Initialize the game engine
        
        Args:
            grid_size: Size of the square grid (default: 10x10)
        """
        self.grid_size = grid_size
        self.grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        self.start = (0, 0)
        self.goal = (grid_size - 1, grid_size - 1)
        
    def initialize_grid(self, trap_count: int = 15) -> None:
        """
        Initialize grid with random traps and mark dangerous zones
        
        Args:
            trap_count: Number of traps to place on the grid
        """
        # Reset grid
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        # Place random traps
        traps_placed = 0
        attempts = 0
        max_attempts = trap_count * 10  # Prevent infinite loop
        
        while traps_placed < trap_count and attempts < max_attempts:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            
            # Don't place traps on start or goal positions
            if (x, y) != self.start and (x, y) != self.goal and self.grid[y][x] != self.TRAP:
                self.grid[y][x] = self.TRAP
                traps_placed += 1
            
            attempts += 1
        
        # Mark dangerous zones (cells adjacent to traps)
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.grid[y][x] == self.TRAP:
                    for nx, ny in self.get_neighbors(x, y):
                        if self.grid[ny][nx] == self.EMPTY:
                            self.grid[ny][nx] = self.DANGEROUS
    
    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """
        Get valid neighbor cells (up, down, left, right)
        
        Args:
            x, y: Current cell coordinates
            
        Returns:
            List of valid neighbor coordinates
        """
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Down, Right, Up, Left
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                neighbors.append((nx, ny))
        
        return neighbors
    
    def is_safe_path(self, x: int, y: int) -> bool:
        """
        LOGICAL REASONING: Determine if a path is safe to explore
        
        Rules:
        1. Never walk into traps (immediate failure)
        2. Avoid cells surrounded by 3+ dangerous/trap neighbors (heuristic)
        
        Args:
            x, y: Cell coordinates to evaluate
            
        Returns:
            True if path is safe, False if it should be pruned
        """
        # Rule 1: Never walk into traps
        if self.grid[y][x] == self.TRAP:
            return False
        
        # Rule 2: Avoid cells surrounded by excessive danger
        neighbors = self.get_neighbors(x, y)
        dangerous_count = sum(
            1 for nx, ny in neighbors 
            if self.grid[ny][nx] in [self.DANGEROUS, self.TRAP]
        )
        
        # Heuristic: If 3 or more neighbors are dangerous, prune this path
        # This reduces exploration in high-risk areas
        if dangerous_count >= 3:
            return False
        
        return True
    
    def heuristic(self, pos: Tuple[int, int]) -> int:
        """
        Manhattan distance heuristic for A* algorithm
        
        Args:
            pos: Current position (x, y)
            
        Returns:
            Estimated distance to goal
        """
        return abs(pos[0] - self.goal[0]) + abs(pos[1] - self.goal[1])
    
    def a_star_search(self) -> Dict:
        """
        A* Search Algorithm with Logical Pruning
        
        Combines:
        - A* for optimal pathfinding
        - Manhattan distance heuristic
        - Logical reasoning to prune unsafe paths
        - Dynamic cost penalties for dangerous zones
        
        Returns:
            Dictionary containing:
                - path: List of coordinates from start to goal
                - visited: List of all explored coordinates
                - stats: Algorithm performance metrics
        """
        # Priority queue: (f_score, position)
        open_set = []
        heapq.heappush(open_set, (0, self.start))
        
        # Track path reconstruction
        came_from = {}
        
        # G-score: Cost from start to current node
        g_score = defaultdict(lambda: float('inf'))
        g_score[self.start] = 0
        
        # F-score: G-score + heuristic (estimated total cost)
        f_score = defaultdict(lambda: float('inf'))
        f_score[self.start] = self.heuristic(self.start)
        
        # Statistics tracking
        explored = 0
        pruned = 0
        visited = set()
        
        while open_set:
            # Get node with lowest f_score
            _, current = heapq.heappop(open_set)
            
            # Skip if already visited (can happen with duplicates in heap)
            if current in visited:
                continue
            
            visited.add(current)
            explored += 1
            
            # Goal reached - reconstruct and return path
            if current == self.goal:
                path = self.reconstruct_path(came_from, current)
                return {
                    'path': path,
                    'visited': list(visited),
                    'stats': {
                        'explored': explored,
                        'pruned': pruned,
                        'path_length': len(path)
                    }
                }
            
            # Explore neighbors
            for neighbor in self.get_neighbors(*current):
                # LOGICAL REASONING: Prune unsafe paths
                if not self.is_safe_path(*neighbor):
                    pruned += 1
                    continue
                
                # Calculate movement cost
                # Dangerous zones have higher cost (weight = 2)
                # Empty cells have normal cost (weight = 1)
                move_cost = 2 if self.grid[neighbor[1]][neighbor[0]] == self.DANGEROUS else 1
                tentative_g_score = g_score[current] + move_cost
                
                # Update path if this is better than previous
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor)
                    
                    # Add to open set for exploration
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        # No path found
        return {
            'path': [],
            'visited': list(visited),
            'stats': {
                'explored': explored,
                'pruned': pruned,
                'path_length': 0
            }
        }
    
    def reconstruct_path(self, came_from: Dict, current: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Reconstruct path from goal to start using came_from tracking
        
        Args:
            came_from: Dictionary mapping each node to its predecessor
            current: Current node (should be goal)
            
        Returns:
            List of coordinates forming the path from start to goal
        """
        path = [current]
        
        # Follow the chain of predecessors back to start
        while current in came_from:
            current = came_from[current]
            path.append(current)
        
        # Reverse to get start-to-goal order
        path.reverse()
        
        return path
    
    def print_grid(self, path: List[Tuple[int, int]] = None) -> None:
        """
        Print grid to console (for debugging)
        
        Args:
            path: Optional path to highlight
        """
        path_set = set(path) if path else set()
        
        print("\n" + "=" * (self.grid_size * 3))
        for y in range(self.grid_size):
            row = ""
            for x in range(self.grid_size):
                if (x, y) == self.start:
                    row += "🔴 "
                elif (x, y) == self.goal:
                    row += "🏁 "
                elif (x, y) in path_set:
                    row += "🔵 "
                elif self.grid[y][x] == self.TRAP:
                    row += "💣 "
                elif self.grid[y][x] == self.DANGEROUS:
                    row += "⚠️  "
                else:
                    row += "□ "
            print(row)
        print("=" * (self.grid_size * 3) + "\n")


# Example usage and testing
if __name__ == "__main__":
    print("🎮 Mario Trap Avoidance - AI Engine Test")
    print("=" * 50)
    
    # Create game instance
    game = MarioTrapAvoidance(grid_size=10)
    game.initialize_grid(trap_count=15)
    
    print("Grid generated with traps and dangerous zones")
    game.print_grid()
    
    # Find path
    print("Running A* search with logical reasoning...")
    result = game.a_star_search()
    
    if result['path']:
        print(f"✅ Path found!")
        game.print_grid(result['path'])
        print(f"📊 Statistics:")
        print(f"   Nodes Explored: {result['stats']['explored']}")
        print(f"   Paths Pruned: {result['stats']['pruned']}")
        print(f"   Path Length: {result['stats']['path_length']}")
        efficiency = (result['stats']['pruned'] / (result['stats']['explored'] + result['stats']['pruned'])) * 100
        print(f"   Efficiency: {efficiency:.1f}% pruned")
    else:
        print("❌ No safe path found!")
        print(f"📊 Statistics:")
        print(f"   Nodes Explored: {result['stats']['explored']}")
        print(f"   Paths Pruned: {result['stats']['pruned']}")