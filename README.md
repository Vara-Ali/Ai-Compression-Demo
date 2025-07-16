#  CompressFlow Studio

CompressFlow Studio is a sleek and interactive Streamlit-based application for visualizing, simulating, and comparing multiple compression algorithms including JPEG, PNG, WebP, GZIP, ZLIB, and AI-powered methods. It includes beautiful metrics dashboards, real-time analytics, and side-by-side performance comparisons.

---

###  Features

-  Visually appealing UI with custom CSS styling
-  Real-time charts for compression ratio, speed, and quality
-  Live compression progress animation
-  Supports simulation of text, image, and byte data
-  AI-based compression simulation for research/education
-  Comparison dashboard for multiple algorithms
-  Uses actual `gzip` and `zlib` compression for realistic results

---

### Technologies Used

- [Streamlit](https://streamlit.io/) for the web UI
- [Plotly](https://plotly.com/python/) for data visualization
- [Pillow](https://pillow.readthedocs.io/) and [OpenCV](https://opencv.org/) for image processing
- [NumPy](https://numpy.org/) and [Pandas](https://pandas.pydata.org/) for data handling
- Python standard libraries: `gzip`, `zlib`, `base64`, `io`, `time`, `random`, etc.

---

### 🔧 Installation

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/compressflow-studio.git
cd compressflow-studio
