import scipy.optimize as so

def Gauss(x,B=1.0,mean=0,s=1):
    return B * np.exp(-(x - mean)**2 / (2 * s**2))

#x peaks προσεγγιστικά
peak1_x = data1.loc[:,"wavelengths"][(data1["wavelengths"] > 661) & (data1["wavelengths"] < 665)]
peak2_x = data1.loc[:,"wavelengths"][(data1["wavelengths"] > 685) & (data1["wavelengths"] < 691)]
peak3_x = data1.loc[:,"wavelengths"][(data1["wavelengths"] > 696) & (data1["wavelengths"] < 701)]
peak4_x = data1.loc[:,"wavelengths"][(data1["wavelengths"] > 708) & (data1["wavelengths"] < 714)]
peak5_x = data1.loc[:,"wavelengths"][(data1["wavelengths"] > 733) & (data1["wavelengths"] < 737)]
peak6_x = data1.loc[:,"wavelengths"][(data1["wavelengths"] > 770) & (data1["wavelengths"] < 776)]

#y peask προσεγιστικά
peak1_y = data1.loc[:,"intensity"][(data1["wavelengths"] > 661) & (data1["wavelengths"] < 665)]
peak2_y = data1.loc[:,"intensity"][(data1["wavelengths"] > 685) & (data1["wavelengths"] < 691)]
peak3_y = data1.loc[:,"intensity"][(data1["wavelengths"] > 696) & (data1["wavelengths"] < 701)]
peak4_y = data1.loc[:,"intensity"][(data1["wavelengths"] > 708) & (data1["wavelengths"] < 714)]
peak5_y = data1.loc[:,"intensity"][(data1["wavelengths"] > 733) & (data1["wavelengths"] < 737)]
peak6_y = data1.loc[:,"intensity"][(data1["wavelengths"] > 770) & (data1["wavelengths"] < 776)]

plt.figure(figsize=(12,6))

plt.scatter(peak1_x,peak1_y,s=9)
plt.scatter(peak2_x,peak2_y,s=9)
plt.scatter(peak3_x,peak3_y,s=9)
plt.scatter(peak4_x,peak4_y,s=9)
plt.scatter(peak5_x,peak5_y,s=9)
plt.scatter(peak6_x,peak6_y,s=9)
plt.show()

init_guesses = [
    {"A": 0.4, "mean": 662.0, "sigma": 1.0},
    {"A": 0.2, "mean": 689.0, "sigma": 1.0},
    {"A": 0.1, "mean": 700.0, "sigma": 1.0}
]

peaks_x = [peak1_x, peak2_x, peak3_x]
peaks_y = [peak1_y, peak2_y, peak3_y]

fit_data = [(so.curve_fit(Gauss, x, y, p0=[init["A"], init["mean"], init["sigma"]])) for x, y, init in zip(peaks_x, peaks_y, init_guesses)]

fit_coeffs, fit_errors = zip(*fit_data)

print("Fitting Results:")
for i, (popt, pcov) in enumerate(fit_data, 1):
    print(f"Peak {i}:")
    print(f"A: {popt[0]:.3f} ± {np.sqrt(pcov[0, 0]):.3f}")
    print(f"mu: {popt[1]:.3f} ± {np.sqrt(pcov[1, 1]):.3f}")
    print(f"sigma: {popt[2]:.3f} ± {np.sqrt(pcov[2, 2]):.3f}")
    print("---")

fig, axs = plt.subplots(len(peaks_x), 1, figsize=(8, 12))

for i, (x, y, (fit_coeff, _)) in enumerate(zip(peaks_x, peaks_y, fit_data), 1):
    axs[i-1].scatter(x, y, s=7, label="Real Peak", color='black')
    x_fit = np.linspace(min(x), max(x), 100)
    y_fit = Gauss(x_fit, *fit_coeff)
    axs[i-1].plot(x_fit, y_fit, label="Fit", color='orange')
    axs[i-1].set_title(f"Peak {i}")
    axs[i-1].set_xlabel("Wavelengths")
    axs[i-1].set_ylabel("Intensity")
    axs[i-1].legend()

plt.tight_layout()
plt.show()

data1["wavenumbers"] = 1 / (data1["wavelengths"] * 10**(-7))
data1

plt.figure(figsize=(10, 6))

for x, y, popt, pcov in zip(peaks_x, peaks_y, fit_coeffs, fit_errors):
    A_opt, mu_opt, sig_opt = popt
    x_model = np.linspace(min(x), max(x), 1000)
    y_model = Gauss(x_model, A_opt, mu_opt, sig_opt)
    plt.plot(x_model, y_model, color='r', lw=2.0)
    plt.axvline(mu_opt, color='black', lw=1)
    text = r"$\lambda_{\rm max}$ = %.3f nm $\pm$ %.3f" % (mu_opt, np.sqrt(pcov[1, 1]))
    plt.text(mu_opt - 5, 0.25, text, rotation=90)

plt.scatter(data1["wavelengths"], data1["intensity"], s=10, label="smoothed spectrum")

plt.legend(fontsize=12)
plt.xlabel("Wavelengths (nm)", fontsize=12)
plt.ylabel("Intensity (arb. unit)", fontsize=12)

# Show the plot
plt.show()

for i in range(len(fit_coeffs)):
    p_sigma = np.sqrt(np.diag(fit_errors[i]))
    popt = fit_coeffs[i]
    print("absolute location of max peak %d : %.3f nm +/- %.3f" % (i+1, popt[1], p_sigma[1]))

laser_wavelength = 650 # in nm

for i in range(len(fit_coeffs)):
    popt = 1/(fit_coeffs[i] * 1e-7) 
    print("absolute location of max peak %d : %.3f cm^(-1)" % (i+1, popt[1]))
    print("relative location of max peak %d : %.3f cm^(-1)" % (i+1, 1/(laser_wavelength * 1e-7) - popt[1]))
    print("\n")

data1["rel_wavenumbers"] = 1/(laser_wavelength * 1e-7) - data1["wavenumbers"]
data1

plt.plot(data1["rel_wavenumbers"], data1["intensity"], label="smoothed spectrum",color='red')
plt.xlabel(r"Raman shift (cm$^{-1}$)", fontsize=11)
plt.ylabel("Intensity (arb. unit)", fontsize=11)
plt.show()

data2=pd.read_csv("data/database.csv",skiprows=8)

data2

data2_laser_wavelength=632

for index, k_range in enumerate(data2["Position (cm^-1)"].values):
   
    k_range = k_range.split(" - ")
    
    
    max_value = (1 / (data2_laser_wavelength * 1e-7)) - int(k_range[0])
    min_value = (1 / (data2_laser_wavelength * 1e-7)) - int(k_range[1])
    
    
    data2.at[index, "abs_position"] = "%d - %d" % (min_value, max_value)

data2

plt.figure(figsize=(13,9))

plt.plot(data1["rel_wavenumbers"], data1["intensity"], label="smoothed spectrum", color='red')


plt.text(350, 0.4, r"C-(NO$_2$) asym", color='red')


plt.text(700, 0.25, "C-ring breathing", color='green')


plt.annotate(
    "C=O\n+\nNH deformation",
    (1_100, 0.1),
    (1_100, 0.35),
    ha="center",
    color='purple',
    arrowprops=dict(arrowstyle = "->", color='purple')
)

plt.xlabel(r"Raman shift (cm$^{-1}$)", fontsize=14)
plt.ylabel("Intensity (arb. unit)", fontsize=14)
plt.title('Raman Spectrum Analysis', fontsize=16)
plt.legend(fontsize=14)
plt.show()

