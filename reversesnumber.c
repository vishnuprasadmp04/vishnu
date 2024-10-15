#include <stdio.h>

int main() {
    int num, reversed = 0, remainder;

    // Input a number from the user
    printf("Enter an integer: ");
    scanf("%d", &num);

    // Reverse the number
    while (num != 0) {
        remainder = num % 10;         // Get the last digit
        reversed = reversed * 10 + remainder; // Build the reversed number
        num /= 10;                    // Remove the last digit
    }

    // Output the reversed number
    printf("Reversed Number: %d\n", reversed);

    return 0;
}