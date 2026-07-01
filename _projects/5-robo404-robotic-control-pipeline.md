---
layout: page
title: "ROBO404++: Robotic Control Pipeline"
description: Autonomous navigation simulation combining Soft Actor-Critic (SAC) reinforcement learning with a real-time YOLO/ONNX perception loop in ROS
importance: 5
category: work
---

## Background

Built as part of the **YBIGTA (Yonsei Big Data Society)** Data Engineering Team's robotics track. ROBO404++ combines reinforcement-learning-based navigation with real-time object perception into a single closed-loop control system running in ROS/Gazebo.

## Architecture

- **Control:** Soft Actor-Critic (SAC) trained for autonomous navigation in simulation, balancing exploration and stability in continuous action spaces.
- **Perception:** YOLO exported to ONNX for low-latency inference, feeding detections directly into the control loop.
- **Perception-Control Loop:** Integrated perception and control into a streamlined real-time loop within ROS, minimizing latency between detection and action.

## My Contributions
- Engineered the SAC-based navigation policy and simulation environment.
- Converted and optimized the YOLO perception model to ONNX for real-time inference.
- Integrated perception and control into a single low-latency ROS pipeline.

## Results & Impact
- Achieved a streamlined, low-latency Perception-Control Loop suitable for real-time autonomous navigation.
- Won **1st Place at the YBIGTA 26-1 Conference** for this project.

## Tech Stack
**ROS · Gazebo · Soft Actor-Critic (SAC) · YOLO · ONNX · Python**
