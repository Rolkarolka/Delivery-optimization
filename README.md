# delivery-optimization
Project created for the subject of machine learning engineering.

Project Organization
------------

    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │
    ├── reports           <- microservice
    |
    ├── poetry.lock        <- Lockfile which allows complete environment reproduction
    │
    └── pyproject.toml     <- file with settings and dependencies for the environment


--------


Setting up the environment
------------

1. Install `poetry`: https://python-poetry.org/docs/#installation
2. Create an environment with `poetry install`
3. Run `poetry shell`
4. To add a new package run `poetry add <package>`. Don't forget to commit the lockfile.
5. To run unit tests for your service use `poetry run pytest` or simply `pytest` within `poetry shell`.

<p><small>Project partially based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>


Timeline:
* 3.12 - etap 1
> Definicja problemu biznesowego, zdefiniowane zadania/zadań modelowania i wszystkich założeń, zaproponowanie kryteriów sukcesu. 
> Analiza danych z perspektywy realizacji tych zadań (trzeba ocenić, czy dostarczone dane są wystarczające - może czegoś brakuje, może coś trzeba poprawić, domagać się innych danych
* 14.01 - etap 2
> Dwa modele: model bazowy (najprostszy możliwy dla danego zadania) i bardziej zaawansowany model docelowy, oraz raport pokazujący proces budowy modelu i porównujący wyniki
> Implementacja aplikacji (w formie mikroserwisu) która pozwala na serwowanie predykcji przy pomocy danego modelu i realizacje eksperymentu A/B - w ramach którego porównywane będą oba modele i zbierane dane niezbędne do późniejszej oceny ich jakości oraz materiały pokazujące, że implementacja działa

## Zadanie

Problem zgłoszony przez klienta: „Mamy problemy z odpowiednim zapełnianiem półek magazynowych. Nigdy nie wiadomo, co tak naprawdę będzie potrzebne w najbliższym tygodniu, co powinniśmy zamówić. Może da się coś z tym zrobić?”

### Definicja problemu biznesowego

Analiza kontekstu: 
- obecna sytuacja: 
    - nie wiadomo jak zapełniać półki magazynowa; sklep nie potrafi przewidzień co będzie potrzebne w najbliższym tygodniu
- co ma zostać wprowadzone? 
    - analiza danych oraz przewidywanie co będzie potrzebne w najbliższym tygodniu
- jakie są oczekiwania, ograniczenia, zasoby? 
    -  oczekiwania: zapełnianie półek magazynowych dobrymi produktami; 
    -  ograniczenia: ilość miejsca w magazynie; 
    -  zasoby: towar dostarczony od dostawców.

Kontekst: sklep internetowy, z którego użytkownicy zamawiają produkty. Długość dostawy zależy, czy produkt znajduje się w magazynie.

Zadanie biznesowe: generowanie listy produktów na kolejny tydzień
Biznesowe kryterium sukcesu: wzrost sprzedaży

### Zdefiniowanie zadania/zadań modelowania i wszystkich założeń
Zadanie modelowania:
Przygotowanie modelu rekomendacyjnego na podstawie ilości zamówień w poprzednim roku oraz tendencji klientów.

Dane do modelowania:
- zamówienia z ostatniego tygodnia (cena, kategorie produktów)
- stosunek ilości zamówień w danych okresach roku (np. miesięcznie, kwartalnie)
- aktywność użytkowników oraz produkty, które wyświetlają.

Zmianna celu: ilość sprzedanych sztuk produktu w przewidywanym tygodniu.

Przewidywanie produktów, które w danym tygodniu powinny znajdować się na półkach magazynowych.

Założenia:
- liczba miejsc w magazynie jest ograniczona - ustalamy ją jako stałą.
- produkty, które zamawiamy trafiają do nas od razu - nie musimy brać pod uwagę czasu potrzebnego na ich dotarcie do naszego magazynu
- produkty, które zamawiamy od dostawców są zawsze dostępne.
### Zaproponowanie kryteriów sukcesu

System powinien przewidywać minimum x% produktów (np. ilość produktów przewidzianych/wszystkich produktów >= x/średnia dzienna ilość zamówień)

x - wartość uzgodniona z klientem wynosząca 5%

## Analiza danych

Umiejscowiona w jupyter notebooku data_analysis.ipynb
