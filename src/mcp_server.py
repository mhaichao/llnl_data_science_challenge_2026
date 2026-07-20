from fastmcp import FastMCP
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
# Initialize the MCP server
mcp = FastMCP("CT Segmentation")

@mcp.tool()
def segment_ct_dataset(input_filepath: str, output_filepath: str, threshold: float) -> str:
    """
    Segments a 3D CT dataset based on a given density threshold value.
    
    Args:
        input_filepath: Path to the input .npy file containing the 3D CT scan data.
        output_filepath: Path indicating where the segmented .npy file should be saved.
        threshold: The density value to use as a threshold. Voxels >= threshold will be set to 1, others to 0.
    
    Returns:
        A status message indicating success and the save location, or an error message.
    """
    try:
        input_path = Path(input_filepath)
        output_path = Path(output_filepath)

        if not input_path.exists():
            return f"Error: Input file does not exist: {input_path}"

        if input_path.suffix.lower() != ".npy":
            return "Error: The input file must be a .npy file."

        if not 0.0 <= threshold <= 1.0:
            return "Error: Threshold must be between 0 and 1."

        ct_data = np.load(input_path)

        if ct_data.ndim != 3:
            return (
                "Error: Expected a 3D CT dataset, "
                f"but received an array with shape {ct_data.shape}."
            )

        segmented_data = (ct_data >= threshold).astype(np.uint8)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        np.save(output_path, segmented_data)

        material_voxels = int(segmented_data.sum())
        total_voxels = int(segmented_data.size)
        material_percentage = material_voxels / total_voxels * 100

        return (
            "Segmentation completed successfully. "
            f"Input shape: {ct_data.shape}. "
            f"Threshold: {threshold}. "
            f"Material voxels: {material_voxels:,} "
            f"({material_percentage:.2f}%). "
            f"Saved result to: {output_path.resolve()}"
        )

    except Exception as error:
        return f"Error while segmenting the CT dataset: {error}"



@mcp.tool()
def visualize_slice(input_filepath: str, output_filepath: str, slice_index: int, axis: int = 0) -> str:
    """
    Loads a 3D CT dataset from a .npy file and saves a visualization of a specific slice to an image file.
    
    Args:
        input_filepath: Path to the input .npy file containing the 3D CT data.
        output_filepath: Path indicating where the output image should be saved (e.g., .png).
        slice_index: The index of the slice to visualize.
        axis: The axis along which to take the slice (0, 1, or 2). Default is 0.
        
    Returns:
        A status message indicating success and the save location, or an error message.
    """
    try:
        input_path = Path(input_filepath)
        output_path = Path(output_filepath)

        # Check that the input file exists.
        if not input_path.exists():
            return f"Error: Input file does not exist: {input_path}"

        # Make sure the input is a NumPy array file.
        if input_path.suffix.lower() != ".npy":
            return "Error: The input file must be a .npy file."

        # Make sure the output is an image format.
        valid_image_extensions = {".png", ".jpg", ".jpeg"}

        if output_path.suffix.lower() not in valid_image_extensions:
            return (
                "Error: The output file must use an image extension "
                "such as .png, .jpg, or .jpeg."
            )

        # Axis must be 0, 1, or 2 for a 3D array.
        if axis not in (0, 1, 2):
            return "Error: Axis must be 0, 1, or 2."

        ct_data = np.load(input_path)

        # Make sure the dataset is three-dimensional.
        if ct_data.ndim != 3:
            return (
                "Error: Expected a 3D CT dataset, "
                f"but received an array with shape {ct_data.shape}."
            )

        # Find how many slices exist along the chosen axis.
        number_of_slices = ct_data.shape[axis]

        # Validate the requested slice index.
        if slice_index < 0 or slice_index >= number_of_slices:
            return (
                f"Error: slice_index must be between 0 and "
                f"{number_of_slices - 1} for axis {axis}."
            )

        # Extract a 2D slice from the 3D array.
        if axis == 0:
            slice_data = ct_data[slice_index, :, :]
        elif axis == 1:
            slice_data = ct_data[:, slice_index, :]
        else:
            slice_data = ct_data[:, :, slice_index]

        # Create the output folder if it does not already exist.
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Create and save the visualization.
        plt.figure(figsize=(8, 8))
        plt.imshow(slice_data, cmap="gray")
        plt.title(f"CT Slice {slice_index} Along Axis {axis}")
        plt.xlabel("Voxel coordinate")
        plt.ylabel("Voxel coordinate")
        plt.colorbar(label="Voxel value")
        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()

        return (
            "Slice visualization completed successfully. "
            f"Input shape: {ct_data.shape}. "
            f"Axis: {axis}. "
            f"Slice index: {slice_index}. "
            f"Slice shape: {slice_data.shape}. "
            f"Saved image to: {output_path.resolve()}"
        )

    except Exception as error:
        return f"Error while visualizing the CT slice: {error}"

@mcp.tool()
def skeletonize(input_filepath: str, output_filepath: str) -> str:
    """
    Creates a skeleton from a 3D segmentation mask.
    
    Args:
        input_filepath: Path to the .npy file containing the 3D mask.
        output_filepath: Path to save the extracted skeleton (.npy).
        
    Returns:
        A status message indicating success and the save location, or an error message.
    """
    pass # Implementation goes here, calling skeletonize_mask internally

if __name__ == "__main__":
    # Run the FastMCP server, exposing the tools over standard I/O (default)
    mcp.run()
