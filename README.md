# Book Scraper Dashboard

## Overview

A comprehensive web scraping and data analysis application that collects book metadata from OpenLibrary and provides an interactive Streamlit dashboard for data exploration, filtering, and sorting using Data Structure Algorithms (DSA).

## Features

### Scraping
- **Web Scraping**: Automated collection of book data from OpenLibrary literature subject
- **Dynamic Control**: START, PAUSE, RESUME, and STOP buttons for scraper management
- **Resume Capability**: Continue scraping from the last successful page
- **Real-time Statistics**: Live tracking of progress, current page, and books collected
- **Data Persistence**: Automatic CSV storage of scraped data

### Data Management
- **Multi-Column Search**: Search across multiple columns simultaneously with AND/OR operators
- **Advanced Filtering**: Case-insensitive string matching across selected columns
- **Multi-Column Sorting**: Sort by multiple columns with custom DSA algorithms
- **Sort Algorithm Selection**: Choose from 6 implementations:
  - BubbleSort
  - InsertionSort
  - SelectionSort
  - MergeSort
  - QuickSort
  - CountSort
- **Performance Timing**: Display sorting execution time with millisecond precision
- **Reverse Sort**: Toggle descending order for any sort operation
- **Data Export**: Generate and download filtered/sorted results as CSV

### User Interface
- **Real-time Dashboard**: Live statistics panel showing status, page count, books scraped, and progress percentage
- **Responsive Layout**: Two-column design with controls and data visualization
- **Interactive Controls**: Intuitive sidebar for all configuration options
- **Session Management**: Persistent state across UI interactions

## Project Structure

```
Project1/
├── app.py                          # Main Streamlit application
├── data/
│   └── books.csv                   # Scraped book data
├── utils/
│   ├── __init__.py                 # Package exports
│   ├── ScraperState.py             # State machine for scraper lifecycle
│   ├── scrap.py                    # Web scraping logic with Selenium
│   ├── algorithms.py               # DSA sorting implementations
│   ├── sorting_handler.py          # Multi-column sorting orchestrator
│   └── search_handler.py           # Multi-column search functionality
└── README.md                        # This file
```

## Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Data Processing**: Pandas (DataFrame manipulation)
- **Web Scraping**: Selenium (WebDriver), BeautifulSoup (HTML parsing)
- **Concurrency**: Python Threading (background scraping)
- **Algorithms**: Custom implementations of 6 sorting algorithms

## Installation

### Prerequisites
- Python 3.8+
- Chrome browser with matching ChromeDriver

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Project1
```

2. Create virtual environment:
```bash
python -m venv lab4
.\lab4\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install streamlit pandas selenium beautifulsoup4
```

4. Download ChromeDriver matching your Chrome version and add to PATH

## Usage

### Running the Application

```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

### Workflow

1. **Start Scraping**: Click START button to begin collecting books
2. **Monitor Progress**: Watch real-time statistics and progress bar
3. **Control Execution**: Use PAUSE/RESUME to adjust scraping speed or STOP to halt
4. **Search Data**: Select columns and enter search value with AND/OR logic
5. **Sort Results**: Choose columns, algorithm, and apply sort
6. **Export Data**: Generate and download filtered/sorted results

## Data Schema

Scraped book data contains 12 columns:
- Title
- By (Author)
- Description
- Rating
- Date
- Publisher
- Language
- Pages
- Want to Read
- Have Read
- Currently Reading
- ISBN

## Configuration

### Scraping Parameters
- **Max Pages**: Configurable maximum pages to scrape (default: 1250)
- **Books Per Page**: 20 (OpenLibrary API standard)
- **Resume Point**: Automatically calculates from saved CSV records

### Sorting Parameters
- **Sort Columns**: Select 1 or more columns
- **Algorithm**: Choose from 6 DSA implementations
- **Reverse Order**: Toggle ascending/descending
- **Operator**: AND (all columns) / OR (any column) for search

## Architecture

### State Management
- **ScraperState**: Manages scraper lifecycle states (IDLE, RUNNING, PAUSED, STOPPED)
- **Session State**: Preserves UI state across Streamlit reruns
- **Cached Resources**: Prevents data duplication on application reload

### Sorting Pipeline
1. **Input**: Multiple columns, search values, algorithm selection
2. **Processing**: Apply DSA algorithm to each column in sequence
3. **Index Mapping**: Track row indices through all sort operations
4. **Output**: Return sorted DataFrame with execution timing

### Search Logic
- **AND Operator**: Returns rows matching search value in ALL selected columns
- **OR Operator**: Returns rows matching search value in ANY selected column
- **Case-Insensitive**: All searches ignore letter casing

## Performance Considerations

- **Lazy Loading**: CSV generation only on user request (prevents MemoryError)
- **Efficient Filtering**: Uses Pandas string operations for fast filtering
- **Parallel Execution**: Scraping runs in background thread without blocking UI
- **Incremental Scraping**: Saves data after each book (ensures data persistence)

## Error Handling

- **Invalid Progress Values**: Automatically clamped to 0.0-1.0 range
- **Sort Errors**: Graceful fallback with user notification
- **Search Errors**: Returns original DataFrame if search fails
- **Download Errors**: Error message displayed instead of crash

## Future Enhancements

- Multiple data source integration
- Advanced analytics and data visualization
- Custom filter expressions
- Batch export in multiple formats (JSON, Excel, etc.)
- Scheduled scraping tasks
- Database backend for large datasets

## License

This project is part of the Data Structures and Algorithms course curriculum.

## Author

Created as a DSA learning project implementing web scraping, state management, and sorting algorithms.

---

**Last Updated**: October 19, 2025
