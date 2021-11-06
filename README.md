# delivery-optimization
Project created for the subject of machine learning engineering.

Project Organization
------------

    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── project_name       <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    ├── tests              <- Unit tests
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

Problem zgłoszony przez klienta: „Mamy problemy odpowiednim zapełnianiem półek magazynowych. Nigdy nie wiadomo, co tak naprawdę będzie potrzebne w najbliższym tygodniu, co powinniśmy zamówić. Może da się coś z tym zrobić?”

Kontekst:
Zadanie biznesowe:
Biznesowe kryterium sukcesu:

Zadanie modelowania:
Dane do modelowania:
Założenia:

Analityczne kryterium sukcesu:

## Analiza danych