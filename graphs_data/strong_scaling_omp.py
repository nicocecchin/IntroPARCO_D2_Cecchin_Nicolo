import pandas as pd
import matplotlib.pyplot as plt

def main():
    # 1) Read OMP results from the CSV file
    # Format: n_threads, n_matrix, iteration, checksym_time, transpose_time
    df = pd.read_csv("omp_results.csv")

    # 2) Group data by (n_threads, n_matrix) and calculate the mean
    grouped = df.groupby(["n_threads", "n_matrix"], as_index=False).mean()

    # 3) Get the set of matrix dimensions
    matrix_sizes = sorted(grouped["n_matrix"].unique())

    # ==================== STRONG SCALING - CHECKSYM ===================== #
    plt.figure(figsize=(8, 6))

    for n in matrix_sizes:
        sub_df = grouped[grouped["n_matrix"] == n].copy()
        sub_df.sort_values("n_threads", inplace=True)

        row_T1 = sub_df[sub_df["n_threads"] == 1]
        if len(row_T1) == 0:
            continue

        T1_checksym = row_T1["checksym_time"].values[0]

        speedups = []
        threads_list = []

        for _, row in sub_df.iterrows():
            t = row["n_threads"]
            Tp = row["checksym_time"]
            if Tp > 0:
                s = T1_checksym / Tp
            else:
                s = float("inf")
            speedups.append(s)
            threads_list.append(t)

        plt.plot(threads_list, speedups, marker='o', label=f"n={n}")

    plt.xlabel("Number of Threads (t)")
    plt.ylabel("Speedup (CheckSym)")
    plt.title("Strong Scaling - CheckSym (OpenMP)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # ==================== STRONG SCALING - TRANSPOSE ===================== #
    plt.figure(figsize=(8, 6))

    for n in matrix_sizes:
        sub_df = grouped[grouped["n_matrix"] == n].copy()
        sub_df.sort_values("n_threads", inplace=True)

        row_T1 = sub_df[sub_df["n_threads"] == 1]
        if len(row_T1) == 0:
            continue

        T1_transpose = row_T1["transpose_time"].values[0]

        speedups = []
        threads_list = []

        for _, row in sub_df.iterrows():
            t = row["n_threads"]
            Tp = row["transpose_time"]
            if Tp > 0:
                s = T1_transpose / Tp
            else:
                s = float("inf")
            speedups.append(s)
            threads_list.append(t)

        plt.plot(threads_list, speedups, marker='o', label=f"n={n}")

    plt.xlabel("Number of Threads (t)")
    plt.ylabel("Speedup (Transpose)")
    plt.title("Strong Scaling - Transpose (OpenMP)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # ==================== EFFICIENCY - CHECKSYM ===================== #
    plt.figure(figsize=(8, 6))

    for n in matrix_sizes:
        sub_df = grouped[grouped["n_matrix"] == n].copy()
        sub_df.sort_values("n_threads", inplace=True)

        row_T1 = sub_df[sub_df["n_threads"] == 1]
        if len(row_T1) == 0:
            continue

        T1_checksym = row_T1["checksym_time"].values[0]

        efficiencies = []
        threads_list = []

        for _, row in sub_df.iterrows():
            t = row["n_threads"]
            Tp = row["checksym_time"]
            if Tp > 0:
                speedup = T1_checksym / Tp
                eff = (speedup / t) * 100
            else:
                eff = float("inf")
            efficiencies.append(eff)
            threads_list.append(t)

        plt.plot(threads_list, efficiencies, marker='o', label=f"n={n}")

    plt.xlabel("Number of Threads (t)")
    plt.ylabel("Efficiency (%) - CheckSym")
    plt.title("Strong Scaling Efficiency - CheckSym (OpenMP)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # ==================== EFFICIENCY - TRANSPOSE ===================== #
    plt.figure(figsize=(8, 6))

    for n in matrix_sizes:
        sub_df = grouped[grouped["n_matrix"] == n].copy()
        sub_df.sort_values("n_threads", inplace=True)

        row_T1 = sub_df[sub_df["n_threads"] == 1]
        if len(row_T1) == 0:
            continue

        T1_transpose = row_T1["transpose_time"].values[0]

        efficiencies = []
        threads_list = []

        for _, row in sub_df.iterrows():
            t = row["n_threads"]
            Tp = row["transpose_time"]
            if Tp > 0:
                speedup = T1_transpose / Tp
                eff = (speedup / t) * 100
            else:
                eff = float("inf")
            efficiencies.append(eff)
            threads_list.append(t)

        plt.plot(threads_list, efficiencies, marker='o', label=f"n={n}")

    plt.xlabel("Number of Threads (t)")
    plt.ylabel("Efficiency (%) - Transpose")
    plt.title("Strong Scaling Efficiency - Transpose (OpenMP)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
