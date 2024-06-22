import pandas as pd
import os  # Import the os module

def read_lst(lst_filepath):
    # Initialize a list to hold the data
    data = []
    # Open the file and process each line
    with open(lst_filepath, 'r') as file:
        # Skip the first two lines of the file
        next(file)
        next(file)
        for line in file:
            # Check if line begins with 6 spaces (indicating it might not contain a valid address)
            if line.startswith('      '):
                # print("Filtered line:", line.strip())
                continue  # Skip this line and don't add it to the DataFrame
            
            # Extract the hexadecimal address and the text from each line,
            # and convert the address to an integer
            address = int(line[:6], 16)
            text = line[32:].strip()  # Adjusted starting point for the text field
            # Add the extracted data to the list
            data.append({"address": address, "text": text})

    # Create a DataFrame from the list, with address already converted to integer
    return pd.DataFrame(data, columns=["address", "text"])


if __name__ == "__main__":
    lst_filepath = "tgt/temp.lst"

    df = read_lst(lst_filepath)

    # Calculate MAX_ADDRESS by converting the last row's address to an integer
    MAX_ADDRESS = df.iloc[-1]['address']
    
    # Adjust the filtering condition to include ".org" and "org"
    filtered_df = df[df['text'].str.startswith(("Combined file ", "Included from: ", ".org ", "org "))]

    # Adjust the file_type assignment to handle the new 'org' type
    filtered_df['file_type'] = filtered_df['text'].apply(
        lambda x: "cmb" if x.startswith("Combined file ") else
                "org" if x.startswith((".org", "org ")) else "inc"
        )

    # Extract filename and store it in a new field
    filtered_df['filename'] = filtered_df['text'].str.replace("Combined file ", "").str.replace("Included from: ", "")
    
    # Use os.path.basename to extract just the base filename
    filtered_df['filename'] = filtered_df['filename'].apply(os.path.basename)

    # Remove the 'text' field
    filtered_df.drop(columns=['text'], inplace=True)

    # Rename 'address' column to 'start_addr'
    filtered_df.rename(columns={'address': 'start_addr'}, inplace=True)
    # Initially set 'end_addr' to the same as 'start_addr' as a placeholder
    filtered_df['end_addr'] = filtered_df['start_addr']

    # Reset index to ensure it's continuous and starts from 0
    filtered_df.reset_index(drop=True, inplace=True)

    # Reorder the columns so that addresses are together
    filtered_df = filtered_df[['start_addr', 'end_addr', 'file_type', 'filename']]

    # 0th Pass: Calculate end address for each record
    for i in range(len(filtered_df) - 1):
        # Check if the next record's start_addr is different from the current record's start_addr
        if filtered_df.at[i, 'start_addr'] != filtered_df.at[i + 1, 'start_addr']:
            filtered_df.at[i, 'end_addr'] = filtered_df.at[i + 1, 'start_addr'] - 1
        # If the start_addr is the same, the end_addr adjustment is skipped

    # Ensure the last record has an appropriate end address.
    filtered_df.at[len(filtered_df) - 1, 'end_addr'] = MAX_ADDRESS

    # First Pass: Adjust addresses based on 'org' records, focusing on updating the previous record's start address
    for i, row in filtered_df.iterrows():
        if row['file_type'] == 'org':
            # Parse the new address from the 'filename' field
            new_org_addr = int(row['filename'].split()[-1].replace('0x', '').replace('$', '').replace('h', ''), 16)
            # Set org_addr to the new address
            if i > 0:
                # Update the previous record's start address to match the new org address
                filtered_df.at[i - 1, 'start_addr'] = new_org_addr
            # Note: No need to update end_addr here as it was pre-calculated in the 0th pass

    # Proceed to remove 'org' records since their adjustments are now reflected in the start addresses of subsequent records
    filtered_df = filtered_df[filtered_df['file_type'] != 'org'].reset_index(drop=True)

    # Optionally, reset the index again if needed for further processing
    filtered_df.reset_index(drop=True, inplace=True)

    # print(filtered_df)
    # quit()


    # Organizing data based on cmb and inc file types
    organized_data = []

    cmb = None  # Track the current 'cmb' file name
    for index, row in filtered_df.iterrows():
        if row['file_type'] == 'cmb':
            cmb = row['filename']  # Update cmb on encountering a cmb record
        elif row['file_type'] == 'inc' and cmb is not None:
            # For inc records, append the data including the current cmb name
            organized_data.append({'start_addr': row['start_addr'], 'end_addr': row['end_addr'], 'cmb': cmb, 'inc': row['filename']})

    # Create a new DataFrame from the organized data
    organized_df = pd.DataFrame(organized_data, columns=['start_addr', 'end_addr', 'cmb', 'inc'])

    # Calculate byte size for each entry
    organized_df['byte_size'] = organized_df['end_addr'] - organized_df['start_addr'] + 1

    # Aggregating data to calculate totals
    inc_totals = organized_df.groupby('inc')['byte_size'].sum()  # Sum bytes by 'inc'
    cmb_subtotals = organized_df.groupby('cmb')['byte_size'].sum()  # Subtotal by 'cmb'
    grand_total = organized_df['byte_size'].sum()  # Grand total

    # Print results
    print(inc_totals)
    print(cmb_subtotals)
    print(f"Grand Total: {grand_total} bytes")
