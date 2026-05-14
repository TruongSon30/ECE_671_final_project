# ECE 671 Final Project: Lightweight AI-Assisted Adaptive Path Control on FABRIC

This repository contains the files needed to reproduce the ECE 671 final project experiment on the FABRIC testbed.

The project implements a lightweight AI-assisted adaptive path controller. It creates a FABRIC topology with a direct path and a backup path between a client and a server. The controller measures network performance, compares direct and backup path quality, and uses a trained local AI model to decide whether to keep the current route, switch to the backup route, or restore the direct route.

---

## Project Overview

The experiment demonstrates a closed-loop network control system:

1. Create a FABRIC slice with five Linux virtual machines.
2. Configure a routed topology with direct and backup paths.
3. Measure RTT, packet loss, and throughput using `ping` and `iperf3`.
4. Simulate path degradation using Linux `tc netem`.
5. Use a lightweight trained AI model to make routing decisions.
6. Save and plot the final control-loop results.

The AI agent predicts one of four routing actions:

```text
KEEP_DIRECT
SWITCH_TO_BACKUP
KEEP_BACKUP
RESTORE_DIRECT
