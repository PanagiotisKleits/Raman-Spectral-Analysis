def modified_z_score(y):
    detrended = np.diff(y)
    detrended_median = np.median(detrended)
    MAD = np.median(np.abs(detrended - detrended_median))
    modified_z_scores = 0.6745 * (detrended - detrended_median) / MAD
    return modified_z_scores



def despike1(y, m=5, threshold=6, inplace=False):
    """
    Remove cosmic spikes from the given array-like spectrum intensity.

    Parameters
    ----------
    y : array-like
        Spectrum intensity values.
    m : int, optional
        Width of the moving window (neighborhood), default is 5.
    threshold : int, optional
        Wavelengths with a modified z-score above this value are flagged as cosmic spikes, default is 6.
    inplace : bool, optional
        If True, overwrite the provided spectrum intensity in-place. If False, create a copy before modification.

    Returns
    -------
    y_interpolated : array-like
        Spectrum intensity with spikes removed and replaced with the interpolated average intensity value
        determined by the neighborhood (window) width.

    Notes
    -----
    The function identifies cosmic spikes based on the modified z-score, and replaces them with the
    interpolated average intensity value calculated from the specified window.

    Examples
    --------
        >>> intensity_values = [2, 4, 100, 9, 11, 13, 16, 18, 20]
        >>> result = despike(intensity_values, m=2, threshold=5)
        >>> print(result)
        array([ 2,  4, 11,  9, 11, 13, 16, 18, 20])

        >>> result_inplace = np.copy(intensity_values)
        >>> despike(result_inplace, m=2, threshold=5, inplace=True)
        >>> print(result_inplace)
        array([ 2,  4, 11,  9, 11, 13, 16, 18, 20])
    """
    if inplace:
        y_interpolated = y
    else:
        y_interpolated = y.copy()

        is_spike = np.abs(np.array(modified_z_score(y))) > threshold
    for i in np.arange(len(y) - 1):
        if is_spike[i] == True:
            try:
                if i - m < 0:
                    window_index = np.arange(i + m, i + 2 * m + 1)
                else:
                    window_index = np.arange(i - m, i + m + 1)

                I = is_spike[window_index] == False
                window_index = window_index[I]
                y_interpolated[i] = np.mean(y[window_index])

            except IndexError:
                if i == len(y) - 2:
                    y_interpolated[-1] = y[i - 1]
                else:
                    window_index = np.arange((i - m * 2), i - m)
                    I = is_spike[window_index] == False
                    window_index = window_index[I]
                    y_interpolated[i] = np.mean(y[window_index])

    return y_interpolated

despiked_spectrum = despike1(data1["intensity"])

plt.figure(figsize=(12,6))

plt.plot(data1["wavelengths"], data1["intensity"], color='black')
plt.plot(data1["wavelengths"], despiked_spectrum,  color='r')
plt.show()


import scipy.optimize as so
from scipy import sparse
from scipy.sparse.linalg import spsolve
from scipy.optimize import minimize,Bounds
from scipy.signal import find_peaks

# Baseline estimation function:
def baseline_cor(y, lam, p, n_iter=100):
    """
    Perform baseline correction on the given spectrum intensity.

    Parameters
    ----------
    y      : array-like
             Spectrum intensity values.
    lam    : float
             Smoothing parameter controlling the trade-off between smoothness and closeness
             to the original data.
    p      : float
             Parameter controlling the threshold for distinguishing between baseline and peaks.
    n_iter : int, optional
             Number of iterations for the baseline correction algorithm, default is 100.

    Returns
    -------
    z : array-like
        Corrected baseline of the input spectrum intensity.

    Notes
    -----
    The function estimates the baseline of the spectrum using a penalized least squares approach.
    It iteratively updates the weights and solves a linear system to find the baseline.

    Examples
    --------
        >>> intensity_values = [2, 4, 7, 9, 11, 13, 16, 18, 20]
        >>> result = baseline_correction(intensity_values, lam=100, p=0.1, n_iter=200)
        >>> print(result)
        array([ 2.12528206,  3.86725664,  6.46214845,  8.26235664, 10.06256482,
               11.862773  , 14.45766482, 16.25787301, 18.05808119])

    References
    ----------
    - Eilers, P. H. C., & Boelens, H. F. M. (2005).
      Baseline correction with asymmetric least squares smoothing.
      Leiden University Medical Center Report.
    """
    L = len(y)
    D = sparse.diags([1, -2, 1], [0, -1, -2], shape=(L, L - 2))
    w = np.ones(L)
    for i in range(n_iter):
        W = sparse.spdiags(w, 0, L, L)
        Z = W + lam * D.dot(D.transpose())
        z = spsolve(Z, w * y)
        w = p * (y > z) + (1 - p) * (y < z)
    return z

for i in np.logspace(-3, -1, 6):
    for l in np.logspace(2, 9, 6):
        print(f"Testing i = {i}, l = {l}")
        
        estimated_baselined = baseline_cor(despiked_spectrum, l, i)
        baselined_spectrum = despiked_spectrum - estimated_baselined
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 4))
        
        ax1.plot(data1["wavelengths"], despiked_spectrum, color='red', label='Mix spectrum with noise' )
        ax1.plot(data1["wavelengths"], estimated_baselined, color='black', label='Estimated baseline')
        ax1.set_title('Baseline estimation', fontsize=12)
        ax1.set_xlabel('Wavelength', fontsize=12)
        ax1.set_ylabel('Intensity', fontsize=12)
        ax1.legend(loc="lower right", fontsize=12)

        ax2.plot(data1["wavelengths"], baselined_spectrum, color='red')
        ax2.set_title('Baseline corrected spectrum', fontsize=12)
        ax2.set_xlabel('Wavelength', fontsize=12)
        ax2.set_ylabel('Intensity', fontsize=12)
        
        plt.show()

i=0.1
l=39810717.05534969

estimated_baselined = baseline_correction(despiked_spectrum, l, i)
baselined_spectrum = despiked_spectrum - estimated_baselined

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16,4))

# We compared the original mix spectrum and the estimated baseline
ax1.plot(data1["wavelengths"], despiked_spectrum, color= 'red', label='Mix spectrum with noise' )
ax1.plot(data1["wavelengths"], estimated_baselined, color='black', label='Estimated baseline')
ax1.set_title('Baseline estimation', fontsize=12)
ax1.set_xlabel('Wavelength', fontsize=12)
ax1.set_ylabel('Intensity)', fontsize=12)
ax1.legend(loc="lower right", fontsize=12)

# We plot the mix spectrum after baseline subtraction
ax2.plot(data1["wavelengths"], baselined_spectrum, color ='red')
ax2.set_title('Baseline corrected spectrum', fontsize=12)
ax2.set_xlabel('Wavelength', fontsize=12)
ax2.set_ylabel('Intensity', fontsize=12)
plt.show()

