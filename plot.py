import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

class TimeSeriesPlot:
    """
    Plot time series data to a graph in real-time.
    """

    def __init__(self, data_queue, num_channels=1, max_points=100, y_label='Value'):
        self.data_queue = data_queue
        self.num_channels = num_channels
        self.max_points = max_points
        self.y_label = y_label
        self.x_data = []
        self.y_data = [[] for _ in range(num_channels)]
        self.start_time = None

        self.fig, self.ax = plt.subplots(figsize=(18, 10))
        self.fig.canvas.manager.set_window_title('Real-Time Serial Data Plotter')
        self.lines = [
            self.ax.plot([], [], label=f'Channel {i+1}')[0]
            for i in range(num_channels)
        ]
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel(y_label)
        self.ax.set_title('Real-Time Serial Data')
        self.ax.legend(loc='upper right')
        self.ax.grid(True)
        self.ax.set_ylim(-100, 4200)  # Fixed y-axis range

    def init_plot(self):
        for line in self.lines:
            line.set_data([], [])
        return self.lines

    def update_plot(self, frame):
        # Consume all available data in the queue
        updated = False
        while not self.data_queue.empty():
            values = self.data_queue.get()
            now = time.time()
            if self.start_time is None:
                self.start_time = now
            elapsed = now - self.start_time
            self.x_data.append(elapsed)
            for i, v in enumerate(values):
                self.y_data[i].append(v)
            # Keep only the last max_points
            if len(self.x_data) > self.max_points:
                self.x_data = self.x_data[-self.max_points:]
                for i in range(self.num_channels):
                    self.y_data[i] = self.y_data[i][-self.max_points:]
            updated = True
        if updated:
            for i, line in enumerate(self.lines):
                line.set_data(self.x_data, self.y_data[i])
            self.ax.relim()
            self.ax.autoscale_view()
        return self.lines

    def run(self):
        ani = animation.FuncAnimation(
            self.fig, self.update_plot, init_func=self.init_plot,
            interval=50, blit=False, cache_frame_data=False
        )
        plt.show()