import pyshorteners as pst

def shortenurl(url):
    try:
        if url == "":
            return "Please Enter the url."
        s = pst.Shortener()
        print(url)
        shortened_url = s.tinyurl.short(url)
        return shortened_url
    except Exception as e:
        print(e)
        return "Error! This url can not be shortened."

    

