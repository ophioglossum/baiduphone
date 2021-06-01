import tldextract
#获取url的主域名家后缀
def get_domain_suffix(url):
    tld = tldextract.extract(url)
    return tld.domain+'.'+tld.suffix