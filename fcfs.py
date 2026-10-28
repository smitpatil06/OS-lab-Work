def main():
    try:
        n = int(input("Enter number of process: "))
    except ValueError:
        print("Please enter a valid integer.")
        return

    # Initialize lists (arrays) for the variables
    at = [0] * n
    bt = [0] * n
    ct = [0] * n
    tat = [0] * n
    wt = [0] * n

    print("\nEnter at and bt:\n")

    for i in range(n):
        at[i] = int(input(f"Process {i + 1} AT: "))
        bt[i] = int(input(f"Process {i + 1} BT: "))

    current_time = 0

    # Calculate CT, TAT, and WT
    for i in range(n):
        if current_time < at[i]:
            current_time = at[i]

        ct[i] = current_time + bt[i]
        current_time = ct[i]

        tat[i] = ct[i] - at[i]
        wt[i] = tat[i] - bt[i]

    # Output formatting
    print("\nProcess | \t AT | \t BT | \t CT | \t TAT | \t WT | ")
    print("-" * 63)
    
    for i in range(n):
        # Using string formatting to match the C++ tabbed spacing
        print(f"Process{i + 1}\t|{at[i]}\t|{bt[i]}\t|{ct[i]}\t|{tat[i]}\t|{wt[i]}  |\t")

    print("-" * 62)

    # Calculate sums
    s1 = sum(tat)
    s2 = sum(wt)

    # Note: The original C++ code used integer division (int/int). 
    # Python uses float division by default with '/'. Use '//' if you strictly want integer truncation.
    a1 = s1 // n  
    a2 = s2 // n  

    print(f"Average TAT:{a1}")
    print(f"Average WT:{a2}")

if __name__ == "__main__":
    main()