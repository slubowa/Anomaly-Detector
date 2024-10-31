from scripts.data_stream import data_stream_simulation
from scripts.anomaly_detection import AnomalyDetector
from scripts.visualisation import real_time_plot


def run_real_time_detection():
    """
    Main function that coordinates the entire process of real-time data streaming,
    anomaly detection, and visualization.
    """
    data_stream = data_stream_simulation(delay=0.05)

    # Initialize the anomaly detector
    anomaly_detector = AnomalyDetector(ema_alpha=0.2, window_size=10, threshold_multiplier=2.2)

    # Start real-time plotting with anomaly detection
    real_time_plot(data_stream, anomaly_detector)


if __name__ == "__main__":
    run_real_time_detection()
