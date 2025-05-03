# Elektros energijos jėgainių valdymo sistema

## Įvadas

Šis projektas – tai objektinio programavimo principus demonstruojanti valdymo sistema, leidžianti efektyviai administruoti skirtingas jėgainių rūšis (saulės, vėjo, branduolinės, anglies, vandens, šiukšlių perdirbimo). Sistema leidžia dinamiškai pridėti ir pašalinti jėgaines, analizuoti jų duomenis, bei įjungti optimalias jėgaines pagal vartotojo pateiktą elektros poreikį.

## Programos paleidimas

1. Atsisiųskite visus failus iš GitHub saugyklos.
2. Įsitikinkite, kad turite įdiegtą **Python 3**.
3. Paleiskite programą su `python` komanda.
4. Norėdami matyti istoriją, naudokite `show_history()` metodą.

## Programos duomenys

- Kalba: Python 3
- Objektinis programavimas (OOP)
- Projektavimo šablonas: **Factory Method**
- Failų įrašymas: rezultatai saugomi `history.txt`
- Testavimas su `unittest` biblioteka
- Kodo stilius: laikytasi PEP8 standarto

## Objektinio programavimo principai

### Abstrakcija

Naudojama `PowerPlant` abstrakti bazinė klasė, kuri apibrėžia bendras jėgainės savybes ir metodus.

```python
class PowerPlant(ABC):
    @abstractmethod
    def fuel_type(self):
        pass
```

---

### Paveldėjimas

Kiekviena jėgainės klasė paveldi `PowerPlant` ir turi specifinę degalų rūšį.

```python
class SolarPlant(PowerPlant):
    def fuel_type(self):
        return "Solar Energy"
```

---

### Polimorfizmas

Kodas naudoja `fuel_type()` metodą, kuris veikia nepriklausomai nuo jėgainės tipo.

```python
for plant in self.plants:
    print(plant.fuel_type())  # Gali būti saulės, vėjo, branduolinė ir kt.
```

---

### Inkapsuliacija

Kiekviena klasė turi privačius atributus, kuriuos valdo per metodus (`start()`, `shutdown()`).

```python
def start(self):
    self.status = "active"
```

---

## Projektavimo šablonas

Naudotas **Factory Method** šablonas (`PowerPlantFactory`) leidžia kurti objektus pagal paduotą tekstinį tipą.

```python
plant = PowerPlantFactory.create_plant("solar", "SunFarm", "Spain", 500, 30, True)
```

Tai leidžia išvengti tiesioginių `SolarPlant(...)` kvietimų.

---

## Rezultatai

- Sukurta funkcionali sistema, galinti:
  - Valdyti skirtingas jėgaines
  - Parinkti optimalų jų rinkinį pagal elektros poreikį
  - Skaičiuoti kainą ir švarios energijos procentą
  - Išsaugoti kiekvieno paleidimo rezultatą faile
- Visi pagrindiniai reikalavimai įgyvendinti.
- Programa sėkmingai ištestuota su `unittest`.

---

## Išvados

Projekto metu sėkmingai pademonstruota:
- Gebėjimas dirbti su OOP principais
- Praktinis projektavimo šablonų taikymas
- Kodo struktūrizavimas ir dokumentavimas
- Failų įrašymo ir testavimo integracija

---

## Autorius

- Mangirdas Rulis EEF-24
- Objektinis programavimas, 2025
