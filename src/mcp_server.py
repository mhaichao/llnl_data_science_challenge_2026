from contextlib import redirect_stdout
from pathlib import Path
import sys

import matplotlib
import numpy as np
from fastmcp import FastMCP

try:
    from .skeletonization import skeletonize_mask
except ImportError:
    from skeletonization import skeletonize_mask


# MCP servers may run without a display, so use Matplotlib's non-interactive
# backend before importing pyplot.
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Initialize the MCP server
mcp = FastMCP("CT Segmentation")


def _input_npy_path(filepath: str) -> Path:
    """Resolve and validate an input NumPy volume path."""
    path = Path(filepath).expanduser().resolve()
    if path.suffix.lower() != ".npy":
        raise ValueError(f"Input file must use the .npy extension: {path}")
    if not path.is_file():
        raise FileNotFoundError(f"Input file does not exist: {path}")
    return path


def _output_path(filepath: str, expected_suffix: str | None = None) -> Path:
    """Resolve an output path and create its parent directory."""
    path = Path(filepath).expanduser().resolve()
    if expected_suffix and path.suffix.lower() != expected_suffix:
        raise ValueError(
            f"Output file must use the {expected_suffix} extension: {path}"
        )
    if path.exists() and path.is_dir():
        raise IsADirectoryError(f"Output path is a directory: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _load_3d_array(filepath: str) -> tuple[Path, np.ndarray]:
    """Load a three-dimensional array without permitting pickled objects."""
    path = _input_npy_path(filepath)
    array = np.load(path, allow_pickle=False)
    if array.ndim != 3:
        raise ValueError(
            f"Expected a 3D array, but {path} has shape {array.shape}."
        )
    return path, array


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
        input_path, volume = _load_3d_array(input_filepath)
        if not np.isfinite(threshold):
            raise ValueError("Threshold must be a finite number.")

        output_path = _output_path(output_filepath, ".npy")
        segmented = (volume >= threshold).astype(np.uint8)
        np.save(output_path, segmented, allow_pickle=False)

        foreground_voxels = int(np.count_nonzero(segmented))
        return (
            f"Segmented {input_path} at threshold {threshold}. "
            f"Saved {foreground_voxels} foreground voxels out of "
            f"{segmented.size} total voxels to {output_path}."
        )
    except Exception as exc:
        return f"Error segmenting CT dataset: {exc}"


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
    figure = None
    try:
        input_path, volume = _load_3d_array(input_filepath)
        if axis not in (0, 1, 2):
            raise ValueError(f"Axis must be 0, 1, or 2; received {axis}.")
        if not 0 <= slice_index < volume.shape[axis]:
            raise IndexError(
                f"Slice index {slice_index} is outside axis {axis}, which has "
                f"valid indices 0 through {volume.shape[axis] - 1}."
            )

        output_path = _output_path(output_filepath)
        image = np.take(volume, slice_index, axis=axis)

        figure, axes = plt.subplots(figsize=(8, 8))
        axes.imshow(image, cmap="gray")
        axes.set_title(f"{input_path.name}: axis {axis}, slice {slice_index}")
        axes.axis("off")
        figure.tight_layout()
        figure.savefig(output_path, dpi=150, bbox_inches="tight")

        return (
            f"Saved axis {axis}, slice {slice_index} from {input_path} "
            f"to {output_path}."
        )
    except Exception as exc:
        return f"Error visualizing CT slice: {exc}"
    finally:
        if figure is not None:
            plt.close(figure)


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
    try:
        input_path = _input_npy_path(input_filepath)
        mask = np.load(input_path, mmap_mode="r", allow_pickle=False)
        if mask.ndim != 3:
            raise ValueError(
                f"Expected a 3D mask, but {input_path} has shape {mask.shape}."
            )

        output_path = _output_path(output_filepath, ".npy")

        # skeletonize_mask reports progress with print(). Redirect that output to
        # stderr so it cannot interfere with MCP's JSON-RPC messages on stdout.
        with redirect_stdout(sys.stderr):
            skeleton = skeletonize_mask(str(input_path), str(output_path))

        if skeleton is None or not output_path.is_file():
            raise RuntimeError("Skeletonization did not produce an output file.")

        skeleton_voxels = int(np.count_nonzero(skeleton))
        return (
            f"Skeletonized {input_path}. Saved {skeleton_voxels} skeleton "
            f"voxels to {output_path}."
        )
    except Exception as exc:
        return f"Error skeletonizing segmentation mask: {exc}"


if __name__ == "__main__":
    # Run the FastMCP server, exposing the tools over standard I/O (default)
    mcp.run()
