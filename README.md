# FBFE - Fast Boolean Function Enumerator

A novel implementation of a boolean function enumerator, that is faster than any known alternative. The algorithm works best for 'bushier' trees, meaning trees that resemble k-nary trees the most. At best the complexity of the algorithm is $O(log(m) \cdot 2^n)$ and at worst it is $O(m \cdot 2^n)$, where $n$ is the number of variables in the function and $m$ is the number of gates. Normal enumerators have a complexity of $O(m \cdot 2^n)$.

# The algorithm
The main idea of the algorithm is to leverage the fact that we are enumerating a function, and the fact that usually the function tree changes very little if we do the evaluation in a certain order. In the implementation I use the Gray code for determining the order of the enumeration. The Gray code is a sequence of binary numbers of length $n$ where each number differs in exactly one digit from the previous one. This property is important for the algorithm, as it allows it not to recalculate big chunks of the tree with every different input.

We start iterating through the algorithm. For the first code which is always when all variables are 0, we do nothing. In the second iteration, when a single bit is changed, we flip it in the equation tree and we start a procedure called upward propagation. The upward propagation essentially uses the chain of parents of each node to update the entire equation, rather than updating the entire equation.

During upward propagation, if the current bit is $1$, we add 1 to a counter in the parent called $trueChildren$, which represents the number of children nodes with value $1$. Similarly, we subtract $1$ if the node is 0. From this we can compute the value of the gate: if $trueChildren$ equals the number of children for an $AND$ gate it is true and if it is greater than 0 for an $OR$ gate, then it is true. We check if the value of the parent changes as a result of the changes in the counter. If it does, we continue the same process on the parent, otherwise we stop. The value of the root node of the equation, will be the result.

# Complexity

A more thorough complexity analysis is required, but it seems that at best the complexity of the algorithm is $O(log(m) \cdot 2^n)$ and at worst it is $O(m \cdot 2^n)$ . The complexity approaches $O(log(m) \cdot 2^n)$ for trees that are more 'complete'. It appears that the complexity is proportional to the metric: $\frac{|G|}{|V|}$, where $|G|$ is the gate count and $|V|$ is the vertex count. We will call this metric the **dispersion** of the function tree. It would probably be useful to do some analysis on different instances of this metrics, to see if the relationship is linear or if it much better. 

The intuition behind this metric is that the more gates there are in the tree relative to the number of events, the more you can avoid recomputing similar paths in the tree (assuming we are not allowing gates which only have a single child).

For example, consider the case of an equation with a single gate and a very large number of children. In this case the dispersion would be approaching $0$, when the number of children becomes very big. In the optimized version and the original version of the function enumeration one gate will have to be evaluated.

If we consider the case where we only use two values for the function and have a gate per depth level, the complexity of the function would be $O((m/2) \cdot 2^n)$. If we generalize the formula, for any Boolean function, then we have $O(avg_d \cdot 2^n)$, where $avg_d$ is the sum of all the depth of all variables divided by the number of all variables.