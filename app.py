import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import io
import base64
import gzip
import zlib
from PIL import Image
import cv2
import threading
from datetime import datetime
import random

# Configure page
st.set_page_config(
    page_title="CompressFlow Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .metric-container {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .comparison-box {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.7rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    .success-metric {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .warning-metric {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .sidebar .stSelectbox {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'compression_history' not in st.session_state:
    st.session_state.compression_history = []
if 'live_metrics' not in st.session_state:
    st.session_state.live_metrics = {
        'compression_ratio': [],
        'processing_speed': [],
        'quality_score': [],
        'timestamps': []
    }

class CompressionEngine:
    def __init__(self):
        self.algorithms = {
            'JPEG': self.jpeg_compression,
            'PNG': self.png_compression,
            'WebP': self.webp_compression,
            'GZIP': self.gzip_compression,
            'ZLIB': self.zlib_compression,
            'Advanced AI': self.ai_compression
        }
    
    def jpeg_compression(self, data, quality=85):
        """Simulate JPEG compression"""
        time.sleep(0.1)  # Simulate processing time
        compression_ratio = random.uniform(0.1, 0.3)
        quality_score = min(100, quality + random.uniform(-5, 5))
        return {
            'compressed_size': len(data) * compression_ratio,
            'quality_score': quality_score,
            'algorithm': 'JPEG'
        }
    
    def png_compression(self, data, level=6):
        """Simulate PNG compression"""
        time.sleep(0.15)
        compression_ratio = random.uniform(0.3, 0.6)
        quality_score = random.uniform(85, 95)
        return {
            'compressed_size': len(data) * compression_ratio,
            'quality_score': quality_score,
            'algorithm': 'PNG'
        }
    
    def webp_compression(self, data, quality=80):
        """Simulate WebP compression"""
        time.sleep(0.08)
        compression_ratio = random.uniform(0.15, 0.35)
        quality_score = min(100, quality + random.uniform(-3, 7))
        return {
            'compressed_size': len(data) * compression_ratio,
            'quality_score': quality_score,
            'algorithm': 'WebP'
        }
    
    def gzip_compression(self, data):
        """Actual GZIP compression"""
        compressed = gzip.compress(data.encode() if isinstance(data, str) else data)
        return {
            'compressed_size': len(compressed),
            'quality_score': 100,  # Lossless
            'algorithm': 'GZIP'
        }
    
    def zlib_compression(self, data):
        """Actual ZLIB compression"""
        compressed = zlib.compress(data.encode() if isinstance(data, str) else data)
        return {
            'compressed_size': len(compressed),
            'quality_score': 100,  # Lossless
            'algorithm': 'ZLIB'
        }
    
    def ai_compression(self, data, model='GPT-4'):
        """Simulate AI-powered compression"""
        time.sleep(0.3)  # AI takes longer
        compression_ratio = random.uniform(0.05, 0.15)  # Better compression
        quality_score = random.uniform(90, 98)
        return {
            'compressed_size': len(data) * compression_ratio,
            'quality_score': quality_score,
            'algorithm': 'Advanced AI'
        }

def create_live_chart(metrics_data):
    """Create live updating chart"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Compression Ratio', 'Processing Speed', 'Quality Score', 'Real-time Performance'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": True}]]
    )
    
    if len(metrics_data['timestamps']) > 0:
        # Compression ratio
        fig.add_trace(
            go.Scatter(
                x=metrics_data['timestamps'],
                y=metrics_data['compression_ratio'],
                mode='lines+markers',
                name='Compression Ratio',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8)
            ),
            row=1, col=1
        )
        
        # Processing speed
        fig.add_trace(
            go.Scatter(
                x=metrics_data['timestamps'],
                y=metrics_data['processing_speed'],
                mode='lines+markers',
                name='Speed (MB/s)',
                line=dict(color='#f093fb', width=3),
                marker=dict(size=8)
            ),
            row=1, col=2
        )
        
        # Quality score
        fig.add_trace(
            go.Scatter(
                x=metrics_data['timestamps'],
                y=metrics_data['quality_score'],
                mode='lines+markers',
                name='Quality Score',
                line=dict(color='#56ab2f', width=3),
                marker=dict(size=8)
            ),
            row=2, col=1
        )
        
        # Combined performance
        fig.add_trace(
            go.Scatter(
                x=metrics_data['timestamps'],
                y=metrics_data['compression_ratio'],
                mode='lines',
                name='Compression',
                line=dict(color='#667eea', width=2)
            ),
            row=2, col=2
        )
        
        fig.add_trace(
            go.Scatter(
                x=metrics_data['timestamps'],
                y=[q/100 for q in metrics_data['quality_score']],
                mode='lines',
                name='Quality (normalized)',
                line=dict(color='#56ab2f', width=2),
                yaxis='y2'
            ),
            row=2, col=2
        )
    
    fig.update_layout(
        height=600,
        showlegend=True,
        title_text="Live Compression Analytics",
        title_x=0.5,
        template='plotly_dark'
    )
    
    return fig

def create_comparison_chart(results):
    """Create side-by-side comparison chart"""
    algorithms = [r['algorithm'] for r in results]
    compression_ratios = [r['original_size'] / r['compressed_size'] for r in results]
    quality_scores = [r['quality_score'] for r in results]
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Compression Efficiency', 'Quality Retention'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Compression efficiency
    fig.add_trace(
        go.Bar(
            x=algorithms,
            y=compression_ratios,
            name='Compression Ratio',
            marker=dict(
                color=compression_ratios,
                colorscale='Viridis',
                showscale=True
            )
        ),
        row=1, col=1
    )
    
    # Quality scores
    fig.add_trace(
        go.Bar(
            x=algorithms,
            y=quality_scores,
            name='Quality Score',
            marker=dict(
                color=quality_scores,
                colorscale='RdYlGn',
                showscale=True
            )
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        title_text="Algorithm Performance Comparison",
        title_x=0.5,
        template='plotly_dark'
    )
    
    return fig

def animate_progress(placeholder, duration=3):
    """Animate progress bar"""
    progress_bar = placeholder.progress(0)
    status_text = placeholder.empty()
    
    for i in range(101):
        progress_bar.progress(i)
        if i < 30:
            status_text.text(f" Analyzing input... {i}%")
        elif i < 70:
            status_text.text(f" Compressing data... {i}%")
        else:
            status_text.text(f" Finalizing results... {i}%")
        time.sleep(duration / 100)
    
    status_text.text(" Compression complete!")

# Header
st.markdown("""
<div class="main-header">
    <h1 style="color: white; text-align: center; margin: 0; font-size: 3rem;">
         CompressFlow Studio
    </h1>
    <p style="color: white; text-align: center; margin: 0; font-size: 1.3rem;">
        Professional Compression Analytics & Visualization Platform
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("###  Control Panel")
compression_mode = st.sidebar.selectbox(
    "Select Compression Mode",
    [" Image Compression", " Text Compression", " Video Compression", " AI-Powered"]
)

algorithm = st.sidebar.selectbox(
    "Choose Algorithm",
    ["JPEG", "PNG", "WebP", "GZIP", "ZLIB", "Advanced AI"]
)

quality = st.sidebar.slider("Quality Level", 1, 100, 85)
live_mode = st.sidebar.checkbox(" Live Mode", value=True)

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("###  Input Data")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload your file",
        type=['jpg', 'jpeg', 'png', 'txt', 'pdf', 'mp4', 'avi']
    )
    
    # Text input
    text_input = st.text_area(
        "Or enter text to compress",
        height=150,
        placeholder="Enter your text here for compression testing..."
    )
    
    # Sample data button
    if st.button("📊 Generate Sample Data"):
        sample_text = "This is a comprehensive sample text for compression testing. " * 100
        text_input = sample_text
        st.success("Sample data generated!")

