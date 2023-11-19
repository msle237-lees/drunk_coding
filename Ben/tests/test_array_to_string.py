import numpy as np

def array_to_csv_string(arr):
    """
    Convert a numpy array to a comma-separated string.

    Parameters:
    arr (np.ndarray): The numpy array to be converted.

    Returns:
    str: Comma-separated string representation of the numpy array.
    """
    # Flatten the array to a 1D array for simplicity
    flat_arr = arr.flatten()

    # Convert each element to a string and join with commas
    return ','.join(map(str, flat_arr))

# Example usage:
my_array = np.array([[1, 2, 3], [4, 5, 6]])
print(array_to_csv_string(my_array))
