#fakenews

##Api do twittera
W klasie TwitterConnection jest atrybut api do twittera poprzez biblioteke tweepy

+ Do uruchomienia jej potrzebujemy pliku twitter-credentials.json ktora wylse wam na FB. Wsadzamy go do /resources/

+ Do gitignore dalem pliki json jeszcze zeby ten plik nie commitowal sie bo to sa dane do mojego(bielas) konta

Dokumentacja ( link umożliwia tylko wyświetlanie, więc podajcie maile to was dodam do edycji ) :
https://docs.google.com/document/d/1WuP45YpfjxqyZbNAFnbzWICVt7ftB1hCSw-E8Wq9o8w/edit?usp=sharing

##Bielas 28.05.2019



###UWAGA!
- zeby moj modul zadzial przy wyszukiwaniu tweetow musz byc ustawione parametry:
    - tweet_mode='extended',
    - include_entities=True
    

###Zwracany wynik i ich kombinacje

w kazdym przypadku zwracam obiekt dict() z kluczami 'fake', 'probability', 'description'

wszystkie mozliwe wyniki mojego modułu:

1. 
                'fake': False,
                'probability': 1,
                'description': 'Tweet był retweetowany - to nie jest bot'

2. 
                'fake': True,
                'probability': 0.7,
                'description': 'User nie opublikowal 10 tweetow - uznajemy za bota'

3.
                'fake': False,
                'probability': 'default value',
                'description': 'default value'

4. 
                'fake': False,
                'probability': 1,
                'description': 'User publikuje z czestotliwoscia wieksza niz dwa dni - to nie ' \
                                                    'jest bot '
5. 
                'fake': True,
                'probability': 0.6,
                'description': 'User nie publikowal nic przez 3,4 lub 5 dni - uzanje za bota z ' \
                                                    'prawd.=0.6 '
                                                    
6. 
                'fake': True,
                'probability': 0.9,
                'description': 'User ma odstep miedzy tweetami wiekszy niz 5 dni - uznaje ' \
                                                    'za bota z prawd.=0.8 '
7.
                'fake': 'default value',
                'probability': 'default value',
                'description': 'Brak URLi w tweecie'
8. 
                 'fake': True,
                 'probability': 1,
                 'description': 'Wylaczono machine learning, kod HTTP jest prawidlowy'

9.
                 'fake': True,
                 'probability': 1,
                 'descripiton': 'Wylaczono machine learning'
10.
                'fake': False,
                'probability': 1,
                'description': 'Wylaczono machine learning, Url nie rzuca bledem ale nieznany jest content url, zwracam prawdo.=0.7'

11.
                'fake': True,
                'probability': url_malicious['score'],
                'description': 'wlaczono machine learning'

12.
                 'fake': False,
                 'probability': url_malicious['score'],
                 'description': 'wlaczono machine learning'


####Omówienie schematu postepowania mojego modułu

Omówienie metod dostępnych na zewnątrz:
Klasa BotChecker,
metody:

- is_fake_based_on_user(self, tweetId) - metoda sprawdza czestotliwosc
postowania tweetow. W tym przypadku prawdopodobienstwo jest umowne i wpisywane z lapy na wartosci: 0.6, 0.7 1 lub 0.9<br/>
Algorytm: 
1. jesli sa jakies retweety tego tweeta to znaczy ze to nie jest bot czyli nie jest to fake news
2. jesli user nie opublikowal min 10 tweetow - moze to byc bot - tweet ustawiany na fake z prawd. = 0.7
3. jesli uzytkownik publikuje tweety czesciej niz co 2 dni - nie jest to bot, news nie jest fake z prawd.=1
4. jesli uzytkownik publikuje tweety czesciej niz 2 dni ale rzadziej niz 5 dni jest ustawiany tweet jako fake z prawd.=0.6
5. jesli uzytkownik publikuje rzadziej niz 5 dni tweet jest ustawiany na fake z prawd.=0.9

- is_fake_based_on_external_urls(self, tweetId, isMachineLearning) - metoda sprawdza zalaczone w tweecie odnosniki
jako parametry wejsciowe oprocz tweetId przyjmuje wartosc True lub False<br/>
Algorytm z isMachineLearning ustawionym na True:

1. jesli nie ma zadnego odnosnika w tweecie zwracamy wartosci "default value"
2. jesli ma odnosniki uzywamy uczynie maszynowego z klasy UrlMachineLearner ktora zwraca nam wartosc fake 
true albo false wrac z prawd.<br/>

Algorytm z isMachineLearning ustawionym na false:
1. Probujemy otworzyc strone z odnosnika
2. jesli kod responsu to error (kody z wartoscia wieksza od 400) to znaczy ze jest to fake i ustawiamy prawd.=1
2. w innym wypadku nie jest to fake z prawd.=1
3. Gdy nie jestesmy w stanie wejsc na odnosnik to znaczy ze jest to fake z prawd.=1


Co moze zostac ulepszone:
- cos sie pieprzylo z importami wiec wszytkie pliki dalem do jednej paczki,
jak ogarniacie lepiej pythona to mozecie zrefactorowac



##Inna sekcja

Przydatne linki : 
- PageRank extractor -> https://github.com/aablack/websearchapp/blob/master/search/rank_provider.py 

- projket w pythonie -> https://github.com/nishitpatel01/Fake_News_Detection

- https://data.world/d1gi/11000-expanded-labeled-links-from-365k-troll-tweets

- https://www.pantechsolutions.net/fake-news-detection-using-machine-learning

- https://towardsdatascience.com/i-built-a-fake-news-detector-using-natural-language-processing-and-classification-models-da180338860e

- https://www.geeksforgeeks.org/project-idea-know-more/

- https://github.com/cvhariharan/fake-news-detector

-  countvectorizer -> https://machinelearningmastery.com/prepare-text-data-machine-learning-scikit-learn/

Dane :

- https://www.kaggle.com/mrisdal/fake-news
