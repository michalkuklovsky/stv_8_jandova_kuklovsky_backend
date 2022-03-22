# MTAA Backend
## Online knihkupectvo BOKKS
### Autori: Alexandra Jandová a Michal Kuklovský

## Changes

- zmenene modely (odstranene prepojovacie tabulky a nahradene pomocou ManyToManyField)
- pridane /events /events/{id} a /search

## TODO
- implementovat soft-delete a brat ho do uvahy v GET requestoch
  - otazka co s PUT... upravit alebo vratit 404
- endpointy
  - /
  - /books
  - /books/{id}
  - /login
  - /logout
  - /profile/{id}
- yaml
  - pridat 'filter' do /search 
- naplnit db datami
- Figma (optional xD)
