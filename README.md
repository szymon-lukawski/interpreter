# Projekt TKOM - Dokumentacja Wstępna
Szymon Łukawski

## Wstęp
Tematem projektu jest implementacja interpretera własnego języka ogólnego przeznaczenia w `Python`-ie. 
Zachowanie zmiennych:
+ typowanie jest **słabe** Typowanie**.
+ **domyślnie stałe**
+ przekazywane przez **wartość** 

Dodakowo mozliwość definiowania struktur oraz struktury wariantowej - typy definiowane przez uzytkownika.
## 1. Zarys uruchomienia:
```
print('Hello World!');
```
Wypisywanie literału.
Po pobraniu repozytorium i zaintalowaniu zalezności z pliku `requirements.txt` nalezy w terminalu wpisać:
```
>python3 interpreter.py <nazwa_pliku>
Hello World!
>
```
Plik musi mieć rozszerzenie `.mc`. 
Istnieje mozliwość stworzenia pliku konfiguracyjnego `config.json` który steruje parametrami interpretera m.i. limity dla typu `int`.
## Typy wbudowane to:
   + `int` - podstawowy typ liczbowy reprezentujący liczby całkowite, domyślnie z przedziału [-99 999 999; +99 999 999]
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
1. Zmienna `x` jest niemutowalna. Próba zmiany jej wartości zwróci błąd `ReassignmentError`.
```
y : mut int = 1;
y = 2;
```
1. Definiowanie zmiennej mutowalnej. Zmiana wartości nie zwraca błędu.
```
z1 : int;
z1 = 0;
z2 : mut int;
z2 = 11; 
```
1. Zarówno zmienne mutowalne jak i niemutowalne mogą nie mieć przypisanej wartości. Próba nadania wartości zmiennej niemutowalnej nie zwraca błędu (o ile typ się zgadza. O kompatybilności typów pózniej).
   Próba odczytania wartości zmiennej która nie ma nadanej wartości zwraca błąd, a nie wartość `null`. 

```
x : mut int;
x = - 99999999;
x = 99999999;
```
Oto domyślne limity dla zmiennej int. Limity mozna modyfikować plikiem konfiguracyjnym o nazwie `config.json` w katalogu w którym uruchomiony został interpreter. Próba stworzenia lierału integer spoza zakresu zgłasza błąd  `LiteralError`

```
y : str = '';
```
Znienna typu `str` z przypisaną wartością pustego stringa jest czym innym niz zmienna `str` bez przypisanej wartości.

### Niestandardowe typy danych: 
   + Język umozliwia tworzenie zlozonych typow danych przez programiste.
   + `struct` - struktura, typ złozony z agregacji innych typów.
     + dostęp do atrybutów instancji struktury po nazwie atrybutu: `nazwa_instancji.nazwa_atrybutu`
     + brak mozliwości przypisania nowej wartości do atrubutu mutowalnego gdy instancja struktury jest niemutowalna
   + `variant` - tagged union:
     + typy w wariancie nie mogą się powtarzać
     + azeby przypisac wartosc do zmiennej wariantowej nalezy uzyć bezpośrednio jednego z typów składowych wariantu.

#### Przykłady:
```
Czlowiek : struct
begin
    imie : str;
    wiek  : mut int;
end
janek : Czlowiek;
janek.imie = 'Janek';
janek.wiek = 20;
```
Definicja struktury jest zawarta między słowami kluczowymi `begin` oraz `end`.
Definicja struktury składa się z zera lub więcej definicji zmiennych - pól w tej strukturze.
Zdefiniowanie zmiennej typu `Czlowiek` odbywa się analogicznie jak przy definicji zmiennych o typach wbudowanych.
Próba zmiany wartości pola `wiek` w instancji struktury `Czlowiek` np. `janek.wiek=21;` zwróci błąd `ReassignmentError` - zmienna `janek` jest niemutowalna.
Zeby zmiana wartości pól w strukturze była mozliwa, zarówno sama zmienna musi być mutowalna jak i jej pola muszą być mutowalne.
```
cos : Cos;
Cos : struct begin end;
```
Typ `Cos` zdefiniowany po próbie definicji zmiennej tego typu zatem zwróbu `UndefinedTypeError: 'Cos'`.
Struktura moze nie miec zadnych pól.

