# Book App

A full-stack web application for discovering, reviewing, and saving books using the Google Books API. Built with Flask and MongoDB, this application provides a platform for book enthusiasts to search for books, read detailed information, leave reviews, and maintain a personal collection of saved books.

## Features

### 🔍 Book Search
- Search for books using keywords, titles, authors, or any relevant terms
- Powered by the Google Books API for comprehensive book database access
- Display search results with book covers, titles, authors, and other metadata

### 📚 Book Details
- Detailed book information pages including:
  - Title, authors, publisher, and publication date
  - Book description
  - Page count
  - Categories/genres
  - Book cover images
- Interactive book detail pages with all relevant information

### 👤 User Authentication & Profiles
- **User Registration**: Create an account with username, email, and password
- **Secure Login**: Password-protected login with bcrypt hashing
- **User Account**: 
  - Upload and manage profile pictures
  - Update username
- **User Detail Pages**: View any user's book reviews

### 💬 Reviews System
- Leave reviews/comments on book detail pages
- View reviews from all users on each book
- Reviews display with:
  - Commenter's username and profile picture
  - Review content
  - Timestamp of when the review was posted
- Browse all reviews by a specific user on their user detail page

### 📖 Saved Books
- Save books to your personal collection
- Access all saved books from your saved books page
- Remove books from your saved collection
- Quick access to saved books with book covers and titles

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS
- **Database**: MongoDB
- **External APIs**: Google Books API (https://developers.google.com/books)