# StatMate: AI-based Grade Analysis & Simulation Platform

## 1. Project Overview
**StatMate** is a comprehensive software platform designed for statistics students and educators. It integrates data processing, statistical simulation, and AI-based handwriting recognition into a single web application.

* **Project Name**: StatMate
* **Subject**: Computational Thinking & SW Coding
* **Submission Date**: 2025-12-27


## 2. Key Features
### 1) Grade Data Analysis
* **Technology**: Pandas
* Automatically processes CSV grade data.
* Handles missing values (Null) and calculates basic statistics (Mean, Std Dev).
* Visualizes student performance distribution.

### 2) Statistical Simulation
* **Technology**: NumPy, Matplotlib
* Simulates the **Law of Large Numbers (LLN)**.
* Users can set the number of trials for dice rolling experiments.
* Provides real-time visualization of empirical vs. theoretical probabilities.

### 3) AI Handwriting Recognition
* **Technology**: **Scikit-Learn (SVM)**, Pillow
* Recognizes handwritten digits (0-100) uploaded by the user.
* Preprocesses images (Grayscale, Resize, Inversion) for optimal model performance.


---

## Note on Technical Implementation
**Migration from TensorFlow to Scikit-Learn**
While the initial Software Requirements Specification (SRS) planned to use **TensorFlow**, the AI module was implemented using **Scikit-Learn (Support Vector Machine)**.

* **Reason**: To ensure stable performance and resolve library compatibility issues on the development environment (standard laptop without GPU support).
* **Result**: The SVM model successfully implements the required character recognition logic with lighter resource usage.

---


## 3. Tech Stack & Environment
* **Language**: Python 3.9+
* **Web Framework**: Streamlit
* **Libraries**: 
  * `pandas` (Data Analysis)
  * `numpy` (Numerical Computing)
  * `scikit-learn` (Machine Learning)
  * `matplotlib` (Visualization)
  * `Pillow` (Image Processing)


## 4. How to Run
To run this project locally, follow these steps:

 1) **Install Dependencies**
    ```bash
    pip install -r requirements.txt

 2) **Run the App**
    ```bash
    streamlit run app.py


## 5. Author
* Name: Lee Sojin
* Student ID: 2023020386
* Department: Statistics / Big Data Convergence
