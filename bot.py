import os
import zipfile
from time import sleep
from selenium import webdriver
import numpy as np

filename = 'proxy.txt'

data = np.loadtxt(filename, delimiter=':',  dtype=str)

  
PROXY_HOST = data[0]  # rotating proxy
PROXY_PORT = data[1]
PROXY_USER = data[2]
PROXY_PASS = data[3]

# PROXY_HOST = '217.171.146.165'  # rotating proxy
# PROXY_PORT = 45785
# PROXY_USER = 'Q5Ys7x'
# PROXY_PASS = 'Hd4aPY'


manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
          singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
          },
          bypassList: ["localhost"]
        }
      };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)



def get_chromedriver(use_proxy=False, user_agent=None):
    path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    driver = webdriver.Chrome(
        os.path.join(path, 'Driver\chromedriver'),
        chrome_options=chrome_options)
    return driver

def main():      
    sayac=0
    driver = get_chromedriver(use_proxy=True)
    #driver.get('https://www.google.com/search?q=my+ip+address')
    driver.get('https://www.twitch.tv/kioptrix')
    #driver.get('https://httpbin.org/ip')
    while True:
        if (sayac==99999):
            break
        else:
            sayac+1
            driver.refresh()
            sleep(300)
    while(True):
     pass
    
if __name__ == '__main__':
    main()