with col2:
    st.markdown("###  Live Metrics")
    
    # Create metric containers
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    
    with metric_col1:
        compression_metric = st.empty()
    with metric_col2:
        speed_metric = st.empty()
    with metric_col3:
        quality_metric = st.empty()

# Compression button
if st.button(" Start Compression", type="primary"):
    if uploaded_file is not None or text_input:
        # Progress animation
        progress_placeholder = st.empty()
        animate_progress(progress_placeholder, duration=2)
        
        # Initialize compression engine
        engine = CompressionEngine()
        
        # Prepare data
        if uploaded_file:
            data = uploaded_file.read()
        else:
            data = text_input.encode()
        
        original_size = len(data)
        
        # Run compression
        start_time = time.time()
        result = engine.algorithms[algorithm](data, quality)
        processing_time = time.time() - start_time
        
        compressed_size = result['compressed_size']
        compression_ratio = original_size / compressed_size
        processing_speed = (original_size / 1024 / 1024) / processing_time  # MB/s
        
        # Update metrics
        st.session_state.live_metrics['compression_ratio'].append(compression_ratio)
        st.session_state.live_metrics['processing_speed'].append(processing_speed)
        st.session_state.live_metrics['quality_score'].append(result['quality_score'])
        st.session_state.live_metrics['timestamps'].append(datetime.now())
        
        # Display results
        st.markdown("###  Compression Results")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="success-metric">
                Compression Ratio<br>
                <span style="font-size: 2rem;">{compression_ratio:.1f}x</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="success-metric">
                Size Reduction<br>
                <span style="font-size: 2rem;">{((1 - compressed_size/original_size) * 100):.1f}%</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="success-metric">
                Quality Score<br>
                <span style="font-size: 2rem;">{result['quality_score']:.1f}</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="success-metric">
                Speed<br>
                <span style="font-size: 2rem;">{processing_speed:.1f} MB/s</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Store results for comparison
        compression_result = {
            'algorithm': algorithm,
            'original_size': original_size,
            'compressed_size': compressed_size,
            'quality_score': result['quality_score'],
            'processing_time': processing_time,
            'timestamp': datetime.now()
        }
        
        st.session_state.compression_history.append(compression_result)
        
        # Progress cleanup
        progress_placeholder.empty()
        
        st.success(f" Compression completed using {algorithm}!")
    else:
        st.error("Please upload a file or enter text to compress.")

