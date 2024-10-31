class EMA:
    def __init__(self, alpha):
        """
        Initialize EMA calculator with a given smoothing factor (alpha).
        :param alpha: The smoothing factor, typically calculated as 2 / (N + 1)
        """
        # alpha should be a float and between 0 and 1
        if not isinstance(alpha, (int, float)):
            raise TypeError("Alpha must be a numerical value.")
        if not (0 < alpha < 1):
            raise ValueError("Alpha must be between 0 and 1 (exclusive).")

        self.alpha = alpha  # Smoothing factor
        self.current_ema = None  # Initialize current EMA value

    def update(self, new_value):
        """
        Update the EMA with a new data point and return the new EMA value.
        :param new_value: The new data point to include in the EMA calculation
        :return: The updated EMA value
        """
        try:
            if not isinstance(new_value, (int, float)):
                raise TypeError("New value must be a numerical value.")

            # If there's no current EMA, initialize it with the first data point
            if self.current_ema is None:
                self.current_ema = new_value
            else:
                # Apply the EMA formula to update the EMA
                self.current_ema = self.alpha * new_value + (1 - self.alpha) * self.current_ema

            return self.current_ema

        except Exception as e:
            print(f"Error while updating EMA: {e}")
            return None
