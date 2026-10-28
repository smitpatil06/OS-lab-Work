def main():
    try:
        n = int(input("Enter number of processes: "))
        tq = int(input("Enter Tq (Time Quantum): "))
    except ValueError:
        print("Please enter a valid integer.")
        return

    # Initialize lists
    at = [0] * n
    bt = [0] * n
    ct = [0] * n
    tat = [0] * n
    wt = [0] * n

    print("\nEnter AT and BT:\n")

    for i in range(n):
        at[i] = int(input(f"Process {i + 1} AT: "))
        bt[i] = int(input(f"Process {i + 1} BT: "))

    # rem_bt tracks the remaining burst time for each process
    rem_bt = bt.copy() 
    
    current_time = 0
    completed = 0
    queue = []
    in_queue = [False] * n
    
    # Track Gantt chart as a list of tuples: (Process_Name, Start_Time, End_Time)
    gantt_chart = []

    print("\n--- Execution Trace (Ready Queue) ---")

    # Main Round Robin Logic
    while completed < n:
        # 1. Add any newly arrived processes to the queue
        for i in range(n):
            if at[i] <= current_time and not in_queue[i] and rem_bt[i] > 0:
                queue.append(i)
                in_queue[i] = True
        
        # 2. If the queue is empty, the CPU is idle. Jump time forward to the next arrival.
        if not queue:
            next_arrivals = [at[i] for i in range(n) if rem_bt[i] > 0]
            if next_arrivals:
                next_time = min(next_arrivals)
                gantt_chart.append(("Idle", current_time, next_time))
                print(f"Time {current_time} to {next_time} | CPU is Idle | Ready Queue: []")
                current_time = next_time
            continue
        
        # Display the Ready Queue before popping the next process
        q_display = [f"P{q + 1}" for q in queue]
        print(f"Time {current_time} | Ready Queue: {q_display}")

        # 3. Pop the first process in the queue to execute
        idx = queue.pop(0)
        start_time = current_time

        # 4. Execute the process
        if rem_bt[idx] > tq:
            # Process executes for the full time quantum but isn't finished
            current_time += tq
            rem_bt[idx] -= tq
            
            # Record execution in Gantt Chart
            gantt_chart.append((f"P{idx + 1}", start_time, current_time))
            
            # Check for NEW arrivals while this process was executing before re-queuing
            for i in range(n):
                if at[i] <= current_time and not in_queue[i] and rem_bt[i] > 0:
                    queue.append(i)
                    in_queue[i] = True
            
            # Push the current, unfinished process to the back of the queue
            queue.append(idx)
        else:
            # Process finishes executing
            current_time += rem_bt[idx]
            
            # Record execution in Gantt Chart
            gantt_chart.append((f"P{idx + 1}", start_time, current_time))
            
            rem_bt[idx] = 0
            completed += 1
            
            # Calculate final metrics for the completed process
            ct[idx] = current_time
            tat[idx] = ct[idx] - at[idx]
            wt[idx] = tat[idx] - bt[idx]
            
            # Check for any new arrivals at this exact completion time
            for i in range(n):
                if at[i] <= current_time and not in_queue[i] and rem_bt[i] > 0:
                    queue.append(i)
                    in_queue[i] = True

    # Output Gantt Chart
    print("\n--- Gantt Chart ---")
    gantt_processes = []
    gantt_times = [str(gantt_chart[0][1])]
    
    for item in gantt_chart:
        gantt_processes.append(item[0])
        gantt_times.append(str(item[2]))
        
    print("| " + " | ".join(gantt_processes) + " |")
    print("   ".join(gantt_times))

    # Output formatting
    print("\nProcess | \t AT | \t BT | \t CT | \t TAT | \t WT | ")
    print("-" * 63)
    
    for i in range(n):
        print(f"Process{i + 1}\t|{at[i]}\t|{bt[i]}\t|{ct[i]}\t|{tat[i]}\t|{wt[i]}  |\t")

    print("-" * 62)

    # Calculate sums
    s1 = sum(tat)
    s2 = sum(wt)

    # Calculate averages (float division is standard, change to '//' for truncation if needed)
    a1 = s1 / n  
    a2 = s2 / n  

    # Formatting to 2 decimal places for cleaner output
    print(f"Average TAT: {a1:.2f}")
    print(f"Average WT: {a2:.2f}")

if __name__ == "__main__":
    main()
