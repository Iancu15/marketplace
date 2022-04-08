Nume: Iancu Alexandru-Gabriel
Grupă: 333CB

# Tema 2

Organizare
-
1. Consumer-Producer

Consumatorul isi parcurge cosurile din lista si pentru fiecare cere un id nou folosind functia new_cart(),
apoi parcurge operatiile de 'add' sau 'remove'. Pentru fiecare operatie pentru o cantitate q se va apela
functia add_cart() sau remove_cart() de q ori, o data pentru fiecare unitate de produs de tipul respectiv.
In cazul in care primeste False la add_cart() asteapta intr-un while pana produsul respectiv pe care vrea
sa il adauge e disponibil in marketplace. Dupa ce a ajuns la cosul final din iteratia curenta va plasa
comanda si afiseaza ce a cumparat.

Producatorul isi parcurge produsele pe care si le poate procesa si le publica unul cate unul la fel cum
consumatorul adauga in cos produsele unul cate unul. Daca coada sa e plina, atunci asteapta pana publish()
intoarce True lucru ce semnifica ca s-a mai golit din coada si poate publica. Dupa ce se termina lista de
produse o parcurge din nou facand acelasi lucru prezentat anterior. Face acest lucru la infinit, producer-ul
fiind un proces de tip daemon.

2. Marketplace

Pentru inregistrarea de cosuri si producatori se foloseste un id ce incepe de la 1 si e incrementat
pentru fiecare nou cos sau producator inregistrat. Piata se simuleaza folosind un dictionar de produse
declarat in clasa ProductDict ce reprezinta un dictionar ce mapeaza un produs la un alt dictionar in
care se tine cont de cantitatea cu care a contribuit fiecare producator pe piata respectiva. Ca exemplu
am test-ul pentru put din ProductDict:

def test_put(self):
    quantity_dict1 = {1: 50, 2: 50, 3: 50, 4: 50, 5: 50}
    quantity_dict2 = {2: 50, 3: 50, 4: 50, 5: 50, 6: 50}
    product_dict = {self.product1: quantity_dict1, self.product2: quantity_dict2}
    self.assertEqual(self.product_dict.dict, product_dict)

Dictionarul de produse are 2 produse, product1 si product2. Fiecare produs are un dictionar de cantitate
asociat. quantity_dict1 ne spune ca producatorii cu id-urile de la 1 la 5 fiecare contribuie cu o cantitate
de 50 din produsul respectiv. Referitor la piata asta inseamna ca fiecare a plasat o cantitate de 50 din produsul
respectiv pe piata.

Pentru a tine cont de dimensiunea cozii producatorilor folosesc un dictionar ce mapeaza id-urile producatorilor
la dimensiunea cozilor lor. La publicarea unui produs de catre producator se incrementeaza dimensiunea cozii sale si
la plasarea comenzii de catre un consumator, pentru fiecare produs din cos produs de acel producator, se va
scadea cu cantitatea produsului respectiv dimensiunea cozii.

Pentru stocarea continutului cosurilor folosesc un dictionar ce are ca chei id-ul cosului si ca valoare continutul
cosului. Continutul cosului il reprezint folosind un ProductDict ca si piata, lucru ce are sens pentru ca cosul
e doar bucata din piata rezervata de un consumator. Adaug sau scot din cosul unui consumator modificand
ProductDict-ul aferent id-ului sau in dictionarul de cosuri. Fac rost de ProductDict-ul unui cart_id apeland functia
get_cart() si apoi folosesc functiile de put() si remove() pe obiectul primit. Nu am nevoie sa apelez lock pe
intregul dictionar de cosuri pentru a modifica un cos pentru ca fiind obiecte au spatiul lor de memorie si nu mai
au treaba cu dictionarul de cosuri dupa ce au fost pusi in el(ii adaug doar o singura data la inceput). Doar cand
il accesez prin intermediul get_cart() trebuie sa folosesc lock pe dictionarul de cosuri.

3. Utilitatea temei

Tema a fost utila pentru a maiestri lucrul cu dictionare sincrozinate in python si pentru a ma familiariza intr-un mod
mai practic cu Producer-Consumer. Mi s-a parut o idee foarte buna sa pui studentul sa-si faca propriul logging si propriile
unit tests, lucruri folosite in industrie. In special partea de unit tests pentru ca partea de testare este aproape neatinsa
in facultate.

4. Eficienta temei

Consider tema ca este destul de eficienta. Am incercat sa folosesc lock-uri doar unde e necesar, motiv pentru care am decis sa
nu folosesc lock-uri pe intregul dictionar de cosuri cand modific un cos din el, ci sa fac rost de cos folosind lock pe
dictionarul de cosuri si apoi sa il modific independent de dictionarul de cosuri. In sensul asta o sincronizare redundanta
este cea din ProductDict() pentru cosuri pentru ca un cos e accesat de acelasi consumator mereu pentru ca cosurile au
id-uri unice pe perioada intregei rulari. Insa piata e accesata de mai multe thread-uri asa ca pentru ea era nevoie
ca ProductDict() sa fie thread safe. Am decis sa o las thread safe pentru o mai frumoasa incapsulare, eu facand clasa ProductDict
pentru a putea folosi put() si remove() fara a ma mai gandi cum am implementat in spate. Daca tineam eu lock in Marketplace
pentru piata se strica din incapsulare.

Faptul ca am folosit dictionare oriunde se putea adauga la eficienta pentru ca dictionarele in python sunt hash map-uri si asa
au accesarea si modificarea O(1), lucru ce e mult mai eficient decat folosirea de liste si cautarea de O(n) in ele.


Implementare
-

Intregul enunt al temei este implementat.

1. Dificultati intampinate

Dificultatea principala a fost sa-mi dau seama cum sa-mi organizez tema, incepusem sa am prea multe dictionare si lock-uri si
era complicat sa le urmaresc in cod. Am observat ca cosurile si piata ajung sa aiba aceeasi structura asa cam decis sa
creez o clasa pentru ele ca sa nu mai repet cod de fiecare data cand puneam un produs sau scoteam un produs din ele si pentru
a urmari mai usor codul scris. Astfel am creat ProductDict si mi-a fost mult mai usor sa incerc sa scriu bine o singura
data put() si remove() in loc de n ori de cate ori repetam functionalitatea in Marketplace inainte. Am pun si un lock intern
astfel incat toata implementarea sa fie incapsulata si sa pot modifica linistit ProductDict-urile. Codul este astfel mult mai
usor de urmarit pentru ca sunt doar cateva linii de put() si remove() per functie si totul are mai mult sens.

Resurse utilizate
-

* M-am folosit de link-urile puse in enuntul temei.

Git
-
1. Link către repo-ul de git

https://github.com/Iancu15/marketplace
