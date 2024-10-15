#include <stdio.h>

int main() {
    int n, i;
    int largest, smallest;

    // Input the number of elements in the array
    printf("Enter the number of elements in the array: ");
    scanf("%d", &n);

    // Declare the array
    int arr[n];

    // Input the elements of the array
    printf("Enter %d integers:\n", n);
    for (i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }

    // Initialize largest and smallest with the first element
    largest = smallest = arr[0];

    // Traverse the array to find the largest and smallest numbers
    for (i = 1; i < n; i++) {
        if (arr[i] > largest) {
            largest = arr[i];
        }
        if (arr[i] < smallest) {
            smallest = arr[i];
        }
    }

    // Output the results
    printf("Largest Number: %d\n", largest);
    printf("Smallest Number: %d\n", smallest);

    return 0;
}