@ typowanie słabe
@ zmienne są domyślnie niemutowalne tzn aeby zmienna była mutowalna trzeba to zaznaczyć
@ Argumenty funkcji są przekazywane domyślnie przez wartość a nie przez referencję


x0: int; @ Deklaracja istnienia zmiennej statycznej ale bez przypisywania wartości
x0 = 1;
x1: int;
x1 = 1.0;
x2: int;
x2 = 1.4;
x3: int;
x3 = 1.5;
x4: int;
x4 = 1.6;
x5: int;
x5 = '1.0';
x6: int;
x6 = '1.5';
x7: int;
x7 = '1.5a'; @ TypeCastError: "Can not automatically cast type: `str` into type: `int` ->  x7 = '1.5a';"



x1: int = 1; @ Najpopularniejsze przypisanie stałej właściwego typu do zmiennej statycznej
x3: int = 1.0; @ Automatyczna konwersja z typu float do int i przypisanie wartości 1 do zmiennej statycznej
x4: int = 1.4; @ - || -
x5: int = 1.5; @ to samo co `x5:int = 2;`
x6: int = 1.6; @ - || - 
x7: int = 1.23e3: @ LexerError: "Invalid token 'e' in numeric literal"
x2: int = '1'; @ Automatyczna konwersja z typu str do int i przypisanie wartości 1 do zmiennej statycznej
x2: int = '1.0'; @ Automatyczna konwersja z typu str do float do int i przypisanie wartości 1 do zmiennej statycznej
x2: int = '1.4'; @ Automatyczna konwersja z typu str do float do int i przypisanie wartości 1 do zmiennej statycznej
x2: int = '1.5'; @ Automatyczna konwersja z typu str do float do int i przypisanie wartości 2 do zmiennej statycznej
x2: int = '1.6'; @ Automatyczna konwersja z typu str do float do int i przypisanie wartości 2 do zmiennej statycznej

x1 = 1; @ ReassignmentError: "Cannot reassign a value to a non mutable variable. Variable `x1` is of type: `int` not `mut int`"

x8: mut int = 1;
x9: mut int = '1';
x10: mut int = '1.0';
x11: mut int = '1.4';
x12: mut int = '1.5';
x13: mut int = '1.6';
x14: mut int = '1.6a'; @ TypeCastError: "Can not automatically cast `1.6a` into type: `mut int` "
x15: mut int = 'a1.6'; @ TypeCastError: "Can not automatically cast `a1.6` into type: `mut int` "
x16: mut int = 1.23e3; @ LexerError: "Invalid token 'e' in numeric literal"


x7: mut int = 1;
x7 = 1;
x7 = 2; @ Da się przypisać wartość wielokrotnie do zmiennej mutowalnej
x7 = 99999999; @ Arbitralnie wybrany limit (W pythonie nie ma to duzego znaczenia)
x7 = 100000000; @ OverflowError: "Trying to assign not supported value to variable: `x7=100000000`"

@ ------------------------------------

y1: float = 1.0;
y1: float = 1.0; @ RedefinitionError: "`y1` has been already defined in this scope"
y2: float = 1; @ int -> float
y3: float = '1'; @ str -> int -> float
y4: float = 1.4; @ float 
y5: float = '1.4'; @ str -> float
y6: float = '1.0'; @ str -> float (value convertable to int)
y7: float = '1.6a'; @ TypeCastError: "Can not automatically cast `1.6a` into type: `float` "
y8: float = 1.23e3; @ LexerError: "Invalid token 'e' in numeric literal"
y9: float = 0.1 + 0.2;
y10: float = 0.1 + '0.2';
y11: float = '0.1' + '0.2';
y12: float = '0.1' + 0.2;
y13; float = 1 * 0.2;
y14: float = 0.2 * 1;
y15: float = 0.2 * 0.2;
y16: float = 2 * 0.2;
y17: float = 0.2 * 2;
y18: float = power(10.0, 308);
y18: float = power(10.0, 309); @ OverflowError

