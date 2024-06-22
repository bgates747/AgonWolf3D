import pandas as pd

# Create the wide format bit_table
bit_table = {
    "7": [8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128],
    "6": [7, 15, 23, 31, 39, 47, 55, 63, 71, 79, 87, 95, 103, 111, 119, 127],
    "5": [6, 14, 22, 30, 38, 46, 54, 62, 70, 78, 86, 94, 102, 110, 118, 126],
    "4": [5, 13, 21, 29, 37, 45, 53, 61, 69, 77, 85, 93, 101, 109, 117, 125],
    "3": [4, 12, 20, 28, 36, 44, 52, 60, 68, 76, 84, 92, 100, 108, 116, 124],
    "2": [3, 11, 19, 27, 35, 43, 51, 59, 67, 75, 83, 91, 99, 107, 115, 123],
    "1": [2, 10, 18, 26, 34, 42, 50, 58, 66, 74, 82, 90, 98, 106, 114, 122],
    "0": [1, 9, 17, 25, 33, 41, 49, 57, 65, 73, 81, 89, 97, 105, 113, 121]
}
df_wide = pd.DataFrame(bit_table)

# Convert the wide dataframe to long format
df_long = df_wide.reset_index().melt(id_vars="index", var_name="bit", value_name="const")
df_long = df_long.rename(columns={"index": "offset"})
df_long.sort_values(by=["offset", "bit"], inplace=True)
df_long.reset_index(drop=True, inplace=True)

# Sample data for new DataFrame
keycodes = {
    'label': ['Shift', 'Ctrl', 'Alt', 'LeftShift', 'LeftCtrl', 'LeftAlt', 'RightShift', 'RightCtrl', 'RightAlt', 'MouseSelect', 'MouseMenu', 'MouseAdjust', 'Q', 'Num3', 'Num4', 'Num5', 'F4', 'Num8', 'F7', 'Minus', 'Hat', 'Left', 'Keypad6', 'Keypad7', 'F11', 'F12', 'F10', 'ScrollLock', 'F0', 'W', 'E', 'T', 'Num7', 'I', 'Num9', 'Num0', 'Underscore', 'Down', 'Keypad8', 'Keypad9', 'Break', 'Tilde', 'Backspace', 'Num1', 'Num2', 'D', 'R', 'Num6', 'U', 'O', 'P', 'LeftBracket', 'Up', 'KeypadPlus', 'KeypadMinus', 'KeypadEnter', 'Insert', 'Home', 'PgUp', 'Caps', 'A', 'X', 'F', 'Y', 'J', 'K', 'At', 'Colon', 'Return', 'KeypadFwdSlash', 'KeypadDel', 'KeypadDot', 'NumLock', 'PgDn', 'ShiftLock', 'S', 'C', 'G', 'H', 'N', 'L', 'Semicolon', 'RightBracket', 'Delete', 'KeypadStar', 'KeypadComma', 'KeypadPlus', 'Underscore1', 'TAB', 'Z', 'Space', 'V', 'B', 'M', 'Comma', 'Dot', 'ForwardSlash', 'CopyEnd', 'Keypad0', 'Keypad1', 'Keypad3', 'Escape', 'F1', 'F2', 'F3', 'F5', 'F6', 'F8', 'F9', 'Right', 'Keypad4', 'Keypad5', 'Keypad2', 'WinLeft', 'WinRight', 'WinMenu'],
    "const": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 92, 93, 94, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 113, 114, 115, 116, 117, 118, 119, 120, 122, 123, 124, 125, 126, 127, 128]
}

df_keys = pd.DataFrame(keycodes)

df_merged = df_long.merge(df_keys, left_on="const", right_on="const", how="inner")

assembly_code_full = "\n".join(
    f"; {row['const']} {row['label']}\n    bit {row['bit']},(ix+{row['offset']})\n    jr z,@{row['label']}\n@{row['label']}:" 
    for index, row in df_merged.iterrows()
)

# Define the output file path
asm_file_out = 'src/asm/keys.inc'

# Write the generated assembly code to the file
with open(asm_file_out, "w") as file:
    file.write(assembly_code_full)


# df_merged.to_csv(asm_file_out, sep='\t', index=False)