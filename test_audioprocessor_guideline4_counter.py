import math
import pytest
from audioprocessor_guideline4_counter import AudioProcessor


class TestNormalize:
    def test_empty_samples(self):
        ap = AudioProcessor([])
        assert ap.normalize() == 0.0

    def test_all_zeros(self):
        ap = AudioProcessor([0.0, 0.0, 0.0])
        assert ap.normalize() == 0.0

    def test_positive_samples(self):
        ap = AudioProcessor([0.2, 0.5, 0.3])
        assert ap.normalize() == 0.5

    def test_negative_samples(self):
        ap = AudioProcessor([-0.7, -0.3, -0.1])
        assert ap.normalize() == 0.7

    def test_mixed_samples(self):
        ap = AudioProcessor([-0.9, 0.4, 0.6])
        assert ap.normalize() == 0.9

    def test_output_never_exceeds_one(self):
        ap = AudioProcessor([1.5, -2.0, 0.8])
        assert ap.normalize() == 1.0

    def test_output_range(self):
        ap = AudioProcessor([0.1, -0.4, 0.7])
        result = ap.normalize()
        assert 0.0 <= result <= 1.0


class TestComputeRms:
    def test_empty_samples(self):
        ap = AudioProcessor([])
        assert ap.compute_rms() == 0.0

    def test_all_zeros(self):
        ap = AudioProcessor([0.0, 0.0, 0.0])
        assert ap.compute_rms() == 0.0

    def test_constant_signal(self):
        ap = AudioProcessor([0.5, 0.5, 0.5])
        assert ap.compute_rms() == pytest.approx(0.5)

    def test_single_sample(self):
        ap = AudioProcessor([0.8])
        assert ap.compute_rms() == pytest.approx(0.8)

    def test_known_value(self):
        # RMS of [1.0, -1.0] = sqrt((1+1)/2) = 1.0
        ap = AudioProcessor([1.0, -1.0])
        assert ap.compute_rms() == pytest.approx(1.0)

    def test_output_range(self):
        ap = AudioProcessor([0.3, -0.7, 0.5, -0.2])
        result = ap.compute_rms()
        assert 0.0 <= result <= 1.0


class TestComputeDecibels:
    def test_empty_samples(self):
        ap = AudioProcessor([])
        assert ap.compute_decibels() == -80.0

    def test_silence_returns_floor(self):
        ap = AudioProcessor([0.0, 0.0, 0.0])
        assert ap.compute_decibels() == -80.0

    def test_max_amplitude(self):
        # RMS of [1.0, 1.0] = 1.0 => 20*log10(1.0) = 0.0 dB
        ap = AudioProcessor([1.0, 1.0])
        assert ap.compute_decibels() == pytest.approx(0.0)

    def test_half_amplitude(self):
        # RMS of [0.5, 0.5] = 0.5 => 20*log10(0.5) ≈ -6.02 dB
        ap = AudioProcessor([0.5, 0.5])
        assert ap.compute_decibels() == pytest.approx(20 * math.log10(0.5), abs=0.01)

    def test_output_range(self):
        ap = AudioProcessor([0.3, -0.7, 0.5])
        result = ap.compute_decibels()
        assert -80.0 <= result <= 0.0

    def test_near_silence_clamps_to_floor(self):
        ap = AudioProcessor([1e-10, -1e-10])
        assert ap.compute_decibels() == -80.0


class TestZeroCrossingRate:
    def test_empty_samples(self):
        ap = AudioProcessor([])
        assert ap.zero_crossing_rate() == 0.0

    def test_single_sample(self):
        ap = AudioProcessor([0.5])
        assert ap.zero_crossing_rate() == 0.0

    def test_no_crossings(self):
        ap = AudioProcessor([0.1, 0.2, 0.3, 0.4])
        assert ap.zero_crossing_rate() == 0.0

    def test_all_crossings(self):
        # Every consecutive pair crosses zero
        ap = AudioProcessor([0.5, -0.5, 0.5, -0.5])
        assert ap.zero_crossing_rate() == pytest.approx(1.0)

    def test_some_crossings(self):
        # Pairs: (1,−1)cross, (−1,−1)no, (−1,1)cross => 2/3
        ap = AudioProcessor([1.0, -1.0, -1.0, 1.0])
        assert ap.zero_crossing_rate() == pytest.approx(2.0 / 3.0)

    def test_output_range(self):
        ap = AudioProcessor([0.3, -0.1, 0.4, -0.5, 0.2])
        result = ap.zero_crossing_rate()
        assert 0.0 <= result <= 1.0


class TestSpectralCentroidBin:
    def test_empty_samples(self):
        ap = AudioProcessor([])
        assert ap.spectral_centroid_bin() == 0.0

    def test_zero_bins(self):
        ap = AudioProcessor([0.5, 0.3])
        assert ap.spectral_centroid_bin(n_bins=0) == 0.0

    def test_all_zeros(self):
        ap = AudioProcessor([0.0, 0.0, 0.0, 0.0])
        assert ap.spectral_centroid_bin() == 0.0

    def test_output_range(self):
        ap = AudioProcessor([0.5, -0.3, 0.8, -0.1, 0.4, -0.6, 0.2, -0.9])
        result = ap.spectral_centroid_bin(n_bins=8)
        assert 0.0 <= result <= 1.0

    def test_dc_signal_centroid_near_zero(self):
        # A constant signal has energy concentrated in the lowest bin
        ap = AudioProcessor([1.0] * 16)
        result = ap.spectral_centroid_bin(n_bins=8)
        assert result < 0.2


class TestSilenceRatio:
    def test_empty_samples(self):
        ap = AudioProcessor([])
        assert ap.silence_ratio() == 1.0

    def test_all_silent(self):
        ap = AudioProcessor([0.001, -0.005, 0.0])
        assert ap.silence_ratio() == pytest.approx(1.0)

    def test_no_silence(self):
        ap = AudioProcessor([0.5, -0.3, 0.8])
        assert ap.silence_ratio() == pytest.approx(0.0)

    def test_mixed(self):
        # 2 silent (0.005, 0.001), 2 loud (0.5, -0.3) => ratio = 0.5
        ap = AudioProcessor([0.5, 0.005, -0.3, 0.001])
        assert ap.silence_ratio() == pytest.approx(0.5)

    def test_custom_threshold(self):
        ap = AudioProcessor([0.1, 0.2, 0.3])
        assert ap.silence_ratio(threshold=0.15) == pytest.approx(1.0 / 3.0)

    def test_output_range(self):
        ap = AudioProcessor([0.05, -0.02, 0.5, 0.001])
        result = ap.silence_ratio()
        assert 0.0 <= result <= 1.0