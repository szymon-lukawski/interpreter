# TKOM Projekt

#### Szymon Łukawski

## Temat Projektu:

Tematem projektu jest implementacja interpretera własnego języka ogólnego przeznaczenia w `Python`-ie w którym:
 + typowanie jest **słabe**
 + zmienne są domyślnie **niemutowalne**
 + argumenty funkcji przekazywane są domyślnie przez **wartość** 
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
   + `str` - typ reprezentujący ciąg znaków . 
   + 