y19: mut float = 1;
y19 = 1.0;
y19 = '1.0';
y19 = '1';
y19 = '1.4';
y19 = '1.6a'; TypeCastError: "Can not automatically cast `1.6a` into type: `float`"
y19 = 1.23e3; @ LexerError: "Invalid token 'e' in numeric literal"
y19 = '10.0*5'; TypeCastError: "Can not automatically cast `10.0*5` into type: `float`"
y19 = 99999999 + 1;  OverflowError
y19 = '99999999' + 1;  OverflowError
y19 = 99999999.0 + 1; To jest ok, float + int -> float + float
y19 = '99999999.0' + '1'; To jest ok, str + str -> konkatenacja i pózniej konwersja na float (99999999.01)
y19 = 1 + 99999999;  OverflowError
y19 = 1 + '99999999';  OverflowError
y19 = 1 + 99999999.0; To jest ok, int + float -> float + float
y19 = '1'+'99999999.0'; To jest ok, str + str -> konkatenacja i pózniej konwersja na float (199999999.0)
y19 = ⅓; LexerError: "Invalid token `⅓` in numeric literal"
y19 = '⅓'; TypeCastError: "Can not automatically cast `⅓` into type: `float`

s0: str = '';
s1: str = '1';
s2: str = '⅓';
s3: str = 'Ala ma kota';
s4: str = 'Ala ma kota' + 'i psa';

@ Konkatenacja stringow
ilosc_psow: mut int = 1;
msg: mut str = 'Ala ma ' + ilosc_psow + ' ps';
if ilosc_psow == 1
begin 
    msg += 'a'
end 
else 
    if 1 < ilosc_psow & ilosc_psow < 5
    begin
        msg += 'y';
    end
else
begin
    msg += 'ów'
end
msg += '.'

@ -----------------------------------------

@ Język ma funkcje wbudowane (np: read, print, ref, power...):
@ if oraz prezentacja zakresów oraz wartosc logiczna 1, uruchomienie funckji print
if 1
begin
    y1: float = 1.0; @ y1 zdefiniowane ale w innym zakresie
    print(y1);
    if 1
    begin
        y1: float = 2.0; @ y1 zdefiniowane ale w innym zakresie
        print(y1);
    end
end
@ Output:
@ 0.1
@ 0.2

@ Definicja funckji
nazwa_mojej_funckji_akceptuje_podkreslniki_i_cyfry_od_0_do_9(argument_1: int, argument_2: float): int
begin
    return argument_1 + argument_2;
end



@ Nazwa nie moze miec wiecej niz 60 (arbitralna liczba) znaków:

ta_nazwa_funkcji_ma_ponad_60_znakow_wiec_jest_nieakceptowalna(): int  @ LexerError: "Identifier: `ta_nazwa_funkcji_ma_ponad_60_znakow_wiec_jest_nieakceptowalna` has more that 60 characters!"
begin
    return 0;
end

@ dotyczy to wszystkich `identifier` - identyfikatorow:
ta_nazwa_zmiennej_ma_ponad_60_znakow_wiec_jest_nieakceptowalna: int = 0; @ LexerError: "Identifier: `ta_nazwa_zmiennej_ma_ponad_60_znakow_wiec_jest_nieakceptowalna` has more that 60 characters!"

to_wywolanie_funkcji_ma_ponad_60_znakow_i_taka_funkcja_nie_istnieje; LexerError: "Identifier: `to_wywolanie_funkcji_ma_ponad_60_znakow_i_taka_funkcja_nie_istnieje` has more that 60 characters!"


change_first_letter_to_next(string_to_change: str): null
begin

end



@ Funkcja zwracajaca nic, prezentacja typu null, zazwyczaj uzyta razem z argumentami mutowalnymi. Funkcja null nie musi miec return, prezentacja while oraz indeksowanie typu mut str
to_upper(string_to_change: mut str) : null
begin
    i: mut int = 0;
    l: int = string_to_change.length;
    current_letter: mut str;
    while i < l:
    begin
        current_letter = string_to_change[i]; @ przekazanie znaku przez wartosc
        if 97 <= current_letter & current_letter <= 122 @ ASCII 97 to `a` oraz ASCII 122 to `z`. Porównanie str do int to Porównanie pierwszej litery str
        begin
            current_letter -= 32 
            string_to_change[i] = current_letter 
        end
    end
end

jakis_napis: mut str = 'ala';
print(jakis_napis); @ 'ala'
to_upper(jakis_napis);
print(jakis_napis); @ 'ala' - przekazalismy jakis napis przez wartosc

to_upper(ref(jakis_napis)); @ nawias dla czytelnosci argumentow: to_upper przyjmuje jeden argument, ref tez. 
print(jakis_napis); 'ALA' - przekazalismy przez referencje 

int add_arg2_to_arg1(arg1: mut int, arg2:int)
begin
    return ref(arg1) + arg2;
end

num1: mut int 








one_arg_function(arg1: int) : int 
begin
    return arg1 + 1;
end
two_arg_function(arg1: int, arg2: int): int
begin
    return arg1 + arg2 + 1;
