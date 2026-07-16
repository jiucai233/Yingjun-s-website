---
layout: post
title: "Paper Review: SkiMo — Skip-Frame Model-Based RL for Generalizable Robotic Manipulation"
date: 2026-07-16
tags: [paper-review, RL, robotics, English]
description: An in-depth review of SkiMo's skip-frame model-based reinforcement learning — skill extraction (VAE), skill dynamics, state reconstruction, skill prior, and downstream planning with TD-MPC.
---

> Since Model-based RL accumulates small errors at each step, the total error will become massive as time goes on. SkiMo mitigates this by abstracting sequences of actions into skills and \"fast-forwarding\" $$H$$ steps at a time in the latent space.

---

## 1. High-level Summary & Architecture

**The Two-Phase Architecture:**

- **Phase 1 (Offline, task-agnostic pre-training):** VAE, Observation/Latent Reconstruction, and Skill Prior.
- **Phase 2 (Online / Downstream task learning):** Reward and Value predictions, RL policy with a custom KL regularizer.

---

## 2. Method Breakdown (Core Loss Equations)

### 2.1 Phase 1 — Task-Agnostic Pre-training

**① Skill Extraction (VAE)**

$$
\mathcal{L}_{\text{VAE}} = \underbrace{\Vert\pi(s_i,z)-a_i\Vert_2^2}_{\text{behavioural cloning}} + \underbrace{\text{KL}(q(z,(s,a)_{0:H-1})\,\Vert\,p(z))}_{\text{KL regularizer}}
$$

_The skill encoder takes the sequence of actions (skills) as input, mapping it to a tanh-transformed Gaussian distribution._

**② Skill Dynamics & State Reconstruction (Understanding Physics)**

$$
\mathcal{L}_{\text{REC}} = \underbrace{\lambda_O \Vert s_{iH} - O_\theta(E_\psi(s_{iH})) \Vert_2^2}_{\text{Observation reconstruction}} + \underbrace{\lambda_L \Vert D_\psi(\hat{h}_{iH}, z_{iH}) - E_{\psi^-}(s_{(i+1)H}) \Vert_2^2}_{\text{Latent state consistency}}
$$

_Observation is the current state and the output of the skill dynamics model is the future state; hence, $$s_{iH}$$ is used in the observation term and $$s_{(i+1)H}$$ is used in the latent state term._

**③ Skill Prior**

$$
\mathcal{L}_{\text{SP}} = \mathbb{E} \left[ \lambda_{\text{SP}} \cdot \text{KL} \Big( \text{sg}(q_\theta(z|(s, a)_{0:H-1})) \;\Big\Vert\; p_\theta(z|s_0) \Big) \right]
$$

_In this stage, we are extracting the prior from the encoder. The student policy $$p_\theta$$ learns knowledge from the encoder $$q_\theta$$. To prevent the encoder from shifting during alignment, a stop-gradient ($$\text{sg}$$) is applied to restrict the $$q_{\theta}$$ term._

The total loss is trained **jointly** ($$\mathcal{L} = \mathcal{L}_{\text{VAE}} + \mathcal{L}_{\text{REC}} + \mathcal{L}_{\text{SP}}$$). _We want the latent space to keep all the dimensional features aligned. If trained separately, the space optimized purely for action decoding ($$\mathcal{L}_{\text{VAE}}$$) might not be structured smoothly enough for the dynamics model to accurately predict the physical future ($$\mathcal{L}_{\text{REC}}$$)._

---

### 2.2 Phase 2 — Downstream Task Learning

When the agent enters the real environment with task-specific (and sparse) rewards:

#### Mental Planning (CEM + MPC)

The execution architecture for model-based RL consists of two components: CEM (Cross-Entropy Method) and TD-MPC.
The CEM plans a sequence of skills to solve the task while maximizing potential scores, and TD-MPC executes only the very first skill in the plan.

- **$$N$$ (Planning Horizon / Size):**
  - Too small $\rightarrow$ long-horizon information is insufficient.
  - Too large $\rightarrow$ prediction errors will accumulate.
- **$$H$$ (Skill Size / Frame-skip):**
  - Too small $\rightarrow$ loses the trait of skill-based abstraction.
  - Too large $\rightarrow$ execution errors will accumulate.
  - _Both hyperparameters perform best when set to 10._

**④ Finetuning the Model**

$$
\mathcal{L}_{\text{REC}}' = \text{(Latent consistency from Phase 1)} + \underbrace{\lambda_R\Vert r_t - R_\varphi(\hat{h}_t, z_t)\Vert_2^2}_{\text{Reward prediction}} + \underbrace{\lambda_V\Vert r_t + \gamma Q_{\varphi^-} - Q_\varphi\Vert_2^2}_{\text{Value prediction}}
$$

_These two prediction terms (Reward and Value) cannot be added during Phase 1 pre-training because Phase 1 is task-agnostic—we cannot obtain the exact reward and value metrics for a specific task even though we can interact with the environment._

**⑤ Task Policy Optimization (The SAC variant)**

$$
\mathcal{L}_{\text{RL}} = \mathbb{E} \left[ - Q_\varphi(\hat{h}_t, \pi_\varphi(\text{sg}(\hat{h}_t))) + \alpha \cdot \text{KL} \Big( \pi_\varphi(z_t|\text{sg}(\hat{h}_t)) \;\Big\Vert\; p_\theta(z_t|s_t) \Big) \right]
$$

_The actor target is slightly modified from the original entropy-based SAC objective to use a KL divergence term. The prior $$p_\theta$$ here ensures the selected actions conform to physical rules._

We apply a stop-gradient ($$\text{sg}$$) to the imagined state $$\hat{h}_t$$ here to **protect the physical rules** learned during Phase 1 pre-training inside the model's dynamics brain. Without it, the policy gradients would cause the physics rule representations to shift, leading the KL term to diverge.
