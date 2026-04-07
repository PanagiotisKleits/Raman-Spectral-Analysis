### Objective
The purpose of this project is to explore a **workflow routine when it comes to analyzing data from a Raman spectrum**. For this purpose, we will construct a synthetic Raman spectrum as a mixture of individual spectra of some constituent elements. The spectrum of each element consists, in turn, of a specific number of Gaussian peaks.
To make our data more realistic and similar to what we would obtain from an actual spectroscopy experiment, we will add various sources of noise.
    
**This stage has already been implemented by the instructors**, and the resulting data has been provided to you in a csv file named `raman_spectrum.csv`. You may, if you wish, experiment with the `mspec.py` class that we created to construct the synthetic spectrum, creating your own spectra with different characteristics. To do this, read the examples we have prepared for you in the corresponding notebook.

***Your goal is twofold: First, you will need to process the spectrum appropriately to prepare it for analysis.*** This stage is often referred to as "pre-processing," and in this step, you must clean the spectrum from noise using techniques mentioned in the theoretical section of this notebook.

Once you complete the pre-processing stage, your spectrum will be ready for analysis and extraction of the desired features. The problem is that you do not know either the number of individual spectra (components) we used to create the final spectrum, or the concentrations of each component. The deconvolution of a spectrum that is a mixture of Gaussians can turn into a tedious process, and while there are various techniques and tools to achieve this, they all fall outside the scope of this project.

Nevertheless, one could estimate the number, type, and concentrations of the constituent elements of the spectrum by comparing the peaks of the spectrum with the peaks of spectra from a database that will be provided to you. **This type of spectral analysis constitutes your second goal for this project**.

