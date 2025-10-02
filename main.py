import pandas as pd
import re

pattern = r'^(?:[a-zA-Z.]{1,6}|.{1,5})$'
df = pd.read_csv("https://d3ry1h4w5036x1.cloudfront.net/reports/Namecheap_Market_Sales.csv")

sdf = (df
    .loc[lambda d: d['name'].str.contains(pattern,regex=True)]
    .loc[lambda d: d['price'] < 50]
    .loc[lambda d: d['bidCount'] == 0]
    .loc[lambda d: d['renewPrice'] < 50]
    .loc[lambda d: pd.to_datetime(d['endDate']).dt.date == pd.Timestamp.today().date()])

html = (sdf
    .sort_values('endDate')
    .assign(time_remaining=lambda d: (pd.to_datetime(d.endDate, utc=True) - pd.Timestamp.now(tz='UTC')).apply(lambda x: f"{x.days}d {x.seconds//3600}h {(x.seconds%3600)//60}m"),
            name = lambda d: d.apply(lambda row: f'<a href="{row.url}" target="_blank">{row["name"]}</a>', axis=1))
    .reset_index(drop=True)
    [['name', 'price', 'renewPrice', 'time_remaining']]
    .style.format(dict(price='${:.0f}', renewPrice='${:.0f}'))
    .to_html())

html_with_css = f'''<!DOCTYPE html>
<html>
<link rel="stylesheet" href="https://cdn.simplecss.org/simple.min.css">
<body>
<main>
<h1>Short domains up for grabs!</h1>
{html}
</main>
</body>
</html>'''

with open('output.html', 'w') as f: f.write(html_with_css)