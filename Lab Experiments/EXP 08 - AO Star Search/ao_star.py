"""
AO* Search Algorithm
Problem: Implement the AO* heuristic search algorithm to find an optimal solution tree
in an AND-OR graph.
Cost calculation:
  For an OR node: cost(n) = min { c(n, child) + h(child) }
  For an AND branch: cost(n) = sum { c(n, child) + h(child) }
"""

class AOStarGraph:
    def __init__(self, graph, heuristic, start_node):
        self.graph = graph                # Representation: {node: [[child1, child2], [child3]]} (each sublist is an AND branch)
        self.heuristic = heuristic        # Current cost / heuristic estimates: {node: value}
        self.start = start_node           # Root start node
        self.solved = set()               # Set of nodes verified as solved
        self.solution_tree = {}           # Best branch pointers for each node

    def get_branch_cost(self, parent, branch):
        """
        Calculates the total cost for an AND branch:
        Cost = Sum of (edge_cost + h(child)) for each child in branch.
        (Standard edge cost = 1 per child edge).
        """
        edge_cost = 1
        return sum(edge_cost + self.heuristic.get(child, 0) for child in branch)

    def compute_minimum_cost_branch(self, node):
        """
        Finds the minimum cost hyper-arc / branch for a node among its options.
        Returns: (min_cost, best_branch)
        """
        branches = self.graph.get(node, [])
        if not branches:
            return self.heuristic.get(node, 0), None

        min_cost = float('inf')
        best_branch = None

        for branch in branches:
            cost = self.get_branch_cost(node, branch)
            if cost < min_cost:
                min_cost = cost
                best_branch = branch

        return min_cost, best_branch

    def ao_star(self, node):
        """
        Recursive AO* procedure:
        1. Explores non-terminal children along the best marked branch.
        2. Updates costs and backpropagates improvements.
        3. Marks nodes as solved when all children in the chosen branch are solved.
        """
        print(f"Exploring node '{node}' (Current heuristic: {self.heuristic[node]})")

        branches = self.graph.get(node, [])
        # Terminal leaf node check
        if not branches:
            if self.heuristic[node] == 0:
                self.solved.add(node)
                print(f"  Node '{node}' is a solved terminal leaf.")
            return

        # Find best branch and update node heuristic
        min_cost, best_branch = self.compute_minimum_cost_branch(node)
        self.heuristic[node] = min_cost
        self.solution_tree[node] = best_branch

        # Recurse on unsolved children in the best branch
        all_children_solved = True
        for child in best_branch:
            if child not in self.solved:
                self.ao_star(child)
            if child not in self.solved:
                all_children_solved = False

        # Re-evaluate node cost after child expansions (bottom-up cost revision)
        revised_min_cost, revised_best_branch = self.compute_minimum_cost_branch(node)
        self.heuristic[node] = revised_min_cost
        self.solution_tree[node] = revised_best_branch

        if all_children_solved:
            self.solved.add(node)
            print(f"  [SOLVED] Node '{node}' is now completely solved with cost {self.heuristic[node]}!")

    def print_solution(self, node, indent=0):
        """Recursively prints the marked optimal solution tree."""
        prefix = " " * indent + ("|-- " if indent > 0 else "")
        branch = self.solution_tree.get(node)
        if branch is None:
            print(f"{prefix}{node} (Leaf, Cost = {self.heuristic[node]})")
        else:
            branch_type = "AND Branch" if len(branch) > 1 else "OR Branch"
            print(f"{prefix}{node} -> {branch} [{branch_type}, Cost = {self.heuristic[node]}]")
            for child in branch:
                self.print_solution(child, indent + 4)


if __name__ == "__main__":
    # AND-OR Graph Definition:
    # A has two choices:
    #   Choice 1: AND branch with children [B, C]
    #   Choice 2: Single child [D]
    # B has single child [E]
    # C has choice between [F] or [G]
    # D has AND branch [H, I]
    # Terminal leaves: E, F, G, H, I (heuristic = 0 indicates goal/solved)
    and_or_graph = {
        'A': [['B', 'C'], ['D']],
        'B': [['E']],
        'C': [['F'], ['G']],
        'D': [['H', 'I']],
        'E': [],
        'F': [],
        'G': [],
        'H': [],
        'I': []
    }

    initial_heuristics = {
        'A': 10,
        'B': 4,
        'C': 2,
        'D': 5,
        'E': 0,  # Terminal goal
        'F': 0,  # Terminal goal
        'G': 3,
        'H': 0,  # Terminal goal
        'I': 0   # Terminal goal
    }

    print("=== AO* Algorithm on AND-OR Graph ===")
    print("Initial Heuristics:", initial_heuristics)
    print("Graph Structure:", and_or_graph)
    print("-" * 50)

    solver = AOStarGraph(and_or_graph, initial_heuristics, 'A')

    iteration = 1
    while solver.start not in solver.solved:
        print(f"\n--- AO* Iteration {iteration} ---")
        solver.ao_star(solver.start)
        iteration += 1

    print("\n" + "=" * 50)
    print(f"OPTIMAL SOLUTION FOUND FOR ROOT '{solver.start}'!")
    print(f"Total Optimal Cost: {solver.heuristic[solver.start]}")
    print("\nOptimal Solution Subgraph / Decision Tree:")
    solver.print_solution(solver.start)