# Live charts
if live_mode and len(st.session_state.live_metrics['timestamps']) > 0:
    st.markdown("###  Live Analytics Dashboard")
    
    # Update live metrics display
    latest_metrics = st.session_state.live_metrics
    if latest_metrics['compression_ratio']:
        latest_compression = latest_metrics['compression_ratio'][-1]
        latest_speed = latest_metrics['processing_speed'][-1]
        latest_quality = latest_metrics['quality_score'][-1]
        
        compression_metric.metric(
            "Compression Ratio",
            f"{latest_compression:.1f}x",
            f"{latest_compression - (latest_metrics['compression_ratio'][-2] if len(latest_metrics['compression_ratio']) > 1 else latest_compression):.1f}"
        )
        
        speed_metric.metric(
            "Speed",
            f"{latest_speed:.1f} MB/s",
            f"{latest_speed - (latest_metrics['processing_speed'][-2] if len(latest_metrics['processing_speed']) > 1 else latest_speed):.1f}"
        )
        
        quality_metric.metric(
            "Quality",
            f"{latest_quality:.1f}",
            f"{latest_quality - (latest_metrics['quality_score'][-2] if len(latest_metrics['quality_score']) > 1 else latest_quality):.1f}"
        )
    
    # Live chart
    live_chart = create_live_chart(st.session_state.live_metrics)
    st.plotly_chart(live_chart, use_container_width=True)

# Comparison section
if len(st.session_state.compression_history) > 1:
    st.markdown("###  Algorithm Comparison")
    
    comparison_chart = create_comparison_chart(st.session_state.compression_history)
    st.plotly_chart(comparison_chart, use_container_width=True)
    
    # Detailed comparison table
    st.markdown("###  Detailed Performance Table")
    
    df = pd.DataFrame([
        {
            'Algorithm': r['algorithm'],
            'Original Size (KB)': r['original_size'] / 1024,
            'Compressed Size (KB)': r['compressed_size'] / 1024,
            'Compression Ratio': r['original_size'] / r['compressed_size'],
            'Quality Score': r['quality_score'],
            'Processing Time (s)': r['processing_time'],
            'Timestamp': r['timestamp'].strftime("%H:%M:%S")
        }
        for r in st.session_state.compression_history
    ])
    
    st.dataframe(df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    <p> CompressFlow Studio - Advanced Compression Analytics Platform</p>
    <p>Enterprise-Ready | Real-Time Performance | Professional Insights</p>
</div>
""", unsafe_allow_html=True)

# Auto-refresh for live mode
if live_mode:
    time.sleep(1)
    st.rerun()
