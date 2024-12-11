# Projekt TKOM - Dokumentacja Wstępna
Szymon Łukawski

## Wstęp
Tematem projektu jest implementacja interpretera własnego języka ogólnego przeznaczenia w `Python`-ie. 
Zachowanie zmiennych:
+ typowanie jest **słabe**.
+ **domyślnie stałe**
+ przekazywane przez **wartość** 

Dodakowo mozliwość definiowania struktur oraz struktury wariantowej - typy definiowane przez uzytkownika.

## Struktura Projektu
Projekt podzielony na części:
1. Czytanie z wejścia, plik lub strumień, znak po znaku i przekazuje wszystkich znaków dalej. Jeśli koniec wejscia to wysyla specjalny znak konca wejscia. Zapytany o kojelny znak znowu specjalny znak konca wejscia, i tak do końca.
2. Analizator Leksykalny, generowanie tokenów, grupowanie znaków.
3. Analizator Składniowy, generowanie drzewa programu (AST) na podstawie gramatyki
4. Interpreter

## 1. Zarys uruchomienia:
```
> git clone https://gitlab-stud.elka.pw.edu.pl/TKOM_24Z_WW/slukawsk/tkom_projekt_sl
> cd tkom_projekt_sl
> python -m venv .venv
> source .venv/bin/activate
> pip install -r requirements.txt
> python main.py --source binary_tree.txt -i
interpreter  >>> Sum of my_tree is:
interpreter  >>> 45
Interactive mode enabled. Type q to quit
Type statement : 
```
## Typy wbudowane to:
   + `int` - podstawowy typ liczbowy reprezentujący liczby całkowite, z przedziału [-99 999 999; +99 999 999]. Operacje logiczne jak `&` oraz `|` czy operacje porównania zwracają ten typ. 
   + `float` - typ liczbowy zmiennoprzecinkowy z utratą precyzji. Podobny do typu float64 ze standardu `IEEE 754-1985`. Operacje na liczbach float zgodne z operacjami w języku python3. 
   + `str` - typ reprezentujący ciąg znaków. Mozna przechowywać znaki specjalne jak znak nowej linii, tabulacja itp. realizacja poprzez escaping `\`.
   + `null_type` - specjalny typ do zaznaczenia ze funkcja nie zwraca wartości. Zmienna nie moze miec tego typu.
  
#### Przykłady:
  ```
  calkowita          : int = 10;
  zmiennoprzecinkowa : float = 3.14;
  napis              : str = 'Ala ma kota.';
  ```
Przykład ilustrujący typowe definiowanie zmiennych.
```
x : int = 1;
```
Zmienna `x` jest niemutowalna. Próba zmiany jej wartości zwróci błąd.
```
y : mut int = 1;
y = 2;
```
Definiowanie zmiennej mutowalnej. Zmiana wartości nie zwraca błędu.
```
z1 : int;
z1 = 0;
z2 : mut int;
z2 = 11; 
```
Zarówno zmienne mutowalne jak i niemutowalne mogą nie mieć przypisanej wartości. Próba nadania wartości zmiennej niemutowalnej nie zwraca błędu (o ile typ się zgadza. O kompatybilności typów pózniej).
   Próba odczytania wartości zmiennej która nie ma nadanej wartości zwraca błąd. 

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
     + zmienna typu struct jest inicjalizowana jeśli dowolne pole w tej strukturze moze zostac zainicjalizowane.
     + przypisanie do atrybutu niezainicjalizowanej struktury tworzy tą strukturę.
        ```
        A : struct
        begin
            x : int;
            y : str;
        end
        B : struct
        begin
            a: A;
        end
        C : struct
        begin
            b: B;
        end
        c : C;                   # zmienna c nie ma wartości
        c.b.a.x = 123;           # zmienna c ma wartość
        c.b.a.y = 'Ala ma kota'; # zwraca błąd bo zmienna c ma wartość a nie jest mutowalna 
        ```  
      + pola w strukturze mogą mieć przypisane wartości domyślne:

        ```
        Point1D : struct
        begin
          x : mut int = 0; @ wartość domyślna wynosi 0
        end
        p : Point; # zmienna p ma wartość poniewaz przynajmniej jeden z jej atrybutów ma wartość
        ``` 
        ```
        Czlowiek : struct
        begin
            imie : str;
            wiek  : mut int;
        end
        janek : mut Czlowiek; # mutowalny zeby mozna bylo przypisac wartosc do wiecej niz jednego atrybutu bez wartosci domyślnej
        janek.imie = 'Janek';
        janek.wiek = 20;
        ```
   + `variant` - tagged union:
     + typy w wariancie nie mogą się powtarzać
     + typy w wariancie nie mogą być typami wariantowymi !
     + variant musi miec przynajmniej 2 typy
     + azeby przypisac wartosc do zmiennej wariantowej nalezy uzyć wartości która ma typ jednego z typów składowych wariantu. 
     + wyjątkiem jest przypisanie wartości typu wbudowanego. Jeśli wariant nie ma bezpośredniej zgodności typów to szuka czy jeden z jego wariantów jest typem wbudowanym. Jeśli tak to następuje próba konwersji wartości na typ wbudowany znaleziony jako pierwszy w dostępnych typach wariantu. Uwaga: ta operacja konwersji moze się nie udać dlatego najlepiej jest przypisywać wartości odpowiedniego typu do typu wariantowego... 
     + variant nie ma wartości domyślnej - pomimo ze typy składowe mogą ją mieć
     + w przeciwieństwie do `struct`, gdy zmienna variantowa nie ma wartości, nie mozna przypisać do atrybutu struktury składowej. # TODO przejrzyj wszystkie named_types które mają strukturę 

Definicja struktury jest zawarta między słowami kluczowymi `begin` oraz `end`.
Definicja struktury składa się z zera lub więcej definicji zmiennych - pól w tej strukturze - chociaz uzyteczność zmiennej tego typu jest wątpliwa - nie mozna przypisać wartości do takiej zmiennej.
```
cos : Cos;
Cos : struct begin end;
```
Typ `Cos` zdefiniowany po próbie definicji zmiennej tego typu zwróci błąd `UndefinedTypeError: 'Cos'`.
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

Punkt : variant
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
        wiadomosc = '[' + p2d.x + '; ' + p2d.y + ']';
    end
    case Punkt3D
    begin
        wiadomosc = '[' + p3d.x + '; ' + p3d.y + '; ' + p3d.z + ']';
    end
end
print(wiadomosc);
```
Powyzszy program prezentuje wariant oraz instrukcję `visit`.
W tym przykladzie zmienna wariantowa `punkt` przechowuje wartość typu `Punkt2D` zatem w instrukcji visit przechodzimy do odpowiadającemu temu typowi bloku (blok po `case Punkt2D`).
Generacja wiadomości w tym przykladzie dotyka tematu operatorów, który będzie omawiany pózniej.
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
### Słabe Typowanie
W ściśle określonych sytuacjach następuje automatyczna konwersja z typu do innego typu.
 + Z `int` do:
   + `float`: zawsze
   + `str`: zawsze, `print(123);` - wyswietli 123
   + `struct`: nigdy
   + `variant`: -- 
 + Z `float` do:
   + `int`: tylko gdy wartosc po odcięciu części ułamkowej jest z zakresu typu `int`.
   + `str`: zawsze, reprezentowana jako zaokrąglona liczba dziesiętna, zawsze z rozwinięciem 7 cyfr po przecinku
   + `struct`: nigdy
   + `variant`: nigdy
  + Z `str` do:
     + `int`: jezeli wartosc typu `str` zlozona ze znakow cyfr oraz cyfry z przedzialu dla `int`. Jeśli wartość typu `str` zawiera znak `.` mozliwa jest konwersja dwuetapowa, najpierw z typu `str` do float (jesli się uda), następnie z `float` do `int`.
     + `float`: jezeli wartość typu `str` zlozona ze znakow cyfr i ewentualnie z kropki. Jezeli po kropce znajduje się wiecej niz 7 cyfr, kolejne cyfry nie mają wpływu na wartość liczby po konwersji.
     + `struct`: nigdy
     + `variant`: nigdy
 + Typy definiowane przez uzytkownika za pomocą : `struct` oraz  `variant`, nie mają automatycznej konwersji do typów wbudowanych 
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

