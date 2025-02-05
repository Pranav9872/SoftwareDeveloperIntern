import matplotlib.pyplot as plt
import seaborn as sns

class DataVisualization:
    def __init__(self, data):
        self.data = data

    def plot_bar_chart(self, column):
        plt.figure(figsize=(10, 5))
        sns.barplot(x=self.data.index, y=self.data[column])
        plt.title(f'Bar Chart of {column}')
        plt.show()

    def plot_line_chart(self, column):
        plt.figure(figsize=(10, 5))
        sns.lineplot(x=self.data.index, y=self.data[column])
        plt.title(f'Line Chart of {column}')
        plt.show()
