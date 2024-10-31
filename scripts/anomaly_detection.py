from collections import deque
import numpy as np
from scripts.ema import EMA


class AnomalyDetector:
    def __init__(self, ema_alpha, window_size, threshold_multiplier):
        """
        Initializing the Anomaly Detector with an EMA calculator and a sliding window.
        :param ema_alpha: Smoothing factor for the EMA calculation
        :param window_size: The size of the sliding window for recent data points
        :param threshold_multiplier: The multiplier for the standard deviation to define thresholds
        """
        # Validate input values
        if not 0 < ema_alpha <= 1:
            raise ValueError("EMA alpha must be between 0 and 1.")
        if window_size <= 0:
            raise ValueError("Window size must be a positive integer.")
        if threshold_multiplier <= 0:
            raise ValueError("Threshold multiplier must be a positive number.")

        self.ema = EMA(ema_alpha)
        self.window = deque(maxlen=window_size)  #sliding window with a fixed size
        self.threshold_multiplier = threshold_multiplier  # Multiplier for dynamic thresholds

    def detect(self, data_point):
        """
        Detect if the new data point is an anomaly based on the EMA and dynamic thresholds.
        :param data_point: A single new data point to analyze
        :return: Tuple (is_anomaly, data_point, EMA, upper_threshold, lower_threshold)
        """
        try:
            current_ema = self.ema.update(data_point)

            # Add the new data point to the sliding window
            self.window.append(data_point)

            # Proceed if the sliding window has enough data points to calculate statistics
            if len(self.window) == self.window.maxlen:
                # Calculate the standard deviation of the sliding window
                std_dev = np.std(self.window)

                # Calculate dynamic upper and lower thresholds
                upper_threshold = current_ema + self.threshold_multiplier * std_dev
                lower_threshold = current_ema - self.threshold_multiplier * std_dev

                # Check if the new data point is outside the thresholds
                is_anomaly = data_point > upper_threshold or data_point < lower_threshold
                return is_anomaly, data_point, current_ema, upper_threshold, lower_threshold

            # If not enough data in the window, return without thresholds
            return False, data_point, current_ema, None, None

        except Exception as e:
            # Catch any errors and return diagnostic information
            print(f"Error during anomaly detection: {e}")
            return None, None, None, None, None
