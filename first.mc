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
@ x7 = '1.5a'; @ TypeCastError: [16, 6] : `str` to `int` : '1.5a'

x1: int = 1; @ Najpopularniejsze przypisanie stałej właściwego typu do zmiennej statycznej
x3: int = 1.0; @ Automatyczna konwersja z typu float do int i przypisanie wartości 1 do zmiennej niemutowalnej
x4: int = 1.4; @ - || -
x5: int = 1.5; @ to samo co `x5:int = 2;`
x6: int = 1.6; @ - || - 
@ x7: int = 1.23e3 @ LexerError
x2: int = '1'; @ Automatyczna konwersja z typu str do int i przypisanie wartości 1 do zmiennej statycznej
x2: int = '1.0'; @ Automatyczna konwersja z typu str do float do int i przypisanie wartości 1 do zmiennej statycznej
x2: int = '1.4'; @ Automatyczna konwersja z typu str do float do int i przypisanie wartości 1 do zmiennej statycznej
x2: int = '1.6'; @ Automatyczna konwersja z typu str do float do int i przypisanie wartości 1 do zmiennej statycznej

x1 = 1; @ ReassignmentError

x8: mut int = 1;
x9: mut int = '1';
x10: mut int = '1.0';
x11: mut int = '1.4';
x12: mut int = '1.5';
x13: mut int = '1.6';
x14: mut int = '1.6a'; @ TypeCastError: `str` to `int` : '1.6a'
x15: mut int = 'a1.6'; @ TypeCastError: `str` to `int` : 'a1.6'
x16: mut int = 1.23e3; @ LexerError


x7: mut int = 1;
x7 = 1;
x7 = 2; @ Da się przypisać wartość wielokrotnie do zmiennej mutowalnej
x7 = 99999999; @ Arbitralnie wybrany limit (W pythonie nie ma to duzego znaczenia)
x7 = 100000000; @ OverflowError

@ ------------------------------------

y1: float = 1.0;
y1: float = 1.0; @ RedefinitionError: variable `y1` has been already defined in this scope
y2: float = 1; @ int -> float
y3: float = '1'; @ str -> int -> float
y4: float = 1.4; @ float 
y5: float = '1.4'; @ str -> float
y6: float = '1.0'; @ str -> float (value convertable to int)
y7: float = '1.6a'; @ TypeCastError: `str` to `float`
y8: float = 1.23e3; @ LexerError
y9: float = 0.1 + 0.2;
y10: float = 0.1 + '0.2';
y11: float = '0.1' + '0.2'; @ TypeCastError: `str` to `float` : '0.10.2'
y12: float = '0.1' + 0.2;   @ TypeCastError: `str` to `float` : '0.10.2000000'
y13; float = 1 * 0.2; @ 0.0
y14: float = 0.2 * 1; @ 0.2
y15: float = 0.2 * 0.2; @ 0.04
y16: float = 2 * 0.2; @ 0
y17: float = 0.2 * 2; @ 0.4

y19: mut float = 1;
y19 = 1.0;
y19 = '1.0';
y19 = '1';
y19 = '1.4';
y19 = 99999999 + 1;       @ OverflowError
y19 = '99999999' + 1;     @  '999999991' OverflowError
y19 = 99999999.0 + 1;     @ To jest ok, float + int -> float + float
y19 = '99999999.0' + '1'; @ To jest ok, str + str -> konkatenacja i pózniej konwersja na float (99999999.01)
y19 = 1 + 99999999;       @  OverflowError
y19 = 1 + '99999999';     @  OverflowError
y19 = 1 + 99999999.0;     @ OverflowError
y19 = '1'+'99999999.0';  @ To jest ok, str + str -> konkatenacja i pózniej konwersja na float (199999999.0)
y19 = ⅓; @ LexerError
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

@ Język ma funkcje wbudowane (np: read, print):
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
@ 0.1000000
@ 0.2000000

@ Definicja funckji
nazwa_mojej_funckji_akceptuje_podkreslniki_i_cyfry_od_0_do_9(argument_1: int, argument_2: float): int
begin
    return argument_1 + argument_2;
end



@ Nazwa nie moze miec wiecej niz 60 (arbitralna liczba) znaków:

ta_nazwa_funkcji_ma_ponad_60_znakow_wiec_jest_nieakceptowalna(): int  
begin
    return 0;
end @ IdentifierTooLongError

@ dotyczy to wszystkich `identifier` - identyfikatorow:
ta_nazwa_zmiennej_ma_ponad_60_znakow_wiec_jest_nieakceptowalna: int = 0; @ IdentifierTooLongError

to_wywolanie_funkcji_ma_ponad_60_znakow_i_taka_funkcja_nie_istnieje; @ @ IdentifierTooLongError


null_function(arg1: str): null
begin

end

jakis_napis: mut str = 'ala';
print(jakis_napis); @ 'ala'

num1: mut int 


f(arg1: int) : int 
begin
    return arg1 + 1;
end
f(arg1: int, arg2: int): int
begin
    return arg1 + arg2 + 1;
end
f(arg1: int, arg2: int, arg3: int) : int
begin
    return arg1 + arg2 + arg3 + 1;
end

x : int = f(3,f(2,f(1)),3)

calculator() : null
begin
    print('Witaj w kalkulatorze');

    a: mut float;
    b: mut float;
    operacja: mut str;
    while 1
    begin
        print('First number:');
        a = read();
        print('Wybierz operację (+, -, *, /) : ');
        operacja = read();
        print('Second number:');
        b = read();
        if operacja == '+'
        begin
            print(a+b);
        end
        else
        begin 
            if operacja == '-'
            begin
                print(a-b);
            end
            else
            begin
                if operacja == '*'
                begin
                    print (a*b);
                end
                else
                begin
                    if operacja == '/'
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
        end
    end
end



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

monika: mut Student; @ zeby moc zmieniac wartosc pól mutowalnych zmienna musi byc mutowalna
monika.imie = 'Monika';
monika.nazwisko = 'Dąb';
monika.wiek = 20;
monika.srednia = 4.75;
@ mija rok
monika.wiek += 1;
monika.srednia = 4.67;


Leaf : struct
begin
    value : mut int
end

Node : struct
begin
    value : mut int; 
    left_child : mut Node = null;
    right_child : mut Node null;

end

BinaryTree : variant
begin
    l : Leaf;
    n : Node;
end

ll : Leaf;
lr : Leaf;
rl : Leaf;
rr : Leaf;
ll.value = 1;
lr.value = 2;
rl.value = 3;
rr.value = 4;

l : Node;
l.value = 5;
l.left_child = ll;
l.right_child = lr;

r : Node;
r.value = 6;
r.left_child = rl;
r.right_child = rr;

my_tree : Node;
my_tree.value = 7;
my_tree.left_child = l;
my_tree.right_child = r;

sum(tree : BinaryTree): int
begin
    visit tree
    begin
        case Leaf
        begin
            return tree.l.value
        end
        case Node
        begin
            return tree.n.value + sum(tree.n.left_child) + sum(tree.n.left_child);
        end
    end
end

jan : Student;
pawel.imie = 'jan';

Inner : struct
begin
    v : int;
end

Middle : struct
begin
    v : Inner;
end

Outer : struct
begin
    v : Middle;
end

l1 : Inner;
l1.v = 123;

l2 : Middle;
l2.v = l1;

l3 : Outer;
l3.v = l2;

print(l3.v.v.v);
