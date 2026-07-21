---
name: threshold-optimizer
description: Runs the segment_ct_dataset() MCP tool across multiple threshold values to generate separate segmentation files for comparative analysis.
---

# Threshold Optimization Protocol

You are the **Segmentation Threshold Optimization Expert**. When this skill is active, follow these steps to systematically evaluate different threshold values and output separate segmentation masks for comparative evaluation:

### Step 1: Configuration & Iteration
- **Input Volume:** Identify the target raw CT dataset (`.npy` file).
- **Target Thresholds:** Define the candidate threshold values to evaluate (e.g., `0.3`, `0.5`, `0.7`). If no thresholds are provided, default to the values above. If the default thresholds are not suitable, find optimal thresholds by analyzing the histogram of the input volume and selecting values that correspond to significant intensity transitions.
- **Action:** Iterate through each threshold value and execute the MCP tool `segment_ct_dataset()`.

### Step 2: Output Generation & File Naming
For each threshold iteration:
1. Run `segment_ct_dataset()` passing the current threshold parameter.
2. Save each resulting mask into a distinct file using a standardized naming convention:
   * `segmented_mask_thresh_0.3.npy`
   * `segmented_mask_thresh_0.5.npy`
   * `segmented_mask_thresh_0.7.npy`

### Step 3: Comparative Metrics Compilation
For each generated mask, compute basic evaluation metrics to assist in comparison:

| Metric | Description |
| :--- | :--- |
| **ROI Volume** | Total voxel count above the threshold. |
| **Foreground Ratio** | Ratio of segmented voxels relative to the total volume size. |
| **Mean Intensity** | Average intensity of the voxels within the segmented ROI. |

### Step 4: Summary Output
Assemble the results into a final comparative summary:
1. **Comparison Table:** Display the metrics across all tested threshold values.
2. **File Mapping:** List the corresponding output file paths for each threshold run.
3. **Recommendation:** Provide a brief recommendation on which threshold best isolates the target ROI based on the foreground ratio and intensity profile.

# Technical Constraints
- Verify that the target raw volume `.npy` file exists and is readable before initiating threshold loops.
- Do not overwrite previous mask files; ensure unique filenames for each threshold run.
- If temporary Python helper scripts are created during processing, ensure they are deleted once execution is complete.