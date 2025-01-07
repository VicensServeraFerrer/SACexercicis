#include <tbb/tbb.h>
#include <vector>
#include <iostream>
#include <algorithm>
#include <atomic>
#include <chrono>

// Seqüencial
std::vector<int> sequential_histogram(const std::vector<double>& data, int num_bins) {
    double min_val = *std::min_element(data.begin(), data.end());
    double max_val = *std::max_element(data.begin(), data.end());
    double bin_width = (max_val - min_val) / num_bins;

    // Comptar frequencies
    std::vector<int> histogram(num_bins, 0);
    for (double value : data) {
        int bin = std::min(static_cast<int>((value - min_val) / bin_width), num_bins - 1);
        histogram[bin]++;
    }

    // Calcular acumulació
    for (int i = 1; i < num_bins; ++i) {
        histogram[i] += histogram[i - 1];
    }
    return histogram;
}

// Parallel Histogram Implementation
std::vector<int> parallel_histogram(const std::vector<double>& data, int num_bins) {
    double min_val = *std::min_element(data.begin(), data.end());
    double max_val = *std::max_element(data.begin(), data.end());
    double bin_width = (max_val - min_val) / num_bins;

    std::vector<std::atomic<int>> global_histogram(num_bins);
    for (int i = 0; i < num_bins; ++i) {
        global_histogram[i] = 0;
    }

    // Calcular frequencies amb parallel for
    tbb::parallel_for(tbb::blocked_range<size_t>(0, data.size()), [&](const tbb::blocked_range<size_t>& range) {
        std::vector<int> local_histogram(num_bins, 0);
        for (size_t i = range.begin(); i < range.end(); ++i) {
            int bin = std::min(static_cast<int>((data[i] - min_val) / bin_width), num_bins - 1);
            local_histogram[bin]++;
        }

        for (int i = 0; i < num_bins; ++i) {
            global_histogram[i].fetch_add(local_histogram[i], std::memory_order_relaxed);
        }
    });

    // Canviar de vector atòmic a vector normal
    std::vector<int> result_histogram(num_bins);
    for (int i = 0; i < num_bins; ++i) {
        result_histogram[i] = global_histogram[i].load(std::memory_order_relaxed);
    }

    // Calcular acumulació de valors
    tbb::parallel_scan(tbb::blocked_range<int>(0, num_bins), 0, 
        [&](const tbb::blocked_range<int>& range, int sum, bool is_final) {
            for (int i = range.begin(); i < range.end(); ++i) {
                sum += result_histogram[i];
                if (is_final) result_histogram[i] = sum;
            }
            return sum;
        }, std::plus<int>());

    return result_histogram;
}

int main() {
    size_t data_size = 200000;
    int num_bins = 100;
    std::vector<double> data(data_size);
    std::generate(data.begin(), data.end(), []() { return static_cast<double>(rand()) / RAND_MAX * 100.0; });

    auto start = std::chrono::high_resolution_clock::now();
    std::vector<int> sequential_result = sequential_histogram(data, num_bins);
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> sequential_time = end - start;

    std::cout << "Sequential execution time: " << sequential_time.count() << " seconds\n";
    std::cout << "Sequential result: ";
    for (int value : sequential_result) {
        std::cout << value << " ";
    }
    std::cout << "\n";

    start = std::chrono::high_resolution_clock::now();
    std::vector<int> parallel_result = parallel_histogram(data, num_bins);
    end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> parallel_time = end - start;

    std::cout << "Parallel execution time: " << parallel_time.count() << " seconds\n";
    std::cout << "Parallel result: ";
    for (int value : parallel_result) {
        std::cout << value << " ";
    }
    std::cout << "\n";

    return 0;
}
