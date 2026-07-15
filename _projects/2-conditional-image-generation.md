---
layout: page
title: "Conditional Eyebrow Image Generation"
description: Celebrity-style eyebrow transfer using Stable Diffusion with LoRA adapters, BiSeNet face parsing, and LaMa inpainting
importance: 3
category: research
github: https://github.com/jiucai233/ConditionalImageGeneration
img: assets/img/ConditionalImageGeneration.png
---

## Background

This project builds a system that translates eyebrows in photographs to match specific celebrity styles (Go Youn Jung, Shin Se Kyung, Hong Su Zu). It combines face analysis, image manipulation, and generative modeling into a fully automated pipeline.

## Pipeline — 5 Stages

1. **Eyebrow Mask Generation** — BiSeNet face parsing produces raw semantic masks, dilated and smoothed for clean regions.
2. **Zoom Crop** — Focus to 512×512 around the eyebrow region.
3. **Eyebrow Erasing** — MediaPipe landmarks guide exclusion masks; LaMa performs 3-pass recursive inpainting.
4. **Conditional Generation** — Stable Diffusion inpainting (epiCRealism base) with celebrity-specific LoRA adapters (scale 1.15, 40 inference steps).
5. **Post-Processing** — LAB color correction, dynamic output detection, alpha blending back to original resolution.

## Key Results

- **LoRA semantic separation:** CLIP silhouette score improved from 0.0211 (base) to **0.7029** (LoRA), confirming distinct style clusters.
- **UNet latent features:** PCA silhouette 0.3012, t-SNE silhouette 0.2854 — clean separation across faces and styles.
- **Inference speed:** ~8s on RTX 3090, ~25s on Apple M-series.

## Tech Stack

PyTorch, Hugging Face Diffusers, PEFT (LoRA), BiSeNet, MediaPipe, LaMa, OpenCV, ONNX Runtime
