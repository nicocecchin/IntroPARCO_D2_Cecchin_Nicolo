import pandas as pd
import matplotlib.pyplot as plt

def main():
    # ====================== DATA READING AND FILTERING ====================== #
    # 1) Read OMP results
    omp_df = pd.read_csv("omp_results.csv")
    # Filter for n_matrix == 4096
    omp_df_4096 = omp_df[omp_df["n_matrix"] == 4096].copy()
    # Group by n_threads and calculate the mean
    omp_grouped = omp_df_4096.groupby("n_threads", as_index=False).mean()
    # Sort by number of threads
    omp_grouped.sort_values("n_threads", inplace=True)

    # 2) Read MPI results
    mpi_df = pd.read_csv("mpi_results.csv")
    # Filter for n_matrix == 4096
    mpi_df_4096 = mpi_df[mpi_df["n_matrix"] == 4096].copy()
    # Group by n_processes and calculate the mean
    mpi_grouped = mpi_df_4096.groupby("n_processes", as_index=False).mean()
    # Sort by number of processes
    mpi_grouped.sort_values("n_processes", inplace=True)

    # ====================== OMP CALCULATIONS ====================== #
    omp_1 = omp_grouped[omp_grouped["n_threads"] == 1]
    T1_checksym_omp = omp_1["checksym_time"].values[0] if not omp_1.empty else None
    T1_transpose_omp = omp_1["transpose_time"].values[0] if not omp_1.empty else None

    x_omp = []
    speedup_omp_checksym = []
    efficiency_omp_checksym = []
    speedup_omp_transpose = []
    efficiency_omp_transpose = []

    for _, row in omp_grouped.iterrows():
        t = row["n_threads"]
        if T1_checksym_omp and row["checksym_time"] > 0:
            s = T1_checksym_omp / row["checksym_time"]
            e = (s / t) * 100
        else:
            s = float("nan")
            e = float("nan")
        speedup_omp_checksym.append(s)
        efficiency_omp_checksym.append(e)

        if T1_transpose_omp and row["transpose_time"] > 0:
            s_t = T1_transpose_omp / row["transpose_time"]
            e_t = (s_t / t) * 100
        else:
            s_t = float("nan")
            e_t = float("nan")
        speedup_omp_transpose.append(s_t)
        efficiency_omp_transpose.append(e_t)

        x_omp.append(t)

    # ====================== MPI CALCULATIONS ====================== #
    mpi_1 = mpi_grouped[mpi_grouped["n_processes"] == 1]
    T1_checksym_mpi = mpi_1["checksym_time"].values[0] if not mpi_1.empty else None
    T1_transpose_mpi = mpi_1["transpose_time"].values[0] if not mpi_1.empty else None

    x_mpi = []
    speedup_mpi_checksym = []
    efficiency_mpi_checksym = []
    speedup_mpi_transpose = []
    efficiency_mpi_transpose = []

    for _, row in mpi_grouped.iterrows():
        p = row["n_processes"]
        if T1_checksym_mpi and row["checksym_time"] > 0:
            s = T1_checksym_mpi / row["checksym_time"]
            e = (s / p) * 100
        else:
            s = float("nan")
            e = float("nan")
        speedup_mpi_checksym.append(s)
        efficiency_mpi_checksym.append(e)

        if T1_transpose_mpi and row["transpose_time"] > 0:
            s_t = T1_transpose_mpi / row["transpose_time"]
            e_t = (s_t / p) * 100
        else:
            s_t = float("nan")
            e_t = float("nan")
        speedup_mpi_transpose.append(s_t)
        efficiency_mpi_transpose.append(e_t)

        x_mpi.append(p)

    # ====================== PLOT 1: CHECKSYM SPEEDUP (OMP vs MPI) ====================== #
    plt.figure(figsize=(8,6))
    plt.plot(x_omp, speedup_omp_checksym, marker='o', label="OMP CheckSym Speedup")
    plt.plot(x_mpi, speedup_mpi_checksym, marker='o', label="MPI CheckSym Speedup")
    plt.title("Strong Scaling (CheckSym) - n=4096")
    plt.xlabel("Number of Threads / Processes")
    plt.ylabel("Speedup")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # ====================== PLOT 2: CHECKSYM EFFICIENCY (OMP vs MPI) ====================== #
    plt.figure(figsize=(8,6))
    plt.plot(x_omp, efficiency_omp_checksym, marker='o', label="OMP CheckSym Efficiency")
    plt.plot(x_mpi, efficiency_mpi_checksym, marker='o', label="MPI CheckSym Efficiency")
    plt.title("Strong Scaling Efficiency (CheckSym) - n=4096")
    plt.xlabel("Number of Threads / Processes")
    plt.ylabel("Efficiency (%)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # ====================== PLOT 3: TRANSPOSE SPEEDUP (OMP vs MPI) ====================== #
    plt.figure(figsize=(8,6))
    plt.plot(x_omp, speedup_omp_transpose, marker='o', label="OMP Transpose Speedup")
    plt.plot(x_mpi, speedup_mpi_transpose, marker='o', label="MPI Transpose Speedup")
    plt.title("Strong Scaling (Transpose) - n=4096")
    plt.xlabel("Number of Threads / Processes")
    plt.ylabel("Speedup")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # ====================== PLOT 4: TRANSPOSE EFFICIENCY (OMP vs MPI) ====================== #
    plt.figure(figsize=(8,6))
    plt.plot(x_omp, efficiency_omp_transpose, marker='o', label="OMP Transpose Efficiency")
    plt.plot(x_mpi, efficiency_mpi_transpose, marker='o', label="MPI Transpose Efficiency")
    plt.title("Strong Scaling Efficiency (Transpose) - n=4096")
    plt.xlabel("Number of Threads / Processes")
    plt.ylabel("Efficiency (%)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
