This is a foundational question that touches on the core architecture of Artificial Intelligence and Statistics. You are asking for a "Grand Unified Theory" of how we estimate relationships between variables when some are hidden, some are proxies, and some are targets.

To capture "everything"—from Maximum Likelihood to Non-Parametrics, from Deep Learning to Graphs—we must categorize these methods not by algorithm, but by their **Fundamental Paradigm**: how they mathematically view reality and uncertainty.

Here are the **Six General Paradigms** for estimating $P(Y, X, Z)$ and $P(Y|X, Z)$ under uncertainty.

---

### 1. The Probabilistic Graphical Model (PGM) Paradigm
**"Structure is Knowledge"**

This paradigm does not see a "black box"; it sees a web of dependencies. It breaks the massive joint distribution $P(Y, X, Z)$ into smaller, local conditional probabilities based on a graph structure.

* **The Model:** You define a graph $G = (V, E)$.
    * **Directed (Bayesian Networks):** Good for causal logical flows (e.g., $X \to Z$, $X \to Y$).
        $$P(Y, X, Z) = P(Z|X)P(Y|X)P(X)$$
    * **Undirected (Markov Random Fields):** Good when direction is unclear but correlation is strong (e.g., pixels in an image, social networks).
        $$P(Y, X, Z) = \frac{1}{Z_{norm}} \prod \phi_c(Y, X, Z)$$
* **Handling Proxies & Missing $X$:**
    * This is the strongest paradigm for this. You explicitly treat $X$ as a **Latent Node**.
    * **Inference:** You use algorithms like **Variable Elimination** or **Belief Propagation** to mathematically sum out the missing $X$ to get the marginals you need ($P(Y|Z)$).
* **Key Algorithms:** Junction Tree Algorithm, Belief Propagation.

### 2. The Frequentist Latent Variable Paradigm (Maximum Likelihood)
**"Optimization of Parameters"**

This paradigm assumes there is a single "true" fixed set of parameters $\theta$ that describes the world. The goal is to find the $\theta$ that makes your observed data $(Y, Z)$ most probable, marginalizing over the missing $X$.

* **The Model:** You assume a parametric form (e.g., Gaussians).
    $$\theta_{MLE} = \arg \max_{\theta} \log P(Y, Z | \theta) = \arg \max_{\theta} \log \int P(Y, Z, X | \theta) dX$$
* **Handling Proxies & Missing $X$:**
    * Since you cannot observe $X$, you cannot just maximize the likelihood directly. You use the **EM Algorithm (Expectation-Maximization)**.
    * **E-Step:** Guess the missing $X$ (calculate its expected value given current parameters).
    * **M-Step:** Update parameters to maximize likelihood assuming the guess was right.
* **Key Algorithms:** EM Algorithm, Factor Analysis, Structural Equation Modeling (SEM).

### 3. The Bayesian Paradigm
**"Uncertainty Propagation"**

Unlike the Frequentist view, this paradigm assumes parameters $\theta$ and latent variables $X$ are random variables. It doesn't give you a point estimate; it gives you a distribution of beliefs.

* **The Model:**
    $$P(X, \theta | Y, Z) = \frac{P(Y, Z | X, \theta)P(X | \theta)P(\theta)}{P(Y, Z)}$$
* **Handling Proxies & Missing $X$:**
    * It treats missing data exactly the same as parameters. $X$ is just another unknown to be sampled.
    * The "Measurement Error" of the proxy $Z$ ($Z \sim N(X, \sigma)$) is integrated into the model, automatically widening the confidence intervals of your prediction $Y$.
* **Key Algorithms:** MCMC (Gibbs Sampling, Hamiltonian Monte Carlo), Variational Inference. 

### 4. The Deep Generative Paradigm (Manifold Learning)
**"Function Approximation of the Distribution"**

This is the modern "Deep Learning" approach to joint distributions. Instead of assuming simple Gaussian shapes (like in Frequentist methods), we use Neural Networks to learn the complex, non-linear shape of the data manifold.