```
Kod_pocztowy : struct
begin
  wartosc : str;
end

Adres : struct
begin 
  miasto : mut str;
  kod_pocztowy : mut Kod_pocztowy;
end

Czlowiek : struct
begin
    imie : str;
    wiek  : mut int;
    adres : mut Adres;
end

janek : mut Czlowiek;
janek.imie = 'Janek';
janek.wiek = 20;

kod_pocz_janka : Kod_pocztowy;
kod_pocz_janka.wartosc = '00-111';

adres_janka : Adres;
adres_janka.miasto = 'Warszawa';
adres_janka.kod_pocztowy = kod_pocztowy_janka;

janek.adres = adres_janka;
print('Kod pocztowy Janka to: ');
print(janek.adres.kod_pocztowy.wartosc);
```
Przykład prezentuję zagniezdzenie typów oraz operator dostępowy do pól struktury: `<instancja_typu>.<nazwa_pola>`.
Próba odwołania się do nieistniejącego pola zwraca błąd `CellNameError: <nazwa nieistniejacego pola>`
W tym przykladzie `janek.a` zwroci bląd `CellNameError: 'a'`

```
Punkt2D : struct
begin
  x : mut int = 0;
  y : mut int = 0;
end

Punkt3D : struct
begin
  x : mut int = 0;
  y : mut int = 0;
  z : mut int = 0;
end

Punkt : variant struct
begin
    p2d : Punkt2D;
    p3d : Punkt3D;
end

A : Punkt2D;
B : Punkt3D;

punkt : Punkt = A;
wiadomosc : str;

visit punkt
begin
    case Punkt2D
    begin
        wiadmosc = '[' + p2d.x + '; ' +p2d.y + ']';
    end
    case Punkt3D
    begin
        wiadmosc = '[' + p3d.x + '; ' +p3d.y + '; ' +p3d.z + ']';
    end
end
print(wiadomosc);
```
Powyzszy program prezentuje wariant oraz instrukcję `visit`.
W tym przykladzie zmienna wariantowa `punkt` przechowuje wartość typu `Punkt2D` zatem w instrukcji visit przechodzimy do odpowiadającemu temu typowi bloku (blok po `case Punkt2D`).
Generacja wiadomości w tym przykladzie dotyka tematu operatorów, który będzie omawiany pózniej.
Próba storzenia bloku `case <NazwaTypuNieistniejacaWDefinicjiRozwazanegoWariantu>` zwroci błąd `VariantTypeNotFound: '<NazwaTypuNieistniejacaWDefinicjiRozwazanegoWariantu>'`.
Próba stworzenia powtarzajacego się bloku `case` zwroci błąd `CaseRedefinitionError: '<NazwaPowtarzającegoTypu>'` czyli w sytuacji:
```
visit punkt
begin
    case Punkt2D
    begin
        wiadmosc = '[' + p2d.x + '; ' +p2d.y + ']';
    end
    case Punkt2D @ CaseRedefinitionError: 'Punkt2D'
    begin
        wiadmosc = '[' + p3d.x + '; ' +p3d.y + '; ' +p3d.z + ']'; @ UndefinedIdentifierError : 'p3d'
    end
end
```
`@` - komentarz po końca linii. 

### Komentarze:

Tylko komentarze jednolinijkowe: `@`.
Koniec linii to znak `\n` 
Znak `@` najlepiej stawiać albo na końcu wpisanej instrukcji albo w zupełnie nowej linii.
```
@ To sa przyklady dobrych komentarzy
a : int = 12; @ To rowniez
Czlowiek : struct @ To tez
begin @ to tez
end @ to tez
```
```
a : int @ to są przyklady blednych kometarzy;
Czlowiek @ To tez : struct 
begin @ to tez
end @ to tez
```


