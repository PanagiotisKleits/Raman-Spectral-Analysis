from scipy.signal import savgol_filter

smoothed_spectrum = savgol_filter(baselined_spectrum, window_length=10, polyorder=3)

plt.figure(figsize=(10,6))

plt.plot(data1["wavelengths"], baselined_spectrum, color='red', label='Baselined')
plt.plot(data1["wavelengths"], smoothed_spectrum, color='black', label='Smoothed')
plt.title('Baselined and smoothed spectrum', fontsize=12)
plt.xlabel('Wavelength', fontsize=12)
plt.ylabel('Intensity',  fontsize=12)
plt.legend()
plt.show()

data1.rename({"intensity":"intensity_raw"}, axis=1, inplace=True)
data1['intensity'] = smoothed_spectrum

data1

_ = data1.plot("wavelengths", figsize=(12,6))