* **The Model:** We learn a mapping from a simple latent distribution (like noise) to our complex data $(Y, X, Z)$.
    * **VAEs (Variational Autoencoders):** Learn an encoder $Q(X|Y,Z)$ and decoder $P(Y,Z|X)$ simultaneously. They maximize a lower bound on the data likelihood (ELBO).
    * **Normalizing Flows:** Learn an invertible chain of transformations that maps simple noise directly to the complex joint density $P(Y, X, Z)$.
* **Handling Proxies & Missing $X$:**
    * Deep Generative Models are excellent at "hallucinating" plausible values for missing $X$ that are consistent with $Y$ and $Z$ because they learn the high-dimensional correlations.
* **Key Algorithms:** VAEs, GANs, Normalizing Flows, Energy-Based Models (EBMs).

### 5. The Discriminative Machine Learning Paradigm
**"Direct Mapping"**

This paradigm ignores the joint distribution $P(Y, X, Z)$. It focuses *only* on the conditional target $P(Y | \text{Input})$. It is pragmatic: "I don't care how the data was generated; I just want to predict Y."

* **The Model:** Minimize a loss function $L(Y, f(\text{Input}))$.
* **Handling Proxies & Missing $X$:**
    * **Scenario A (Training):** If you have $X$ during training, you train $f(X, Z) \to Y$.
    * **Scenario B (Deployment):** If $X$ is missing at test time, this paradigm struggles. You typically have to:
        * Train a separate "imputer" model $g(Z) \to \hat{X}$, then feed $\hat{X}$ into $f$.
        * Or, simply train a weaker model $f(Z) \to Y$ that ignores $X$ entirely, treating $Z$ as a noisy feature.
* **Key Algorithms:** Gradient Boosting (XGBoost), Deep Neural Networks (ResNets, Transformers), SVMs.

### 6. The Non-Parametric Paradigm
**"Let the Data Speak"**

This paradigm refuses to assume a formula (like "it's a line" or "it's a bell curve"). The "model" is the data itself.

* **The Model:**
    * **Kernel Density Estimation (KDE):** Place a small "bump" (kernel) on every data point you have. The sum of these bumps is your estimated Probability Density Function (PDF).
    * **Gaussian Processes (GP):** Define a "similarity" function (kernel). If inputs are similar, outputs should be similar.
* **Handling Proxies & Missing $X$:**
    * **GP-LVM (Gaussian Process Latent Variable Models):** A powerful technique where you assume the observed $Y$ and $Z$ are generated by a Gaussian Process mapping from an unknown, lower-dimensional $X$. You optimize to find the "best" latent $X$ coordinates that explain the data.
* **Key Algorithms:** KDE, Gaussian Processes, k-Nearest Neighbors.

---

### Summary Comparison Table

| Paradigm | Philosophy | Best For | How it handles "X is missing" |
| :--- | :--- | :--- | :--- |
| **1. PGM (Graphs)** | Relationships are structured (Causal/Logical). | Interpretable systems, domain knowledge integration. | Mathematical Marginalization (Summing out). |
| **2. Frequentist (MLE/EM)** | Optimization of fixed parameters. | Standard statistical modeling, clustering. | EM Algorithm (Iterative guessing). |
| **3. Bayesian** | Parameters are distributions; uncertainty is key. | Small data, high risk, rigorous proxy handling. | Sampling (MCMC) - treats X as a parameter. |
| **4. Deep Generative** | The distribution is a complex manifold. | Images, Audio, High-Dimensional complex data. | Learning a latent space that represents X. |
| **5. Discriminative ML** | Minimize prediction error directly. | Pure prediction accuracy when X is known. | Struggles; requires imputation or feature dropping. |
| **6. Non-Parametric** | The data *is* the model. | Unknown, weirdly shaped distributions. | GP-LVM (Inferring latent coordinates). |