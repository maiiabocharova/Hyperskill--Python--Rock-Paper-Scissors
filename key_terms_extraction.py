import xml.etree.ElementTree as ET
import string
import nltk
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('wordnet')
#nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter
tree = ET.parse('news.xml')
# data = '''<?xml version='1.0' encoding='UTF8'?>
# <data>
#   <corpus>
#     <news>
#       <value name="head">New Portuguese skull may be an early relative of Neandertals</value>
#       <value name="text">Half a million years ago, several different members of our genus, Homo, had spread throughout Europe and Asia, where some would eventually evolve into Neandertals.
#           But which ones has been the subject of intense debate.
#           A newly discovered partial skull is offering another clue to help solve the mystery of the ancestry of Neandertals.
#           Found in 2014 in the Gruta da Aroeira cave in central Portugal with ancient stone hand axes, the skull (3D reconstruction pictured) is firmly dated to 400,000 years old and an archaic member of our genus, according to a study published today in the Proceedings of the National Academy of Sciences.
#           The skull shows a new mix of features not seen before in fossil humans-it has traits that link it to Neandertals, such as a fused brow ridge, as well as some primitive traits that resemble other extinct fossils in Europe.
#           This new combination of features on a well-dated skull may help researchers sort out how different fossils in Europe are related to each other-and which ones eventually evolved into Neandertals.</value>
#     </news>
#     <news>
#       <value name="head">Loneliness May Make Quitting Smoking Even Tougher</value>
#       <value name="text">Being lonely may make it harder to quit smoking, a new British study suggests.
#           Using genetic and survey data from hundreds of thousands of people, researchers found that loneliness makes it more likely that someone will smoke.
#           This type of analysis is called Mendelian randomization.
#           'This method has never been applied to this question before and so the results are novel, but also tentative,' said co-lead author Robyn Wootton, a senior research associate at the University of Bristol in the United Kingdom.
#           'We found evidence to suggest that loneliness leads to increased smoking, with people more likely to start smoking, to smoke more cigarettes and to be less likely to quit,' Wootton said in a university news release.
#           These data mesh with an observation that during the coronavirus pandemic, more British people are smoking.
#           Senior study author Jorien Treur said, 'Our finding that smoking may also lead to more loneliness is tentative, but it is in line with other recent studies that identified smoking as a risk factor for poor mental health.
#           A potential mechanism for this relationship is that nicotine from cigarette smoke interferes with neurotransmitters such as dopamine in the brain.'
#           Treur is a visiting research associate from Amsterdam UMC.
#           The researchers also looked for a connection between loneliness and drinking but found none.
#           Still, if loneliness causes people to smoke, it is important to alert smoking cessation services so they can add this factor as they help people to quit, the study authors said.
#           The report was published June 16 in the journal Addiction.</value>
#     </news>
#   </corpus>
# </data>'''
# root = ET.fromstring(data)
root = tree.getroot()
heads = []
texts = []
stopwords = set(stopwords.words('english'))
punct = list(string.punctuation)
lemmatizer = WordNetLemmatizer()
for head in root.findall("./corpus/news/value[@name='head']"):
    heads.append(head.text)
for text in root.findall("./corpus/news/value[@name='text']"):
    tokenized = word_tokenize(text.text.lower())
    lemmas = [lemmatizer.lemmatize(word) for word in tokenized]
    without_stopwords = [word for word in lemmas if word not in stopwords and word not in punct]
    nouns = [word for (word,pos) in nltk.pos_tag(without_stopwords) if pos[:2] == 'NN']
    most_common = Counter(nouns).most_common(5)
    most_common = [(lambda x: x[0])(x) for x in most_common]
    texts.append(" ".join(most_common))

for head, text in zip(heads, texts):
    print(f'{head}:')
    print(text)

answer = {'Brain Disconnects During Sleep:': ['sleep', 'cortex', 'consciousness', 'activity', 'tononi'],
          'New Portuguese skull may be an early relative of Neandertals:': ['skull', 'europe', 'fossil', 'year',
                                                                            'member'],
          'Living by the coast could improve mental health:': ['health', 'mental', 'coast', 'household', 'living'],
          'Did you knowingly commit a crime? Brain scans could tell:': ['brain', 'study', 'wa', 'suitcase', 'result'],
          'Computer learns to detect skin cancer more accurately than doctors:': ['dermatologist', 'skin', 'melanoma',
                                                                                  'cnn', 'year'],
          'US economic growth stronger than expected despite weak demand:': ['u', 'quarter', 'ha', 'growth', 'year'],
          'Microsoft becomes third listed US firm to be valued at $1tn:': ['microsoft', 'share', 'cloud', 'market',
                                                                           'ha'],
          "Apple's Siri is a better rapper than you:": ['siri', 'time', 'ha', 'rhyme', 'wa'],
          'Netflix viewers like comedy for breakfast and drama at lunch:': ['netflix', 'comedy', 'day', 'show',
                                                                            'viewer'],
          'Loneliness May Make Quitting Smoking Even Tougher:': ['smoking', 'loneliness', 'study', 'smoke', 'quit']}
