import pandas as pd

df = pd.read_csv("job_offers.csv")

def make_clickable(link):
    return f'<a href="{link}" target="_blank">{link}</a>'

# Apply clickable formatting to the 'links' column
df['links'] = df['links'].apply(make_clickable)

# Display the DataFrame with clickable links
styled_df = df.style.format({'links': lambda x: x if pd.isnull(x) else x.replace('\n', '<br>'),
                             'job': lambda x: x.replace('\n', '<br>')})

# Convert the styled DataFrame to an HTML table
html_table = styled_df.to_html(escape=False, index=False)

# Write the HTML table to a CSV file
with open("test.csv", "w") as f:
    f.write(html_table)
