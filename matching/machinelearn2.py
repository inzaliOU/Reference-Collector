import io
import requests
from PyPDF2 import PdfReader
import re
from sentence_transformers import SentenceTransformer, util
url = 'https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=65e283a565b98fc8d3e6aa4069f13ea32dda9a03'
words = ''

def getlist(url):
  r = requests.get(url)
  f = io.BytesIO(r.content)
  # Create a PDF reader object
  try:
    pdf_reader = PdfReader(f, strict = False)
    pass
  except Exception as e:
    print(e,url)
    return
      
  # Define the keyword to search for
  keywords = ['Index Terms','keywords']
  matched_keyword=''
  # Define the regular expression pattern to search for
  # pattern = re.compile(r'\b{}\b\s+(.*?[.?!])'.format('|'.join(keywords)), re.IGNORECASE | re.DOTALL)
  page_text=""
  for page_num in range(len(pdf_reader.pages)):    
  # Get the text of the current page
   page = pdf_reader.pages[page_num]
   page_text+= page.extract_text()

  paragraph=""
  for w in keywords: 
    pattern = re.compile(r'\b{}\b\s+(.*?[.?!])'.format(w), re.IGNORECASE | re.DOTALL)
  
    match = pattern.search(page_text)
  # If a match is found, extract the words and print them
    if match:
      paragraph = match.group(0)
      matched_keyword=w
      break
    else:
      paragraph = "No matching paragraph found."
  

  paragraph = ''.join(paragraph)
  print(paragraph)
  # Remove the word "keyword" (case-insensitive)

  new_sentence = paragraph.replace(matched_keyword, '')

  sentences1 = ['architecture, Flask, django, backend, web application']

  sentences2 = [new_sentence]

  model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

  #Compute embedding for both lists
  embedding_1= model.encode(sentences1, convert_to_tensor=True)
  embedding_2 = model.encode(sentences2, convert_to_tensor=True)

  cosine_scores =util.cos_sim(embedding_1, embedding_2)
  #Output the pairs with their score
  print("{} \t\t {} \t\t Score: {:.4f}".format(sentences1[0], sentences2[0], cosine_scores[0][0]))
  return cosine_scores[0][0].item()