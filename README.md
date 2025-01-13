# Advanced Workload Scheduling and Resource Management in Cloud Environments

This repository contains the implementation and results of the **Cloud Computing Architecture** (CCA) semester project conducted at **ETH Zurich** (Spring 2023). The project explores advanced concepts in cloud orchestration, scheduling, and resource management using Kubernetes, focusing on optimizing the performance of latency-sensitive and batch applications in a cloud environment.

### Authors
- [Antonino Orofino](https://github.com/antoorofino)
- [Lorenzo Paleari](https://github.com/LorenzoPaleari)
- [Julian Sainz Martinez](https://github.com/jellothere)

## Project Overview
The **Cloud Computing Architecture** project is divided into four parts, each focusing on specific aspects of cloud computing:

1. **Part 1**: Performance analysis of a latency-sensitive application (*memcached*) under various hardware resource interference scenarios using iBench.
2. **Part 2**: Resource interference profiling and parallel behavior analysis for batch workloads from the PARSEC benchmark suite.
3. **Part 3**: Co-scheduling *memcached* and batch workloads in a heterogeneous Kubernetes cluster while ensuring performance guarantees.
4. **Part 4**: Dynamic scheduling of workloads under varying load conditions to meet strict service level objectives (SLOs).

The project aims to balance resource allocation efficiency and performance while leveraging Kubernetes features like node affinity, resource requests, and limits.

For detailed results and analyses, refer to our reports [`Part 1 & 2`](./docs/CCA_Report_Parts_1_2.pdf) - [`Part 3 & 4`](./docs/CCA_Report_Parts_3_4.pdf).

### Key Features

- **Container Orchestration**:
  - Deploy and manage applications using Kubernetes.
  - Utilize advanced Kubernetes features like node affinity and resource limits.
- **Performance Analysis**:
  - Measure and analyze 95th percentile latency and saturation points.
  - Profile resource sensitivity for batch workloads.
- **Scheduling Optimization**:
  - Design and implement dynamic scheduling policies for mixed workloads.
  - Optimize resource allocation for multi-threaded applications.
- **Dyn
amic Load Handling**:
  - Develop controllers for adaptive resource management under varying workloads.

### Motivation
Efficient workload scheduling in cloud environments is essential for:  
- Guaranteeing performance for latency-critical applications.
- Optimizing resource usage for batch workloads.
- Reducing cloud operational costs.

This project provides practical insights into managing competing workloads in heterogeneous clusters, bridging theoretical concepts with real-world applications.

## Reproduction Steps

To replicate the experiments, follow these instructions:

1. **Part 1 and Part 2**:
   - Follow the instructions in the provided documentation to set up clusters and execute workloads.

2. **Part 3 and Part 4**:
   - Refer to the README files in the respective folders for implementation details and execution steps. [`Part 3 README`](./src/part3/README.md) - [`Part 4 README`](./src/part4/README.md).

## Results

### Highlights
- **Memcached Performance**:
  - Achieved 95th percentile latency < 1ms at 30K QPS.
  - Demonstrated impact of resource interference on tail latency.
- **Batch Workloads**:
  - Analyzed resource sensitivity and parallel scalability.
  - Optimized co-location strategies for minimal execution time.
- **Dynamic Scheduling**:
  - Developed a policy ensuring SLO compliance under dynamic loads.
  - Improved overall resource utilization and reduced batch completion time.

For detailed results, refer to the reports [`Part 1 & 2`](./docs/CCA_Report_Parts_1_2.pdf) - [`Part 3 & 4`](./docs/CCA_Report_Parts_3_4.pdf).