'|' oraz '&' - zwraca wartość typu `int` 0 albo 1. Następuje automatyczna konwersja pierwszego jak i drugiego argumentu na typ `int` i następnie wykonywana jest operacja.

Pierwszy argument to `str`:
 + `+` - konkatenacja
 + `-` - usunięcie pierwszego wystąpienia wartosci drugiego argumentu z pierwszego
 + `==` oraz `!=` - porównanie znak po znaku
 + `*` jeśli drugi argument jest typu `int` to powtórzenie sekwencji czyli `'ABC'*3` to `'ABCABCABC'`, jeśli drugi argument jest typu `str` to iloczyn kartezjański czyli `'AB'*'12'` to `'A1A2B1B2'`
 + `/` usuniecie kazdego wystapienia wartosci drugiego argumentu z pierwszego

Tylko struktury oraz warianty mają dostęp do operatora `.`

Dla typów `int` oraz `float` operacje porównania, dodawanie, odejmowanie, mnozenie, dzielenie - **Zgodnie z intuicją**

Gdy pierwszy argument jest typu `int` to dzielenie jest całkowite, gdy float to dzielenie jest zgodnie z intuicją.

### Funkcje
  + istnieją funkcje wbudowane:
    + `print(msg : str) : null` - funkcja do wyswietlania typu `str`
    + `read() : str` - funkcja do wczytywania wartości typu `str` od uzytkownika.
  + funkcje mozna definiowac w róznych zakresach a nie tylko w globalnym
