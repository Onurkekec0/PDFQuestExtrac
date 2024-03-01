from sumy.summarizers.lex_rank import LexRankSummarizer
from .forms import SoruForm
from django.shortcuts import render, redirect
import fitz
import spacy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
import nltk
import openai
import json
from django.core.cache import cache
import re
Gcevap=[]
GCEVAP_CACHE_KEY = 'gcevap_cache_key'

nltk.download('punkt')


def handle_uploaded_file(f):
    file_path = r'C:\Users\Hp\Desktop\GPT Project\PDFQuestExtrac\Temp/' + f.name
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path  # Dosyanın yüklendiği yolunu döndür
def AnaSayfa(request):
    return render(request,'PdfEkran.html')
def ExamplesPDF(request):
    return render(request,'ExamplesPDF.html')
def sorular(request):
    global Gcevap  # Global değişkeni kullan
    if request.method == 'POST' and request.FILES['dosya']:
        dosya = request.FILES['dosya']
        file_path = handle_uploaded_file(dosya)
    summary = smmry(file_path)
    openai.api_key="<<openai api should come here>>"
    a=""
    result_all=""
    for i in range(3):
        completion = openai.completions.create(
        model="text-davinci-003",
        prompt="'" + summary + f"""'Bu metin ile ilgili TÜRKÇE 5 adet soru hazırla, çok seçmeli olsun!  (5 şıktan!(Soru\nA)...\n B)....\n C)....\n D)...\n E)....\n şıklar alt alta olsun en son cevap olsun) ve soruların sonlarına cevapları yaz cevap: şeklinde!(cevapları da kendin yaz!)
şablon: alttaki gibi olsun
soru
A)
B)
C)
D)
E)
Cevap:
""",
        max_tokens=2048,
        temperature=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        result=completion.choices[0].text
        result_all+=result
    print(result_all)
    metin=result_all
    t_sorular = list()
    sorular = list()
    t_siklar = list()
    siklar = list()
    for i in metin.split("\n"):
        if "A)" in i and "B)" in i and "?" in i:
            metin = metin.replace(i, i.replace("? ", "\n"))
        else:
            pass
    for i in metin.split("\n"):
        if("A)" in i and "B)" in i and ("Cevap" in i or "cevap" in i) ):
            if (i.find("Cevap") > 0):
                metin = metin.replace(i[:i.find("Cevap")], i[:i.find("Cevap") - 1] + "\n")
            elif (i.find("cevap") > 0):
                metin = metin.replace(i[:i.find("cevap") - 1], "\n")
            else:
                pass
    for index, i in enumerate(metin.split("\n")):
        if (re.search('^\d', i)):
            i = str(i).strip("{}. ".format(str(i)[0]))
            t_sorular.append(i)
        else:
            pass
    for index, i in enumerate(t_sorular):
        i = str(index + 1) + ". " + i
        sorular.append(i)
    for index, i in enumerate(metin.split("\n")):
        if (re.search(r'^(([A-E | a-e](\)|\.)))', i)):
            pattern = re.compile(r'([A-Ea-e]\) (\S+(?:\s*\S+)?)\s*)')
            matches = pattern.findall(i)
            if (len(matches) > 4):  # burada yan yana yazılan şıkları buluyor ve ayrı ayrı listeye ekliyor
                for j in matches:
                    t_siklar.append(j[0])
                continue
            t_siklar.append(i)
        else:
            pass
    t1_siklar = list()
    cevaplar = list()
    # burada bütün şıkları 5 er 5 er ayırıyor
    for index, i in enumerate(t_siklar):
        if ((index + 1) % 5 == 0):
            t1_siklar.append(i)
            siklar.append(t1_siklar)
            t1_siklar = list()
        else:
            t1_siklar.append(i)
    for i in metin.split("\n"):
        if (re.search(r'(Cevap|cevap|CEVAP)', i)):
            cevaplar.append(i)
        else:
            pass
    QuestAndOpti = list()
    QuestAndOpti_temp = list()
    for q, a in zip(sorular, siklar):
        QuestAndOpti_temp.append(q)
        for option in a:
            QuestAndOpti_temp.append(option)
        QuestAndOpti.append(QuestAndOpti_temp)
        QuestAndOpti_temp = list()
    cache.set(GCEVAP_CACHE_KEY, cevaplar, timeout=None)
    time = 35
    return render(request,'Sorular.html',{'questions': QuestAndOpti,"cevaplar":cevaplar,'time':time})

def loading_view(request):

    return render(request, 'loading.html')
def pdf_to_english(pdf_file):
    text = ""
    doc = fitz.open(pdf_file)
    # translator = Translator()
    for page_num in range(doc.page_count):
        try:
            page = doc.load_page(page_num)
            # translation = translator.translate(page.get_text(), dest="en")
            text += page.get_text()
        except:
            pass
    string_text=str(text)
    return string_text

def summarize_text(text, sentences_count=30):
    nlp = spacy.load("en_core_web_sm")

    def split_sentences(text):
        return [sent.text for sent in nlp(text).sents]

    doc = nlp(text)
    sentences = split_sentences(text)
    summarizer = LexRankSummarizer()
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summary = summarizer(parser.document, sentences_count)
    return " ".join([str(sentence) for sentence in summary])

def smmry(pdf_file):
    text = pdf_to_english(pdf_file)  # PDF metnini İngilizce'ye çevirin
    summary = summarize_text(text)
    return summary


def cevaplar(request):
    if request.method == 'POST':
        Vcevap=[]
        cevaplar = request.POST.get('cevaplar')
        for i in json.loads(cevaplar):
            Vcevap.append(str(i["value"])[0])

        Gcevap = cache.get(GCEVAP_CACHE_KEY)
        d_say,y_say=0,0
        for i in range(len(Vcevap)):

            if(Gcevap[i].split(":")[1].strip().lower()==str(Vcevap[i]).strip().lower()):
                d_say+=1
            else:
                y_say+=1
        return render(request,"sonuclar.html",{"Cevaplar":cevaplar,"dogru":d_say,"yanlis":y_say})
    else:
        # GET istekleri için başka bir şey yapabilirsiniz (örneğin, hata mesajı gösterme)
        pass
def ilerlemeli_form(request):
    sorular = [
        {"soru": "Hangi renkler bayrağımızda bulunur?", "cevap": "A"},
        {"soru": "Hangi renkler bayrağımızda bulunur?", "cevap": "A"},
        {"soru": "Hangi renkler bayrağımızda bulunur?", "cevap": "A"},
        {"soru": "Hangi renkler bayrağımızda bulunur?", "cevap": "A"},

        # Diğer soruları ekleyin
    ]

    if request.method == 'POST':
        form = SoruForm(request.POST)
        if form.is_valid():
            # Formu işleme alın
            # İlerleyebilirsiniz veya sonuçları görüntüleyebilirsiniz
            return redirect('ilerle')
    else:
        form = SoruForm()

    return render(request, 'ilerlemeli_form.html', {'form': form, 'sorular': sorular})
