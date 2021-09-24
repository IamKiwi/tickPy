# System obsługi ticketów - tickPy

# Technologie:

- Język Python 3.8
- Framework Django - Backend
- <del>Vue.js - Frontend</del> <-- (zabrakło czasu :( ) System szablonowania wbudowany w Django

# Funkcjonalności:

ticket = zgłoszenie

3 role w systemie - Administrator, Inżynier, Użytkownik
- Administrator - zarządza aplikacją
- Inżynier - osoba przyjmująca/wystawiająca/rozwiązująca zgłoszenia problemów
- Użytkownik - osoba wystawiająca zgłoszenia problemów

Administrator - zarządza aplikacją:
- tworzy/modyfikuje/usuwa użytkowników
- tworzy/modyfikuje/usuwa kolejki
- tworzy/modyfikuje/usuwa zasoby (na co można wystawić ticket,
np. serwer x, stacja robocza y, laptop z)

Inżynier - osoba odpowiedzialna za rozwiązywanie ticketów:
- pobiera tickety ze swojej kolejki, do której obsługi został przypisany przez 
administratora
- może oznaczyć ticket jako:
    + rozwiązany - problem został rozwiązany i ticket można zamknąć 
    + odrzucony - problemu nie da się rozwiązać lub osoba wystawiająca 
    rażąco zaniedbała opis w tickecie (nie da się ustalić przyczyny, 
    użytkownik nie wie o czym mówi)
    + wymagane informacje - użytkownik musi sprecyzować szczegóły problemu,
    ponieważ pierwotny opis w tickecie nie pozwala na ustalenie przyczyny
    i podjęcie działania
- może zmienić priorytet zgłoszenia
    
Użytkownik - osoba wystawiająca zgłoszenia problemów:
- może wystawić zgłoszenie na dowolną kolejkę
- może zgłosić problem tylko dla zasobów, dla których przypisał ją administrator
- może ustalić priorytet zgłoszenia
