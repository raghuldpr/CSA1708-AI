% ==============================================================================
% Depth-First Backtracking for Pathfinding in Prolog
% Problem: Find a path between two cities using depth-first search with backtracking.
% ==============================================================================

% Knowledge Base: Directed or bidirectional road connections between cities with distances
road(delhi, agra, 210).
road(agra, kanpur, 280).
road(kanpur, lucknow, 90).
road(lucknow, varanasi, 320).
road(delhi, jaipur, 270).
road(jaipur, ajmer, 130).
road(ajmer, udaipur, 260).
road(agra, gwalior, 120).
road(gwalior, jhansi, 100).
road(jhansi, kanpur, 220).

% Symmetric connectivity rule: road is bi-directional
connected(X, Y, Distance) :- road(X, Y, Distance).
connected(X, Y, Distance) :- road(Y, X, Distance).

% Pathfinding Base Case: When start city is the destination
dfs_path(Destination, Destination, Visited, [Destination], 0).

% Pathfinding Recursive Step with Backtracking:
% Select an adjacent neighbor that has not yet been visited,
% then recursively explore from the neighbor to the destination.
dfs_path(Current, Destination, Visited, [Current | RestOfPath], TotalCost) :-
    connected(Current, NextCity, Distance),
    \+ member(NextCity, Visited),           % Avoid cyclic loops
    dfs_path(NextCity, Destination, [NextCity | Visited], RestOfPath, RemainingCost),
    TotalCost is Distance + RemainingCost.

% Top-level goal to find and display a path
find_path(Start, Destination) :-
    format('~nSearching for path from ~w to ~w via Depth-First Backtracking:~n', [Start, Destination]),
    dfs_path(Start, Destination, [Start], Path, Cost),
    format('Path Found: ~w~n', [Path]),
    format('Total Distance: ~w km~n~n', [Cost]).

% Main entry point to demonstrate pathfinding
main :-
    writeln('=== Prolog Depth-First Backtracking Pathfinding ==='),
    find_path(delhi, lucknow),
    halt.
