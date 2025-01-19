import pandas as pd
import matplotlib.pyplot as plt

def main():
    # Read the CSV file
    df = pd.read_csv("sequential_results.csv")

    # Group data by matrix dimension
    grouped = df.groupby("n_matrix")

    # Calculate the average times for checksym and transpose operations
    mean_df = grouped[["checksym_time", "transpose_time"]].mean().reset_index()

    # Plot CheckSym Time vs. Matrix Dimension (log-log scale)
    plt.figure(figsize=(8, 6))
    plt.plot(mean_df["n_matrix"], mean_df["checksym_time"], marker='o', label="CheckSym Time")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Matrix Dimension (n)")
    plt.ylabel("Average Time (s)")
    plt.title("CheckSym Time vs. n_matrix")
    plt.grid(True, which="both", ls="--", linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Plot Transpose Time vs. Matrix Dimension (log-log scale)
    plt.figure(figsize=(8, 6))
    plt.plot(mean_df["n_matrix"], mean_df["transpose_time"], marker='o', color="red", label="Transpose Time")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Matrix Dimension")
    plt.ylabel("Average Time (s)")
    plt.title("Transpose Time vs. n_matrix")
    plt.grid(True, which="both", ls="--", linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
