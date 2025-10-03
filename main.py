import pandas as pd
import re

pattern = r'^(?:[a-zA-Z.]{1,6}|.{1,5})$'
df = pd.read_csv("https://d3ry1h4w5036x1.cloudfront.net/reports/Namecheap_Market_Sales.csv")

sdf = (df
    .loc[lambda d: d['name'].str.contains(pattern,regex=True)]
    .loc[lambda d: d['bidCount'] == 0]
    .loc[lambda d: d['price'] < 50]
    .loc[lambda d: d['renewPrice'] < 50]
)

html_table = (sdf
    .sort_values('endDate')
    .assign(name = lambda d: d.apply(lambda row: f'<a href="{row.url}" target="_blank">{row["name"]}</a>', axis=1),
            end_date_iso = lambda d: pd.to_datetime(d.endDate, utc=True).dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
    .reset_index(drop=True)
    [['name', 'price', 'renewPrice', 'end_date_iso']]
    .style.format(dict(price='${:.0f}', renewPrice='${:.0f}'))
    .to_html())

html = f'''<!DOCTYPE html>
<html>
<link rel="stylesheet" href="https://cdn.simplecss.org/simple.min.css">
<body><main>
<h1>Short domains up for grabs!</h1>
<p>Short domains are convenient: easy to type, and easy to remember. But, obtaining a 3-letter domain name directly is usually difficult and expensive. Luckily, these no-bid auctions can be a practical way to find a short domain for a business, project, or personal use.</p>
<p>This page lists short, no-bid Namecheap auction domains under $50, sorted by expiration date. Updated hourly.</p>
<p>
You can browse the full Namecheap marketplace <a href="https://www.namecheap.com/market/auctions/" target="_blank">here</a>.<br>
The code for this site is open source and available <a href="https://github.com/rensdimmendaal/cheap-short-domains" target="_blank">on GitHub</a>.
</p>
<p><i>(yes I'm aware of the irony that the url of this page is extremely long)</i></p>
{html_table}

<script>
function updateCountdowns() {{
    const endDateCells = document.querySelectorAll('td.col3');
    const now = new Date();
    
    endDateCells.forEach(cell => {{
        const endDate = new Date(cell.textContent);
        const diff = endDate - now;
        
        if (diff <= 0) {{
            cell.textContent = 'EXPIRED';
            cell.style.color = 'red';
            return;
        }}
        
        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        
        cell.textContent = `${{days}}d ${{hours}}h ${{minutes}}m`;
    }});
}}

// Update immediately and then every minute
updateCountdowns();
setInterval(updateCountdowns, 60000);
</script>
</main></body>
</html>'''

with open('output.html', 'w') as f: f.write(html)