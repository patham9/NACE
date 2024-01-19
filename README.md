<div style="text-align:center"><img src="https://github.com/patham9/NACE/assets/8284677/152ff170-772d-4d81-b74c-ae5d84190235" height="250"></div>

## Aim

This project builds upon an [implementation of Berick Cook's AIRIS](https://gist.github.com/patham9/ac25f7c85c82cebc0cb816823a4a6499), with support for partial observability. The aim is to enhance its capabilities to handle non-deterministic and non-stationary environments, as well as changes external to the agent. This will initially be achieved by incorporating relevant components of Non-Axiomatic Logic (NAL).

## Background

Several AI systems, as referenced in related works, employ a form of Cognitive Schematics. These systems learn and use empirically-causal temporal relations, typically in the form of **(precondition, operation) => consequence**. This approach allows the AI to develop a goal-independent understanding of its environment, primarily derived from correlations with the AI's actions. However, albeit not "necessarily causal" these "hypotheses" are not passively obtained correlations, as they can be re-tested and seeked for by the AI to improve its predictive power. This is a significant advantage over the axiomatic relations proposed by Judea Pearl. Pearl's approach is fundamentally limited, as it cannot learn from correlation alone, but only through adjusting probabilities of already-given causal relations. This limitation is not present in the cognitive schematic approach, which makes it a more general adaptive learning model better-suited for autonomous agents. Additionally, the use of the NAL frequency and confidence values to represent hypothesis truth value enables efficient revision of the agent's knowledge in realistic settings. Unlike the probabilistic approach, this method can function effectively even with small sample sizes, can handle novel events (unknown unknowns) and has a low computational cost since only local memory updates are necessary.

## Architecture

![image](https://github.com/patham9/NACE/assets/8284677/778e4639-e079-4cce-8a4f-caed7d139c46)

## Related works:

[Autonomous Intelligent Reinforcement Interpreted Symbolism (AIRIS)](https://github.com/berickcook/AIRIS_Public)

[OpenNARS for Applications (ONA)](https://github.com/opennars/OpenNARS-for-Applications/)

[Rational OpenCog Controlled Agent (ROCCA)](https://github.com/opencog/rocca)

## Demo videos:

NACE Soccer: http://91.203.212.130/NACE/NACE_Soccer.mov

AIRIS Project 2023 Demonstration: https://www.youtube.com/watch?v=40W2OmV_rm0

OpenNARS for Applications v0.8.8 Demos: https://www.youtube.com/watch?v=oyQ250H5owE

