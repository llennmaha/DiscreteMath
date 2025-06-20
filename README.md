# DiscreteMath
# Turn-Based Batch Scheduling in ‘Reincarnation Journey: Fantasy Fate’ using Priority Queues

A simulation project that implements turn-based batch scheduling using **priority queues**, inspired by gameplay mechanics from the fictional RPG **Reincarnation Journey: Fantasy Fate**. This system models how in-game character turns are scheduled dynamically based on their priority, simulating fair and strategic turn distribution in a fantasy combat scenario.

## 🧠 Project Overview

In many turn-based RPGs, the order in which characters act can make a significant difference in battle outcomes. This project introduces a batch scheduling system where multiple characters are queued and processed based on **priority levels**, mimicking CPU scheduling techniques to balance responsiveness and fairness.

Key features:
- Priority Queue implemented using heap structures.
- Simulation of turn-based mechanics for characters with varying speed.
- Support for batch mode (multiple characters processed per tick).
- Optional enhancements: Speed buff/debuff and attack point buff/debuff

## 🛠️ Technologies Used

- Language: `Python` 
- Data Structures: Priority Queue (Min Heap)

## 📂 Project Structure

```bash
.
├── src/
│   ├── main.py
├── README.md                 # Project documentation
