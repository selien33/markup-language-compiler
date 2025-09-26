from graphviz import Digraph

def add_node(dot, parent_id, node):
    """Recursively add nodes to the graph from the tree."""
    if isinstance(node, dict):
        for key, value in node.items():
            node_id = f"{parent_id}_{key}"
            dot.node(node_id, label=key)
            dot.edge(parent_id, node_id)  # Connect parent to current node
            # Recursively add children
            add_node(dot, node_id, value)
    elif isinstance(node, list):
        for idx, item in enumerate(node):
            node_id = f"{parent_id}_list_{idx}"
            dot.node(node_id, label=f"List Item {idx}")
            dot.edge(parent_id, node_id)
            add_node(dot, node_id, item)
    else:
        # Leaf node (value of the tree)
        node_id = f"{parent_id}_leaf"
        dot.node(node_id, label=str(node))
        dot.edge(parent_id, node_id)

def generate_tree_image(tree_data):
    """Generate and save a graphical tree from tree data."""
    dot = Digraph(comment='Parse Tree')

    # Initialize root
    dot.node('root', label="Root")
    
    # Add tree nodes recursively
    add_node(dot, 'root', tree_data)
    
    # Render and save the tree as an image (PNG format)
    dot.render('parse_tree', format='png', cleanup=True)
    print("Parse tree image generated as 'parse_tree.png'")