```
add(arg1: int, arg2: int) : int
begin
  add_sub_function(arg1: int, arg2: int) : int
  begin
    return arg1 + arg2;
  end
  
  add(arg1: int, arg2: int) : int
  begin
    return add_sub_function(arg1, arg2);
  end

  return add(arg1, arg2);
end
```
W tym przykładzie nie ma rekurencji. Funkcja wewnętrzna add przysłania nazwę funkcji add z odpowiadającymi sobie parametrami. 
  + funkcje są 'widoczne' od momentu jej zadeklarowania:
```
@ Tutaj nie widać funkcji add
add(arg1: int, arg2: int) : int
begin
  @ od tego momentu widać funkcję add
  return arg1 + arg2;
end
@ tutaj tez widac funkcje add
```
```
factorial(n : int) : int 
begin
  if n < 0
  begin
    return -1;
  end
  if n <= 1
  begin
    return 1;
  end
  return n*factorial(n-1);
end

```
  + argumenty do funkcji przekazywane są przez **wartość**: 
```
add(a : int, b : int) : int
begin
  a = 100;
  b = 101;
  return a + b;
end

x : int = 0;
y : int = 1;

print(x); 
print(y);
c : int = add(x, y);
print(x); 
print(y); @ to samo co przed wywolaniem funkcji
```
   + Definicja funkcji w ogólności:
```
NazwaFunkcji : NazwaTypuZwracanejWartości
begin
<Ciało Funkcji>
end
```  
  + Jezeli funkcja nie zwraca wartości nalezy w miejsce nazwy typu zwracanej wartosci wpisac specjalny typ `null_type`
```
wypisz_na_ekran(wiadomosc: str) : null_type 
begin
  print(wiadomosc);
end
```
  + Brak instrukcji `return` w funkcji oznacza ze funkcja nie zwraca wartości
### Zakresy widoczności obiektów:
  + 
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
```
x : int = 1;
print(x); @ 1
begin
  x : str = 'Ala ma kota';
  begin
    x : float = 2.0;
    print(x); @ 2.0000000
  end
  begin
    x : float = 3.0;
    print(x); @ 3.0000000
  end
  print(x); @ Ala ma kota
end
print(x); @ 1
```

### Błędy
+ Po natrafieniu na błąd, przerywamy program
+ błędy zwracane przez lekser:
  + za długie literały
  + za długie nazwy identyfikatora
  + uzycie niedozwolonego znaku, np emotki
+ błędy zwracane przez parser:
  + niedopasowane nawiasy
  + niedopasowane `begin`, `end`