end
three_arg_function(arg1: int, arg2: int, arg3: int) : int
begin
    return arg1 + arg2 + arg3 + 1;
end

case1 : mut int = one_arg_function(two_arg_function(three_arg_function(1, 2, 3), 4));
case2 : mut int = three_arg_function(two_arg_function(one_arg_function(1), 2), 3, 4);

read_float() : float @ - mechanizm wyjątków + funckja wbudowana read (return read automatycznie konwertuje na zadeklarowany typ zwracany przez funkcje)
begin
    print('Write number:');
    while 1
    begin
        try
        begin
            return read(); 
        end
        catch TypeCastError
        begin
            print('Can not interpret it as float. Try again');
        end
end

@ Funckja kalkulatora - uzycie wczesniej zdefiniowanej funkcji bezargumentowej (read_float) + funkcji 1-argumentowej wbudowanej (print) która autmatycznie konwertuje float na str
calculator() : null
begin
    print('Witaj w kalkulatorze');

    a: mut float;
    b: mut float;
    operacja: mut str;
    while 1
    begin
        a = read_float();
        print('Second number:');
        print('Wybierz operację (+, -, *, /) : ');
        read(operacja);
        if operacja == '+'
        begin
            print(a+b);
        end
        elif operacja == '-'
        begin
            print(a-b);
        end
        elif operacja == '*'
        begin
            print (a*b);
        end
        elif operacja == '/'
        begin
            if b == 0
            begin
                print('Dzielenie przez 0');
            end
            else
            begin
                print(a/b);
            end
        end
        else
        begin
            print('Operation' operacja 'is not supported! Try again')
        end
    end
end

@ int + int <=> dodawanie intów
@ float + float <=> dodawanie liczb float
@ int + float <=> float + float
@ int + str <=> zamieniasz str na liczbe jesli sie da
@ float + int <=> float + float
@ float + str <=> zamieniasz str na liczbe jesli sie da
@ str + str <=> konkatenacja stringow
@ str + int <=> potraktuj pierwszy znak jak liczbe i dodaj do niej int-a. nastepnie potraktuj jak stringa
@ str + float <=> str + int

@ int - int <=> odejmowanie intów
@ float - float <=> odejmowanie liczb float
@ int - float <=> float - float
@ int - str <=> zamieniasz str na liczbe jesli sie da
@ float - int <=> float - float
@ float - str <=> zamieniasz str na liczbe jesli sie da
@ str - str <=> usun pierwsze wystapienie drugiego stringa z pierwszego.
@ str - int <=> potraktuj pierwszy znak jak liczbe i odejmij do niej int-a. nastepnie potraktuj jak stringa
@ str - float <=> str - int

@ int * int <=> mnozenie intow
@ float * float <=> mnozenie floatow
@ str * int <=> wynik to zwielokrotnienie stringa int razy
@ str * float <=> str * int
@ str * str <=> zamien drugiego stringa na liczbe, jesli nie to TypeCastErrort
@ float * int <=> float * float
@ float * str <=> zamien string na liczbe jesli sie da, jesli nie to TypeCastError


NazwaStruktury: struct
begin
    nazwa_atrybutu1: int;
    nazwa_atrybutu2: mut str;
    nazwa_atrybutu3: mut float = 1.1;
end

Student: struct
begin
    imie: str;
    nazwisko: str;
    wiek: mut int;
    srednia: mut float;
end

pawel: Student;
pawel.imie = 'Pawel';
pawel.nazwisko = 'Kowalski';
pawel.wiek = 21;
pawel.srednia = 4.254;

monika: mut Student;
monika.imie = 'Monika';
monika.nazwisko = 'Dąb';
monika.wiek = 20;
monika.srednia = 4.75;
@ mija rok
monika.wiek += 1;
monika.srednia = 4.67;




int_lub_str1: mut variant(int, str) = 1;
print(int_lub_str1); @ '1' - 1 zamienione na '1'
print(type(int_lub_str1.get_value())); @ int

int_lub_str2: mut variant(int, str) = '1';
print(type(int_lub_str2.get_value())); @ str


@ Funkcja z argumentami przekazywanymi przez referencje (typy proste)
@ Struktura
@ Czy struktura musi być zdefiniowana wyzej niz jest uzywana skoro mamy leniwie parsować input?
@ Wariant to ENUM? Czy po prostu to jest klasa przechowywyjąca wartość jednej z podanych klas?
@ Funkcje z argumentami typu nieprostego - struktury + warianty
