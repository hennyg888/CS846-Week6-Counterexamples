class AudioProcessor:
    """Processes audio signals where most outputs have constrained ranges
    that type hints alone cannot express."""

    def __init__(self, samples: list[float]):
        """
        Args:
            samples: Raw audio samples, each in range [-1.0, 1.0]
        """
        self.samples = samples

    def normalize(self) -> float:
        pass

    def compute_rms(self) -> float:
        pass

    def compute_decibels(self) -> float:
        pass

    def zero_crossing_rate(self) -> float:
        pass

    def spectral_centroid_bin(self, n_bins: int = 256) -> float:
        pass

    def silence_ratio(self, threshold: float = 0.01) -> float:
        pass