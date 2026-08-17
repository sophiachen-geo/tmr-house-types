import json,sys,time,urllib.parse,urllib.request
API="https://commons.wikimedia.org/w/api.php?"
UA={"User-Agent":"tmr-house-types-research/1.0 (heritage typology research; noncommercial)"}
def q(params,tries=6):
    params.setdefault("format","json"); params.setdefault("formatversion","2")
    for i in range(tries):
        try:
            req=urllib.request.Request(API+urllib.parse.urlencode(params),headers=UA)
            return json.load(urllib.request.urlopen(req,timeout=90))
        except Exception as e:
            if i==tries-1: raise
            time.sleep(4*(i+1))
def cat(name,limit=60):
    r=q({"action":"query","list":"categorymembers","cmtitle":"Category:"+name,"cmtype":"file","cmlimit":str(limit)})
    return [x["title"] for x in r.get("query",{}).get("categorymembers",[])]
def info(titles):
    out=[]
    for i in range(0,len(titles),10):
        chunk=titles[i:i+10]
        r=q({"action":"query","titles":"|".join(chunk),"prop":"imageinfo",
             "iiprop":"url|extmetadata|size|mime","iiextmetadatafilter":
             "License|LicenseShortName|Artist|Credit|ImageDescription|DateTimeOriginal|Attribution|UsageTerms|Permission|LicenseUrl|ObjectName"})
        for p in r.get("query",{}).get("pages",[]):
            ii=(p.get("imageinfo") or [{}])[0]; em=ii.get("extmetadata",{}) or {}
            g=lambda k:(em.get(k,{}) or {}).get("value")
            out.append({"title":p.get("title"),"url":ii.get("url"),"w":ii.get("width"),"h":ii.get("height"),
                        "licence":g("LicenseShortName"),"licence_url":g("LicenseUrl"),"usage":g("UsageTerms"),
                        "artist":g("Artist"),"credit":g("Credit"),"desc":g("ImageDescription"),
                        "date":g("DateTimeOriginal"),"attr":g("Attribution")})
        time.sleep(1.5)
    return out
if __name__=="__main__":
    mode=sys.argv[1]
    if mode=="cat":
        for t in cat(sys.argv[2]): print(t)
    else:
        import re
        titles=[l.strip() for l in sys.stdin if l.strip()]
        for r in info(titles):
            print(json.dumps(r,ensure_ascii=False))
