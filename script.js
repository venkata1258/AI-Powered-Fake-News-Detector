document.getElementById('news-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting normally
    
    const newsText = document.getElementById('news-text').value.trim(); // Get input text and trim whitespace

    // Check if the input is empty
    if (!newsText) {
        alert("Please enter some text to check!");
        return;
    }

    // Send the news text to the backend via a POST request
    fetch('/check-news', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ news_text: newsText }), // Send text as JSON
    })
    .then(response => response.json()) // Parse the response as JSON
    .then(data => {
        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = `<h3>Result:</h3><p class="${data.result === 'Real' ? 'success' : 'fake'}">This news is <strong>${data.result}</strong>.</p>`;
        
        // Apply specific styles based on result
        if (data.result === 'Real') {
            resultDiv.querySelector('p').style.color = '#388e3c'; // Green for real
        } else if (data.result === 'Fake') {
            resultDiv.querySelector('p').style.color = '#d32f2f'; // Red for fake
        }
        
        resultDiv.style.display = 'block'; // Show result div
    })
    .catch(error => {
        console.error('Error:', error);
        alert("There was an error processing the request. Please try again.");
    });
});
