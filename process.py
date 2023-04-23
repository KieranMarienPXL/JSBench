import pandas as pd

# Load JSON data into a DataFrame
data = pd.read_json('2023-04-23-06-56-53.json')

# Calculate summary statistics
summary = pd.DataFrame({
    'max': data.max(),
    'min': data.min(),
    'mean': data.mean(),
    'median': data.median(),
    'std': data.std()
})

print(summary)

