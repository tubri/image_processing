import requests
import pandas as pd

#institution code: cumv,utep,uam
institutioncode = 'nhmuk'

urls = pd.read_table("D:/HDR/multimedia_5/splitedworksheet/"+ institutioncode +".txt")
urls['redirectURI'] = None

for index in range(len(urls)):
    url = urls['ac:accessURI'][index]
    r = requests.get(url, allow_redirects=True)
    urls['redirectURI'][index] = r.url
    print(url,r.url)

redirect_urls = urls['redirectURI'].values.tolist()
urls.to_csv('D:/HDR/multimedia_5/splitedworksheet/' + institutioncode + '_ar.txt',sep='\t', index=False)
with open('D:/HDR/multimedia_5/splitedworksheet/' + institutioncode + '_redirect.txt', 'w') as f:
    for item in redirect_urls:
        f.write("%s\n" % item)