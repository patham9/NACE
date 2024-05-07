<div style="text-align:center"><img alt="Non-Axiomatic Causal Explorer" src="https://github.com/patham9/NACE/assets/8284677/09b4aea3-b6e0-4fc1-87d8-a8c238831d2d" height="250"></div>

## Aim

This project builds upon an [implementation of Berick Cook's AIRIS](https://gist.github.com/patham9/ac25f7c85c82cebc0cb816823a4a6499), with support for partial observability. The aim is to enhance its capabilities to handle non-deterministic and non-stationary environments, as well as changes external to the agent. This will initially be achieved by incorporating relevant components of Non-Axiomatic Logic (NAL).

## Background

Several AI systems, as referenced in related works, employ a form of Cognitive Schematics. These systems learn and use empirically-causal temporal relations, typically in the form of **(precondition, operation) => consequence**. This approach allows the AI to develop a goal-independent understanding of its environment, primarily derived from correlations with the AI's actions. However, albeit not "necessarily causal" these "hypotheses" are not passively obtained correlations, as they can be re-tested and seeked for by the AI to improve its predictive power. This is a significant advantage over the axiomatic relations proposed by Judea Pearl. Pearl's approach is fundamentally limited, as it cannot learn from correlation alone, but only obtain new probability spaces with a graph of already-given causal relations. This limitation is not present in the cognitive schematic approach, which makes it a more general adaptive learning model better-suited for autonomous agents. Additionally, the use of the NAL frequency and confidence values to represent hypothesis truth value enables efficient revision of the agent's knowledge in real-time. Unlike the probabilistic approach, this method can function effectively even with small sample sizes, can handle novel events (unknown unknowns) and has a low computational cost since only local memory updates are necessary.

## Architecture

![image](https://github.com/patham9/NACE/assets/8284677/2911ac01-d73a-45cd-a8ce-aa2333e35435)

## Demonstration scenarios

- Learning to collect salad from scratch: [World1](http://91.203.212.130/NACE/world1.gif)
- Learning how to put the cup on the table, in this case the goal is known to the agent: [World2](http://91.203.212.130/NACE/world2.gif)
- Learning to collect batteries and to pick up keys in order to make it through doors: [World3](http://91.203.212.130/NACE/world3.gif)
- Learning to collect salad with a moving cat as disturbance: [World4](http://91.203.212.130/NACE/world4.gif)
- Learning to play Pong in the grid world: [World5](http://91.203.212.130/NACE/world5.gif)
- Learning to bring eggs to the chicken: [World6](http://91.203.212.130/NACE/world6.gif)
- Learning to play soccer: [World7](http://91.203.212.130/NACE/world7.gif)
- Learning to collect salad while avoiding to get shocked by electric fences [World8](http://91.203.212.130/NACE/world8.gif)

## Related works:

[Autonomous Intelligent Reinforcement Interpreted Symbolism (AIRIS)](https://github.com/berickcook/AIRIS_Public)

[OpenNARS for Applications (ONA)](https://github.com/opennars/OpenNARS-for-Applications/)

[Rational OpenCog Controlled Agent (ROCCA)](https://github.com/opencog/rocca)
