import re,requests,json
ip="178.128.103.59" # change your ip here coded by @SomawDev
h=requests.get(f"https://scamalytics.com/ip/{ip}",headers={"User-Agent":"Mozilla/5.0"}).text
f=lambda p,c=None:(m:=re.search(p,h,re.I)) and (c(m) if c else m.group(1))
b=lambda p:bool(re.search(p,h,re.I))
r={
 "ip":ip,
 "fraud_score":f(r"Fraud Score:\s*(\d+)",lambda m:int(m.group(1))),
 "risk_level":f(r"(\bLow|Medium|High)\s*Risk",lambda m:m.group(1).capitalize()),
 "operator":{"ISP_Name":f(r"ISP Name\s*([\w\s\.,\-&]+)"),
             "Organization":f(r"Organization Name\s*([\w\s\.,\-&]+)")},
 "location":{"country_name":f(r"Country Name\s*([\w\s\.,\-&]+)"),
             "country_code":f(r"Country Code\s*([A-Z]{2})"),
             "city":f(r"City\s*([\w\s\.,\-&]+)"),
             "postal_code":f(r"Postal Code\s*(\d+)"),
             "latitude":f(r"Latitude\s*([0-9\.\-]+)",lambda m:float(m.group(1))),
             "longitude":f(r"Longitude\s*([0-9\.\-]+)",lambda m:float(m.group(1)))},
 "datacenter":b(r"Datacenter\s*Yes"),
 "blacklists":{k:b(rf"{k}\s*Yes") for k in["Firehol","IP2ProxyLite","IPsum","Spamhaus","X4Bnet Spambot"]},
 "proxies":{k:b(rf"{k}\s*Yes") for k in["Anonymizing VPN","Tor Exit Node","Server","Public Proxy","Web Proxy"]}
}
print(json.dumps(r,indent=2))
