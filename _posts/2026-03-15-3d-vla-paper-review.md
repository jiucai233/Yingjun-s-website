---
layout: post
title: "Paper Review: 3D-VLA — Bridging 3D Representations into Vision-Language-Action Models"
date: 2026-03-15
tags: [paper-review, VLA, robotics, 3D, English]
description: Reviewing 3D-VLA's approach to injecting 3D understanding into VLA models — custom dataset construction, interaction tokens, dual diffusion model goal imagination, and multi-stage transformer alignment.
---

> Why train separate decoders and re-align them, when you could decode multiple representations in a single high-dimensional space?

## 1. 3D Dataset Construction

Since existing datasets lack the annotation density needed for 3D-aware VLA training, the authors built a custom data pipeline to curate 2D video/image data into rich 3D annotations:

> Obtaining annotations for point clouds, depth maps, 3D bounding boxes, the robot's 7D actions, and textual descriptions.

**Depth** — Used ZoeDepth to extract depth from raw images, then multiplied by a normalization coefficient.

**Optical Flow** — Applied RAFT to generate flow maps, enabling the model to distinguish moving objects from static background.

**3D Bounding Boxes** — Used spaCy for object name extraction, then SAM for mask generation, which are converted to 3D bounding boxes.

## 2. Interaction Tokens

When generating image captions, the authors introduced special **interaction tokens** to help the model converge faster and better distinguish objects:

```python
<obj> a chocolate bar </obj> [loc tokens] on the table
```

| Token | Purpose |
|-------|---------|
| `<obj>` `</obj>` | Enclose the object name |
| `<loc0-255>` | Ground referred objects in space |
| `<scene>` `</scene>` | Enclose embeddings of a static scene |
| `<aloc0-255>`, `<arot0-255>` | Robot location and rotation control |
| `<gripper0/1>` | Gripper open/close |

All tokens here are **discrete**, which means in practice this model may not be directly applicable to industrial scenarios requiring continuous control precision.

## 3. Diffusion Models and Training Objectives

The model can "imagine" goal scenarios using two pre-trained diffusion models, which are later re-aligned via a transformer-based projector:

> For RGBD-to-RGBD generation, we employ Stable Diffusion V1.4 [...] We concatenate the RGB latent and depth latent as the image condition. For point-to-point generation, we use Point-E, to which we add a point cloud condition input.

For alignment, the authors used **LoRA** to fine-tune the diffusion models and an LLM to avoid catastrophic forgetting. The paper doesn't elaborate on the loss design — because it's quite straightforward. From the code:

### T5 LLM Objective — Cross Entropy

```python
outputs = self.t5_model(
    inputs_embeds=inputs_embeds,
    attention_mask=encoder_atts,
    decoder_attention_mask=output_tokens.attention_mask,
    return_dict=True,
    labels=targets,
)
loss = outputs.loss
```

### Goal Image Diffusion — MSE

```python
model_pred = unet(concatenated_noisy_latents, timesteps, 
                  encoder_hidden_states).sample
loss = F.mse_loss(model_pred.float(), target.float(), reduction="mean")
```

### Goal Point Cloud Diffusion — MSE

```python
noise_pred = model(noisy_pointcloud, timesteps, pointcloud, texts=text)
loss = F.mse_loss(noise_pred, noise)
```

The loss design is intuitive: cross-entropy for the LLM, MSE for diffusion denoising.

## 4. Transformer Roles and Feature Alignment

The transformer architecture appears **three times** in the pipeline, each serving a different alignment role:

1. **Q-Former** — Compresses and translates 3D features into the text feature space. Accepts current images and "imagined" multimodal data, outputs the final action.
2. **Pretrained LLM (T5)** — Accepts translated 3D input + text input, generates text with interaction tokens.
3. **Transformer-based Projector** — Projects LLM output into the diffusion model's latent space for goal imagination.

The pattern: Q-Former handles **image → text**, the projector handles **text → image embedding**. These translators ensure the system works across modalities.

## 5. My Opinion

**Speed concerns.** The paper doesn't mention action frequency, but with 2 latent diffusion models and 3 transformers for alignment/generation, the inference latency is likely prohibitive for real-time industrial deployment.

**Value of the work.** As a study on integrating 3D features into VLA, this is an excellent reference. The dataset pipeline alone is a valuable contribution.

**Future direction.** The entire system is built on pre-trained modules stitched together. With recent breakthroughs in diffusion transformers (DiT), combining these separate modules into a **single model with a unified objective** seems like the natural next step — and would address the latency problem.

**The fundamental question:** Does 3D-VLA need to be better at *accuracy* or *response frequency*? Is it too redundant for a VLA model to process full 3D representations when a well-designed 2D system (like OpenVLA) already achieves decent generalization?
