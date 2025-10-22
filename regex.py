
import pandas as pd
import re

#creating file
data = {
    "full_address": [
        "House 81 Mansi Vihar Raj Nagar Extension Ghaziabad 201001",
        "Flat 22 Ashok Vihar Phase II Delhi 110052",
        "14/6 Vaishali Sector 5 Ghaziabad UP 201010",
        "B-203 Shakti Khand Indirapuram Ghaziabad",
        "9 Anand Vihar Noida Uttar Pradesh",
        "12 Krishna Nagar Meerut 250002"
    ]
}

df = pd.DataFrame(data)
df.to_excel("addresses.xlsx", index=False)
print("Demo Excel file created successfully!")




INPUT_FILE  = "addresses.xlsx"         # Input Excel file name
OUTPUT_FILE = "cleaned_addresses.xlsx" # Output file name
ADDRESS_COL = "full_address"           # Column name in your Excel file



# Clean state/city/pincode words
def clean_address(text):
    if pd.isna(text):
        return ""
    # Remove common city/state/pincode words
    text = re.sub(r'(?i)(india|uttar pradesh|up|delhi|ghaziabad|noida|gurgaon|faridabad|meerut|[0-9]{6})', '', text)
    text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)  # remove punctuation
    text = re.sub(r'\s+', ' ', text)  # collapse multiple spaces
    return text.strip()


# Extract sublocality and locality
def extract_locality(address):
    if not address:
        return None, None

    # Match common Indian address suffixes (extend if needed)
    pattern = r'([A-Za-z ]+(?:Vihar|Nagar|Colony|Extension|Extn|Sector|Phase|Enclave|Khand|Puram|Bagh|Garden|City|Heights|Residency|Avenue|Park))'

    matches = re.findall(pattern, address, flags=re.IGNORECASE)

    if len(matches) >= 2:
        return matches[0].strip(), matches[1].strip()
    elif len(matches) == 1:
        return matches[0].strip(), None
    else:
        return None, None


# Load Excel file
print("Reading Excel file...")
df = pd.read_excel(INPUT_FILE)

if ADDRESS_COL not in df.columns:
    raise KeyError(f"Column '{ADDRESS_COL}' not found in Excel. Please rename your address column to '{ADDRESS_COL}'.")

# Clean and extract
print("Cleaning and extracting locality info...")
df['cleaned_address'] = df[ADDRESS_COL].apply(clean_address)

# Apply the extraction function
df[['sublocality', 'locality']] = df['cleaned_address'].apply(
    lambda x: pd.Series(extract_locality(str(x)))
)

# Save to Excel
print("Saving results")
df.to_excel(OUTPUT_FILE, index=False)

print("Extracted data saved to:", OUTPUT_FILE)
