import io
import pytesseract
from PIL import Image
from wand.image import Image as wi
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
from django.conf import settings
import networkx as nx

pytesseract.pytesseract.tesseract_cmd = r'F:\Tesseract-OCR\tesseract.exe'
# nltk.download('stopwords')


def imageSummary(fname):
    im = Image.open(fname)
    orignaltext = pytesseract.image_to_string(im, lang='eng')
    #orignaltext=orignaltext.replace('\n',' ')
    # print(orignaltext)
    with open('imgtext.txt', 'w+') as imgtxt:
        imgtxt.write(orignaltext)
    #summarizetext=generate_summary('imgtext.txt', 2)
    with open('imgtextsummary.txt', 'w+') as imgtextsummary:
        imgtextsummary.write(generate_summary('imgtext.txt', 2))
    '''
	print('Summarized Text from image: ')
	summary=generate_summary( "imgtext.txt", 2)
	#print(summary)

	'''
    return (orignaltext, 'hello')


def pdfsummary(fname):
    file = settings.BASE_DIR+'/media/'+str(fname)
    pdf = wi(filename=file, resolution=300)
    pdfImage = pdf.convert('jpeg')
    imageBlobs = []
    orignaltext = ''
    for img in pdfImage.sequence:
        imgPage = wi(image=img)
        imageBlobs.append(imgPage.make_blob('jpeg'))
    for imgBlob in imageBlobs:
        im = Image.open(io.BytesIO(imgBlob))
        text = pytesseract.image_to_string(im, lang='eng')
        orignaltext += text
    #print('Orignal Text from pdf:')
    orignaltext = recognized_text.replace('\n', '')
    print(recognized_text)
    with open('pdftext.txt', 'w+') as pdftxt:
        pdftxt.write(recognized_text)
    print('Summarized Text from pdf: ')
    summary = generate_summary('pdftext.txt', 2)
    print(summary)
    with open('pdftextsummary.txt', 'w+') as pdftextsummary:
        pdftextsummary.write(summary)
    ''' 
	'''
    return (orignaltext, 'summarizetext')


def textsummary(fname):
    orignaltext = ""
    file = settings.BASE_DIR+'/media/'+str(fname)
    print(fname, type(fname), file)
    with open(file, "r") as text_file:
        orignaltext = text_file.read()
    print(orignaltext)
    summarizedtext = generate_summary(file, 2)
    return (orignaltext, summarizedtext)


def docsummary():
    pass


def read_article(file_name):
    file = open(file_name, "r")
    filedata = file.readlines()
    article = filedata[0].split(". ")
    sentences = []
    for sentence in article:
        print(sentence)
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    sentences.pop()
    return sentences


def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
    all_words = list(set(sent1 + sent2))
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
    # build the vector for the first sentence
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1
    # build the vector for the second sentence
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1
    return 1 - cosine_distance(vector1, vector2)


def build_similarity_matrix(sentences, stop_words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2:  # ignore if both are same sentences
                continue
            similarity_matrix[idx1][idx2] = sentence_similarity(
                sentences[idx1], sentences[idx2], stop_words)
    return similarity_matrix


def generate_summary(file_name, top_n=2):
    stop_words = stopwords.words('english')
    summarize_text = []
    # Step 1 - Read text anc split it
    sentences = read_article(file_name)
    print(read_article(file_name))
    # Step 2 - Generate Similary Martix across sentences
    sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)
    # Step 3 - Rank sentences in similarity martix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph)
    # Step 4 - Sort the rank and pick top sentences
    ranked_sentence = sorted(
        ((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    #print("Indexes of top ranked_sentence order are \n", ranked_sentence)
    for i in range(top_n):
        summarize_text.append(" ".join(ranked_sentence[i][1]))
        # print(i)
    # Step 5 - Offcourse, output the summarize texr
    print(type(sentences), len(sentences), sentences)
    print(type(ranked_sentence), len(ranked_sentence), ranked_sentence)
    #summarize_text.append(" ".join(ranked_sentence[0][1]))
    return summarize_text
