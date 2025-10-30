from flask_cors import CORS
from flask import Flask, request, jsonify, render_template
import time

# --- Import your puzzle code ---
from main import PuzzleNode, bfs, dfs, iddfs, A_star

app = Flask(__name__)
CORS(app) # To allow the Javascript frontend to make requests

def get_solution_path(goal_node):
    #Helper function to trace the path from the goal node back to the start
    
    path_actions = []
    current_node = goal_node
    
    while current_node.parent_node is not None:
        path_actions.append(current_node.parent_action)
        current_node = current_node.parent_node
        
    path_actions.reverse() # The path is traced from end to start, so reverse it
    return path_actions

# --- Main API Endpoint ---
@app.route("/")
def home():
    return render_template("index.html")
@app.route('/solve', methods=['POST'])
def solve_puzzle():
    try:
        data = request.json
        
        # 1. Get state from frontend (ensure it's a tuple)
        initial_state = tuple(data['initial_state'])
        algorithm = data['algorithm']
        
        print(f"Request received: State={initial_state}, Algorithm={algorithm}")

        solution_node = None
        nodes_expanded_count = 0
        
        start_time = time.time()
        
        # 2. Select algorithm based on frontend request
        if algorithm == 'bfs':
            solution_node, _, nodes_expanded_count = bfs(initial_state)
            
        elif algorithm == 'dfs':
            solution_node, _, nodes_expanded_count = dfs(initial_state)
            
        elif algorithm == 'iddfs':
            limit = 30 # Default depth limit for IDDFS
            solution_node, _, nodes_expanded_count = iddfs(initial_state, limit)

        elif algorithm == 'a_star_manhattan':
            solution_node, _, nodes_expanded_count = A_star(initial_state, h_name="Manhattan")
            
        elif algorithm == 'a_star_euclidean':
            solution_node, _, nodes_expanded_count = A_star(initial_state, h_name="Euclidean")
            
        else:
            return jsonify({"error": "Unknown algorithm"}), 400
        
        end_time = time.time()
        search_time = end_time - start_time

        # 3. Format the response
        if solution_node:
            # If solution found, trace the path
            path = get_solution_path(solution_node)
            result = {
                "path": path,
                "cost": solution_node.g,
                "nodes_expanded": nodes_expanded_count,
                "search_depth": solution_node.g,
                "time_taken": search_time
            }
            return jsonify(result)
        else:
            return jsonify({"error": "Solution not found"}), 404

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the server
    app.run(debug=True, port=5000,host="0.0.0.0")

