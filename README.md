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
├── ai_mcp_tradeoff_results.csv
├── improved_fabric_tradeoff_ai_agent.joblib
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

## 3. How to Download the Project

### Option A: Clone directly as `hello-fabric`

Open a terminal in the FABRIC Jupyter environment:

```text
File -> New -> Terminal
```

Then run:

```bash
cd /home/fabric/work
git clone https://github.com/TruongSon30/ECE_671_final_project.git hello-fabric
cd hello-fabric
```

Check the folder:

```bash
ls
```

Expected files:

```text
README.md
ai_mcp_fabric_recovery_agent_final.ipynb
ai_mcp_tradeoff_results.csv
improved_fabric_tradeoff_ai_agent.joblib
src
```

Then open:

```text
ai_mcp_fabric_recovery_agent_final.ipynb
```

---

### Option B: Copy into an existing `hello-fabric/` folder

If the Hello FABRIC tutorial already created or uses a `hello-fabric/` folder, go into that folder first:

```bash
cd /home/fabric/work/hello-fabric
```

Clone this repository into a temporary folder:

```bash
git clone https://github.com/TruongSon30/ECE_671_final_project.git temp_project
```

Copy the required files into the current `hello-fabric/` folder:

```bash
cp temp_project/README.md .
cp temp_project/ai_mcp_fabric_recovery_agent_final.ipynb .
cp temp_project/ai_mcp_tradeoff_results.csv .
cp temp_project/improved_fabric_tradeoff_ai_agent.joblib .
cp -r temp_project/src .
```

Remove the temporary folder:

```bash
rm -rf temp_project
```

Check the folder:

```bash
ls
```

Expected files:

```text
README.md
ai_mcp_fabric_recovery_agent_final.ipynb
ai_mcp_tradeoff_results.csv
improved_fabric_tradeoff_ai_agent.joblib
src
```

---

### Option C: Download ZIP from GitHub

1. Open the GitHub repository page.
2. Click the green `Code` button.
3. Select `Download ZIP`.
4. Upload the ZIP file into the FABRIC Jupyter environment.
5. Open a terminal and unzip it.

Example:

```bash
cd /home/fabric/work
unzip ECE_671_final_project-main.zip
mv ECE_671_final_project-main hello-fabric
cd hello-fabric
```

Check the folder:

```bash
ls
```

Expected files:

```text
README.md
ai_mcp_fabric_recovery_agent_final.ipynb
ai_mcp_tradeoff_results.csv
improved_fabric_tradeoff_ai_agent.joblib
src
```

---

## 4. Repository Files

| File                                       | Purpose                                                                                                                                                                  |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `README.md`                                | Reproduction guide for the experiment.                                                                                                                                   |
| `ai_mcp_fabric_recovery_agent_final.ipynb` | Main Jupyter notebook for creating the FABRIC topology, configuring routes, measuring the network, loading or training the AI model, and running the final control loop. |
| `src/ai_agent.py`                          | Python helper file for the lightweight AI agent. The notebook imports this file.                                                                                         |
| `improved_fabric_tradeoff_ai_agent.joblib` | Saved trained AI model. This lets the final control-loop experiment run without collecting the full training dataset again.                                              |
| `ai_mcp_tradeoff_results.csv`              | Saved final experiment results from the tradeoff-aware control loop.                                                                                                     |

---

## 5. Project Topology

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

## 6. Required Packages and Tools

Most Python packages should already be available in the FABRIC Jupyter environment. If any package is missing, run this in a notebook cell:

```python
!pip install pandas numpy matplotlib scikit-learn joblib networkx
```

The FABRIC nodes also use standard Linux tools:

```text
ping
iperf3
tc netem
ip route
```

The notebook installs required node-side packages during the resource configuration step.

---

## 7. How to Run the Experiment

### Step 1: Open the notebook

In the FABRIC Jupyter environment, open:

```text
ai_mcp_fabric_recovery_agent_final.ipynb
```

Run the notebook cells from top to bottom.

---

### Step 2: Check FABRIC configuration

The notebook starts by loading FABlib:

```python
from fabrictestbed_extensions.fablib.fablib import FablibManager as fablib_manager

fablib = fablib_manager()
fablib.show_config()
```

The output should show that the FABRIC configuration is valid.

---

### Step 3: Select a FABRIC site

The experiment needs enough resources for five virtual machines and multiple network interfaces.

The final project run used the `MAX` site. Before creating the slice, it is useful to check site resources:

```python
fablib.show_site("MAX")
fablib.show_site("MASS")
```

In the original run, one attempt on `EDUKY` failed during VM provisioning. The failed slice was deleted, and the final run was created on `MAX`.

If a site fails, delete the failed slice:

```python
fablib.delete_slice(slice_name)
```

Then choose another site by changing:

```python
site_name = "MAX"
```

