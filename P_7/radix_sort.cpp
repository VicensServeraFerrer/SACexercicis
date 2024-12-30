#include <vector>
#include <iostream>
#include <algorithm>
#include <cmath>

#include <tbb/tbb.h>
#include "oneapi/tbb/blocked_range.h"
#include "oneapi/tbb/parallel_for.h"

using namespace tbb;
using namespace std;

int getDigit(int number, int digitPosition, int base) {
    return (number / static_cast<int>(pow(base, digitPosition))) % base;
}

#include <vector>
#include <tbb/parallel_for.h>
#include <tbb/blocked_range.h>

using namespace std;
using namespace tbb;

void sortByDigit(vector<int>& arr, int digitPosition, int base) {
    size_t size = arr.size();
    vector<int> output(size);
    vector<int> count(base, 0);

    tbb::parallel_for(size_t(0), size, [&](size_t i) {
        int digit = getDigit(arr[i], digitPosition, base);
        count[digit]++;
    });

    // Paso 2: Calcular las posiciones iniciales ajustadas usando parallel_scan
    vector<int> positions(base, 0);
    tbb::parallel_scan(
        blocked_range<int>(0, base),
        0,
        [&](const blocked_range<int>& range, int running_total, auto is_final_scan) -> int {
            for (int i = range.begin(); i < range.end(); ++i) {
                int current_count = count[i];
                if (is_final_scan) {
                    positions[i] = running_total;
                }
                running_total += current_count;
            }
            return running_total;
        },
        [](int x, int y) { return x + y; }
    );

    // Paso 3: Construir el array ordenado y copiar los datos de vuelta al arreglo original
    tbb::parallel_for(size_t(0), size, [&](size_t i) {
        int digit = getDigit(arr[i], digitPosition, base);
        output[positions[digit]++] = arr[i];
    });

    tbb::parallel_for(size_t(0), size, [&](size_t i) {
        arr[i] = output[i];
    });
}

void radixSort(vector<int>& arr) {
    if (arr.empty()) return;

    int maxElement = *max_element(arr.begin(), arr.end());
    int base = 10;
    int numDigits = static_cast<int>(log10(maxElement) + 1);

    for (int digitPosition = 0; digitPosition < numDigits; ++digitPosition) {
        sortByDigit(arr, digitPosition, base);
    }
}

int main() {
    vector<int> arr = {170, 50, 45, 75, 90, 802, 24, 2, 66, 0, 1, 171};

    cout << "Original array:" << endl;
    for (int num : arr) {
        cout << num << " ";
    }
    cout << endl;

    radixSort(arr);

    cout << "Sorted array:" << endl;
    for (int num : arr) {
        cout << num << " ";
    }
    cout << endl;

    return 0;
}
