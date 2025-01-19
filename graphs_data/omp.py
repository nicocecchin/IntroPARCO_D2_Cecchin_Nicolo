import pandas as pd
import matplotlib.pyplot as plt

def main():
    # Read the CSV file
    df = pd.read_csv("omp_results.csv")

    # Group by (n_threads, n_matrix) and calculate the mean of the values
    grouped_df = df.groupby(["n_threads", "n_matrix"], as_index=False).mean()

    # Extract the list of unique threads and sort the table by n_matrix
    unique_procs = sorted(grouped_df["n_threads"].unique())

    # ========== PLOT 1: checksym_time ========== #
    plt.figure(figsize=(8, 6))

    for p in unique_procs:
        # Filter data for the specific number of threads p
        sub_df = grouped_df[grouped_df["n_threads"] == p]
        sub_df = sub_df.sort_values("n_matrix")

        # Plot the line for these data points
        plt.plot(
            sub_df["n_matrix"], 
            sub_df["checksym_time"], 
            marker='o', 
            label=f"{p} threads"
        )

    # Set logarithmic scale for x and y axes
    plt.xscale("log")
    plt.yscale("log")

    plt.xlabel("Matrix Dimension (n)")
    plt.ylabel("Average Time (s)")
    plt.title("CheckSym Time vs. n_matrix for every number of threads")
    plt.grid(True, which="both", ls="--", linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # ========== PLOT 2: transpose_time ========== #
    plt.figure(figsize=(8, 6))

    for p in unique_procs:
        sub_df = grouped_df[grouped_df["n_threads"] == p]
        sub_df = sub_df.sort_values("n_matrix")

        plt.plot(
            sub_df["n_matrix"], 
            sub_df["transpose_time"], 
            marker='o', 
            label=f"{p} threads"
        )

    plt.xscale("log")
    plt.yscale("log")

    plt.xlabel("Matrix Dimension (n)")
    plt.ylabel("Average Time (s)")
    plt.title("Transpose Time vs. n_matrix for every number of threads")
    plt.grid(True, which="both", ls="--", linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
