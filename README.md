# [triangle](https://github.com/amirouche/triangle)

Compilateur de LISP vers WebAssembly en Python.

![Interior of Louvre pyramide](https://images.unsplash.com/photo-1608494603993-d16a0841a78b?ixlib=rb-1.2.1&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=1920)

- The meta language is Python;
- The target language is WebAssembly.
- The object language is inspired from [R-1RK by Dr. John Nathan Shutt](https://web.cs.wpi.edu/~jshutt/kernel.html);

## Le langage objet: triangle

### Syntaxe

Le langage objet, appelle triangle, est un langage issue de la famille
LISP, herite de Scheme, et plus particulierement de Kernel tel que
decrit par le [docteur John Nathan Shutt dans
R-1RK](https://web.cs.wpi.edu/~jshutt/kernel.html).

Il utilise comme ponctuation:

- l'espace
- le retour a la ligne
- les parentheses
- les guillemets droits

Les guillemets droits delimitent les chaines de caracteres. Les
parentheses delimitent les listes. Les retours a la ligne sont traites
comme les espaces pour delimiter les elements d'une liste.

Une expression est une liste, donc une suite d'elements delimites par 
une paire de parentheses, peux contenir:

- un nombre
- une chaine de caractere
- un symbole
- une liste

Un symbole est definit comme n'etant ni un nombre, ni une chaine de 
caracteres, c'est-a-dire que tous ce qui n'est pas nombre, ou chaine
de caracteres forme un symbole. Remarquez qu'il n'y a jamais d'espace
ou de retour a a ligne dans un symbole. Un symbole peut etre vue comme
un mot.

### Semantique

L'introduction d'une variable nommee ce fait a l'aide du mot sans espace
`ilya`  qui se lit "il y a", exemple l'expression suivante definit `reponse`
comme etant le nombre 42:

```scheme
(ilya reponse 42)
```

Pour changer la valeur d'une variable, on utilise le mot `est`, exemple 
le code suivant fait suite au precedent, et etablit que `reponse` vaut 
un autre nombre super hero `1337`:

```scheme
(est reponse 1337)
```

Il est possible de repeter cette derniere operation autant de fois que 
necessaire, par exemple on peux associer `reponse` au nombre `2006`:

```scheme
(est reponse 2006)
```

Il existe des mots qui remplissent une fonctions tel que `chaine-attache`
qui va creer une chaine a partir d'au moins deux chaines. Le code suivant 
s'evalue a la valeur "bonjour le monde":

```scheme
(chaine-attache "bonjour" " le " "monde")
```

Il est possible de definir des mots qui prennent en compte des variables
passees par l'utilisateur, par exemple la fonction suivante `bonjour` va 
dire bonjour:

```scheme
(ilya bonjour (lambda (mister) (afficher (chaine-attache "Bonjour " mister))))
```

Ensuite on peux appeller `bonjour`:

```scheme
(bonjour "Amirouche")
```

Dans ce cas, cela va afficher:

```
Bonjour Amirouche
```
