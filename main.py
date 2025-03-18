import streamlit as st
import pandas as pd
import os

# File to store the library data
LIBRARY_FILE = "library.csv"

# Load the library from a CSV file
def load_library():
    if os.path.exists(LIBRARY_FILE):
        return pd.read_csv(LIBRARY_FILE)
    return pd.DataFrame(columns=["Title", "Author", "Year", "Genre", "Read Status"])

# Save the library to a CSV file
def save_library(library):
    library.to_csv(LIBRARY_FILE, index=False)

# Add a book to the library
def add_book(library, title, author, year, genre, read_status):
    new_book = pd.DataFrame({
        "Title": [title],
        "Author": [author],
        "Year": [year],
        "Genre": [genre],
        "Read Status": [read_status]
    })
    return pd.concat([library, new_book], ignore_index=True)

# Remove a book from the library
def remove_book(library, title):
    return library[library["Title"].str.lower() != title.lower()]

# Search for books by title or author
def search_books(library, search_term, search_by="Title"):
    return library[library[search_by].str.lower().str.contains(search_term.lower())]

# Display statistics
def display_statistics(library):
    total_books = len(library)
    read_books = library["Read Status"].sum()
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
    return total_books, percentage_read

# Streamlit App
def main():
    st.set_page_config(page_title="Personal Library Manager", layout="wide")
    st.title("📚 Personal Library Manager")

    # Load the library
    library = load_library()

    # Sidebar for actions
    st.sidebar.header("Actions")
    action = st.sidebar.radio(
        "Choose an action:",
        ["Add a Book", "Remove a Book", "Search for a Book", "View All Books", "View Statistics"]
    )

    # Add a Book
    if action == "Add a Book":
        st.header("Add a Book")
        with st.form("add_book_form"):
            title = st.text_input("Title")
            author = st.text_input("Author")
            year = st.number_input("Publication Year", min_value=1800, max_value=2100, step=1)
            genre = st.text_input("Genre")
            read_status = st.checkbox("Have you read this book?")
            submitted = st.form_submit_button("Add Book")
            if submitted:
                if title and author and genre:
                    library = add_book(library, title, author, year, genre, read_status)
                    save_library(library)
                    st.success("Book added successfully!")
                else:
                    st.error("Please fill in all fields.")

    # Remove a Book
    elif action == "Remove a Book":
        st.header("Remove a Book")
        title_to_remove = st.text_input("Enter the title of the book to remove:")
        if st.button("Remove Book"):
            if title_to_remove:
                library = remove_book(library, title_to_remove)
                save_library(library)
                st.success("Book removed successfully!")
            else:
                st.error("Please enter a title.")

    # Search for a Book
    elif action == "Search for a Book":
        st.header("Search for a Book")
        search_by = st.radio("Search by:", ["Title", "Author"])
        search_term = st.text_input(f"Enter the {search_by}:")
        if search_term:
            results = search_books(library, search_term, search_by)
            if not results.empty:
                st.write("Matching Books:")
                st.dataframe(results)
            else:
                st.write("No matching books found.")

    # View All Books
    elif action == "View All Books":
        st.header("Your Library")
        if not library.empty:
            st.dataframe(library)
        else:
            st.write("Your library is empty.")

    # View Statistics
    elif action == "View Statistics":
        st.header("Library Statistics")
        total_books, percentage_read = display_statistics(library)
        st.write(f"Total books: {total_books}")
        st.write(f"Percentage read: {percentage_read:.1f}%")

# Run the app
if __name__ == "__main__":
    main()