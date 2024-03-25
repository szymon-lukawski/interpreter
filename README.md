# TKOM Projekt

#### Szymon Łukawski

## Temat Projektu:

Tematem projektu jest implementacja interpretera własnego języka ogólnego przeznaczenia w `Python`-ie w którym:
 + niestandardowe typy danych: 
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
 + typy wbudowane to:
   + `int` - podstawowy typ liczbowy reprezentujący liczby całkowite z przedziału [-99 999 999; +99 999 999]
   + `float` - typ liczbowy zmiennoprzecinkowy z utratą precyzji. Operacje na liczbach float zgodne z operacjami w języku python3.
   + `str` - typ reprezentujący ciąg znaków.
 + komentarz do końca linii po znaku `@`
 + zmienne:
    + typowanie jest **słabe**
    + zmienne są domyślnie **niemutowalne**
    + argumenty funkcji przekazywane są domyślnie przez **wartość** 
    + nowy zakres widoczności zmiennej jest wyznaczany przez zagniezdzone słowa kluczowe `begin` oraz `end`
  
#### Typowanie jest słabe zatem tabele konwersji typów wbudowanych:

##### Pojęcia:
 + ***Current type*** - obecny typ pewnej wartości.
 + ***Target type*** - typ do którego interpreter zamierza skonwertować wartość  typu ***current type***.


Ogólne zasady konwersji:
 1. Jezeli ***Current type*** jest ten sam co ***Target type*** to nic nie rób.
 2. Kazdy typ bazowy ma listę potencjalnych konwersji do innych typów bazowych:
    1. `int` do `float` zawsze
    2. `int` do `str` zawsze
    3. `float` do `int` jeśli wartość po zaokrągleniu jest z przedziału `int`.  
    4. `float` do `str` zawsze - do doprecyzowania czy ciąg 64 zer i jedynek czy do siódmej cyfry rozwinięcia dziesiętnego.
    5. `str` do `float` gdy wartość da się zinterpretować jak `float` analogicznie jak w gramatyce języka. Gdy wartość nie ma znaku `.` konwersja następuję pośrednio ze `str` do `int`, a następnie z `int` do `float`
    6. `str` do `int` gdy wartość da się zinterpretować jak `int` analogicznie jak w gramatyce języka. Gdy wartość ma znak `.` interpretujemy jak `float` i konwertujemy do `int` jeśli się da.
 3. TODO: specjalne funckje konwersji w definicji struktur.
