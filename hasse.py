import sys
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

def get_user_input():
    print("Enter the elements of the set A\nYou can add the element in the below mention manner")
    print("1, 2, 5, 8, 10")
    print("This version only supports a|b relation")
    print("Seperate all by commas")
    user_input = input("Enter Here: ")
    elements_str = user_input.replace(" ", "").split(",")
    
    elements = []

    for element in elements_str:
        try:
            value = float(element)

            elements.append(int(value) if value.is_integer() else value)

        except ValueError:
            print(f"{element} is invalid")
            return []
    
    seen = set()
    index = 0

    while index < len(elements):
        element = elements[index]

        if element in seen:
            elements.pop(index)

        else:
            seen.add(element)
            index += 1

    elements = sorted(elements)

    return elements


def generate_divisibility_relations(elements):
    # Actually not a poset because does not have reflexive relations
    relations = []
    for a in elements:
        for b in elements:
            if a != b and b % a == 0:
                relations.append([a, b])
    
    return relations


def remove_transitive_relations(relations):
    to_remove = set()

    relations_set = set(map(tuple, relations))

    for [a, b] in relations:
        for [b2, c] in relations:
            if b2 == b and (a, c) in relations_set:
                to_remove.add((a, c))

    filtered_relations = [pair for pair in relations if tuple(pair) not in to_remove]

    return filtered_relations


def main():
    elements = get_user_input()
    if not elements:
        sys.exit(1)
    relations = generate_divisibility_relations(elements)
    filtered_relations = remove_transitive_relations(relations)
    print(filtered_relations)

    # Create a directed graph
    G = nx.DiGraph()

    # Add edges to the graph
    G.add_edges_from(filtered_relations)

    # Generate positions using NetworkX's spring layout
    pos = nx.spring_layout(G, seed=42)  # Seed for reproducible layout

    # Draw the graph
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_size=500, node_color='lightblue', font_size=12, font_weight='bold', arrows=True, arrowsize=20)

    # Draw edge labels (if any)
    edge_labels = {tuple(edge): "" for edge in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title('Hasse Diagram')
    plt.grid('on')
    plt.show()


if __name__ == "__main__":
    main()