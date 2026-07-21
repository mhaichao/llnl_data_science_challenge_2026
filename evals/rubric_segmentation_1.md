### Input:
* a ground truth png
* a result png

### Analysis:
Comapre the two images at the same scale. Compatr both images as black and white. Ignore any text and scales. Allow a 10% threshold in slight pixel differences.

#### Criteria:
1. **Structural Integrity**: Does the result capture the connectivity of the lattice struts compared to the ground truth?
2. **False Positives/Negatives**: Identify over-segmentation (extra noise) or under-segmentation (missing struts).
3. **Topology**: Are the nodes (junctions) preserved?
4. **Noise and Artifacts**: Does the result image contain noise or artifacts not present in the clean ground truth?

#### Scoring (0-5):
* 5: Identical to ground truth. No missing structures, no false positives.
* 4: Excellent with very minor differences.
* 3: Main topology is correct, but noticeable noise or thin struts are missing.
* 2: Fair, but with significant differences (e.g., large chunks missing).
* 1: Major structural failure or excessive noise.
* 0: Blank or unrelated output.

#### Output:
Return a JSON block with "reasoning" and "score".