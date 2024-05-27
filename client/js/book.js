document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const bookId = urlParams.get('id');
    fetchBookDetails(bookId);
});

function fetchBookDetails(id) {
    fetch(`/api/books/${id}`)
        .then(response => response.json())
        .then(data => {
            const bookDetail = document.getElementById('bookDetail');
            bookDetail.innerHTML = `
                <p><strong>Title:</strong> ${data.title}</p>
                <p><strong>Author:</strong> ${data.author}</p>
                <p><strong>ISBN:</strong> ${data.isbn}</p>
                <p><strong>Barcode:</strong> ${data.barcode}</p>
            `;
        });
}

function deleteBook() {
    const urlParams = new URLSearchParams(window.location.search);
    const bookId = urlParams.get('id');
    fetch(`/api/books/${bookId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = 'index.html';
        } else {
            alert(data.error);
        }
    });
}
