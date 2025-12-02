import sys
import os

# Add the 'backend' folder to the system path so that Streamlit can find the backend module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.graph_objects as go
from backend.report_builder import generate_report

# Set up the page configuration
st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    /* Main styling */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Headers */
    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        padding: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .main-subheader {
        font-size: 1.2rem;
        color: #718096;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    .section-header {
        font-size: 1.6rem;
        font-weight: 700;
        color: #2d3748;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 3px solid;
        border-image: linear-gradient(90deg, #667eea, #764ba2) 1;
    }
    
    .subsection-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #4a5568;
        margin: 1.2rem 0 0.8rem 0;
        padding-left: 0.5rem;
        border-left: 4px solid #667eea;
    }
    
    /* Cards with enhanced styling */
    .card {
        background: linear-gradient(145deg, #ffffff, #f7fafc);
        padding: 1.75rem;
        border-radius: 16px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08), 0 0 0 1px rgba(102, 126, 234, 0.05);
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-left: 5px solid #667eea;
    }
    
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12), 0 0 0 1px rgba(102, 126, 234, 0.1);
    }
    
    .issue-card {
        background: linear-gradient(145deg, #fff5f5, #fed7d7);
        padding: 1.25rem;
        border-radius: 12px;
        margin: 0.75rem 0;
        border-left: 4px solid #fc8181;
        box-shadow: 0 4px 12px rgba(252, 129, 129, 0.1);
        transition: all 0.3s ease;
    }
    
    .issue-card:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 16px rgba(252, 129, 129, 0.15);
    }
    
    .suggestion-card {
        background: linear-gradient(145deg, #f0fff4, #c6f6d5);
        padding: 1.25rem;
        border-radius: 12px;
        margin: 0.75rem 0;
        border-left: 4px solid #68d391;
        box-shadow: 0 4px 12px rgba(104, 211, 145, 0.1);
        transition: all 0.3s ease;
    }
    
    .suggestion-card:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 16px rgba(104, 211, 145, 0.15);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea15, #764ba215);
        padding: 1.5rem;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        border-color: rgba(102, 126, 234, 0.2);
    }
    
    /* Status indicators */
    .status-excellent {
        color: #48bb78;
        font-weight: 700;
        font-size: 1.1em;
    }
    
    .status-good {
        color: #68d391;
        font-weight: 700;
        font-size: 1.1em;
    }
    
    .status-warning {
        color: #ed8936;
        font-weight: 700;
        font-size: 1.1em;
    }
    
    .status-error {
        color: #f56565;
        font-weight: 700;
        font-size: 1.1em;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.9rem 2.5rem;
        font-weight: 700;
        border-radius: 12px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        font-size: 1.1rem;
        letter-spacing: 0.3px;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.5);
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1.5rem;
        padding: 0.5rem;
        background: linear-gradient(145deg, #f7fafc, #edf2f7);
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 55px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 1rem;
        color: #4a5568;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Badges */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 0.35rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
        margin: 0.2rem;
    }
    
    .badge-success {
        background: linear-gradient(135deg, #68d391, #48bb78);
        color: white;
    }
    
    .badge-warning {
        background: linear-gradient(135deg, #ed8936, #dd6b20);
        color: white;
    }
    
    .badge-error {
        background: linear-gradient(135deg, #fc8181, #f56565);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'report' not in st.session_state:
    st.session_state.report = None
if 'user_code' not in st.session_state:
    st.session_state.user_code = ""

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem 0;'>
        <div style='font-size: 3.5rem; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem;'>
            🔍
        </div>
        <h1 style='color: #2d3748; margin: 0;'>AI Code Reviewer</h1>
        <p style='color: #718096; font-size: 0.95rem; margin-top: 0.25rem;'>Advanced Code Analysis Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📋 How to Use")
    st.markdown("""
    1. **Paste** your Python code in the editor
    2. **Click** the Review Code button
    3. **Explore** the comprehensive analysis
    4. **Implement** AI suggestions
    """)
    
    st.markdown("---")
    
    st.markdown("### 🎯 Features")
    features = {
        "🔍 Static Analysis": "Detects bugs & vulnerabilities",
        "⚡ Performance": "Optimization tips & metrics",
        "📊 Code Quality": "Pylint scores & maintainability",
        "🤖 AI Suggestions": "LLM-powered recommendations",
        "🔢 Embeddings": "Vector analysis & visualization",
        "📈 Complexity": "Cyclomatic complexity analysis"
    }
    
    for icon, desc in features.items():
        st.markdown(f"""
        <div style='display: flex; align-items: flex-start; margin: 0.5rem 0;'>
            <span style='font-size: 1.2rem; margin-right: 0.5rem;'>{icon.split()[0]}</span>
            <div>
                <div style='font-weight: 600; color: #2d3748;'>{icon.split()[1]}</div>
                <div style='font-size: 0.9rem; color: #718096;'>{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    with st.expander("📊 **Metrics Guide**", expanded=False):
        st.markdown("""
        **🎯 Pylint Score (0-10)**
        - 9-10: Excellent
        - 7-8: Good
        - 5-6: Fair
        - <5: Needs improvement
        
        **📈 Maintainability (0-100)**
        - 85-100: Very High
        - 65-84: High
        - 45-64: Medium
        - <45: Low
        
        **🔍 Issues Found**
        - 0: Perfect
        - 1-3: Minor
        - 4-6: Moderate
        - >6: Many issues
        """)

# Main content area
st.markdown('<h1 class="main-header">🔍 AI-Powered Code Reviewer</h1>', unsafe_allow_html=True)
st.markdown("""
<div class="main-subheader">
    Get instant, comprehensive code analysis with AI-powered insights, bug detection, and performance optimization suggestions.
</div>
""", unsafe_allow_html=True)

# Create main layout with columns
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown('<div class="section-header">📝 Your Code</div>', unsafe_allow_html=True)
    
    user_code = st.text_area(
        "",
        height=320,
        placeholder="""# Paste your Python code here
def fibonacci(n):
    \"\"\"Calculate Fibonacci sequence up to n.\"\"\"
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[-1] + sequence[-2])
    return sequence

# Example usage
result = fibonacci(10)
print(f"Fibonacci sequence: {result}")""",
        label_visibility="collapsed",
        key="code_input"
    )

with col2:
    st.markdown('<div class="section-header">⚡ Quick Analysis</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea20, #764ba220); padding: 2rem; border-radius: 16px; border: 1px solid rgba(102, 126, 234, 0.1); box-shadow: 0 8px 25px rgba(102, 126, 234, 0.1);'>
        <div style='text-align: center;'>
            <div style='font-size: 3rem; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1rem;'>
                ⚡
            </div>
            <h3 style='color: #2d3748; margin: 0 0 1rem 0;'>Instant Code Insights</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='margin-top: 1rem;'>
        <div style='display: flex; align-items: center; margin: 0.8rem 0; padding: 0.8rem; background: rgba(255, 255, 255, 0.5); border-radius: 10px;'>
            <span style='font-size: 1.3rem; margin-right: 0.8rem;'>🔍</span>
            <div>
                <div style='font-weight: 600; color: #2d3748;'>Bug Detection</div>
                <div style='font-size: 0.85rem; color: #718096;'>Advanced pattern matching</div>
            </div>
        </div>
        <div style='display: flex; align-items: center; margin: 0.8rem 0; padding: 0.8rem; background: rgba(255, 255, 255, 0.5); border-radius: 10px;'>
            <span style='font-size: 1.3rem; margin-right: 0.8rem;'>⚡</span>
            <div>
                <div style='font-weight: 600; color: #2d3748;'>Performance</div>
                <div style='font-size: 0.85rem; color: #718096;'>Optimization analysis</div>
            </div>
        </div>
        <div style='display: flex; align-items: center; margin: 0.8rem 0; padding: 0.8rem; background: rgba(255, 255, 255, 0.5); border-radius: 10px;'>
            <span style='font-size: 1.3rem; margin-right: 0.8rem;'>📊</span>
            <div>
                <div style='font-weight: 600; color: #2d3748;'>Quality Metrics</div>
                <div style='font-size: 0.85rem; color: #718096;'>Comprehensive scoring</div>
            </div>
        </div>
        <div style='display: flex; align-items: center; margin: 0.8rem 0; padding: 0.8rem; background: rgba(255, 255, 255, 0.5); border-radius: 10px;'>
            <span style='font-size: 1.3rem; margin-right: 0.8rem;'>🤖</span>
            <div>
                <div style='font-weight: 600; color: #2d3748;'>AI Review</div>
                <div style='font-size: 0.85rem; color: #718096;'>Smart suggestions</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Review button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    review_button = st.button(
        "🔍 **REVIEW CODE**",
        use_container_width=True,
        type="primary",
        key="review_button"
    )

# Process review when button is clicked
if review_button:
    if not user_code.strip():
        st.warning("⚠️ Please paste some code to review.")
    else:
        with st.spinner("🔄 **Analyzing your code...** This may take a moment."):
            try:
                report = generate_report(user_code)
                st.session_state.report = report
                st.session_state.user_code = user_code
                
                # Success message
                st.success("""
                ✅ **Analysis Complete!**  
                Your code has been thoroughly analyzed. Explore the detailed report below.
                """)
                
                # Create tabs for different sections
                tabs = st.tabs([
                    "📊 **Overview**",
                    "🔍 **Static Analysis**", 
                    "📈 **Metrics & Complexity**",
                    "🤖 **AI Suggestions**",
                    "🔢 **Embeddings**"
                ])
                
                # Tab 1: Overview
                with tabs[0]:
                    st.markdown('<div class="section-header">📊 Code Health Overview</div>', unsafe_allow_html=True)
                    
                    # Create metrics grid
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        pylint_score = report.get('pylint_score', 0)
                        try:
                            score_value = float(pylint_score)
                        except:
                            score_value = 0.0
                        
                        if score_value >= 8:
                            status = "status-excellent"
                            label = "Excellent"
                            badge = "badge-success"
                        elif score_value >= 6:
                            status = "status-good"
                            label = "Good"
                            badge = "badge-success"
                        elif score_value >= 4:
                            status = "status-warning"
                            label = "Fair"
                            badge = "badge-warning"
                        else:
                            status = "status-error"
                            label = "Poor"
                            badge = "badge-error"
                        
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3 style='margin: 0 0 0.5rem 0; color: #4a5568; font-size: 1.1rem;'>Pylint Score</h3>
                            <div style='font-size: 2.8rem; font-weight: 800; margin: 0.5rem 0;' class='{status}'>
                                {score_value:.1f}<span style='font-size: 1.5rem; color: #a0aec0;'>/10</span>
                            </div>
                            <div style='margin: 0.5rem 0;'>
                                <span class='{badge}'>{label}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        maintainability = report.get('maintainability_index', 0)
                        try:
                            maint_value = float(maintainability)
                        except:
                            maint_value = 0.0
                        
                        if maint_value >= 80:
                            status = "status-excellent"
                            label = "Very High"
                            badge = "badge-success"
                        elif maint_value >= 65:
                            status = "status-good"
                            label = "High"
                            badge = "badge-success"
                        elif maint_value >= 50:
                            status = "status-warning"
                            label = "Medium"
                            badge = "badge-warning"
                        else:
                            status = "status-error"
                            label = "Low"
                            badge = "badge-error"
                        
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3 style='margin: 0 0 0.5rem 0; color: #4a5568; font-size: 1.1rem;'>Maintainability</h3>
                            <div style='font-size: 2.8rem; font-weight: 800; margin: 0.5rem 0;' class='{status}'>
                                {maint_value:.0f}<span style='font-size: 1.5rem; color: #a0aec0;'>/100</span>
                            </div>
                            <div style='margin: 0.5rem 0;'>
                                <span class='{badge}'>{label}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        issues_count = len(report.get('static_analysis', []))
                        
                        if issues_count == 0:
                            status = "status-excellent"
                            label = "Perfect"
                            badge = "badge-success"
                        elif issues_count <= 3:
                            status = "status-good"
                            label = "Minor"
                            badge = "badge-success"
                        elif issues_count <= 6:
                            status = "status-warning"
                            label = "Moderate"
                            badge = "badge-warning"
                        else:
                            status = "status-error"
                            label = "Many Issues"
                            badge = "badge-error"
                        
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3 style='margin: 0 0 0.5rem 0; color: #4a5568; font-size: 1.1rem;'>Issues Found</h3>
                            <div style='font-size: 2.8rem; font-weight: 800; margin: 0.5rem 0;' class='{status}'>
                                {issues_count}
                            </div>
                            <div style='margin: 0.5rem 0;'>
                                <span class='{badge}'>{label}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col4:
                        complexity_items = report.get('complexity', [])
                        complexity_count = len(complexity_items)
                        
                        if complexity_count == 0:
                            status = "status-excellent"
                            label = "Simple"
                            badge = "badge-success"
                        elif complexity_count == 1:
                            status = "status-good"
                            label = "Low"
                            badge = "badge-success"
                        elif complexity_count <= 3:
                            status = "status-warning"
                            label = "Moderate"
                            badge = "badge-warning"
                        else:
                            status = "status-error"
                            label = "Complex"
                            badge = "badge-error"
                        
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3 style='margin: 0 0 0.5rem 0; color: #4a5568; font-size: 1.1rem;'>Complexity</h3>
                            <div style='font-size: 2.8rem; font-weight: 800; margin: 0.5rem 0;' class='{status}'>
                                {complexity_count}
                            </div>
                            <div style='margin: 0.5rem 0;'>
                                <span class='{badge}'>{label}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Code preview
                    st.markdown('<div class="subsection-header">📋 Code Preview</div>', unsafe_allow_html=True)
                    st.code(user_code[:500] + ("..." if len(user_code) > 500 else ""), language='python')
                
                # Tab 2: Static Analysis
                with tabs[1]:
                    st.markdown('<div class="section-header">🔍 Static Analysis Results</div>', unsafe_allow_html=True)
                    
                    static_analysis = report.get('static_analysis', [])
                    if static_analysis:
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #fff5f5, #fed7d7); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 5px solid #fc8181;'>
                            <div style='display: flex; align-items: center; justify-content: space-between;'>
                                <div>
                                    <h3 style='margin: 0; color: #c53030;'>⚠️ Issues Detected</h3>
                                    <p style='color: #744242; margin: 0.5rem 0 0 0;'>
                                        Found {len(static_analysis)} potential issues in your code
                                    </p>
                                </div>
                                <span class='badge-error'>{len(static_analysis)} Issues</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        for idx, issue in enumerate(static_analysis, 1):
                            col1, col2 = st.columns([1, 20])
                            with col1:
                                st.markdown(f"""
                                <div style='background: #fc8181; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 1.2rem;'>
                                    {idx}
                                </div>
                                """, unsafe_allow_html=True)
                            with col2:
                                st.markdown(f"""
                                <div class="issue-card">
                                    <div style='display: flex; align-items: center; margin-bottom: 0.5rem;'>
                                        <span style='background: #c53030; color: white; padding: 0.2rem 0.8rem; border-radius: 4px; font-size: 0.85rem; font-weight: 600; margin-right: 0.5rem;'>
                                            ISSUE
                                        </span>
                                        <strong style='color: #2d3748; font-size: 1.1rem;'>Potential Issue Found</strong>
                                    </div>
                                    <div style='color: #4a5568; line-height: 1.6;'>{issue}</div>
                                </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div style='text-align: center; padding: 4rem 2rem; background: linear-gradient(135deg, #f0fff4, #c6f6d5); border-radius: 16px; margin: 2rem 0;'>
                            <div style='font-size: 4rem; margin-bottom: 1rem;'>🎉</div>
                            <h2 style='color: #276749; margin: 0 0 1rem 0;'>No Issues Found!</h2>
                            <p style='color: #4a5568; font-size: 1.1rem; max-width: 500px; margin: 0 auto;'>
                                Your code passed all static analysis checks. Great job!
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Tab 3: Metrics & Complexity
                with tabs[2]:
                    st.markdown('<div class="section-header">📈 Metrics & Complexity Analysis</div>', unsafe_allow_html=True)
                    
                    complexity = report.get('complexity', [])
                    if complexity:
                        for comp in complexity:
                            st.markdown(f"""
                            <div class="card">
                                <div style='display: flex; align-items: center; margin-bottom: 0.5rem;'>
                                    <span style='background: linear-gradient(135deg, #4299e1, #3182ce); color: white; padding: 0.3rem 0.6rem; border-radius: 6px; font-size: 0.9rem; font-weight: 600; margin-right: 0.5rem;'>
                                        METRIC
                                    </span>
                                </div>
                                <div style='color: #4a5568; line-height: 1.6;'>{comp}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Additional metrics section
                    st.markdown('<div class="subsection-header">📋 Additional Metrics</div>', unsafe_allow_html=True)
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Code Lines", len(user_code.split('\n')))
                    with col2:
                        st.metric("Characters", len(user_code))
                    with col3:
                        st.metric("Functions", user_code.count('def '))
                    with col4:
                        st.metric("Classes", user_code.count('class '))
                
                # Tab 4: AI Suggestions
                with tabs[3]:
                    st.markdown('<div class="section-header">🤖 AI-Powered Suggestions</div>', unsafe_allow_html=True)
                    
                    llm_review = report.get('llm_review', '')
                    if llm_review:
                        # Check if it's a string or list
                        if isinstance(llm_review, str):
                            suggestions = [s.strip() for s in llm_review.split('\n') if s.strip()]
                        elif isinstance(llm_review, list):
                            suggestions = llm_review
                        else:
                            suggestions = [str(llm_review)]
                        
                        # Filter out short items
                        suggestions = [s for s in suggestions if len(s) > 10]
                        
                        if suggestions:
                            st.markdown(f"""
                            <div style='background: linear-gradient(135deg, #f0fff4, #c6f6d5); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 5px solid #68d391;'>
                                <div style='display: flex; align-items: center; justify-content: space-between;'>
                                    <div>
                                        <h3 style='margin: 0; color: #276749;'>💡 AI Recommendations</h3>
                                        <p style='color: #4a5568; margin: 0.5rem 0 0 0;'>
                                            Found {len(suggestions)} improvement suggestions
                                        </p>
                                    </div>
                                    <span class='badge-success'>{len(suggestions)} Suggestions</span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            for idx, suggestion in enumerate(suggestions, 1):
                                st.markdown(f"""
                                <div class="suggestion-card">
                                    <div style='display: flex; align-items: center; margin-bottom: 0.8rem;'>
                                        <span style='background: #38a169; color: white; padding: 0.3rem 0.8rem; border-radius: 6px; font-size: 0.9rem; font-weight: 600; margin-right: 0.5rem;'>
                                            SUGGESTION {idx}
                                        </span>
                                        <strong style='color: #2d3748; font-size: 1.1rem;'>AI Recommendation</strong>
                                    </div>
                                    <div style='color: #4a5568; line-height: 1.6; padding-left: 1rem; border-left: 3px solid #68d391;'>
                                        {suggestion}
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("No structured suggestions available from AI.")
                    else:
                        st.info("No AI suggestions available for this code.")
                
                # Tab 5: Embeddings
                with tabs[4]:
                    st.markdown('<div class="section-header">🔢 Embedding Vector Analysis</div>', unsafe_allow_html=True)
                    
                    embedding_vector = report.get('embedding_vector_first_10_values', [])
                    if embedding_vector:
                        st.markdown("""
                        <div style='margin-bottom: 1.5rem; color: #4a5568; line-height: 1.6;'>
                            These are the first 10 values from your code's embedding vector. 
                            This numerical representation helps in comparing code similarity and patterns.
                            Embeddings capture semantic meaning of your code in a high-dimensional space.
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display embeddings in a beautiful grid
                        st.markdown("### 📊 Embedding Values (First 10)")
                        
                        # Create a grid of embedding values
                        cols = st.columns(5)
                        for i, value in enumerate(embedding_vector[:10]):
                            with cols[i % 5]:
                                # Format the value
                                try:
                                    val = float(value)
                                    color_intensity = min(abs(val) * 50, 100)
                                    if val > 0:
                                        bg_color = f"rgba(104, 211, 145, {0.2 + color_intensity/100})"
                                        text_color = "#276749"
                                    else:
                                        bg_color = f"rgba(252, 129, 129, {0.2 + color_intensity/100})"
                                        text_color = "#c53030"
                                    
                                    st.markdown(f"""
                                    <div style='background: {bg_color}; padding: 1rem; border-radius: 10px; text-align: center; margin-bottom: 0.5rem; border: 1px solid {text_color}20;'>
                                        <div style='font-size: 0.8rem; color: #718096; margin-bottom: 0.3rem;'>Dimension {i+1}</div>
                                        <div style='font-size: 1.2rem; font-weight: 700; color: {text_color}; font-family: monospace;'>
                                            {val:.4f}
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                except:
                                    st.markdown(f"""
                                    <div style='background: #e2e8f0; padding: 1rem; border-radius: 10px; text-align: center; margin-bottom: 0.5rem;'>
                                        <div style='font-size: 0.8rem; color: #718096; margin-bottom: 0.3rem;'>Dimension {i+1}</div>
                                        <div style='font-size: 1rem; font-weight: 600; color: #4a5568;'>
                                            {value}
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                        
                        # Show statistics
                        st.markdown("---")
                        st.markdown("### 📈 Embedding Statistics")
                        
                        try:
                            vec_array = np.array(embedding_vector[:10], dtype=float)
                            col1, col2, col3, col4 = st.columns(4)
                            
                            with col1:
                                st.metric("Mean", f"{vec_array.mean():.6f}")
                            with col2:
                                st.metric("Std Dev", f"{vec_array.std():.6f}")
                            with col3:
                                st.metric("Min", f"{vec_array.min():.6f}")
                            with col4:
                                st.metric("Max", f"{vec_array.max():.6f}")
                            
                            # Create a visualization
                            st.markdown("### 📊 Embedding Distribution")
                            fig = go.Figure()
                            
                            fig.add_trace(go.Scatter(
                                x=list(range(1, 11)),
                                y=vec_array,
                                mode='lines+markers',
                                name='Embedding Values',
                                line=dict(color='#667eea', width=3),
                                marker=dict(size=10, color='#764ba2')
                            ))
                            
                            fig.update_layout(
                                title="Embedding Values Across Dimensions",
                                xaxis_title="Dimension",
                                yaxis_title="Value",
                                height=400,
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                font=dict(color="#4a5568"),
                                showlegend=True
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                            
                        except Exception as e:
                            st.warning(f"Could not create statistics: {str(e)}")
                        
                        # Explanation
                        with st.expander("ℹ️ What are Embeddings?", expanded=False):
                            st.markdown("""
                            **Code Embeddings** are numerical representations of your code that capture its semantic meaning:
                            
                            - **Dimensionality**: Each dimension represents a feature of your code
                            - **Semantic Meaning**: Similar code produces similar embeddings
                            - **Use Cases**: Code similarity, pattern detection, clustering
                            - **Visualization**: Helps understand code structure patterns
                            
                            Higher absolute values indicate stronger presence of certain features.
                            """)
                    else:
                        st.info("No embedding vector available for this code.")
                
                # Export option
                st.markdown("---")
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("📥 Export Full Report as JSON", use_container_width=True):
                        report_json = json.dumps(report, indent=2)
                        st.download_button(
                            label="Download JSON Report",
                            data=report_json,
                            file_name="code_review_report.json",
                            mime="application/json",
                            use_container_width=True
                        )
                
            except Exception as e:
                st.error(f"❌ An error occurred while processing your code: {str(e)}")
                st.info("Please check your code syntax and try again.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #718096; padding: 2.5rem 0 1.5rem; margin-top: 3rem; border-top: 1px solid #e2e8f0;'>
    <p style='font-size: 1.1rem; margin-bottom: 0.5rem;'>🔍 AI Code Reviewer • Powered by Advanced AI Models</p>
    <p style='font-size: 0.9rem;'>Review your Python code for quality, security, and performance</p>
</div>
""", unsafe_allow_html=True)