> For a brief introduction to the data analysis routine commonly used for analyzing Raman spectra, see the work of Ryabchykov, Guo, and Bocklitz: [Ryabchykov, O., Guo, S., & Bocklitz, T. (2019), Analyzing Raman spectroscopic data, Physical Sciences Reviews, 4(2)](https://www.degruyter.com/document/doi/10.1515/9783110515312-004/pdf).
>
> A more comprehensive approach to Raman spectroscopy can be found in the textbook by Ewen Smith and Geoffrey Dent: [Modern Raman Spectroscopy – A Practical Approach](https://www.chemistry.uoc.gr/lapkin/Modern_Raman_Spectroscopy__A_Practical_Approach.pdf).

This notebook is divided into four parts:

1. The theoretical background, which serves as a short introduction to the concepts you will encounter and the techniques you will need to successfully complete the spectrum analysis.


2. The preparation of the data for the spectrum pre-processing stage. This involves reading and cleaning the data from various imperfections that might burden the data file (e.g., missing/blank entries).


3. The pre-processing of the spectrum. This includes identifying and removing noise sources as well as smoothing the spectrum prior to the final analysis.


4. The analysis of the spectrum aimed at determining certain molecular vibrations contained in this (theoretical) material.

## Theoretical background

Raman spectroscopy is a non-destructive chemical analysis technique that provides detailed information about the chemical structure, phase, polymorphism, and crystallinity of a sample, as well as the molecular interactions within a material. This technique is based on the interaction of light with the chemical bonds within the material through the phenomenon of Raman scattering. 

Due to its properties, Raman spectroscopy is commonly used to provide a structural "fingerprint" by which the molecules contained in a material sample can be identified. This makes it a highly popular technique in numerous fields such as Medicine, Biology, and Pharmacology (identification of active pharmaceutical ingredients, study of collective motions in proteins and DNA and their biological functions), in Physics (material characterization and finding the orientation of asymmetric crystals), in Chemistry, in Nanotechnology, and also in Archaeology for the analysis of corrosion products on the surfaces of artifacts (statues, vases, etc.), which can help determine the authenticity of valuable historical objects.


### The phenomenon of Raman scattering

When monochromatic electromagnetic radiation of frequency $\omega_i$ falls on a medium, it is scattered at various angles. From the analysis of the frequency spectrum of the scattered radiation, two main categories of scattering are observed: **elastic** and **inelastic**. In the first, the scattered radiation has the same frequency as the incident $\omega_i$, while in the second, the frequency differs by $d\omega$ from $\omega_i$. If the elastically scattered radiation originates from scattering centers with a dimension smaller than or comparable to the wavelength of the incident radiation (e.g., molecules) or larger than it (e.g., dust on the sample surface), then the scattering is elastic and is called `Rayleigh scattering` and `Mie scattering`, respectively. Their separation, however, in the solid state is difficult, so they are referred to by the general term Rayleigh scattering.


**Inelastic scattering is due to the interaction of light with the elementary excitations of a medium, including the vibrations of atoms in molecules or the collective vibrational excitations of the lattice of a crystalline solid.** If these excitations are acoustic (lattice vibrations excited by pressure waves or sound waves - acoustic phonons), then the scattering is called `Brillouin scattering` and typically involves frequency values of $0 - 1$ cm$^{-1}$ relative to the elastically scattered Rayleigh radiation. On the other hand, if the phonons are optical (vibrations excited by light of a certain frequency), then the scattering is called `Raman scattering`, with typical frequency values of $100 - 1000$ cm$^{-1}$ (relative to Rayleigh) for inorganic materials, while for organic materials and the corresponding molecular crystals, the frequency range is larger, starting below $100$ cm$^{-1}$ and often reaching $3000$ cm$^{-1}$.


The description of the Raman phenomenon can be done both quantum mechanically and through classical physics. The difference lies in the fact that through the classical approach, the connection of the Raman spectrum of a material with the properties, for example, of molecules can only be made qualitatively, while quantum mechanics provides the ability to make this connection quantitative and lays the groundwork for the proper treatment of molecular rotations and vibrations. Thus, a more complete picture of the factors affecting the scattered radiation is formed.


> **In short**
>
>To achieve Raman spectroscopy, a monochromatic light source is used, usually a laser at visible wavelengths, whose photons are scattered by a molecule of the material they fall upon. Most of the scattered light is at the same wavelength as the laser source and does not provide useful information - this is called **Rayleigh scattering**. However, a small amount of light (usually 0.0000001%) is scattered at different wavelengths due to the interaction of the laser photons with molecular vibrations, phonons (lattice vibrations), magnons (spin waves), plasmons (collective electron excitation), or other excitations in the system - this is called **Raman scattering**. These wavelengths depend on the chemical structure of the analyzed substance and result in the energy of the laser photons being shifted either upwards (shorter wavelengths - blueshifted) or downwards (longer wavelengths - redshifted). The shift/change in energy provides information about the vibrational modes in the system.


To study a material using Raman spectroscopy, the necessary equipment is required. The main parts of such an experimental setup are:

1. A source of monochromatic and parallel light beam (laser). Before the technological development of lasers, high-power spectral lamps were used to produce the exciting radiation. Specifically, the discrete spectral emission lines of a gas (e.g., mercury) were utilized. Initially, transparent samples were mostly chosen as study samples for Raman spectroscopy due to the large penetration depth of the radiation in them. However, with the development of powerful laser sources, opaque materials also began to be studied.


2.  A system for guiding and focusing the exciting radiation beam onto the sample. Usually, this system consists of an arrangement of lenses and filters that redirect the beam, change its power, and/or its width.


3.  A spectrometer for the spectral analysis of the scattered radiation from the studied sample. This device must have a resolving power such that the inelastically scattered radiation (Raman) is separated from the elastically scattered radiation (Rayleigh), considering the fact that Raman lines are more than 1000 times weaker than the Rayleigh line. Finally, the spectrometer must feature a function to reject stray radiation, which appears due to imperfections in the setup as well as the environment, such as the scattering of radiation by air particles and/or on the walls of the spectrometer.


4.  A detector of the scattered light that possesses particularly high sensitivity. A common device is a photomultiplier or a charge-coupled device (CCD).

### Typical Raman spectra and noise sources

A typical Raman spectrum features a number of peaks, showing the intensity and wavelength position of the scattered light. Each peak corresponds to a specific molecular bond vibration, including individual bonds such as C-C, C=C, N-O, C-H, etc., as well as complex groups of bonds such as polymer chain vibrations, etc.

Generally, the profile with the features of a spectrum (position and relative peak intensity) provides a unique chemical "fingerprint" that can be used to identify a material and distinguish it from all others.

The Raman spectrum from a material will contain information about all the molecules present within the sample. Thus, if there is a mixture of molecules, the Raman spectrum will contain peaks at specific wavelengths that are characteristic of all the different molecules.

As can be understood, a Raman spectrum (especially a spectrum originating from a mixture of materials) can be particularly complex to analyze. Additionally, under real experimental conditions, there are various sources of noise. These sources can be related to the material (sample-dependent artifacts), the experimental setup, and other exogenous factors such as cosmic radiation (non-sample-dependent artifacts). As a result, the spectra we obtain in an experiment are contaminated with structures beyond the characteristics of the material. For this reason, prior to analysis and drawing conclusions, appropriate pre-processing of the spectrum is necessary by identifying and removing these noise sources.

### Methods of dealing with noise

#### Cosmic ray spike removal (despiking)
Unlike other noise sources, the presence of cosmic ray spikes in spectroscopic data does not depend on the material sample, the laser, or the spectrometer. When high-energy particles hit the detector (CCD camera), electrons are generated due to the photoelectric effect, which are recorded along with the electrons caused by the energy of the scattered Raman photons. This results in some "spikes" appearing at random positions in the data (i.e., they do not correspond to a specific wavelength) that have characteristics of very high intensity and very narrow width.

![despiking.png](attachment:despiking.png)

To address this problem, we need two things:

1. A method for identifying these cosmic spikes within our data that constitute the actual spectrum.

2. A method for removing these structures and replacing them with an appropriate value.

To identify the spikes among the spectroscopic data, one can use the **modified z-score** as a metric, which we will define as:

$$Z_t = \frac{0.6745 \times (\nabla Y_t - M)}{\text{MAD}},$$
where
- $\nabla Y_t$ is the discrete difference $\nabla Y_t = Y_t - Y_{t-1},\,\,(t = 2, \dots, n)$. 
- $M$ is the median of this difference $\nabla Y_t$: $M = $ median($\nabla Y_t$).
- MAD is the median of the difference $|\nabla Y_t - M|$: MAD $=$ median($|\nabla Y_t - M|$)

The logic is that for each point in our data, we can assign it a z-score. If the score of a point exceeds a threshold $\tau$ that we have set $(|Z_t| > \tau)$, then this data point is marked as a point contributing to the creation of a spike.

Having marked all our spectral data in this way, we have managed to locate the problematic points that create the spikes. Now we must remove them and replace the resulting gap with an appropriate value. This value is derived by calculating the average of the values neighboring the problematic point. Specifically, the interpolated value ($\tilde{Y}_t$) will be:

$$\tilde{Y}_t = \frac{1}{w}\sum_{t-m}^{t+m} Y_t \times \mathbb{I}(Z_t < \tau)$$
where for the function $\mathbb{I}(u)$ the following applies:

\begin{equation}
    \mathbb{I}(u)=
    \begin{cases}
        1, & \text{if } u\,\,\text{is true}\\
        0, & \text{if }u\,\,\text{is false}
    \end{cases}
\end{equation}
and $$w = \sum_{t-m}^{t+m} \mathbb{I}(Z_t < \tau)$$

More detailed information regarding the removal of cosmic ray spikes in Raman spectra can be found in the work of Whitaker and Hayes: [Despiking algorithm with modified z-scores, Whitaker et al., Chemometrics and Intelligent Laboratory Systems Vol 179, 15 August 2018.](https://chemrxiv.org/engage/api-gateway/chemrxiv/assets/orp/resource/item/60c73e33469df41c2af4281c/original/a-simple-algorithm-for-despiking-raman-spectra.pdf).
