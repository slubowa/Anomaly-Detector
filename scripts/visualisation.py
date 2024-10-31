import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


# Function for real-time plotting
def real_time_plot(data_stream, anomaly_detector):
    fig, ax = plt.subplots(figsize=(10, 6))

    data_points, ema_values, upper_thresholds, lower_thresholds, anomalies = [], [], [], [], []

    # Initialize empty plot lines
    data_line, = ax.plot([], [], label="Data Stream")
    ema_line, = ax.plot([], [], label="EMA", linestyle="--")
    upper_thresh_line, = ax.plot([], [], label="Upper Threshold", linestyle=":")
    lower_thresh_line, = ax.plot([], [], label="Lower Threshold", linestyle=":")
    anomaly_scatter = ax.scatter([], [], color='red', label="Anomalies")

    # Update function for FuncAnimation
    def update(frame):
        try:
            data_point = next(data_stream)

            # Validate the data point
            if not isinstance(data_point, (int, float)):
                raise ValueError(f"Invalid data point: {data_point}. Expected a number.")

            # Detect anomaly
            is_anomaly, data_point, current_ema, upper_threshold, lower_threshold = anomaly_detector.detect(data_point)

            # Append values to the respective lists for plotting
            data_points.append(data_point)
            ema_values.append(current_ema)
            upper_thresholds.append(upper_threshold)
            lower_thresholds.append(lower_threshold)

            # Update plot data
            data_line.set_data(np.arange(len(data_points)), data_points)
            ema_line.set_data(np.arange(len(ema_values)), ema_values)
            upper_thresh_line.set_data(np.arange(len(upper_thresholds)), upper_thresholds)
            lower_thresh_line.set_data(np.arange(len(lower_thresholds)), lower_thresholds)

            # Update anomalies if detected
            if is_anomaly:
                anomalies.append((len(data_points) - 1, data_point))
                anomaly_scatter.set_offsets(anomalies)

            # Rescale the axes limits dynamically
            ax.relim()
            ax.autoscale_view()

            return data_line, ema_line, upper_thresh_line, lower_thresh_line, anomaly_scatter

        except StopIteration:
            print("Data stream has ended.")
            return
        except Exception as e:
            print(f"Error during plot update: {e}")

    # plot details
    ax.set_title("Efficient Data Stream Anomaly Detection")
    ax.set_xlabel("Data Point Index")
    ax.set_ylabel("Value")
    ax.legend()

    # Real-time animation of graph, with frame caching disabled to reduce memory usage
    ani = FuncAnimation(fig, update, interval=2000, cache_frame_data=False)

    plt.show()