or another available site.

---

### Step 4: Create and configure the slice

The notebook creates the FABRIC slice, adds the five nodes, connects the networks, assigns IP addresses, enables forwarding on the routers, and installs needed packages.

Wait until the slice reaches:

```text
StableOK
```

If the slice reaches:

```text
StableError
```

delete the failed slice and try another site.

---

### Step 5: Run the control loop

Each control-loop round measures and records:

```text
end-to-end RTT
packet loss
throughput
direct path RTT/loss
backup path RTT/loss
direct path score
backup path score
score delta
AI action probability
```

The AI agent predicts one of four routing actions:

```text
KEEP_DIRECT
SWITCH_TO_BACKUP
KEEP_BACKUP
RESTORE_DIRECT
```

The path score is computed as:

```text
score = RTT + 20 * packet_loss
```

Lower score means better path quality.

The score delta is:

```text
score_delta = direct_score - backup_score
```

Interpretation:

```text
positive score_delta -> backup path is better
negative score_delta -> direct path is better
near zero -> paths are similar
```

---

## 8. Using the Saved Model

The repository includes a trained model:

```text
improved_fabric_tradeoff_ai_agent.joblib
```

The notebook can load it with:

```python
import joblib

agent = joblib.load("improved_fabric_tradeoff_ai_agent.joblib")
```

Using the saved model avoids rerunning the full training-data collection process.

---

## 9. Retraining the Model

The notebook also includes a training-data collection and retraining section.

The training process collects live FABRIC measurements under randomized network conditions. It includes:

* random congestion strength
* random congestion start time
* random recovery timing
* gradual degradation
* gradual recovery
* direct-path impairment
* backup-path impairment
* switching cost through a switching margin
* teacher-policy labels

The notebook trains lightweight local models such as:

```text
Decision Tree
Random Forest
Gradient Boosting
```

The best model is saved as:

```text
improved_fabric_tradeoff_ai_agent.joblib
```

Retraining is optional. For reproducing the final demo, the saved model can be used directly.

---

## 10. Expected Final Behavior

A successful final run should show behavior similar to:

| Round  | Expected Behavior                                                            |
| ------ | ---------------------------------------------------------------------------- |
| 1--4   | Direct path is healthy, so the agent keeps the direct path.                  |
| 5      | Direct path becomes degraded, so the agent switches to backup.               |
| 6--13  | Backup path remains better, so the agent keeps backup.                       |
| 14     | Direct path recovers, but the score gap is small, so the agent keeps backup. |
| 15     | Backup path becomes worse, but direct stability is still building.           |
| 16     | Direct path is stable and clearly better, so the agent restores direct.      |
| 17--20 | Direct path remains stable, so the agent keeps direct.                       |

This demonstrates that the controller is not simple failover. It is tradeoff-aware because it compares both paths and avoids unnecessary route switching.

---

## 11. Results Files

The final results are saved in:

```text
ai_mcp_tradeoff_results.csv
```

The notebook also generates plots for:

```text
RTT
packet loss
throughput
direct vs backup path score
path preference signal
```

These plots show:

* direct-path degradation
* switching to the backup route
* temporary backup-path degradation
* restoring the direct route
* tradeoff-aware decision behavior

---

## 12. Cleanup

When finished, delete the FABRIC slice to release resources:

```python
fablib.delete_slice(slice_name)
```

You can check active slices with:

```python
fablib.list_slices()
```

Do not leave the slice running after finishing the experiment.

---

## 13. Troubleshooting

### Slice enters `StableError`

This usually means the selected FABRIC site failed to provision one or more virtual machines.

Fix:

1. Delete the failed slice.
2. Check another site using `fablib.show_site()`.
3. Change `site_name`.
4. Rerun slice creation.

Example:

```python
fablib.delete_slice(slice_name)
site_name = "MAX"
```

---

### SSH wait fails

Try rerunning:

```python
slice.wait_ssh(progress=True)
```

If it still fails, check the slice state:

```python
slice.show()
```

---

### `iperf3` fails

Make sure the server-side `iperf3` process is running. The notebook includes:

```python
start_iperf_server()
```

Run this before the final control-loop experiment.

---

### Import error for `src.ai_agent`

Make sure the folder structure is correct:

```text
hello-fabric/
├── ai_mcp_fabric_recovery_agent_final.ipynb
└── src/
    └── ai_agent.py
```

The notebook expects the `src/` folder to be in the same directory as the notebook.

---

## 14. Note on MCP-Inspired Design

This project does not implement a full Model Context Protocol server.

Instead, it uses an MCP-inspired design idea: the AI decision logic is separated from external monitoring and control tools. The AI model receives structured measurements and returns high-level actions, while Python functions safely handle the actual FABRIC commands.

---

## Author

Truong Son Vu
University of Massachusetts Amherst
ECE 671 Final Project
