import os
from fastmcp import FastMCP
import numpy as np
import matplotlib.pyplot as plt

# Import the existing skeletonization function from skeletonization.py
from skeletonization import skeletonize_mask

# Initialize the MCP server
mcp = FastMCP("CT Segmentation")


@mcp.tool()
def segment_ct_dataset(input_filepath: str, output_filepath: str, threshold: float) -> str:
    """
    Segments a 3D CT dataset based on a given density threshold value[span_3](start_span)[span_3](end_span)[span_4](start_span)[span_4](end_span).
    
    Args:
        input_filepath: Path to the input .npy file containing the 3D CT scan data[span_5](start_span)[span_5](end_span)[span_6](start_span)[span_6](end_span).
        output_filepath: Path indicating where the segmented .npy file should be saved[span_7](start_span)[span_7](end_span)[span_8](start_span)[span_8](end_span).
        threshold: The density value to use as a threshold. Voxels >= threshold will be set to 1, others to 0[span_9](start_span)[span_9](end_span)[span_10](start_span)[span_10](end_span).
    
    Returns:
        A status message indicating success and the save location, or an error message[span_11](start_span)[span_11](end_span)[span_12](start_span)[span_12](end_span).
    """
    try:
        if not os.path.exists(input_filepath):
            return f"Error: Input file not found at '{input_filepath}'."

        data = np.load(input_filepath)
        mask = (data >= threshold).astype(np.uint8)

        os.makedirs(os.path.dirname(os.path.abspath(output_filepath)), exist_ok=True)
        np.save(output_filepath, mask)

        fg_count = int(np.sum(mask))
        total_voxels = mask.size

        return (f"Successfully segmented CT dataset. Saved to '{output_filepath}'. "
                f"Foreground voxels: {fg_count}/{total_voxels} ({fg_count/total_voxels:.2%}).")

    except Exception as e:
        return f"Error segmenting dataset: {str(e)}"


@mcp.tool()
def visualize_slice(input_filepath: str, output_filepath: str, slice_index: int, axis: int = 0) -> str:
    """
    Loads a 3D CT dataset from a .npy file and saves a visualization of a specific slice to an image file[span_13](start_span)[span_13](end_span)[span_14](start_span)[span_14](end_span).
    
    Args:
        input_filepath: Path to the input .npy file containing the 3D CT data[span_15](start_span)[span_15](end_span)[span_16](start_span)[span_16](end_span).
        output_filepath: Path indicating where the output image should be saved (e.g., .png)[span_17](start_span)[span_17](end_span)[span_18](start_span)[span_18](end_span).
        slice_index: The index of the slice to visualize[span_19](start_span)[span_19](end_span)[span_20](start_span)[span_20](end_span).
        axis: The axis along which to take the slice (0, 1, or 2). Default is 0[span_21](start_span)[span_21](end_span)[span_22](start_span)[span_22](end_span).
        
    Returns:
        A status message indicating success and the save location, or an error message[span_23](start_span)[span_23](end_span)[span_24](start_span)[span_24](end_span).
    """
    try:
        if not os.path.exists(input_filepath):
            return f"Error: Input file not found at '{input_filepath}'."

        if axis not in (0, 1, 2):
            return f"Error: Invalid axis {axis}. Must be 0, 1, or 2."

        data = np.load(input_filepath)

        max_index = data.shape[axis] - 1
        if slice_index < 0 or slice_index > max_index:
            return f"Error: slice_index {slice_index} is out of bounds for axis {axis} (valid range: 0 to {max_index})."

        if axis == 0:
            slice_data = data[slice_index, :, :]
        elif axis == 1:
            slice_data = data[:, slice_index, :]
        else:
            slice_data = data[:, :, slice_index]

        os.makedirs(os.path.dirname(os.path.abspath(output_filepath)), exist_ok=True)

        plt.figure(figsize=(6, 6))
        plt.imshow(slice_data, cmap="gray")
        plt.title(f"Slice {slice_index} (Axis {axis})")
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(output_filepath, dpi=150)
        plt.close()

        return f"Successfully saved slice visualization to '{output_filepath}'."

    except Exception as e:
        return f"Error visualizing slice: {str(e)}"


@mcp.tool()
def skeletonize(input_filepath: str, output_filepath: str) -> str:
    """
    Creates a skeleton from a 3D segmentation mask[span_25](start_span)[span_25](end_span)[span_26](start_span)[span_26](end_span).
    
    Args:
        input_filepath: Path to the .npy file containing the 3D mask[span_27](start_span)[span_27](end_span)[span_28](start_span)[span_28](end_span).
        output_filepath: Path to save the extracted skeleton (.npy)[span_29](start_span)[span_29](end_span)[span_30](start_span)[span_30](end_span).
        
    Returns:
        A status message indicating success and the save location, or an error message[span_31](start_span)[span_31](end_span)[span_32](start_span)[span_32](end_span).
    """
    try:
        if not os.path.exists(input_filepath):
            return f"Error: Input file not found at '{input_filepath}'."

        # Ensure the destination folder exists before saving
        os.makedirs(os.path.dirname(os.path.abspath(output_filepath)), exist_ok=True)

        # Call the existing skeletonize_mask function internally
        skeleton = skeletonize_mask(file_path=input_filepath, output_path=output_filepath)

        if skeleton is None:
            return f"Error: Skeletonization returned no result."

        nonzero_count = int(np.count_nonzero(skeleton))

        return f"Successfully extracted skeleton and saved to '{output_filepath}'. Total skeleton voxels: {nonzero_count}."

    except Exception as e:
        return f"Error running skeletonize: {str(e)}"


if __name__ == "__main__":
    mcp.run()