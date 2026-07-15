---
layout: page
title: "ROBO404++: Robotic Control Pipeline"
description: Jetson-based line-following robot combining a SAC-trained control policy with a real-time YOLO/TensorRT traffic-light perception loop in ROS2
importance: 1
category: work
github: https://github.com/jiucai233/28th-conference-robo404_plus
img: assets/img/robo404-cover.png
---

{% assign robo404_poster_url = page.img | relative_url %}
{% include video.liquid path="assets/video/robo404-demo.mp4" class="portfolio-video-portrait rounded z-depth-1" poster=robo404_poster_url autoplay=true loop=true muted=true controls=true caption="Real-car demo — line following, traffic-light stop/go" %}

## Background

Built as part of the **YBIGTA (Yonsei Big Data Society)** Data Engineering Team's robotics track. ROBO404++ is a Jetson-based robot that follows a line, obeys a traffic light, and recovers when it loses the line — the first-phase scope runs end-to-end from raw camera input to the final `/cmd_vel` motor command.

## Architecture

The pipeline splits perception and decision-making across two CSI cameras and a single arbitrating node:

```
Bottom Camera → follower_node        → /cmd_vel_line, /path_state
Top Camera    → yolo_node (TensorRT) → /yolo/detections
                → traffic_light_node → /traffic_light_state

decision_node ← /cmd_vel_line, /path_state, /traffic_light_state
              → /cmd_vel   (the only node allowed to publish the final drive command)
```

- **Control:** `follower_node` only proposes a line-following candidate velocity (`/cmd_vel_line`); a dedicated `decision_node` is the single point that fuses line state and traffic-light state into the actual `/cmd_vel` sent to the motors — this separation is what let traffic-light stopping and line-recovery behavior be added without destabilizing line following.
- **RL Control Policy:** A Soft Actor-Critic (SAC) agent is trained (`train_agent.py`, TensorBoard-logged) against a custom line-tracking environment and exported to ONNX (`export_onnx.py`) for on-device inference.
- **Perception:** YOLO runs on Jetson via TensorRT (`yolo_jetson`) on the top camera feed to detect the traffic light; a `traffic_light_node` turns detections into a discrete state (`/traffic_light_state`) consumed by the decision node.
- **Debugging:** A `debug_monitor_node` aggregates all pipeline topics and warnings into a single `/debug/pipeline_state` stream for live diagnosis.

## My Contributions
- Designed and trained the SAC-based line-tracking control policy and exported it to ONNX for real-time Jetson inference.
- Built the YOLO/TensorRT traffic-light detection path and integrated it with the decision node.
- Helped define the `decision_node`-only `/cmd_vel` contract so perception and control could evolve independently.

## Results & Impact
- Shipped a working end-to-end pipeline: line following, traffic-light stop/go, and line-loss recovery, running live on Jetson hardware.
- Won **1st Place at the YBIGTA 26-1 Conference** for this project.

## Tech Stack
**ROS2 · Jetson · TensorRT · YOLO · Soft Actor-Critic (SAC) · ONNX · Python**
