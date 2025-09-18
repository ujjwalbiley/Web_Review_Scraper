document.addEventListener('DOMContentLoaded', function() {
    const scrapeForm = document.getElementById('scrapeForm');
    const resultsSection = document.getElementById('resultsSection');
    const loadingElement = document.getElementById('loading');
    const errorElement = document.getElementById('error');
    const reviewsList = document.getElementById('reviewsList');
    const reviewCount = document.getElementById('reviewCount');
    const exportBtn = document.getElementById('exportBtn');
    
    let currentReviews = [];
    
    scrapeForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const website = document.getElementById('websiteSelect').value;
        const productUrl = document.getElementById('productUrl').value;
        const maxReviews = document.getElementById('maxReviews').value;
        
        // Validate URL
        if (!isValidUrl(productUrl)) {
            showError('Please enter a valid URL');
            return;
        }
        
        // Show loading, hide error
        loadingElement.style.display = 'block';
        errorElement.style.display = 'none';
        
        try {
            const response = await fetch('/scrape', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    url: productUrl,
                    website: website,
                    max_reviews: maxReviews
                })
            });
            
            const data = await response.json();
            
            if (data.error) {
                showError(data.error);
                return;
            }
            
            currentReviews = data.reviews;
            displayReviews(currentReviews);
            reviewCount.textContent = `(${data.count} reviews)`;
            resultsSection.style.display = 'block';
            
        } catch (error) {
            showError('An error occurred while scraping: ' + error.message);
        } finally {
            loadingElement.style.display = 'none';
        }
    });
    
    exportBtn.addEventListener('click', async function() {
        const website = document.getElementById('websiteSelect').value;
        
        try {
            const response = await fetch('/export', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    website: website
                })
            });
            
            if (response.ok) {
                // Create a blob from the response and trigger download
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = `${website}_reviews.xlsx`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
            } else {
                const errorData = await response.json();
                showError(errorData.error || 'Export failed');
            }
        } catch (error) {
            showError('Export error: ' + error.message);
        }
    });
    
    function displayReviews(reviews) {
        reviewsList.innerHTML = '';
        
        reviews.forEach(review => {
            const row = document.createElement('tr');
            
            // Create star rating
            const ratingStars = '★'.repeat(Math.round(review.rating)) + 
                               '☆'.repeat(5 - Math.round(review.rating));
            
            row.innerHTML = `
                <td>${escapeHtml(review.product)}</td>
                <td>${escapeHtml(review.user)}</td>
                <td class="rating" title="${review.rating}">${ratingStars}</td>
                <td>${escapeHtml(review.title)}</td>
                <td>${escapeHtml(review.comment)}</td>
                <td>${escapeHtml(review.date)}</td>
            `;
            
            reviewsList.appendChild(row);
        });
    }
    
    function showError(message) {
        errorElement.style.display = 'block';
        document.getElementById('errorMessage').textContent = message;
    }
    
    function isValidUrl(url) {
        try {
            new URL(url);
            return true;
        } catch (e) {
            return false;
        }
    }
    
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
});
