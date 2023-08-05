"""Tests the proc functions."""
# pylint: disable=invalid-name
# pylint: disable=missing-docstring
# pylint: disable=redefined-outer-name

import pytest
import numpy as np
import matplotlib.pyplot as plt

from gxps.spectrum import Spectrum
from gxps import io
from gxps import processing as proc


########## Fixtures

parsed_sdicts = [
    io.parse_spectrum_file("tests/fixtures/TiO2-110-f.txt"),
    io.parse_spectrum_file("tests/fixtures/Al-NE-FeCr-S02p6-Fe2p-3.xy"),
    io.parse_spectrum_file("tests/fixtures/21-04_015-XAS_100.xy"),
]

parsed_spectra = [Spectrum(**sdictlist[-1]) for sdictlist in parsed_sdicts]

@pytest.fixture
def tio2f():
    """TiO2-110-f dataset containing 22 individual spectra."""
    specdicts = io.parse_spectrum_file("tests/fixtures/TiO2-110-f.txt")
    return Spectrum(**specdicts[3])

parsed_spectra.append(Spectrum(
    energy=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    intensity=[4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
    filename="fixture_fname",
    name="fixture",
    key="T 3"
))


########## Test functions

@pytest.mark.parametrize("spectrum", parsed_spectra)
def test_bg_single_funcs(spectrum):
    i1, i2 = int(len(spectrum.energy) / 3), int(len(spectrum.energy) * 2 / 3)
    e, i = spectrum.energy[i1:i2], spectrum.intensity[i1:i2]
    try:
        bg_s = proc.shirley(e, i)
        assert len(bg_s) == len(e)
    except FloatingPointError:
        pass
    bg_l = proc.linear_bg(e, i)
    assert len(bg_l) == len(e)

@pytest.mark.parametrize("spectrum,method", [
    *[(spectrum, "linear") for spectrum in parsed_spectra],
    *[(spectrum, "shirley") for spectrum in parsed_spectra]
])
def test_calculate_background(spectrum, method):
    min_e = spectrum.energy.min()
    span = spectrum.energy.max() - min_e
    bg = proc.calculate_background(
        method,
        np.array([
            int(min_e + span * 0.1),
            int(min_e + span * 0.5),
            int(min_e + span * 0.6),
            int(min_e + span * 0.8)
        ]),
        spectrum.energy,
        spectrum.intensity
    )
    assert len(bg) == len(spectrum.energy)
    plt.plot(spectrum.energy, spectrum.intensity)
    plt.plot(spectrum.energy, bg)
    suffix = (spectrum.meta.filename.split("/")[-1]).split(".")[0]
    plt.savefig("tests/plot_verification/bg_{}_{}.png".format(method, suffix))
    plt.clf()

@pytest.mark.parametrize("spectrum", parsed_spectra)
def test_calculate_normalization_divisor(spectrum):
    e, i = spectrum.energy, spectrum.intensity
    d = spectrum.normalization_divisor
    divisor = proc.calculate_normalization_divisor("highest", d, e, i)
    assert np.isclose(divisor, i.max())
    divisor = proc.calculate_normalization_divisor("high_energy", d, e, i)
    assert np.isclose(divisor, i[-2], rtol=0.5)
    divisor = proc.calculate_normalization_divisor("low_energy", d, e, i)
    assert np.isclose(divisor, i[2], rtol=0.5)
    divisor = proc.calculate_normalization_divisor("manual", 4, e, i)
    assert np.isclose(divisor, 4)
    divisor = proc.calculate_normalization_divisor("none", d, e, i)
    assert np.isclose(divisor, 1.0)
