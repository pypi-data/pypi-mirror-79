import os

def wrap_encoded_data(data: str) -> str:
    """Wrap encoded data in a self-extracting HTML file

    Args:
        data (str): Encoded data

    Returns:
        str: Output file
    """

    # Open the template and do an in-place replacement
    return open(os.path.join(os.path.dirname(__file__), "template.html"), "r").read().replace("{{encoded_data}}", data)
