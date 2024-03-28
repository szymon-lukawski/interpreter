# Projekt TKOM - Dokumentacja Wstępna

Szymon Łukawski

## Wstęp
Tematem projektu jest implementacja interpretera własnego języka ogólnego przeznaczenia w `Python`-ie. 
Zachowanie zmiennych:
+ typowanie jest **słabe** Typowanie**.
+ **domyślnie stałe**
+ przekazywane przez **wartość** 

Dodakowo mozliwość definiowania struktur oraz struktury wariantowej - typy definiowane przez uzytkownika.
## 1. Zarys:
```
print('Hello World!');
```
Wypisywanie literału.

### Typy wbudowane to:
   + `int` - podstawowy typ liczbowy reprezentujący liczby całkowite z przedziału [-99 999 999; +99 999 999]
   + `float` - typ liczbowy zmiennoprzecinkowy z utratą precyzji. Podobny do typu float64 ze standardu `IEEE 754-1985`. Operacje na liczbach float zgodne z operacjami w języku python3.
   + `str` - typ reprezentujący ciąg znaków.
   + `null_type` - specjalny typ reprezentujący dokładnie jedną specjalną wartość `null`. Proba uzyskania wartości zmiennej niezainicjowanej zwraca błąd, a **nie** wartość `null`!
  
#### Przykłady:
Najpierw przykład a pózniej wyjaśnienie:
  ```
  calkowita          : int = 10;
  zmiennoprzecinkowa : float = 3.14;
  napis              : str = 'Ala ma kota.';
  ```
1. Przykład ilustrujący typowe definiowanie zmiennych.
```
x : int = 1;
```
2. Zmienna `x` jest niemutowalna. Próba zmiany jej wartości zwróci błąd `ReassignmentError`.
```
y : mut int = 1;
y = 2;
```
3. Definiowanie zmiennej mutowalnej. Zmiana wartości nie zwraca błędu.
```
z1 : int;
z1 = 0;
z2 : mut int;
z2 = 11; 
```
4. Zarówno zmienne mutowalne jak i niemutowalne mogą nie mieć przypisanej wartości. Próba nadania wartości zmiennej niemutowalnej nie zwraca błędu (o ile typ się zgadza. O kompatybilności typów pózniej).
   Próba odczytania wartości zmiennej która nie ma nadanej wartości zwraca błąd, a nie wartość `null`. 


### Niestandardowe typy danych: 
   + Język umozliwia tworzenie zlozonych typow danych przez programiste.
   + `struct` - struktura, typ złozony z agregacji innych typów.
     + dostęp do atrybutów instancji struktury po nazwie atrybutu: `nazwa_instancji.nazwa_atrybutu`
     + brak mozliwości przypisania nowej wartości do atrubutu mutowalnego gdy instancja struktury jest niemutowalna
   + `variant` - tagged union:
     + dostęp do atrybutów instancji wariantu po nazwie pola, analogicznie jak w przypadku struktur. Wyjątek gdy nazwa atrybutu istnieje ale wariant aktualnie okupowany przez inny typ.
 + zachowane są priorytety operacji matematycznych, logicznych oraz porównania:
   1. `|` - lub
   2. `&` - i
   3. `<=; <; ==; !=; >=; >` - operatory porównania
   4. `+; -` - dodawanie, odejmowanie
   5. `*; /` - mnozenie, dzielenie
   6. `-` - przeciwieństwo (unarny)
   7. `()` - nawiasowanie
 + komentarze:
   +  znak `@` - komentarz do końca lini
   +  koniec linii to znak `\n`
 + zmienne:
    + typowanie jest **słabe**. Szczegóły w sekcji **Słabe Typowanie**.
    + zmienne są domyślnie **niemutowalne**
    + argumenty funkcji przekazywane są domyślnie przez **wartość** 
  + Zakresy widoczności obiektów:
    + obiekty to: 
      + zmienne
      + struktury:
        1. warianty
      + funkcje
    + domyślny jest zakres globalny
    + nowe zakresy są ograniczone przez słowa kluczowe `begin` oraz `end`
    + zakresy mogą być zagniezdzone
    + zakres bardziej zagniezdzony "przysłania" nazwy z zakresow mniej zagniezdzonych
  
### 2. Słabe Typowanie

##### Pojęcia:
 + ***Current type*** - obecny typ pewnej wartości.
 + ***Target type*** - typ do którego interpreter zamierza skonwertować wartość  typu ***current type***.


Ogólne zasady konwersji:
 1. Jezeli ***Current type*** jest ten sam co ***Target type*** to nic nie rób.
 2. Kazdy typ wbudowany ma listę potencjalnych konwersji do innych typów wbudowanych:
    1. `int` do `float` zawsze. Ta konwersja zachodzi bez utraty precyzji. 
    2. `int` do `str` zawsze
    3. `float` do `int` jeśli wartość po zaokrągleniu jest z przedziału `int`.  
    4. `float` do `str` zawsze - do doprecyzowania czy ciąg 64 zer i jedynek czy do siódmej cyfry rozwinięcia dziesiętnego.
    5. `str` do `float` gdy wartość da się zinterpretować jak `float` analogicznie jak w gramatyce języka. Gdy wartość nie ma znaku `.` konwersja następuję pośrednio ze `str` do `int`, a następnie z `int` do `float`
    6. `str` do `int` gdy wartość da się zinterpretować jak `int` analogicznie jak w gramatyce języka. Gdy wartość ma znak `.` interpretujemy jak `float` i konwertujemy do `int` jeśli się da.
 3. TODO: specjalne funckje konwersji w definicji struktur.
