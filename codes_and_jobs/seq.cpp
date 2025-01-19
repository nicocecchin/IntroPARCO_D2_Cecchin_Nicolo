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

// Function to check if the matrix is symmetric
bool checkSym(const std::vector<std::vector<float>> &matrix) {
    int n = matrix.size();
    bool isSymmetric = true;
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            if (matrix[i][j] != matrix[j][i]) {
                isSymmetric = false; 
            }
        }
    }
    return isSymmetric;
}

// Function to transpose a matrix
std::vector<std::vector<float>> matTranspose(const std::vector<std::vector<float>> &matrix) {
    int n = matrix.size();
    std::vector<std::vector<float>> transpose(n, std::vector<float>(n));

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            transpose[j][i] = matrix[i][j];
        }
    }
    return transpose;
}

int main(int argc, char *argv[]){
    
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <matrix_size>" << std::endl;
        return 1;
    }

    int n = std::stoi(argv[1]);

    // Initialize the matrix
    auto matrix = initializeMatrix(n);

    // Measure symmetry check time
    auto start = std::chrono::high_resolution_clock::now();
    bool isSymmetric = checkSym(matrix);
    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double> checkSymDur = end - start; 
    std::cout << checkSymDur.count() << ",";

    // Measure transpose time
    start = std::chrono::high_resolution_clock::now();
    auto transpose = matTranspose(matrix);
    end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double> matTransposeDur = end - start; 
    std::cout << matTransposeDur.count();

    return 0;
}