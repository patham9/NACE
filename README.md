# NACE ( Non-Axiomatic Causal Explorer )

<div style="text-align:center"><img src="https://private-user-images.githubusercontent.com/8284677/293242166-7bde5719-96fe-4165-b5c4-ee36d3d1d02b.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTEiLCJleHAiOjE3MDM3ODE1OTYsIm5iZiI6MTcwMzc4MTI5NiwicGF0aCI6Ii84Mjg0Njc3LzI5MzI0MjE2Ni03YmRlNTcxOS05NmZlLTQxNjUtYjVjNC1lZTM2ZDNkMWQwMmIucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQUlXTkpZQVg0Q1NWRUg1M0ElMkYyMDIzMTIyOCUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyMzEyMjhUMTYzNDU2WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9ZDA5ZTY5NDU1MDhjOTNlZmNmNDkwOWZjODgwZTc0M2M4NTQ2NzA5M2MyMDUxMDFlNjg0ZGMxOTRlNjE2MDI0YyZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmYWN0b3JfaWQ9MCZrZXlfaWQ9MCZyZXBvX2lkPTAifQ.c77NRjoyjvEWw4HspeJBFtuCgov0M98PjA0r7jIQ1RY" height="250"></div>

## Aim
This project builds upon an ![implementation of Berick Cook's AIRIS](https://gist.github.com/patham9/ac25f7c85c82cebc0cb816823a4a6499), with support for partial observability. The aim is to enhance its capabilities to handle non-deterministic and non-stationary environments, as well as changes external to the agent. This will initially be achieved by incorporating relevant components of Non-Axiomatic Logic (NAL).

## Background

Several AI systems, as referenced in related works, employ a form of Cognitive Schematics. These systems learn and use empirically-causal temporal relations, typically in the form of **(precondition, operation) => consequence**. This approach allows the AI to develop a goal-independent understanding of its environment, primarily derived from correlations with the AI's actions. However, albeit not "necessarily causal" these "hypotheses" are not passively obtained correlations, as they can be re-tested and seeked for by the AI to improve its predictive power. This is a significant advantage over the axiomatic relations proposed by Judea Pearl. Pearl's approach is fundamentally limited, as it cannot learn from correlation alone, but only through adjusting probabilities of already-given causal relations. This limitation is not present in the cognitive schematic approach, which makes it a more general adaptive learning model better-suited for autonomous agents. Additionally, the use of two real values to represent hypothesis truth enables a more effective revision of the agent's knowledge. Unlike the probabilistic approach, this method can function effectively even with small sample sizes.

## Implementation

While the initial prototype is developed in Python, it will be integrated with ![Hyperon](https://github.com/trueagi-io/hyperon-experimental) using MeTTa. This integration will enable the use of the existing NAL implementation of ![MeTTa-NARS](https://github.com/patham9/metta-nars/tree/main), its attention and resource allocation mechanisms for scalability, and ![Probabilistic Logic Networks (PLN)](https://github.com/trueagi-io/hyperon-pln). The latter provides alternative methods for handling uncertainty and will improve the overall integration with other mechanisms developed within the Hyperon project.

## Related works:

![Autonomous Intelligent Reinforcement Interpreted Symbolism (AIRIS)](https://github.com/berickcook/AIRIS_Public)

![OpenNARS for Applications (ONA)](https://github.com/opennars/OpenNARS-for-Applications/)

![Rational OpenCog Controlled Agent (ROCCA)](https://github.com/opencog/rocca)

## Demo videos:

AIRIS Project 2023 Demonstration: https://www.youtube.com/watch?v=40W2OmV_rm0

OpenNARS for Applications v0.8.8 Demos: https://www.youtube.com/watch?v=oyQ250H5owE

