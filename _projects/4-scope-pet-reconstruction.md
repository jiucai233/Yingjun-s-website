---
layout: page
title: "SCOPE: Slice-Consistent PET Reconstruction with 2D BBDM"
description: Medical image reconstruction addressing noise and slice inconsistency in PET imaging using 2D Bilateral Boundary Diffusion Models
importance: 5
category: research
img: assets/img/SCOPEProject.jpg
---

## Background

Positron Emission Tomography (PET) scanning is a critical tool in clinical diagnosis — used for detecting cancer, evaluating brain function, and monitoring cardiovascular disease. However, **low-dose PET images** suffer from two major challenges:

1. **High noise levels** — due to reduced radiotracer dose.
2. **Slice inconsistency** — when reconstructing 3D volumes from 2D PET slices, adjacent slices can appear visually inconsistent, reducing diagnostic reliability.

**SCOPE** (Slice-COnsistent PET rEconstruction) is a method designed to address both problems simultaneously.

## Method — 2D BBDM (Bilateral Boundary Diffusion Model)

SCOPE leverages a **2D Bilateral Boundary Diffusion Model (BBDM)** — a generative diffusion model — for image-to-image translation from low-dose to standard-dose PET.

### Key Innovations

**Diffusion-based Denoising**
Unlike traditional deep learning approaches (U-Net, GAN), diffusion models learn to iteratively denoise images through a Markov chain process, producing high-quality, realistic outputs while preserving structural detail.

**Bilateral Boundary Constraint**
The "bilateral boundary" component ensures that reconstructed 2D slices are constrained to remain consistent with their neighboring slices, effectively eliminating inter-slice discontinuities in the 3D reconstructed volume.

**Slice Consistency Enforcement**
By explicitly modeling the relationship between adjacent PET slices during training, SCOPE achieves visually smooth and clinically meaningful 3D reconstructions — a significant improvement over slice-by-slice processing methods.

## My Contributions
- Implemented the 2D BBDM architecture and integrated the bilateral boundary consistency constraint.
- Designed and ran experiments on low-dose PET datasets to evaluate reconstruction quality.
- Evaluated using standard medical imaging metrics (SSIM, PSNR, FID) against baseline denoising models.

## Results & Impact
- SCOPE produced PET reconstructions with significantly improved slice consistency compared to baseline 2D denoising approaches.
- The approach demonstrates the potential of diffusion models in clinical medical imaging workflows.

## Tech Stack
**PyTorch · Diffusion Models · BBDM · Medical Imaging (PET/MRI) · Python · NumPy**
