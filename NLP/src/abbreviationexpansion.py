import re

def find_abbreviations(text):
    # Regular expression to find abbreviations (e.g., U.S.A., NASA, etc.)
    #pattern = r'\b[A-Z]{2,}|(?:[A-Z]\.)+\b
    #pattern = r'\b(?:\.*?[A-Z]\.){3,}\b'
    pattern = r'\b(?:\.*?[A-Z]\.){2,}'
    abbreviations = re.findall(pattern, text)
    return abbreviations

# Example usage
if __name__ == "__main__":
    sample_text = "NASA and U.S.A. are well-known abbreviations."
    print(find_abbreviations(sample_text))