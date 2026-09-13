PRODUCTS = [
    {
        "id": "p001",
        "title": "Sluchátka SoundMax Pro X200",
        "description": (
            "Sluchátka SoundMax Pro X200 jsou bezdrátová sluchátka s aktivním "
            "potlačením hluku (ANC). Výdrž baterie je 30 hodin s vypnutým ANC "
            "a 20 hodin se zapnutým ANC. Podporují Bluetooth 5.3 a rychlé "
            "nabíjení - 10 minut nabíjení stačí na 5 hodin poslechu. "
            "Cena: 2 990 Kč."
        ),
    },
    {
        "id": "p002",
        "title": "Notebook ProBook 15 R7",
        "description": (
            "Notebook ProBook 15 R7 má procesor AMD Ryzen 7, 16 GB RAM a "
            "512 GB SSD disk. Displej má úhlopříčku 15,6 palce s rozlišením "
            "Full HD. Výdrž baterie při běžném použití je přibližně 8 hodin. "
            "Váha notebooku je 1,7 kg. Cena: 18 990 Kč."
        ),
    },
    {
        "id": "p003",
        "title": "Chytré hodinky FitPulse 4",
        "description": (
            "Chytré hodinky FitPulse 4 měří tep, kvalitu spánku a saturaci "
            "kyslíku v krvi. Jsou vodotěsné do 50 metrů (5 ATM). Výdrž "
            "baterie je až 7 dní při běžném používání. Kompatibilní s "
            "Android i iOS. Cena: 1 590 Kč."
        ),
    }
]

FAQ = [
{
        "id": "f001",
        "title": "Reklamace zboží",
        "description": (
            "Zboží zakoupené na e-shopu lze reklamovat do 24 měsíců od "
            "zakoupení. Reklamaci lze podat online přes zákaznický účet "
            "nebo osobně na prodejně. Vyřízení reklamace trvá standardně "
            "do 30 dnů. V případě uznané reklamace nabízíme opravu, výměnu "
            "za nový kus, nebo vrácení peněz."
        ),
    },
    {
        "id": "f002",
        "title": "Vrácení zboží do 14 dnů",
        "description": (
            "Zboží zakoupené online lze vrátit bez udání důvodu do 14 dnů "
            "od převzetí. Zboží musí být nepoškozené a v původním obalu, "
            "pokud je to možné. Peníze za vrácené zboží jsou vráceny do "
            "14 dnů od doručení vráceného zboží zpět na sklad."
        ),
    },
    {
        "id": "f003",
        "title": "Stav objednávky",
        "description": (
            "Stav objednávky lze zkontrolovat v zákaznickém účtu v sekci "
            "'Moje objednávky', nebo pomocí sledovacího čísla zaslaného "
            "e-mailem po expedici zásilky. Standardní doba doručení je "
            "1-3 pracovní dny od expedice."
        ),
    },
]

def get_documention():
    documents = []
    for product in PRODUCTS:
        documents.append(
            {
                "id": product["id"],
                "typ": "product",
                "title": product["title"],
                "description": product["description"],
            }
        )
    for faq in FAQ:
        documents.append(
            {
                "id": faq["id"],
                "typ": "faq",
                "title": faq["title"],
                "description": faq["description"],
            }
        )
    return documents