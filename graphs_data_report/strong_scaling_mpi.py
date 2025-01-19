import pandas as pd
import matplotlib.pyplot as plt

def main():
    # 1) Read MPI results from the CSV file
    # Format: n_processes, n_matrix, iteration, checksym_time, transpose_time
    df = pd.read_csv("mpi_results.csv")

    # 2) Group data by (n_processes, n_matrix) and calculate the mean
    grouped = df.groupby(["n_processes", "n_matrix"], as_index=False).mean()

    # 3) Get the set of unique matrix dimensions (each considered a fixed "problem")
    matrix_sizes = sorted(grouped["n_matrix"].unique())

    # Prepare plots: Four separate ones will be created
    #  A) Speedup CheckSym
    #  B) Speedup Transpose
    #  C) Efficiency CheckSym
    #  D) Efficiency Transpose

    # =========== A) STRONG SCALING - SPEEDUP CHECKSYM =========== #
    plt.figure(figsize=(8, 6))

    for n in matrix_sizes:
        sub_df = grouped[grouped["n_matrix"] == n].copy()
        sub_df.sort_values("n_processes", inplace=True)

        row_T1 = sub_df[sub_df["n_processes"] == 1]
        if len(row_T1) == 0:
            continue

        T1_checksym = row_T1["checksym_time"].values[0]

        speedups = []
        procs = []
        for _, row in sub_df.iterrows():
            p = row["n_processes"]
            Tp_checksym = row["checksym_time"]
            if Tp_checksym > 0:
                s = T1_checksym / Tp_checksym
            else:
                s = float("inf")
            speedups.append(s)
            procs.append(p)

        plt.plot(procs, speedups, marker='o', label=f"n={n}")

    plt.xlabel("Number of Processes (p)")
    plt.ylabel("Speedup (CheckSym)")
    plt.title("Strong Scaling - CheckSym")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # =========== B) STRONG SCALING - SPEEDUP TRANSPOSE =========== #
    plt.figure(figsize=(8, 6))

    for n in matrix_sizes:
        sub_df = grouped[grouped["n_matrix"] == n].copy()
        sub_df.sort_values("n_processes", inplace=True)

        row_T1 = sub_df[sub_df["n_processes"] == 1]
        if len(row_T1) == 0:
            continue

        T1_transpose = row_T1["transpose_time"].values[0]

        speedups = []
        procs = []
        for _, row in sub_df.iterrows():
            p = row["n_processes"]
            Tp_transpose = row["transpose_time"]
            if Tp_transpose > 0:
                s = T1_transpose / Tp_transpose
            else:
                s = float("inf")
            speedups.append(s)
            procs.append(p)

        plt.plot(procs, speedups, marker='o', label=f"n={n}")

    plt.xlabel("Number of Processes (p)")
    plt.ylabel("Speedup (Transpose)")
    plt.title("Strong Scaling - Transpose")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # =========== C) EFFICIENCY CHECKSYM =========== #
    plt.figure(figsize=(8, 6))

    for n in matrix_sizes:
        sub_df = grouped[grouped["n_matrix"] == n].copy()
        sub_df.sort_values("n_processes", inplace=True)

        row_T1 = sub_df[sub_df["n_processes"] == 1]
        if len(row_T1) == 0:
            continue

        T1_checksym = row_T1["checksym_time"].values[0]

        efficiencies = []
        procs = []
        for _, row in sub_df.iterrows():
            p = row["n_processes"]
            Tp_checksym = row["checksym_time"]
            if Tp_checksym > 0:
                speedup = T1_checksym / Tp_checksym
                eff = (speedup / p) * 100
            else:
                eff = float("inf")
            efficiencies.append(eff)
            procs.append(p)

        plt.plot(procs, efficiencies, marker='o', label=f"n={n}")

    plt.xlabel("Number of Processes (p)")
    plt.ylabel("Efficiency (%) - CheckSym")
    plt.title("Strong Scaling Efficiency - CheckSym")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # =========== D) EFFICIENCY TRANSPOSE =========== #
    plt.figure(figsize=(8, 6))

    for n in matrix_sizes:
        sub_df = grouped[grouped["n_matrix"] == n].copy()
        sub_df.sort_values("n_processes", inplace=True)

        row_T1 = sub_df[sub_df["n_processes"] == 1]
        if len(row_T1) == 0:
            continue

        T1_transpose = row_T1["transpose_time"].values[0]

        efficiencies = []
        procs = []
        for _, row in sub_df.iterrows():
            p = row["n_processes"]
            Tp_transpose = row["transpose_time"]
            if Tp_transpose > 0:
                speedup = T1_transpose / Tp_transpose
                eff = (speedup / p) * 100
            else:
                eff = float("inf")
            efficiencies.append(eff)
            procs.append(p)

        plt.plot(procs, efficiencies, marker='o', label=f"n={n}")

    plt.xlabel("Number of Processes (p)")
    plt.ylabel("Efficiency (%) - Transpose")
    plt.title("Strong Scaling Efficiency - Transpose")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
