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
