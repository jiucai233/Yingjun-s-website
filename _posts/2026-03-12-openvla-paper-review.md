---
layout: post
title: "Paper Review: OpenVLA — Open-Source Vision-Language-Action Model"
date: 2026-03-12
tags: [paper-review, VLA, robotics, English]
description: A deep dive into OpenVLA's architecture — dual vision backbone, action tokenization, and data mixing strategy that enables a 7B model to achieve strong generalization in robotic manipulation.
---

## Key Questions

**Q: What is the backbone model?**

The backbone is **Llama 2 (7B)**. The VLM (Prismatic) uses this as its language model, combined with a dual vision encoder.

**Q: What's the most important innovation?**

OpenVLA proved that even a **7B model**, with the right data mixture and vision backbone design, can achieve decent generalization in robotic manipulation while consuming far less compute than larger alternatives. And it's fully open-sourced.

---

## Core Architecture

### 1. Dual Vision Backbone

The vision encoder consists of two complementary modules:

- **DinoV2** — Provides precise object shape and depth information. Without it, the robot knows *what* the object is but cannot grasp it precisely.
- **SigLIP** — Combines object recognition with semantic/language alignment. Without it, the robot knows the object's shape and depth but cannot relate it to a language prompt.

```python
# Two modules' features are simply concatenated
def forward(self, pixel_values):
    dino_patches = self.dino_featurizer(pixel_values["dino"])
    siglip_patches = self.siglip_featurizer(pixel_values["siglip"])
    return torch.cat([dino_patches, siglip_patches], dim=2)
```

An important detail: the authors extract features from the **second-to-last layer** (`n={len(blocks) - 2}`), since the final layer's features lean toward classification while the penultimate layer retains more spatial/action-relevant information.

### 2. Action Tokenization

The key insight is converting continuous robot actions into discrete tokens that the LLM can generate:

```python
class ActionTokenizer:
    def __init__(self, tokenizer, bins=256, min_action=-1, max_action=1):
        self.bins = np.linspace(min_action, max_action, self.n_bins)
        self.bin_centers = (self.bins[:-1] + self.bins[1:]) / 2.0
        self.action_token_begin_idx = int(tokenizer.vocab_size - (bins + 1))
```

Three steps:
1. **Initialize bins** — `np.linspace` creates 256 uniform bins across the action range
2. **Clip and normalize** — Ensure values fall within the tokenizer's vocabulary range
3. **Discretize** — `np.digitize` converts continuous actions to bin indices

**Why 256 bins?** Following $$2^8$$ (8-bit encoding), this gives a discretization granularity of roughly **4mm per meter** of workspace — the intrinsic error margin of the action representation.

The reverse mapping (token → action) uses bin centers:

```python
def decode_token_ids_to_actions(self, action_token_ids):
    discretized_actions = self.tokenizer.vocab_size - action_token_ids
    discretized_actions = np.clip(discretized_actions - 1, 
                                   a_min=0, 
                                   a_max=self.bin_centers.shape[0] - 1)
    return self.bin_centers[discretized_actions]
```

### 3. Data Mixing Strategy

A common misconception: OpenVLA was **not** trained by mixing internet-scale data with robot data. Instead, it fine-tunes a **pretrained VLM** (already trained on internet data) using only robot trajectory datasets.

Two key filtering decisions:

1. **Restrict to manipulation datasets** with at least one 3rd-person camera and single-arm end-effector control — ensuring coherent I/O space.
2. **Leverage Octo's data mixture weights** for balanced distribution across embodiments and tasks.

The authors also removed the DROID dataset due to slow training and redistributed its weight across remaining datasets. The goal: enhance generalization and out-of-the-box deployment ability.

### 4. Additional Thoughts

> "We found fine-tuning the vision encoder during VLA training to be crucial for good VLA performance."

This opens an interesting direction: **Vision-Action (VA) models** that use only visual features to generate actions, bypassing the language component entirely.

Since all training data is robot-specific and the LLM output is action tokens (not natural language), it may be possible to run inference without industrial-grade GPUs. Perhaps this is another reason the team chose to open-source the entire codebase. As a student and engineer — big thanks to the open source community.
