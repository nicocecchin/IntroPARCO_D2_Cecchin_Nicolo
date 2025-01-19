import pandas as pd
import matplotlib.pyplot as plt

def main():
    # ======== 1) Reading the Sequential CSV ======== #
    seq_df = pd.read_csv("sequential_results.csv")
    # Group by n_matrix and calculate the mean
    seq_grouped = seq_df.groupby("n_matrix", as_index=False).mean()
    seq_grouped.sort_values("n_matrix", inplace=True)

    # ======== 2) Reading the OMP CSV ======== #
    omp_df = pd.read_csv("omp_results.csv")
    # Group by (n_threads, n_matrix) and calculate the mean
    omp_grouped = omp_df.groupby(["n_threads", "n_matrix"], as_index=False).mean()
    # Filter for n_threads == 32
    omp_32 = omp_grouped[omp_grouped["n_threads"] == 32].copy()
    omp_32.sort_values("n_matrix", inplace=True)

    # ======== 3) Reading the MPI CSV ======== #
    mpi_df = pd.read_csv("mpi_results.csv")
    # Group by (n_processes, n_matrix) and calculate the mean
    mpi_grouped = mpi_df.groupby(["n_processes", "n_matrix"], as_index=False).mean()
    # Filter for n_processes == 32
    mpi_32 = mpi_grouped[mpi_grouped["n_processes"] == 32].copy()
    mpi_32.sort_values("n_matrix", inplace=True)

    # ======== PLOT 1: CheckSym Time ======== #
    plt.figure(figsize=(8, 6))

    # Sequential
    plt.plot(seq_grouped["n_matrix"], seq_grouped["checksym_time"], 
             marker='o', label="Sequential")

    # OMP 32 threads
    plt.plot(omp_32["n_matrix"], omp_32["checksym_time"], 
             marker='o', label="OMP - 32 threads")

    # MPI 32 processes
    plt.plot(mpi_32["n_matrix"], mpi_32["checksym_time"], 
             marker='o', label="MPI - 32 processes")

    plt.xscale("log")  
    plt.yscale("log")
    plt.xlabel("Matrix Dimension (n)")
    plt.ylabel("Average CheckSym Time (s)")
    plt.title("CheckSym Comparison: Sequential vs OMP(32) vs MPI(32)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # ======== PLOT 2: Transpose Time ======== #
    plt.figure(figsize=(8, 6))

    # Sequential
    plt.plot(seq_grouped["n_matrix"], seq_grouped["transpose_time"], 
             marker='o', label="Sequential")

    # OMP 32 threads
    plt.plot(omp_32["n_matrix"], omp_32["transpose_time"], 
             marker='o', label="OMP - 32 threads")

    # MPI 32 processes
    plt.plot(mpi_32["n_matrix"], mpi_32["transpose_time"], 
             marker='o', label="MPI - 32 processes")

    plt.xscale("log")  
    plt.yscale("log")  

    plt.xlabel("Matrix Dimension (n)")
    plt.ylabel("Average Transpose Time (s)")
    plt.title("Transpose Comparison: Sequential vs OMP(32) vs MPI(32)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
