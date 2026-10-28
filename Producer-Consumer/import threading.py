import threading
import time
import queue
import random

# --- Shared GitHub Repository (Bounded Buffer) ---
BUFFER_SIZE = 3
repo_buffer = []

# Synchronization primitives
buffer_lock = threading.Lock()
empty_slots = threading.Semaphore(BUFFER_SIZE)  # Space available in GitHub repo
full_slots = threading.Semaphore(0)            # Commits available to pull

# Control flag for simulation stop
simulation_running = True

# --- Developer A: Producer ---
def developer_a():
    commit_id = 1
    while simulation_running:
        # Simulate local code creation time
        time.sleep(random.uniform(0.5, 1.2))
        commit_data = f"Commit-{commit_id}: Feature update {commit_id}"
        print(f"[Dev A (Producer)]  Created local change: {commit_data}")

        # Wait for available buffer space (e.g., storage/review limits)
        empty_slots.acquire()
        
        # Critical Section: Push to GitHub Repository
        with buffer_lock:
            repo_buffer.append(commit_data)
            print(f"[Dev A (Producer)]  ==> GIT PUSH: '{commit_data}' added to GitHub Repository.")
            print(f"                     [Repo State: {len(repo_buffer)}/{BUFFER_SIZE} commits pending]\n")

        # Signal Consumer that a new commit is ready
        full_slots.release()
        commit_id += 1

# --- Developer B: Consumer ---
def developer_b():
    while simulation_running or not is_buffer_empty():
        # Wait for commits to become available in the remote repo
        if not full_slots.acquire(timeout=2):
            # Break if simulation finished and buffer is empty
            if not simulation_running and is_buffer_empty():
                break
            continue

        # Critical Section: Pull from GitHub Repository
        with buffer_lock:
            commit_data = repo_buffer.pop(0)
            print(f"                     [Dev B (Consumer)]  <== GIT PULL: Retrieved '{commit_data}' from GitHub.")
            print(f"                     [Repo State: {len(repo_buffer)}/{BUFFER_SIZE} commits pending]\n")

        # Signal Producer that a slot in the buffer is now free
        empty_slots.release()

        # Simulate local integration and testing of the pulled changes
        time.sleep(random.uniform(0.8, 1.5))
        print(f"[Dev B (Consumer)]  Processed and integrated {commit_data} into local environment.\n")

def is_buffer_empty():
    with buffer_lock:
        return len(repo_buffer) == 0

# --- Execution Simulation ---
if __name__ == "__main__":
    print("=== Starting Git Collaborative Producer-Consumer Simulation ===\n")
    
    # Create threads
    thread_dev_a = threading.Thread(target=developer_a, name="Developer-A")
    thread_dev_b = threading.Thread(target=developer_b, name="Developer-B")

    # Start execution
    thread_dev_a.start()
    thread_dev_b.start()

    # Run the simulation for 10 seconds
    time.sleep(10)
    simulation_running = False
    print("\n--- Stopping Simulation: Waiting for remaining pulls to complete ---")

    thread_dev_a.join()
    thread_dev_b.join()
    print("=== Simulation Finished ===")