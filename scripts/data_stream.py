import numpy as np
import random
import time


def data_stream_simulation(delay=0.01):
    """
    Simulates a continuous data stream with seasonal patterns, random noise, and occasional anomalies.
    Emits one data point at a time with a 'delay' to simulate real-time streaming.
    """
    t = 0
    while True:
        try:
            # Simulate a continuously evolving sine wave with noise
            seasonal_pattern = 10 * np.sin(2 * np.pi * t / 100)
            noise = np.random.normal(0, 2)
            data_point = seasonal_pattern + noise

            # Introduce anomalies occasionally
            if random.choice([True, False]):
                data_point *= random.uniform(2, 4)

            yield data_point

            t += 1
            time.sleep(delay)  # Simulate real-time data generation with a delay

        except Exception as e:
            print(f"Error during data stream generation: {e}")
            yield None
