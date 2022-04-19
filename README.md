# MTAA Backend
## Online knihkupectvo BOKKS
### Autori: Alexandra Jandová a Michal Kuklovský

## Changes

- zmenene modely (odstranene prepojovacie tabulky a nahradene pomocou ManyToManyField)
- pridane /events /events/{id} a /search

## TODO
- pridany endpoint na get obrazka
- do /books pridane do response 'quantity'
- pridany endpoint GET /cart
- pridany endpoint POST /cart
- pridany endpoint DELETE /cart
- pridany endpoint GET /orders
- pridany endpoint POST /orders
- pridany endpoint GET /orders/{id}