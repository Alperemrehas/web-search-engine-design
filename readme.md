# Search Engine Indexing Simulation

This repository contains a Python-based implementation of a simulation for search engine indexing methods. The project includes term-based and document-based partitioning of search index data and evaluates the performance of these methods using various metrics.

## Overview

The goal of this project is to simulate two partitioning methods for search engine indexing:
1. Term-Based Partitioning: Terms are assigned to nodes in a round-robin fashion.
2. Document-Based Partitioning: Each node stores a fraction of the posting lists for every term.

The simulation evaluates the query processing cost for each partitioning method over a given set of queries.

## Features
- Simulates term-based and document-based partitioning methods.
- Evaluates query processing costs for both methods.
- Generates detailed logs, cost analysis, and load distribution plots.
- Saves results to a `results/` directory for easy analysis.

## Directory Structure
```
.
├── data/
│   ├── data.txt        # Input file containing terms and posting list lengths.
│   ├── querries.topics        # Input file containing queries.
├── results/
│   ├── term_based_costs_K8.txt       # Term-based costs for K=8.
│   ├── term_based_costs_K32.txt      # Term-based costs for K=32.
│   ├── document_based_cost_K8.txt    # Document-based cost for K=8.
│   ├── document_based_cost_K32.txt   # Document-based cost for K=32.
│   ├── execution_log.txt             # Execution details and timings.
│   ├── Term-Based_Partitioning_K8.png
│   ├── Term-Based_Partitioning_K32.png
├── main.py                 # Main script for the simulation.
└── README.md               # Documentation for the project.
```

## Getting Started

### Prerequisites
- Python 3.7 or higher
- Required libraries:
  - `matplotlib`

Install the required library:
```bash
pip install matplotlib
```

### Data Files
Place the following input files in the `data/` directory:
- `data.txt`: A file containing terms, posting list lengths, and IDF-like values (e.g., `term PLL IDF`).
- `querries.topics`: A file containing query IDs and query strings (e.g., `1:query text`).

### Running the Simulation
Execute the main script:
```bash
python main.py
```

### Outputs
1. Execution Logs: Stored in `results/execution_log.txt`, including:
   - Data loading time.
   - Partitioning execution times.
   - File paths for saved costs and plots.

2. Costs:
   - Term-based costs: `results/term_based_costs_K8.txt`, `results/term_based_costs_K32.txt`
   - Document-based costs: `results/document_based_cost_K8.txt`, `results/document_based_cost_K32.txt`

3. Plots:
   - Load distribution plots: `results/Term-Based_Partitioning_K8.png`, `results/Term-Based_Partitioning_K32.png`

## Details of the Simulation

### Partitioning Methods
1. Term-Based Partitioning:
   - Terms are distributed across nodes using round-robin assignment.
   - Costs include node-level query processing and broker-level computation for distributed terms.

2. Document-Based Partitioning:
   - Each node stores a fraction (1/K) of the postings for every term.
   - All processing occurs at the node, so no broker cost is incurred.

### Metrics
- Query Processing Cost (QPq):
  - Calculated as the sum of:
    - Maximum cost among nodes.
    - Broker computation cost (if applicable).

### Results
- Average query processing costs and load distribution are computed for both methods.

## Contributing
If you would like to contribute, please fork the repository and submit a pull request with your improvements.

## License
This project is provided under the MIT License.
