import numpy as np

from . import hankel


def power2xi(Pk_func, R):
    """Calculate the correlation function using the Hankel
    transform of the power spectrum

    Taken from the KiDS-GGL pipeline, credit Andrej Dvornik.

    Reference:
        H. Ogata,
        A Numerical Integration Formula Based on the Bessel Functions,
        Publ. Res. Inst. Math. Sci. 41 (2005), 949-970.
        doi: 10.2977/prims/1145474602
    """
    assert len(np.squeeze(R).shape) == 1, 'R must be 1-d'
    result = np.zeros(R.shape)
    h = hankel.SphericalHankelTransform(0,10000,0.00001)
    for i in range(result.size):
        integ = lambda x: \
            np.exp(Pk_func(np.log(x/R[i]))) * (x**2) / (2*pi**2)
        result[i] = h.transform(integ)[0]
    return result / R**3
