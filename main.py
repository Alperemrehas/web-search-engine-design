import os
import math
import matplotlib.pyplot as plt

def load_worldlist(file_path):
    print("Loading worldlist from file: ", file_path)
    print("Absolute path: ", os.path.abspath(file_path))
    
    if not os.path.exists(file_path):
        print("File does not exist.")
        return {}
    
    worldlist = {}
    with open(file_path, 'r') as file:
        for line in file:
            term, pll, _ = line.strip().split()
            worldlist[term] = int(pll)
    return worldlist

def load_querry(file_path):
    print("Loading querry from file: ", file_path)

    if not os.path.exists(file_path):
        print("File not found: ", file_path)
        return []
    
    queries = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                query = line.split(':', 1)[1].strip()
                queries.append(query)
    except UnicodeDecodeError:
        print("UTF-8 decoding failed. Trying with 'latin-1' encoding...")
        with open(file_path, 'r', encoding='latin-1') as file:
            for line in file:
                query = line.split(':', 1)[1].strip()
                queries.append(query)
    return queries

def term_based_partitioning(worldlist, K):
    nodes = {i: {} for i in range(K)}
    for i, (term, pll) in enumerate(worldlist.items()):
        node_id = i % K
        nodes[node_id][term] = pll
    return nodes

def compute_term_based_cost(queries, nodes, K):
    costs_per_node = [0] * K  # Track costs for each node
    broker_costs = []  # Track broker costs for each query
    overall_costs = []  # Track overall costs for each query

    for query in queries:
        query_terms = query.split()
        node_costs = [0] * K
        partial_results = []

        for term in query_terms:
            for node_id, node_terms in nodes.items():
                if term in node_terms:
                    node_costs[node_id] += node_terms[term]
                    partial_results.append(node_terms[term])
                    break

        max_node_cost = max(node_costs)
        broker_cost = sum(min(partial_results[i], partial_results[j]) for i in range(len(partial_results)) for j in range(i, len(partial_results)))
        overall_cost = max_node_cost + broker_cost

        # Update costs
        for i in range(K):
            costs_per_node[i] += node_costs[i]
        broker_costs.append(broker_cost)
        overall_costs.append(overall_cost)

    return costs_per_node, broker_costs, overall_costs

def document_based_partitioning(wordlist, K):
    factor = 1 / K
    partitioned_terms = {term: math.ceil(pll * factor) for term, pll in wordlist.items()}
    return partitioned_terms

def compute_document_based_cost(queries, partitioned_terms):
    costs = 0

    for query in queries:
        query_terms = query.split()
        query_cost = 0

        for term in query_terms:
            if term in partitioned_terms:
                query_cost += partitioned_terms[term]

        costs += query_cost

    return costs

def ensure_results_folder():
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    return results_dir


def plot_load_distribution(costs_per_node, broker_costs, K, title, results_dir):
    plt.bar(range(K), costs_per_node, label="Node Costs")
    plt.bar(K, sum(broker_costs), label="Broker Costs", color='r')
    plt.xlabel("Node ID")
    plt.ylabel("Processing Cost")
    plt.title(title)
    plt.legend()
    # Save plot
    plot_filename = os.path.join(results_dir, f"{title.replace(' ', '_')}.png")
    plt.savefig(plot_filename)
    plt.close()  
    print(f"Plot saved to: {plot_filename}")

def save_costs_to_file(filename, costs):
    with open(filename, 'w') as file:
        for cost in costs:
            file.write(f"{cost}\n")
    print(f"Costs saved to: {filename}")

def main():
    # Create results folder
    results_dir = ensure_results_folder()

    # Load data
    wordlist = load_worldlist('data/wordlist.txt')
    queries = load_querry('data/10000.topics')

    # Term-based partitioning
    for K in [8, 32]:
        print(f"Processing Term-Based Partitioning with K={K}")
        nodes = term_based_partitioning(wordlist, K)
        costs_per_node, broker_costs, overall_costs = compute_term_based_cost(queries, nodes, K)
        
        # Save plot
        plot_load_distribution(costs_per_node, broker_costs, K, f"Term-Based Partitioning (K={K})", results_dir)
        
        # Save costs
        save_costs_to_file(os.path.join(results_dir, f"term_based_costs_K{K}.txt"), overall_costs)

    # Document-based partitioning
    for K in [8, 32]:
        print(f"Processing Document-Based Partitioning with K={K}")
        partitioned_terms = document_based_partitioning(wordlist, K)
        total_cost = compute_document_based_cost(queries, partitioned_terms)
        
        # Save total cost
        with open(os.path.join(results_dir, f"document_based_cost_K{K}.txt"), 'w') as file:
            file.write(f"Total Cost: {total_cost}\n")
        print(f"Total Cost for Document-Based Partitioning (K={K}) saved.")



if __name__ == "__main__":
    main()
