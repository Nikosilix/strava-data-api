{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 #!/bin/bash\
\
echo "\uc0\u9203  Refreshing Strava data..."\
python3 refresh_data.py\
\
echo "\uc0\u9989  Strava data refreshed. Now committing to GitHub..."\
git add cached_data.json\
git commit -m "update: new Strava data $(date '+%Y-%m-%d %H:%M')"\
git push origin main\
echo "\uc0\u55357 \u56960  All done! Data pushed to GitHub."}