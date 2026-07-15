---
layout: page
title: Food Detection by YOLO
description: Food detection system for delivery services using YOLOv8 nano — custom dataset built from enterprise CCTV footage, with a full data pipeline I designed end-to-end
importance: 2
category: work
github: https://github.com/jiucai233/DSL13thEnterpriseProject
img: assets/img/YoloDetection.jpg
images:
  slider: true
---

## Background

Conducted as part of the **Yonsei Data Science Lab (DSL)** 13th Enterprise Project. Our 6-member team partnered with a food delivery enterprise that was receiving high volumes of customer complaints related to incorrect or missing food items. The goal was to use computer vision to automate food item identification from **overhead CCTV-style camera footage** provided by the company.

## Custom Dataset & Data Pipeline

Unlike typical YOLO tutorials that pull pre-made datasets, **we built our own dataset from scratch** using surveillance-angle video frames provided by the enterprise partner:

1. **Frame Extraction** — Sampled key frames from the company's overhead monitoring camera recordings.
2. **Annotation** — Manually labeled bounding boxes for food categories relevant to the company's menu using LabelImg.
3. **Augmentation** — Applied rotation, brightness/contrast variation, and mosaic augmentation to handle the challenging top-down camera perspective, varying lighting, and partial occlusion.
4. **Quality Control** — Iteratively cleaned mislabeled samples and balanced class distribution.

I designed and implemented this **entire data pipeline** — from raw video to training-ready YOLO format.

## Model Training

- **Model:** YOLOv8n (nano variant — optimized for edge deployment)
- **Image size:** 640×640
- **Key metrics:** $$mAP_{50}$$ and $$mAP_{50-95}$$

We compared YOLOv8n, YOLOv8s, and YOLOv8m. **YOLOv8n achieved the best trade-off** between inference speed and accuracy for real-time deployment on the enterprise's existing infrastructure.

## Detection Results

<swiper-container keyboard="true" navigation="true" pagination="true" pagination-clickable="true" pagination-dynamic-bullets="true" rewind="true">
  <swiper-slide>{% include figure.liquid loading="eager" path="assets/img/YoloDetection.jpg" class="img-fluid rounded z-depth-1" caption="Multiple delivery boxes detected with food items" %}</swiper-slide>
  <swiper-slide>{% include figure.liquid loading="eager" path="assets/img/yolo_result_1.jpg" class="img-fluid rounded z-depth-1" caption="3 delivery boxes with food — overhead CCTV angle" %}</swiper-slide>
  <swiper-slide>{% include figure.liquid loading="eager" path="assets/img/yolo_result_2.jpg" class="img-fluid rounded z-depth-1" caption="Hand + closed box + food detection in action" %}</swiper-slide>
  <swiper-slide>{% include figure.liquid loading="eager" path="assets/img/yolo_result_3.jpg" class="img-fluid rounded z-depth-1" caption="Open containers with food items detected" %}</swiper-slide>
</swiper-container>

## Results & Impact
- Achieved **~95% detection accuracy** on real-world food delivery images from surveillance cameras.
- Effectively automated identification of missing or incorrect food items in customer complaints.
- Reduced manual complaint-handling workload for the enterprise partner.

## Tech Stack
**PyTorch · YOLOv8 · LabelImg · Python · OpenCV**
