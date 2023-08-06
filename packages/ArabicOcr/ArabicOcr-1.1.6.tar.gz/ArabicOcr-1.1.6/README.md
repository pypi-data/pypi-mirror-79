# ArabicOcr Package to convert any Arabic image text to text by ocr techniques 
## about

Python Package to convert arabic images to text 

# Installation

```
pip install ArabicOcr
or in colab google cloud
!pip install ArabicOcr
```

## Usage for get frames images 

```
from ArabicOcr import arabicocr
```
```
image_path='1.jpg'
out_image='out.jpg'
results=arabicocr.arabic_ocr(image_path,out_image)
print(results)
words=[]
for i in range(len(results)):	
		word=results[i][1]
		words.append(word)
with open ('file.txt','w',encoding='utf-8')as myfile:
		myfile.write(str(words))
import cv2
img = cv2.imread('out.jpg', cv2.IMREAD_UNCHANGED)
cv2.imshow("arabic ocr",img)
cv2.waitKey(0)

```

## Tutorial 
u can see tutorial in colab 

https://colab.research.google.com/drive/1ay5KT9Za340_kN7fhS2xuJX8suCigaF6?usp=sharing



