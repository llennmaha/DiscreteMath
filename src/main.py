import heapq
import sys
from collections import Counter, defaultdict
import functools

print = functools.partial(print, flush=True)

# KONFIGURASI 
BASE_DELAY = 1000.0
EPS = sys.float_info.epsilon * 100
N_TURNS = 100

AP_BUFF_schedule = {5: (3, +3), 15: (8, +2)}
SPEED_BUFF_schedule = {10: (2, +30, 3), 25: (7, -40, 2)}

# Speed pemain sesuai data
speeds = {
    1: 123, 2: 167, 3: 157, 4: 138,
    5: 123, 6: 127, 7: 132, 8: 139,
    9: 147, 10: 146, 11: 129, 12: 130
}

active_speed_buffs = defaultdict(list)
turn_count = Counter()

def almost_equal(a, b):
    return abs(a - b) <= max(abs(a), abs(b)) * EPS

def init_queue():
    pq = []
    for pid, sp in speeds.items():
        heapq.heappush(pq, (BASE_DELAY / sp, pid, sp))
    return pq

pq = init_queue()

print("Interactive Scheduler (Enter to run each turn)\n")

for turn_idx in range(1, N_TURNS + 1):
    print(f"\n--- Upcoming Turn {turn_idx} (before pressing Enter) ---")
    upcoming = sorted(pq, key=lambda x: x[0])
    for t, pid, sp in upcoming:
        print(f"Character {pid:2}: t_next = {t:.2f} ms | speed = {sp}")
    input("Press Enter to execute this turn...")

    # Attack Point Buff/Debuff
    if turn_idx in AP_BUFF_schedule:
        pid_b, delta_b = AP_BUFF_schedule[turn_idx]
        t0, pid0, sp0 = pq[0]
        if pid0 == pid_b:
            new_entry = (max(t0 - delta_b, 0), pid0, sp0)
            heapq.heapreplace(pq, new_entry)
            print(f"[AP Buff] Turn {turn_idx}: Character {pid_b} gets AP delta {delta_b:+} ms (new t_next = {new_entry[0]:.2f} ms)")
        else:
            for i, (t, pid, sp) in enumerate(pq):
                if pid == pid_b:
                    new_t = max(t - delta_b, 0)
                    print(f"[AP Buff] Turn {turn_idx}: Character {pid_b} gets AP delta {delta_b:+} ms (old t_next = {t:.2f} ms → new t_next = {new_t:.2f} ms)")
                    pq[i] = (new_t, pid, sp)
                    heapq.heapify(pq)
                    break

    # Speed Buff/Debuff
    if turn_idx in SPEED_BUFF_schedule:
        pid_s, delta_s, dur = SPEED_BUFF_schedule[turn_idx]
        active_speed_buffs[pid_s].append([dur, delta_s])
        speeds[pid_s] += delta_s
        print(f"[Speed Buff] Turn {turn_idx}: Character {pid_s} speed changes by {delta_s:+.1f} for {dur} turns")
        for i, (t, pid, sp) in enumerate(pq):
            if pid == pid_s:
                pq[i] = (t, pid, speeds[pid_s])
                break

    # Execute turn
    t_min, active_pid, active_sp = heapq.heappop(pq)
    print(f"\n>>> TURN {turn_idx}: Character {active_pid} acts now at t = 0.00 ms | speed = {active_sp}")
    turn_count[active_pid] += 1

    # Expire speed buffs
    for pid in list(active_speed_buffs):
        new_list = []
        for dur, delta in active_speed_buffs[pid]:
            if pid == active_pid:
                dur -= 1
            if dur > 0:
                new_list.append([dur, delta])
            else:
                speeds[pid] -= delta
                print(f"[Buff Expired] Character {pid}: speed delta {delta:+.1f} removed")
        active_speed_buffs[pid] = new_list

    # Reset times and requeue
    temp = []
    for t, pid, sp in pq:
        new_t = t - t_min
        temp.append((new_t, pid, sp))
    temp.append((BASE_DELAY / speeds[active_pid], active_pid, speeds[active_pid]))
    pq = temp
    heapq.heapify(pq)

print("\n=== SUMMARY ===")
for pid in sorted(speeds):
    print(f"Character {pid:2}: total turns = {turn_count[pid]}")
