#include <mpi.h>
#include <iostream>
#include <vector>
#include <random>
#include <chrono>

// Function to initialize a random n x n matrix
std::vector<std::vector<float>> initializeMatrix(int n) {
    std::vector<std::vector<float>> matrix(n, std::vector<float>(n));
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<float> dist(0.0, 100.0);

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            matrix[i][j] = dist(gen);
        }
    }
    return matrix;
}

// Function to flatten a 2D matrix into a 1D vector
std::vector<float> flattenMatrix(const std::vector<std::vector<float>> &matrix) {
    int n = matrix.size();
    std::vector<float> flatMatrix(n * n);
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            flatMatrix[i * n + j] = matrix[i][j];
        }
    }
    return flatMatrix;
}

// Function to reconstruct a 2D matrix from a 1D vector
std::vector<std::vector<float>> reconstructMatrix(const std::vector<float> &flatMatrix, int n) {
    std::vector<std::vector<float>> matrix(n, std::vector<float>(n));
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            matrix[i][j] = flatMatrix[i * n + j];
        }
    }
    return matrix;
}

void printMatrix(const std::vector<std::vector<float>> &matrix, const std::string &label) {
    std::cout << label << ":\n";
    for (const auto &row : matrix) {
        for (const auto &value : row) {
            std::cout << value << " ";
        }
        std::cout << "\n";
    }
    std::cout << "\n";
}

// Function to check if the matrix is symmetric
bool checkSymMPI(const std::vector<std::vector<float>> &matrix, int rank, int size) {
    int n = matrix.size();
    bool localSymmetric = true;
    
    // Each process gets a range of rows to check
    int rowsPerProcess = n / size;
    int startRow = rank * rowsPerProcess;
    int endRow  = (rank == size - 1) ? n : startRow + rowsPerProcess;

    for (int i = startRow; i < endRow; ++i) {
        for (int j = i + 1; j < n; ++j) {
            if (matrix[i][j] != matrix[j][i]) {
                localSymmetric = false;
            }
        }
    }

    // Combine results from all processes
    int localSym = localSymmetric ? 1 : 0;
    int globalSym;
    MPI_Allreduce(&localSym, &globalSym, 1, MPI_INT, MPI_LAND, MPI_COMM_WORLD);

    return globalSym == 1;
}

std::vector<std::vector<float>> matTransposeMPI(const std::vector<std::vector<float>> &local_matrix, int n, int rank, int size) {
    int rows_per_process = n / size;
    std::vector<std::vector<float>> local_transposed_chunk(rows_per_process, std::vector<float>(n));
    std::vector<std::vector<float>> transpose(n, std::vector<float>(n));

    // transpose a chunk for every process 
    for (int i = 0; i<rows_per_process; i++){
        for (int j = 0; j<n; j++){
            local_transposed_chunk[i][j] = local_matrix[j][i+(rank*rows_per_process)];
        }
    }

    // flatten the chunk
    std::vector<float> local_flat_chunk(rows_per_process * n);
    for (int i = 0; i < rows_per_process; ++i) {
        for (int j = 0; j < n; ++j) {
            local_flat_chunk[i * rows_per_process + j] = local_transposed_chunk[i][j];
        }
    }

    // the process with rank 0 gathers all the transposed chunks
    std::vector<float> flat_transpose(n * n);
    MPI_Gather(local_flat_chunk.data(), rows_per_process*n, MPI_FLOAT, flat_transpose.data(), rows_per_process*n, MPI_FLOAT, 0, MPI_COMM_WORLD);
    
    // retransform the flat matrix into the 2d matrix
    if (rank == 0) {
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                transpose[i][j] = flat_transpose[i * n + j];
            }
        }
    }

    return transpose;
}

int main(int argc, char *argv[]) {
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (argc != 2) {
        if (rank == 0) {
            std::cerr << "Usage: " << argv[0] << " <matrix_size>\n";
        }
        MPI_Finalize();
        return 1;
    }

    int n = std::stoi(argv[1]);
    if (n % size != 0) {
        if (rank == 0) {
            std::cerr << "Matrix size must be divisible by the number of processes.\n";
        }
        MPI_Finalize();
        return 1;
    }

    std::vector<std::vector<float>> local_matrix;
    std::vector<float> flatMatrix;

    if (rank == 0) {
        // Initialize the matrix in rank 0
        local_matrix = initializeMatrix(n);
        flatMatrix = flattenMatrix(local_matrix);
        // std::cout << std::endl;
        // printMatrix(local_matrix, "Original Matrix");

    } else {
        flatMatrix.resize(n * n);
    }

    // Broadcast the flattened matrix to all processes
    MPI_Bcast(flatMatrix.data(), n * n, MPI_FLOAT, 0, MPI_COMM_WORLD);

    // Reconstruct the matrix from the received vector
    local_matrix = reconstructMatrix(flatMatrix, n);

    // Measure symmetry check time
    auto start = MPI_Wtime();
    bool isSymmetric = checkSymMPI(local_matrix, rank, size);
    auto end = MPI_Wtime();

    if (rank == 0) {
        std::cout << (end - start) << ",";
    }

    // Measure transpose time
    start = MPI_Wtime();
    auto transposed_matrix = matTransposeMPI(local_matrix, n, rank, size);
    end = MPI_Wtime();

    if (rank == 0) {
        std::cout << (end - start);
        // std::cout << std::endl;
        // printMatrix(transposed_matrix, "Transposed Matrix");

    }

    MPI_Finalize();
    return 0;
}
