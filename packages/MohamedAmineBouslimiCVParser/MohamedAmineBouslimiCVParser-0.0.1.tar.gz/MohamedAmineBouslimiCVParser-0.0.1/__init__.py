def convert_pdf_to_txt(path):
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfpage import PDFPage
    from io import StringIO
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

def getPhone(path):
    text = convert_pdf_to_txt(path)
    try:
        pattern = re.compile(r'([+(]?\d+[)\-]?[ \t\r\f\v]*[(]?\d{2,}[()\-]?[ \t\r\f\v]*\d{2,}[()\-]?[ \t\r\f\v]*\d*[ \t\r\f\v]*\d*[ \t\r\f\v]*)')
        phone = pattern.findall(text)
        phone = [re.sub(r'[,.]', '', el) for el in phone if len(re.sub(r'[()\-.,\s+]', '', el))>6]
        phone = [re.sub(r'\D$', '', el).strip() for el in phone]
        phone = [el for el in phone if len(re.sub(r'\D','',el)) <= 13 and len(re.sub(r'\D','',el))>=10]
        return phone[0]
    except:
        return None

def getEmail(path): 
    text = convert_pdf_to_txt(path)
    
    try:
        pattern = re.compile(r'\S*@\S*')
        email = pattern.findall(text)
        return email[0]
    except:
        return None

def getExperience(path):
    text = convert_pdf_tp_txt(path)
    import re
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.tag import pos_tag
    from nltk import word_tokenize, pos_tag, ne_chunk
    sentences = nltk.sent_tokenize(text)
    sentences = [nltk.word_tokenize(el) for el in sentences]
    sentences = [nltkpos_tag(el) for el in sentences]
    try:
        sen=[]
        z=0
        exps = ['experience','experiences','stage','stages','travail','expérience']
        for words in sentences:
            for i in range(len(words)):
                if(words[i][0].lower() in exps):
                    index=[z,i]
                    break
            z+=1
        
        exp=[]
        for i in sentences[index[0]][index[1]+1:]:
            if i[0].isalpha() and i[1]=='NNP':
                exp.append(i[0])
        
        return exp        
        
    except:
        return None

def getSkills(path):
    text = convert_pdf_tp_txt(path)
    import re
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.tag import pos_tag
    from nltk import word_tokenize, pos_tag, ne_chunk
    sentences = nltk.sent_tokenize(text)
    sentences = [nltk.word_tokenize(el) for el in sentences]
    sentences = [nltkpos_tag(el) for el in sentences]
    try:
        sen=[]
        z=0
        wrds = ['domaine','competence','compétence','compétences','skills']
        for words in sentences:
            for i in range(len(words)):
                if(words[i][0].lower() in wrds) and words[i][1]=='NNP':
                    index =[z,i]
                    break
            z+=1

        skills=[]
        for i in sentences[index[0]][index[1]+1:]:
            if i[0].isalpha() and i[1]=='NNP':
                skills.append(i[0])

        return skills
    except:
        return None

def getCertification(sentences):
    text = convert_pdf_to_txt(path)
    import re
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.tag import pos_tag
    from nltk import word_tokenize, pos_tag, ne_chunk
    sentences=nltk.sent_tokenize(text)
    sentences=[nltk.word_tokenize(el) for el in sentences]
    sentences=[nltk.pos_tag(el) for el in sentences]
    try:
        sen=[]
        z=0
        certs = ['certifications','moocs','diplome','certificat','certificats']
        global index
        for words in sentences:
            for i in range(len(words)):
                if(words[i][0].lower() in certs):
                    index=[z,i]
                    break
            z+=1

        certis=" ".join([sentences[index[0]][k][0] for k in range(1,len(sentences[index[0]]))])

        return certis
    except:
        return None

def getDetails(path):
    text = convert_pdf_to_txt(path)
    import re
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.tag import pos_tag
    from nltk import word_tokenize, pos_tag, ne_chunk
    sentences=nltk.sent_tokenize(text)
    sentences=[nltk.word_tokenize(el) for el in sentences]
    sentences=[nltk.pos_tag(el) for el in sentences]
    phone=getPhone(text)
    mail=getEmail(text)
    exp=getExperience(sentences)
    quals=getQual(sentences)
    skills=getSkills(sentences)
    certis=getCertification(sentences)
    dict={
        'Phone_no': phone,
        'Email':mail,
        'Experience': exp,
        'Qualification':quals,
        'Compétences': skills,
        'Certifications': certis
    }
    return dict

getDetails('./')