### Słabe Typowanie
W ściśle określonych sytuacjach następuje automatyczna konwersja z typu do innego typu.
 + Z `int` do:
   + `float`: zawsze
   + `str`: zawsze, `print(123);` - wyswietli 123
   + `struct`: nigdy
   + `variant`: nigdy
 + Z `float` do:
   + `int`: tylko gdy wartosc jest z zakresu typu `int`
   + `str`: zawsze, reprezentowana jako zaokrąglona liczba dziesiętna, zawsze z literalnym rozwinięciem 7 cyfr po przecinku
   + `struct`: nigdy
   + `variant`: nigdy
  + Z `str` do:
     + `int`: jezeli wartosc typu `str` zlozona ze znakow cyfr oraz cyfry z przedzialu dla `int`. Jeśli wartość typu `str` zawiera znak `.` mozliwa jest konwersja dwuetapowa, najpierw z typu `str` do float (jesli się uda), następnie z `float` do `int`.
     + `float`: jezeli wartość typu `str` zlozona ze znakow cyfr i ewentualnie z kropki. Jezeli po kropce znajduje się wiecej niz 7 cyfr, kolejne cyfry nie mają wpływu na wartość liczby po konwersji.
     + `struct`: nigdy
     + `variant`: nigdy
 + Konwersje z typów definiowanych przez uzytkownika za pomocą : `struct` oraz  `variant`, nie mają automatycznej konwersji do typów wbudowanych 
```
print(1.0);       @ wyświetla na ekranie 7 cyfr rozwinięcia dziesiętnego: '1.0000000'
```

### Operacje
Generalne zasady dla operacji:
 + operacje mają rózny priorytet
 + operacje są lewo-łączne dla operatorów o tym samym priorytecie, `x * y * z` to to samo co `(x * y) * z`
 + pierwszy argument operacji to argument tuz przed operatorem
 + typ pierwszego argumentu definiuje typ wyniku operacji - **Mogą być wyjątki!**

Priorytety operacji posortowane od najmniejszego do najwyzszego:
   1. `|` - lub
   2. `&` - i
   3. `<=; <; ==; !=; >=; >` - operatory porównania
   4. `+; -` - dodawanie, odejmowanie
   5. `*; /` - mnozenie, dzielenie
   6. `-` - przeciwieństwo (unarny)
   7. `.` - operator dostepu do pola w strukturze
   8. `()` - nawiasowanie

Przykłady:


### Funkcje
    + argumenty do funkcji przekazywane są przez **wartość** 
    + 
### Zakresy widoczności obiektów:
  + obiekty to: 
    + zmienne
    + struktury
    + warianty
    + funkcje
  + Rózne rodzaje obiektow mogą mieć tą samą nazwę w tym samym zakresie
  ```
  A : int;
  A : struct begin end
  A : variant struct begin A : int; end
  A() : int begin return 0; end @ definicja funkcji o nazwie A 
  ```
  + Funkcje o róznej liczbie parametrow równiez mogą miec tą samą nazwę:
```
A() : int begin return 0; end
A(param1: int) : int begin return 1; end
A(param1: int, param2: int) : int begin return 2; end
```
  + domyślny jest zakres globalny
  + obiekty nie mogą mieć nazwy ze zbioru ***słów kluczowych***.
  + nowe zakresy są ograniczone przez słowa kluczowe `begin` oraz `end` - ***Wyjątek*** w instrukcji `visit` widoczna jest dodatkowo nazwa z definicji wariantu odpowiadająca typowi z przypadku `case` 
```
W : variant struct
begin
a : int;
b : str;
end

c : W = 1;

visit c
begin
    case int
    begin
        print('Widoczna zmienna a');
    end
    case str
    begin
        print('Widoczna zmienna b');
    end
end
```
  + zakresy mogą być zagniezdzone
  + zakres bardziej zagniezdzony "przysłania" nazwy z zakresow mniej zagniezdzonych
  