+ błędy semantyczne:
  + funkcja nieznaleziona, np jesli w wywołaniu podamy złą ilośc argumentów 
  + Niezgodność typów 
  + Błąd konwersji 
  + brak `return` w ciele funkcji zwracającej typ inny niz `null_type`
  + ponowne przypisanie wartosci do zmiennej niemutowalnej
  + odwołania się do nieistniejącego pola w strukturze
  + niestniejaca nazwa typu w waraincie podczas instrukcji `visit`
  + powtórka typu w przypadkach w instrukcji `visit`
  + niewspierana operacja, np `'abb' < 'abc'`
  
+ błędy podczas wykonania:
  + dzielenie przez zero
  + próba uzyskania wartosci zmiennej niezainicjowanej
  
+ Pozycja błędu, numer wiersza, pozycja w wierszu - pozycja pierwszego znaku fragmentu kodu generującego błąd

### Testowanie
Testy jednostkowe do kadej funkcji.
Testy integracyjne do sprawdzenia współpracy między modułami projektu.
Testy na całych złozonych programach.
terminal:
```PYTHONPATH="$(pwd)" pytest tests/ -q```

### Więcej przykładów:
W pliku `first.mc`
  
### Gramatyka w EBNF 2.0:
```
program             ::= {statement};

statement           ::=  variable_declaration_statement
                       | assignment_statement
                       | if_statement
                       | while_statement
                       | function_definition_statement
                       | type_definition_statement
                       | return_statement
                       | block;

block                           ::= 'begin', program, 'end';
return_statement                ::== 'return', expression, ';';

variable_declaration_statement  ::= variable_declaration, ';';
variable_declaration            ::= identifier, ':', ['mut'], type, ['=', expression];



assignment_statement            ::= object_access, '=', expression, ';';

if_statement                    ::= 'if', expression, block, ['else', block];

while_statement                 ::= 'while', expression, block;

function_definition_statement   ::= identifier, '(', params, ')', ':', type, block; 

type_definition_statement       ::= struct_def | variant_def;
struct_def                      ::= identifier, ':', 'struct', 'begin', {variable_declaration_statement} ,'end';
variant_def                     ::= identifier, ':', 'variant', 'begin', {named_type_statement} ,'end';

named_type_statement            ::= identifier, ':', type, ';'

expression              ::= logical_or_expression;
logical_or_expression   ::= logical_and_expression, {'|', logical_and_expression};
logical_and_expression  ::= relational_expr {'&', relational_expr};
relational_expr         ::= additive_expr, {relational_operator, additive_expr};
additive_expr           ::= multi_expr, {additive_operator, multi_expr};
multi_expr              ::= unary_expr, {multi_operator, unary_expr};
unary_expr              ::= ['-'], term;
term                    ::=	literal
                          | object_access;

object_access           ::=  identifier, {('.', identifier)};

function_call ::= identifier, '(', [expression , (',', expression)], ')';

param         ::= identifier, ':', ['mut'], type;
params        ::= param , {',', param};

type          ::=  'int'
        		| 'float'
        		| 'str'
        		| 'null'
        		| identifier;

literal        ::=  int_literal
            	| float_literal
            	| str_literal;
            	| 'null'

----------------------------------------------------------------------------------------

str_literal  ::= ''',{all_chars_from_utf8_if_Apostrophe_is_escaped} , ''';

int_literal  ::=  '0'
                 | digit_positive, {digit};

float_literal ::= int_literal, ".", digit, { digit };

digit          ::= digit_positive 
                | '0';

digit_positive ::= '1' 
                 | '2' 
                 | '3' 
                 | '4' 
                 | '5' 
                 | '6' 
                 | '7' 
                 | '8' 
                 | '9';
				  


identifier   ::= letter, {alphanumeric | '_'};
alphanumeric ::= letter | digit;
letter       ::= 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G'
               | 'H' | 'I' | 'J' | 'K' | 'L' | 'M' | 'N'
               | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U'
               | 'V' | 'W' | 'X' | 'Y' | 'Z' | 'a' | 'b'
               | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i'
               | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p'
               | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w'
               | 'x' | 'y' | 'z' ;

comment      ::= '@', {all_exept_newline}, newline;
newline      ::= '\n'
              |  '\r\n';


```