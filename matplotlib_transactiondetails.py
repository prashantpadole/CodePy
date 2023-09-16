import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class SuperstoreTransactionAnalyzer:
    def __init__(self, csv_file):
        self.csv_file = csv_file

    def load_data(self):
        self.data = pd.read_csv(self.csv_file)
        self.data['TransactionDate'] = pd.to_datetime(self.data['TransactionDate'])

    def analyze_data(self):
        self.data['ProcessingTime'] = self.data['EndTime'] - self.data['StartTime']

    def plot_processing_time(self):
        plt.figure(figsize=(12, 6))
        plt.plot(self.data['TransactionDate'], self.data['ProcessingTime'], marker='o', markersize=2, linestyle='-', color='b')
        plt.title('Transaction Processing Time Over Time')
        plt.xlabel('Transaction Date')
        plt.ylabel('Processing Time (seconds)')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

    def show_plot(self):
        plt.show()

# Generate sample data (you should replace this with your own CSV file)
np.random.seed(0)
date_rng = pd.date_range(start='2023-01-01', end='2023-01-31', freq='H')
data = {
    'TransactionDate': date_rng,
    'StartTime': date_rng + pd.to_timedelta(np.random.randint(1, 60, len(date_rng)), unit='s'),
    'EndTime': date_rng + pd.to_timedelta(np.random.randint(61, 600, len(date_rng)), unit='s')
}
df = pd.DataFrame(data)

# Save sample data to CSV file (replace 'sample_data.csv' with your desired file path)
sample_csv_file = 'sample_data.csv'
df.to_csv(sample_csv_file, index=False)

# Initialize and analyze the data
analyzer = SuperstoreTransactionAnalyzer(sample_csv_file)
analyzer.load_data()
analyzer.analyze_data()

# Plot and display the graph
analyzer.plot_processing_time()
analyzer.show_plot()
