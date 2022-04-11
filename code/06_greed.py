import re

html = """
<div><p>如果你为门中弟子伤她一分,我便屠你满门</p></div>
<div><p>如果你为天下人损她一毫,我便杀尽天下人</p></div>
"""

regex = '<div><p>(.*)</p></div>'
r_list = re.findall(regex, html, re.S)
print(r_list)























