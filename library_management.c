#include <stdio.h>
#include <string.h>

#define MAX_BOOKS 100
#define MAX_TITLE 100
#define MAX_AUTHOR 100

// Structure to represent a book
struct Book {
    int id;
    char title[MAX_TITLE];
    char author[MAX_AUTHOR];
};

// Global array to store books
struct Book library[MAX_BOOKS];
int bookCount = 0;

// Function to add a book
void addBook() {
    if (bookCount >= MAX_BOOKS) {
        printf("Library is full, cannot add more books.\n");
        return;
    }

    struct Book newBook;

    printf("Enter book ID: ");
    scanf("%d", &newBook.id);
    getchar(); // Clear newline from buffer

    printf("Enter book title: ");
    fgets(newBook.title, MAX_TITLE, stdin);
    newBook.title[strcspn(newBook.title, "\n")] = 0; // Remove newline

    printf("Enter book author: ");
    fgets(newBook.author, MAX_AUTHOR, stdin);
    newBook.author[strcspn(newBook.author, "\n")] = 0; // Remove newline

    library[bookCount] = newBook;
    bookCount++;

    printf("Book added successfully!\n");
}

// Function to display all books
void displayBooks() {
    if (bookCount == 0) {
        printf("No books in the library.\n");
        return;
    }

    printf("\nList of Books:\n");
    for (int i = 0; i < bookCount; i++) {
        printf("ID: %d\n", library[i].id);
        printf("Title: %s\n", library[i].title);
        printf("Author: %s\n\n", library[i].author);
    }
}

// Main function
int main() {
    int choice;

    do {
        printf("\nLibrary Management System\n");
        printf("1. Add Book\n");
        printf("2. Display Books\n");
        printf("3. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                addBook();
                break;
            case 2:
                displayBooks();
                break;
            case 3:
                printf("Exiting the system.\n");
                break;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    } while (choice != 3);

    return 0;
}