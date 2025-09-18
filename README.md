# Web_Review_Scraper
A comprehensive Flask-based web application designed to extract, analyze, and export product reviews from major e-commerce platforms like Flipkart and Amazon. This tool provides businesses, researchers, and consumers with valuable insights from customer feedback through an intuitive interface and powerful data processing capabilities.
## Key Features

- **Dual Platform Support**: Extract reviews from both Flipkart and Amazon with customized scraping algorithms for each platform
- **Structured Data Extraction**: Captures comprehensive review information including user details, ratings, comments, dates, and product specifics
- **Excel Export Functionality**: One-click export to Excel format for further analysis and reporting
- **MongoDB Integration**: Optional database storage for persistent data management and historical tracking
- **Modern Web Interface**: Responsive design with smooth animations and intuitive user experience
- **RESTful API**: Complete API endpoints for integration with other applications and services

## Technology Stack

- **Backend Framework**: Python with Flask for robust server-side processing
- **Web Scraping**: BeautifulSoup4 and Requests for efficient data extraction
- **Frontend Development**: HTML5, CSS3 with animations, and vanilla JavaScript
- **Data Management**: MongoDB with PyMongo for flexible data storage
- **Export Capabilities**: OpenPyXL for professional Excel report generation
- **CORS Support**: Flask-CORS for cross-origin resource sharing

## Installation & Setup

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/product-review-scraper.git
cd product-review-scraper
```

2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

3. **(Optional) Setup MongoDB**:
   - Install MongoDB locally or use a cloud service
   - Update connection string in database.py if needed

4. **Launch the application**:
```bash
python app.py
```

5. **Access the application**:
   Open your browser and navigate to `http://localhost:5000`

## How It Works

1. **Input Product URL**: Paste any Flipkart or Amazon product page URL
2. **Configure Parameters**: Select platform and number of reviews to extract
3. **Initiate Scraping**: The system automatically extracts review data using advanced web scraping techniques
4. **View Results**: Analyze reviews in the clean tabular interface
5. **Export Data**: Download the collected data as Excel spreadsheets for further analysis

## Use Cases

- **Market Research**: Analyze customer sentiments and preferences for products
- **Competitive Analysis**: Compare product reviews across different brands and categories
- **Academic Research**: Gather data for consumer behavior studies and analysis
- **Product Development**: Identify common issues and improvement opportunities from customer feedback
- **Content Creation**: Generate authentic review content for blogs and videos

## Ethical Considerations

This tool is developed for educational and research purposes. Users are encouraged to:
- Respect websites' terms of service and robots.txt files
- Implement reasonable request delays to avoid overwhelming servers
- Use official APIs where available and appropriate
- Consider legal and ethical implications of web scraping in their region

## Contributing

We welcome contributions to enhance functionality, improve efficiency, and add support for additional e-commerce platforms. Please refer to the contribution guidelines in the repository for more information.

## License

This project is released under the MIT License, making it suitable for both personal and commercial use with proper attribution.
