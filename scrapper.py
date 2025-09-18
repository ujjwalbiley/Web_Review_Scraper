from bs4 import BeautifulSoup
import requests
import re
import time

def get_soup(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        raise Exception(f"Error fetching page: {str(e)}")

def scrape_flipkart_reviews(product_url, max_reviews=10):
    reviews = []
    page = 1
    
    # Extract product ID from URL
    match = re.search(r'pid=([A-Z0-9]+)', product_url)
    if not match:
        raise Exception("Invalid Flipkart product URL")
    
    product_id = match.group(1)
    base_url = f"https://www.flipkart.com/api/3/product/reviews?productId={product_id}"
    
    while len(reviews) < max_reviews:
        url = f"{base_url}&page={page}&limit=10"
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'X-User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 FKUA/website/41/website/Desktop'
            }
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            if not data or 'RESPONSE' not in data:
                break
                
            for review_data in data['RESPONSE']['data']:
                if len(reviews) >= max_reviews:
                    break
                    
                review = {
                    'product': review_data.get('product', {}).get('product_name', 'N/A'),
                    'user': review_data.get('author', {}).get('name', 'Anonymous'),
                    'rating': review_data.get('rating', 0),
                    'title': review_data.get('title', 'No Title'),
                    'comment': review_data.get('text', 'No Comment'),
                    'date': review_data.get('created', 'N/A'),
                    'website': 'flipkart'
                }
                reviews.append(review)
                
            if not data['RESPONSE'].get('next_page', False):
                break
                
            page += 1
            time.sleep(1)  # Be polite to the server
            
        except Exception as e:
            print(f"Error scraping Flipkart reviews: {str(e)}")
            break
    
    return reviews

def scrape_amazon_reviews(product_url, max_reviews=10):
    reviews = []
    
    # Extract product ASIN from URL
    match = re.search(r'/dp/([A-Z0-9]{10})', product_url)
    if not match:
        raise Exception("Invalid Amazon product URL")
    
    asin = match.group(1)
    base_url = f"https://www.amazon.in/product-reviews/{asin}"
    
    page = 1
    while len(reviews) < max_reviews:
        url = f"{base_url}/?pageNumber={page}"
        soup = get_soup(url)
        
        if not soup:
            break
            
        review_elements = soup.find_all('div', {'data-hook': 'review'})
        
        if not review_elements:
            break
            
        for review_element in review_elements:
            if len(reviews) >= max_reviews:
                break
                
            try:
                user_element = review_element.find('span', class_='a-profile-name')
                rating_element = review_element.find('i', {'data-hook': 'review-star-rating'})
                title_element = review_element.find('a', {'data-hook': 'review-title'})
                comment_element = review_element.find('span', {'data-hook': 'review-body'})
                date_element = review_element.find('span', {'data-hook': 'review-date'})
                
                review = {
                    'product': soup.title.text.replace('Amazon.in:Customer reviews:', '').strip() if soup.title else 'N/A',
                    'user': user_element.text.strip() if user_element else 'Anonymous',
                    'rating': float(rating_element.text.split()[0]) if rating_element else 0,
                    'title': title_element.text.strip() if title_element else 'No Title',
                    'comment': comment_element.text.strip() if comment_element else 'No Comment',
                    'date': date_element.text.split('on')[-1].strip() if date_element else 'N/A',
                    'website': 'amazon'
                }
                reviews.append(review)
            except Exception as e:
                print(f"Error parsing Amazon review: {str(e)}")
                continue
                
        # Check if there's a next page
        next_button = soup.find('li', class_='a-last')
        if not next_button or 'a-disabled' in next_button.get('class', []):
            break
            
        page += 1
        time.sleep(2)  # Be polite to the server
    
    return reviews