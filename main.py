
import urllib.request
link = "https://www.youtube.com/watch?v="
video = "fbjFofNGHks"
url = link+video
print(url)


opener = urllib.request.FancyURLopener({})
f = opener.open(url)
content = f.read()

print(content)
