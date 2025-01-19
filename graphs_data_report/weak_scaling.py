import pandas as pd
import matplotlib.pyplot as plt

def main():
    # ===================== READ CSV FILES =====================
    # 1) OpenMP
    omp_df = pd.read_csv("omp_results.csv")
    # Group and calculate mean by (n_threads, n_matrix)
    omp_grouped = omp_df.groupby(["n_threads", "n_matrix"], as_index=False).mean()

    # 2) MPI
    mpi_df = pd.read_csv("mpi_results.csv")
    # Group and calculate mean by (n_processes, n_matrix)
    mpi_grouped = mpi_df.groupby(["n_processes", "n_matrix"], as_index=False).mean()

    # ===================== DEFINE WEAK SCALING POINTS =====================
    # Using p and n as specified:
    #   p=1 -> n=1024
    #   p=4 -> n=2048
    #   p=16 -> n=4096
    # For OMP, p corresponds to n_threads; for MPI, p corresponds to n_processes.
    weak_points = [(1, 1024), (4, 2048), (16, 4096)]

    # ===================== HELPER FUNCTIONS =====================
    def get_time_omp(p, n, which_time="checksym_time"):
        """
        Returns the (already averaged) time from omp_grouped for n_threads=p and n_matrix=n
        in the column 'which_time' (checksym_time or transpose_time).
        If not found, returns None.
        """
        row = omp_grouped[(omp_grouped["n_threads"] == p) & (omp_grouped["n_matrix"] == n)]
        if len(row) == 0:
            return None
        return row[which_time].values[0]

    def get_time_mpi(p, n, which_time="checksym_time"):
        """
        Returns the (already averaged) time from mpi_grouped for n_processes=p and n_matrix=n
        in the column 'which_time'. If not found, returns None.
        """
        row = mpi_grouped[(mpi_grouped["n_processes"] == p) & (mpi_grouped["n_matrix"] == n)]
        if len(row) == 0:
            return None
        return row[which_time].values[0]

    # ===================== WEAK SCALING FOR CHECKSYM =====================
    p_list = [p for (p, _) in weak_points]  # [1, 4, 16]

    # Get T1(N) = time with p=1 and n=1024, separately for OMP and MPI
    T1_checksym_omp = get_time_omp(1, 1024, "checksym_time")
    T1_checksym_mpi = get_time_mpi(1, 1024, "checksym_time")

    Sw_omp_checksym = []
    Sw_mpi_checksym = []

    for (p, n) in weak_points:
        # OMP
        T_p_omp = get_time_omp(p, n, "checksym_time")
        if T1_checksym_omp is not None and T_p_omp is not None and T_p_omp > 0:
            Sw = T1_checksym_omp / T_p_omp
        else:
            Sw = float("nan")
        Sw_omp_checksym.append(Sw)

        # MPI
        T_p_mpi = get_time_mpi(p, n, "checksym_time")
        if T1_checksym_mpi is not None and T_p_mpi is not None and T_p_mpi > 0:
            Sw = T1_checksym_mpi / T_p_mpi
        else:
            Sw = float("nan")
        Sw_mpi_checksym.append(Sw)

    # ===================== WEAK SCALING FOR TRANSPOSE =====================
    T1_transpose_omp = get_time_omp(1, 1024, "transpose_time")
    T1_transpose_mpi = get_time_mpi(1, 1024, "transpose_time")

    Sw_omp_transpose = []
    Sw_mpi_transpose = []

    for (p, n) in weak_points:
        # OMP
        T_p_omp = get_time_omp(p, n, "transpose_time")
        if T1_transpose_omp is not None and T_p_omp is not None and T_p_omp > 0:
            Sw = T1_transpose_omp / T_p_omp
        else:
            Sw = float("nan")
        Sw_omp_transpose.append(Sw)

        # MPI
        T_p_mpi = get_time_mpi(p, n, "transpose_time")
        if T1_transpose_mpi is not None and T_p_mpi is not None and T_p_mpi > 0:
            Sw = T1_transpose_mpi / T_p_mpi
        else:
            Sw = float("nan")
        Sw_mpi_transpose.append(Sw)

    # ===================== PLOT 1: CHECKSYM (WEAK SCALING) =====================
    plt.figure(figsize=(8, 6))
    plt.plot(p_list, Sw_omp_checksym, marker='o', label="OMP")
    plt.plot(p_list, Sw_mpi_checksym, marker='o', label="MPI")
    plt.title("Weak Scaling - CheckSym")
    plt.xlabel("Number of Threads/Processes (p)")
    plt.ylabel("S_w(p) = T1(N) / T_p(p*N)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # ===================== PLOT 2: TRANSPOSE (WEAK SCALING) =====================
    plt.figure(figsize=(8, 6))
    plt.plot(p_list, Sw_omp_transpose, marker='o', label="OMP")
    plt.plot(p_list, Sw_mpi_transpose, marker='o', label="MPI")
    plt.title("Weak Scaling - Transpose")
    plt.xlabel("Number of Threads/Processes (p)")
    plt.ylabel("S_w(p) = T1(N) / T_p(p*N)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
