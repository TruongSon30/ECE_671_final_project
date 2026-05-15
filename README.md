# ECE 671 Final Project: Lightweight AI-Assisted Adaptive Path Control on FABRIC

This repository contains the files needed to reproduce the ECE 671 final project experiment on the FABRIC testbed.

This project builds a small routed FABRIC topology with one direct path and one backup path between a client and a server. A lightweight local AI model observes live network measurements, compares the quality of both paths, and decides whether to keep the current route, switch to the backup route, or restore the direct route.

This project should be run **after completing the Hello FABRIC tutorial**:

https://teaching-on-testbeds.github.io/hello-fabric/

All files from this repository must be downloaded or copied into the `hello-fabric/` folder after the tutorial setup is complete.

---

## 1. Required Starting Point

Before running this project, complete the Hello FABRIC tutorial and confirm that the FABRIC environment is working.

The following setup should already be complete:

* FABRIC account access
* FABRIC project membership
* FABRIC Jupyter environment access
* Bastion SSH key setup
* Slice SSH key setup
* FABRIC project ID configuration
* `fabric_rc` configuration file
* Valid FABRIC token
* Working FABlib configuration

You should be able to run this in a FABRIC notebook:

```python
from fabrictestbed_extensions.fablib.fablib import FablibManager as fablib_manager

fablib = fablib_manager()
fablib.show_config()
```

The output should show that the FABRIC configuration and bastion key are valid.

---

## 2. Required Folder Structure

After finishing the Hello FABRIC tutorial, place this project directly inside the `hello-fabric/` folder.

The folder must look like this:

```text
hello-fabric/
├── README.md
├── ai_mcp_fabric_recovery_agent_final.ipynb
├── ai_mcp_tradeoff_results.csv <--- This one will be created during the .ipynb file running
├── improved_fabric_tradeoff_ai_agent.joblib <--- This one will be created during the .ipynb file running
└── src/
    └── ai_agent.py
```

The notebook must stay at the same folder level as `README.md`, and the `src/` folder must stay directly inside `hello-fabric/`.

This is important because the notebook imports the AI helper code from:

```python
from src.ai_agent import ...
```

If the notebook is moved outside the `hello-fabric/` folder, or if the `src/` folder is moved, the import may fail.

---

## 3. Repository Files

| File                                       | Purpose                                                                                                                                                                  |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `README.md`                                | Reproduction guide for the experiment.                                                                                                                                   |
| `ai_mcp_fabric_recovery_agent_final.ipynb` | Main Jupyter notebook for creating the FABRIC topology, configuring routes, measuring the network, loading or training the AI model, and running the final control loop. |
| `src/ai_agent.py`                          | Python helper file for the lightweight AI agent. The notebook imports this file.                                                                                         |
| `improved_fabric_tradeoff_ai_agent.joblib` | Saved trained AI model. This lets the final control-loop experiment run without collecting the full training dataset again.                                              |
| `ai_mcp_tradeoff_results.csv`              | Saved final experiment results from the tradeoff-aware control loop.                                                                                                     |

---

## 4. Project Topology

The notebook creates a five-node FABRIC topology:

```text
client -- r1 -- r2 -- server
          \    /
            r3
```

The direct path is:

```text
client -> r1 -> r2 -> server
```

The backup path is:

```text
client -> r1 -> r3 -> r2 -> server
```

The node names used in the notebook are:

```text
client
server
r1
r2
r3
```

Network segment names follow this naming scheme:

```text
net_<nodeA>_<nodeB>
```

Examples:

```text
net_client_r1
net_r1_r2
net_r1_r3
net_r3_r2
net_r2_server
```

---

## Author

Truong Son Vu
University of Massachusetts Amherst
ECE 671 Final Project
