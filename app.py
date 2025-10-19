import streamlit as st
import pandas as pd
import threading
import time
from io import StringIO
from utils import (
    ScraperState,
    ScrapeData,
    df,
    state,
    MAX_PAGES,
    Algorithm,
    sortDataFrameByColumns,
    searchMultipleColumns
)

# Cache the dataframe reference so it doesn't reload on every rerun
@st.cache_resource
def get_df():
    return df

# # Get the cached dataframe
cached_df = get_df()

# Initialize sorting algorithm
algo = Algorithm()

# --- Page Config ---
st.set_page_config(
    page_title="Web Scraper UI",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Book Scraper Dashboard")

# Initialize session state for threading
if 'scraper_thread' not in st.session_state:
    st.session_state.scraper_thread = None
if 'is_scraping' not in st.session_state:
    st.session_state.is_scraping = False
if 'show_download' not in st.session_state:
    st.session_state.show_download = False

# --- Sidebar Controls ---
st.sidebar.header("Scraper Controls")

col1, col2, col3 = st.sidebar.columns(3)

with col1:
    if st.button("START", key="start_btn", width='content'):
        if not st.session_state.is_scraping and state.status.value != 'running':
            st.session_state.is_scraping = True
            # Start scraping in a thread to avoid blocking the UI
            st.session_state.scraper_thread = threading.Thread(target=ScrapeData, daemon=True)
            st.session_state.scraper_thread.start()
            st.success("Scraping started!")
            st.rerun()

with col2:
    # Dynamic button text based on state
    if state.status.value == 'paused':
        button_text = "RESUME"
    else:
        button_text = "PAUSE"
    
    if st.button(button_text, key="pause_resume_btn", width='content'):
        result = state.togglePauseResume()
        if result == "paused":
            st.info("Paused")
        elif result == "resumed":
            st.success("Resumed")
        st.rerun()

with col3:
    if st.button("STOP", key="stop_btn", width='content'):
        state.stop()
        st.session_state.is_scraping = False
        st.warning("Stopped")
        st.rerun()

st.sidebar.divider()

# Sidebar filters
st.sidebar.header("Filters & Sort")
if len(cached_df) > 0:
    st.sidebar.subheader("Multi-Column Search")
    search_cols = st.sidebar.multiselect("Select columns to search:", cached_df.columns)
    search_value = st.sidebar.text_input("Search value:")
    search_operator = st.sidebar.radio("Operator:", ["AND", "OR"], horizontal=True)
    
    st.sidebar.divider()
    st.sidebar.subheader("Sort Settings")
    sort_cols = st.sidebar.multiselect("Select columns to sort:", cached_df.columns, key="sort_cols")
    
    sort_algorithms = [
        "BubbleSort",
        "InsertionSort",
        "SelectionSort",
        "MergeSort",
        "QuickSort",
        "CountSort",
        "RadixSort",
        "BucketSort"
    ]
    selected_algo = st.sidebar.selectbox("Sort algorithm:", sort_algorithms)
    reverse_sort = st.sidebar.checkbox("Reverse sort order", value=False)
    
    sort_col_btn1, sort_col_btn2 = st.sidebar.columns(2)
    with sort_col_btn1:
        apply_sort = st.button("Apply Sort", use_container_width=True)
    with sort_col_btn2:
        reset_sort = st.button("Reset", use_container_width=True)
    
else:
    st.sidebar.info("No data available for filtering yet")

# --- Main Layout ---
col1, col2 = st.columns([2, 8])

# LEFT COLUMN: Controls & Stats
with col1:
    st.markdown("##### Statistics", unsafe_allow_html=True)
    
    status_dict = state.getStatus()
    
    # Status cards
    st.metric(
        "Status",
        status_dict['status'].upper(),
        delta=None
    )
    
    st.metric(
        "Current Page",
        f"{status_dict['currentPage']}/{status_dict['maxPages']}",
        delta=status_dict['currentPage']
    )
    
    st.metric(
        "Books Scraped",
        len(cached_df),
        delta=None
    )
    
    
    
    
    # Progress bar
    st.markdown("##### Progress", unsafe_allow_html=True)
    progress_percent = status_dict['progressPercent'] / 100
    progress_percent = min(progress_percent, 1.0)
    st.progress(progress_percent)
    st.caption(f"{status_dict['progressPercent']:.2f}% Complete")


# RIGHT COLUMN: Data Display
with col2:
    st.markdown("##### Scraped Books", unsafe_allow_html=True)
    
    if len(cached_df) > 0:
        display_df = cached_df.copy()
        
        if 'search_cols' in locals() and search_cols and 'search_value' in locals() and search_value:
            display_df = searchMultipleColumns(display_df, search_cols, search_value, search_operator)
        
        sort_time = 0
        
        if 'apply_sort' in locals() and apply_sort and 'sort_cols' in locals() and sort_cols and 'selected_algo' in locals() and len(display_df) > 0:
            try:
                display_df, sort_time = sortDataFrameByColumns(display_df, sort_cols, selected_algo, reverse_sort)
                        
            except Exception as e:
                st.warning(f"Sorting error: {e}")
        
        if 'reset_sort' in locals() and reset_sort:
            display_df = cached_df.copy()
            if 'search_cols' in locals() and search_cols and 'search_value' in locals() and search_value:
                display_df = searchMultipleColumns(display_df, search_cols, search_value, search_operator)
        
        # Display dataframe
        st.dataframe(
            display_df,
            width='content',
            hide_index=True,
            height=500
        )
        
        # Display sorting time if sort was applied
        if sort_time > 0:
            st.info(f"Sorting took: **{sort_time:.4f} seconds**")
        
        # Download button - only prepare on demand
        st.divider()
        if st.button("Generate Download", key="gen_download"):
            try:
                buffer = StringIO()
                cached_df.to_csv(buffer, index=False)
                csv_data = buffer.getvalue()
                st.session_state.show_download = True
                st.session_state.csv_data = csv_data
            except Exception as e:
                st.error(f"Cannot generate download: {str(e)}")
        
        # Show download button only after generation
        if st.session_state.show_download:
            st.download_button(
                label="Download CSV",
                data=st.session_state.csv_data,
                file_name="books_scraped.csv",
                mime="text/csv",
                width='content'
            )
            if st.button("Clear Download", key="clear_download"):
                st.session_state.show_download = False
                st.rerun()   
        
    else:
        st.info("No data scraped yet. Click START to begin scraping books from OpenLibrary!")
        st.info(f"Max pages to scrape: {MAX_PAGES}")

st.divider()
st.caption("**Developed by:** Hussain Shahbaz (2024-CS-04) | DSA Project 1")

# Auto-refresh if scraping is active
if st.session_state.is_scraping and state.status.value == 'running':
    time.sleep(1)
    st.rerun()

