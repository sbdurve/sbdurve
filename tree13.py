# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 09:19:59 2023

@author: SUK910665
"""

import os
import numpy as np
import pandas as pd

str1  = '''
<html>
  <head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: Arial;
}

</style>
</head>


<body>
<!-- <br>    <p> Missing Photos</p> -->
<!--           <iframe  src="https://drive.google.com/embeddedfolderview?id=1v9elPfRdwqNYWTbb8XA85Vy_cKp-YrQA#grid"  style="width:30%; height:400px; border: 5px solid black;"></iframe> -->
<nav>
  <ul>
    <li><a href="#chart_div"> Family Tree </a></li>
    <li><a href="#links"> Family Links </a></li>
    <li><a href="#photos"> Family Photos </a></li>
  </ul>
</nav>


  <style>

    div {
      font-family: Helvetica, sans-serif, Impact, Arial;
      font: 10px Arial, sans-serif;
      padding: 1px 0;
      background-color: tan;
      color: tan;
    }


    p {
      background-color: blue;
      font: 45px Arial, sans-serif;
      padding: 1px 0;
    }

    ul {
      background-color: honeydew;
      font: 15px Arial, sans-serif;
      padding: 1px 0;
    }

    img {
      background-color: green;
      padding: 10px 0;
      border-radius: 30%;
    }

  </style>




   <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">

      google.charts.load('current', {packages:["orgchart"]});
      google.charts.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Name');    // Name is json object of the form {"v": "val1","f":"val2"}
        data.addColumn('string', 'Parent');
        data.addColumn('string', 'Tooltip');
        data.addRows([


'''
str2 = '''
         ]);


      function myFunction(imgs) {
        var expandImg = document.getElementById("expandedImg");
        var imgText = document.getElementById("imgtext");
        expandImg.src = imgs.src;
        imgText.innerHTML = imgs.alt;
        expandImg.parentElement.style.display = "block";
}
        var chart = new google.visualization.OrgChart(document.getElementById('chart_div'));
        chart.draw(data, {'allowHtml':true});
      }
   </script>
  </head>
  <body>
    <div id="chart_div"></div>

    <div id="links"></div>

'''




def IMG(name,width,height):
    return name.apply(lambda x : '    <img src="'   + images[x][0] + '" alt="' + x + '.jpg" width="'+str(width)+'" height="'+str(height)+'">   ' \
                      if len(x) > 3 and isinstance(images[x][0],str) else '')
def img(src):
    return '<img src=' + inquote(src)+ ' alt="Nature" style="width:100%" onclick="myFunction(this);">\n'
def BOLD(text):
    return '<b>'+text+'</b>'
def COLOR(color):
    return color + '; font-style:italic">'
def IFRAME(link,description):
    folder_id = link.apply(lambda x: x.replace('https://drive.google.com/drive/folders/','https://drive.google.com/embeddedfolderview?id=').
                           replace('?usp=share_link','#grid"'))
    str1 = ''
    str1 += '<br>    <p> ' + description + '</p>\n          <iframe  src=\"'+ folder_id + '  style="width:100%; height:250px; border: 10px solid black;"></iframe>\n'
    return str1
def A(link,data):
    if len(link) :
        return ('<a  href=\"' + link + '\" > ' + data + '</a>').apply(lambda f : f.ljust(150))
def P(person,link,data):
    return '<p  id=\"'+person+'\">'+A(link,data)+'</p>'
def LI(item):
    return '    <li>'+item+'</li>\n'
def div(item):
    return '    <div>'+item+'</div>\n    '
def UL(links,descriptions):
    str1  = '\n<ul>\n'
    for link, description in zip(links,descriptions) :
        str1 += LI(A(link, description))
    str1 += '</ul>\n\n'
    return str1
def DIV(item):
    return '<div style=\"color:'+ item +'</div>'
def BR():
    return '<br>'
def inquote(arg):
    return "'"+str(arg)+"'"

############################ Read data and perform validation/uniqueness checks #############################
dfile = 'C:\\Users\\SUKCO0665\\Downloads\\Dasharath.xlsx'
data   = pd.read_excel(dfile,sheet_name="Main",na_filter=False)
images = pd.read_excel(dfile,sheet_name="images",na_filter=False).set_index('person').T.to_dict('list')
data['person_link'] = data.person.apply(lambda x : images[x][0] if x else '')
data['spouse_link'] = data.spouse.apply(lambda x : images[x][0] if x else '')

assert data.spouse[data.spouse != ''].is_unique
assert data.person.is_unique
assert data.spouse_link[data.spouse_link != ''].is_unique
assert data.person_link[data.person_link != ''].is_unique

spouse = data[['spouse','spouse_full']][data.spouse != '']
spouse.columns = ['person','person_full']
tot = pd.DataFrame(pd.concat([data[['person','person_full']],spouse]),columns = ['person','person_full'])

f2 = open(os.path.join(os.path.dirname(dfile),'tree.html'),'w')
f2.write(str1)
############################ Draw family tree ###############################################################
data['v'] = data.person
scale = 4
wid,hei = scale * 10,scale * 12
data['f'] = A(data.person_link , IMG(data.person,wid,hei)  + DIV(COLOR('blue')+ data.person_full)) + BR() +\
            A(data.spouse_link , IMG(data.spouse,wid,hei)  + DIV(COLOR('red') + data.spouse_full))  

for ii in data.index :                                       # Name, Parent Tooltip
    dt = '['+ data[['v','f']].loc[ii,:].to_json()+ ','  +\
    inquote(data.loc[ii,'parent']) +               ','  +\
    inquote(data.loc[ii,'tooltip'])+                    '],\n'
    f2.write(dt)

f2.write(str2)

############################ Display Links ###################################################################
# pld = pd.read_excel(dfile,sheet_name='links')
# pld.sort_values(by='person',inplace=True)
# pld = pld.merge(tot)
# lds = []
# for person in pld.person.unique():
#     lds.append(pld[pld.person == person])
# for ld in lds:
#     f2.write(P(ld.person.unique()[0],ld.person.unique()[0],ld.person_full.unique()[0]))    
#     f2.write(UL(ld.link,ld.description))
    
# str3 = '''
#     <div id="photos"></div>

# '''
# ############################ Display Googledrive Photos ######################################################
# ld   = pd.read_excel(dfile,sheet_name='gdrives')
# for ii in list(IFRAME(ld.link,ld.description)):
#     str3+=ii
# str3 += '''
#   </body>
# </html>
# '''
# f2.write(str3)
f2.close()
