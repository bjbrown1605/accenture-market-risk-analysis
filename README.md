# Market Risk Analysis - Accenture RiskControl

This project demonstrates the creation of a basic pipeline for market risk analysis using data from financial assets traded in Brazil. This work was developed as part of the selection process for the RiskControl internship position at Accenture.

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Project Objective

The main goal of this project is to develop a functional pipeline to:
* Collect historical data of Brazilian financial assets.
* Calculate the following market risk indicators: Annualized Historical Volatility, Parametric Value at Risk (VaR), and Correlation between assets.
* Present and visualize the results in a clear and interactive manner through a Jupyter Notebook report and an interactive Streamlit dashboard.

## 📂 Project Structure

The repository is organized as follows:

```
accenture-market-risk-analysis/
│
├── .venv/                  # Virtual environment directory
├── .gitignore              # Files and folders to be ignored by Git
├── LICENSE                 # Project license file
├── README.md               # This file
├── requirements.txt        # Project dependencies
├── pipeline.ipynb          # Jupyter Notebook with the detailed analysis
└── app.py                  # Python script for the Streamlit interactive dashboard
```

## 🛠️ Tools Used

The following languages and libraries were used in the development of this project:

* **Programming Language:** Python
* **Python Libraries:**
    * `pandas`: For data manipulation and analysis.
    * `numpy`: For numerical and mathematical operations.
    * `scipy`: For statistical functions, especially for VaR calculation.
    * `yfinance`: For collecting historical data from Yahoo Finance.
    * `plotly`: For creating interactive visualizations.
    * `streamlit`: For building the interactive web dashboard.
    * `jupyter`: For the development and presentation of the interactive notebook.

## 🚀 How to Run the Project

To replicate and run this project in your local environment, follow the steps below:

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/bjbrown1605/accenture-market-risk-analysis.git](https://github.com/bjbrown1605/accenture-market-risk-analysis.git)
    cd accenture-market-risk-analysis
    ```
2.  **Set Up the Virtual Environment (Recommended):**
    It is highly recommended to create a virtual environment to isolate project dependencies.
    ```bash
    # Create the virtual environment
    python -m venv .venv

    # Activate the virtual environment (Windows PowerShell):
    .venv\Scripts\Activate.ps1
    
    # Activate the virtual environment (Linux/macOS or WSL Bash):
    source .venv/bin/activate
    ```
3.  **Install Dependencies:**
    With the virtual environment activated, install all necessary libraries using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```
4.  **View the Results:**
    After installing the dependencies, you have two options to view the project's results:

    * **Option A: Run the Jupyter Notebook Report:**
        Start Jupyter Notebook and open the `pipeline.ipynb` file.
        ```bash
        jupyter notebook
        ```
        (Alternatively, open the `pipeline.ipynb` file directly in VS Code and run the cells.)

    * **Option B: Run the Interactive Dashboard:**
        Execute the `app.py` script with Streamlit to launch the web dashboard.
        ```bash
        streamlit run app.py
        ```

## 🧮 Calculation Explanations

This section details the formulas and methods used to calculate the risk indicators.

### Annualized Historical Volatility
* **Definition:** Measures the dispersion of returns for a given asset over a specific period.
* **Calculation:** It is based on the standard deviation of daily returns. To annualize, the daily standard deviation is multiplied by the square root of the number of trading days in a year (typically 252 for the Brazilian market).
    $$
    \text{Annualized Volatility} = \sigma_{\text{daily}} \times \sqrt{252}
    $$

### Parametric Value at Risk (VaR) at 95%
* **Definition:** Estimates the maximum expected loss of an investment over a given time horizon and with a specified confidence level, assuming a normal distribution of returns.
* **Calculation:** For a 95% VaR, assuming normally distributed returns, we use the mean of returns ($\mu$) and the standard deviation of returns ($\sigma$), along with the Z-score corresponding to the 5th percentile.
    $$
    \text{VaR}_{95\%} = -(\mu + Z_{0.05} \times \sigma)
    $$
    Where $Z_{0.05}$ is the critical value of the standard normal distribution for a 95% confidence level. The result is expressed as a positive value representing the potential loss.

### Correlation Between Assets
* **Definition:** Measures the strength and direction of the linear relationship between the returns of two assets. It ranges from -1 (perfect negative correlation) to +1 (perfect positive correlation).
* **Calculation:** The correlation function from the `pandas` library is used on the daily returns of the assets.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
