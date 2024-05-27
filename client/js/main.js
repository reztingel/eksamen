document.addEventListener('DOMContentLoaded', () => {
    fetchBooks();

    document.getElementById('addBookForm').addEventListener('submit', addBook);
});

function fetchBooks() {
    fetch('/api/books')
        .then(response => response.json())
        .then(data => {
            const bookList = document.getElementById('bookList');
            bookList.innerHTML = '';
            data.forEach(book => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <strong>${book.title}</strong> by ${book.author} 
                    <button onclick="viewBook(${book.id})">View</button>
                    <button onclick="deleteBook(${book.id})">Delete</button>
                `;
                bookList.appendChild(li);
            });
        });
}

function sokBoker() {
    const searchInput = document.getElementById('searchInput').value;
    fetch(`/api/books?filter=${searchInput}`)
        .then(response => response.json())
        .then(data => {
            const bookList = document.getElementById('bookList');
            bookList.innerHTML = '';
            data.forEach(book => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <strong>${book.title}</strong> by ${book.author} 
                    <button onclick="viewBook(${book.id})">View</button>
                    <button onclick="deleteBook(${book.id})">Delete</button>
                `;
                bookList.appendChild(li);
            });
        });
}

function leggTilBok(event) {
    event.preventDefault();
    const title = document.getElementById('title').value;
    const author = document.getElementById('author').value;
    const isbn = document.getElementById('isbn').value;
    const number = document.getElementById('number').value;

    fetch('/api/books', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title, author, isbn, number })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            fetchBooks();
        }
    });
}

function visBok(id) {
    window.location.href = `book.html?id=${id}`;
}

function deleteBook(id) {
    fetch(`/api/books/${id}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            fetchBooks();
        } else {
            alert(data.error);
        }
    });
}
