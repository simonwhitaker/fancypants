from fancypants import Dataset, Rect, Point

# Example: OECD data on broadband subscriber statistics
# http://www.guardian.co.uk/news/datablog/2009/may/20/broadband-internetphonesbroadband

data = [
    ('Australasia', [
        ('Australia', 5368000),
        ('New Zealand', 914961),
    ]),
    ('Europe', [
        ('Austria', 1792408),
        ('Belgium', 2962450),
        ('Czech Republic', 1769684),
        ('Denmark', 2021404),
        ('Finland', 1616900),
        ('France', 17725000),
        ('Germany', 22532000),
        ('Greece', 1506614),
        ('Hungary', 1696714),
        ('Iceland', 99883),
        ('Ireland', 896346),
        ('Italy', 11283000),
        ('Luxembourg', 141584),
        ('Netherlands', 5855000),
        ('Norway', 1607750),
        ('Poland', 3995458),
        ('Portugal', 1692306),
        ('Slovak Republic', 618871),
        ('Spain', 9156969),
        ('Sweden', 2905000),
        ('Switzerland', 2533643),
        ('United Kingdom', 17275660),
    ]),
    ('North America', [
        ('Canada', 9577648),
        ('United States', 80071074),
    ]),
    ('Asia', [
        ('Japan', 30107327),
        ('Korea', 15474931),
        ('Turkey', 5736619),
    ]),
    ('South America', [
        ('Mexico', 7604629),
    ]),
]

ig = Dataset(data)

frames = ig.treemap(Rect(600,420), origin=Point(0,0), padding=1, threshold=40000000)

with open("oecd-broadband.html", "w") as f:

    f.write("""<html>
<head>
    <title>fancypants example: OECD broadband subscriptions</title>
    <style>
        @import url('oecd-broadband.css');
    </style>
</head>
<body>
<p>Broadband subscribers (millions) per OECD country. Data source: <a href="http://www.guardian.co.uk/news/datablog/2009/may/20/broadband-internetphonesbroadband">Guardian Datablog</a>. Created using <a href="http://github.com/simonwhitaker/fancypants">fancypants</a></p>
<div style="position:relative">
""")

    for frame in frames:
        f.write("""<div class='frame %s' style='position: absolute; top: %ipx; left: %ipx; width: %ipx; height: %ipx'>
    <div class="text">
        <div class="value">%i</div>
        <div class="label">%s</div>
    </div>
</div>
""" %
            (
                frame.label.replace(' ', '_').replace('.', ' '),
                frame.y,
                frame.x,
                frame.width,
                frame.height,
                round(frame.value/1000000),
                frame.label.split('.')[-1],
            )
        )

    f.write("</div></body></html>")