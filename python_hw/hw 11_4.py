import re
with open('filasafy.html', 'r', encoding = 'utf-8') as f1:
    html = f1.read()
    line = re.sub('Философ', 'Астролог', html, flags = re.U)
    line = re.sub('философ', 'астролог', html, flags = re.U)
    line = re.sub('философск', 'астрологическ', html, flags = re.U)
    line = re.sub('Философск', 'Астрологическ', html, flags = re.U)
    line = re.sub('философы', 'астрологи', html, flags = re.U)
    line = re.sub('Философы', 'Астрологи', html, flags = re.U)
    line = re.sub('филосо́ф', 'астроло́г', html, flags = re.U)
    line = re.sub('Филосо́ф', 'Астроло́г', html, flags = re.U)
        
with open('astrology.html', 'w', encoding = 'utf-8') as f2:
    f2.write(line)



    
    

    
    
   
    

    
    




