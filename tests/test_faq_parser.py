import unittest
from unittest.mock import mock_open, patch
import textwrap

from prompt_model.faq_parser import parse_file_generator

class ParseFileTest(unittest.TestCase):
    def test_parse_file_generator(self):
        mock_file_content1 = textwrap.dedent("""
            # bezpieczeństwo # https://www.mbank.pl/bezpieczenstwo/

            ## bankowość internetowa # https://www.mbank.pl/bezpieczenstwo/bezpieczna-bankowosc-internetowa/

            ### Czym jest przeglądarka internetowa?
            Przeglądarka internetowa to program, który umożliwia wyświetlanie stron internetowych (np. Chrome, Mozilla Firefox, Opera).
        """)
        mock_file_content2 = textwrap.dedent("""
        # całodobowe wsparcie # https://www.mbank.pl/kontakt/oferta-indywidualna/

        ## zastrzeż kartę lub dowód osobisty # https://www.mbank.pl/bezpieczenstwo/sprawdz-co-robic/

        ### Nie mogę znaleźć karty lub ktoś mi ją ukradł, co mam zrobić?
        - tymczasowo zablokuj kartę. Skorzystaj z tymczasowej blokady, gdy nie masz pewności, gdzie jest Twoja karta. Jeśli znajdziesz kartę, w każdej chwili możesz ją odblokować i dalej z niej korzystać.  

        - zastrzeż kartę. Zastrzeż kartę, gdy obawiasz się, że ktoś może z niej skorzystać (np. ktoś Ci ją ukradł lub podejrzewasz, że ktoś zdobył dane Twojej karty oraz w sytuacji gdy ktoś znalazł Twoją kartę i Ci ją oddał - w takiej sytuacji również rozważ zastrzeżenie karty, ponieważ taka osoba zna dane Twojej karty i może je wykorzystać bez Twojej wiedzy). Zastrzeżenie karty jest nieodwracalne - nikt już z niej nie skorzysta.  

        - zgłoś sprawę na policję lub do prokuratury, jeśli widzisz transakcje, których nie rozpoznajesz  

        Powiadom o sprawie policję lub prokuraturę. Możesz skorzystać z przygotowanego przez nas [wzoru](https://www.mbank.pl/pdf/inne/formularz-zgloszenia-zawiadomienia.pdf).  

        Możesz przesłać nam zaświadczenie, że policja/prokuratura rozpoczęły postępowanie: 

        - e-mailem na adres: [kontakt@mbank.pl](mailto:kontakt@mbank.pl)
            
        - pocztą na adres: mBank S.A. Bankowość Detaliczna, Skrytka Pocztowa 2108, 90-959 Łódź
            

        Jeśli przekażesz policji lub prokuraturze [upoważnienie](https://www.mbank.pl/pdf/inne/upowaznienie-dla-organow-scigania.pdf), które zwalnia nas z tajemnicy bankowej, będziemy mogli przekazywać materiały i wyjaśnienia, które pomogą rozwiązać Twoją sprawę.  """)

        with patch("builtins.open", mock_open(read_data=mock_file_content1)):
            result = list(parse_file_generator("dummy_path.txt"))
            result_string = " ".join(result)

        self.assertEqual(result_string, "[DZIEDZINA] bezpieczeństwo > bankowość internetowa\n[PYTANIE] Czym jest przeglądarka internetowa?\n[ODPOWIEDŹ] Przeglądarka internetowa to program, który umożliwia wyświetlanie stron internetowych (np. Chrome, Mozilla Firefox, Opera).")

        with patch("builtins.open", mock_open(read_data=mock_file_content2)):
            result = list(parse_file_generator("dummy_path.txt"))
            result_string = " ".join(result)
        print(result_string)
        self.assertEqual(result_string, """[DZIEDZINA] całodobowe wsparcie > zastrzeż kartę lub dowód osobisty
[PYTANIE] Nie mogę znaleźć karty lub ktoś mi ją ukradł, co mam zrobić?
[ODPOWIEDŹ] - tymczasowo zablokuj kartę. Skorzystaj z tymczasowej blokady, gdy nie masz pewności, gdzie jest Twoja karta. Jeśli znajdziesz kartę, w każdej chwili możesz ją odblokować i dalej z niej korzystać.
- zastrzeż kartę. Zastrzeż kartę, gdy obawiasz się, że ktoś może z niej skorzystać (np. ktoś Ci ją ukradł lub podejrzewasz, że ktoś zdobył dane Twojej karty oraz w sytuacji gdy ktoś znalazł Twoją kartę i Ci ją oddał - w takiej sytuacji również rozważ zastrzeżenie karty, ponieważ taka osoba zna dane Twojej karty i może je wykorzystać bez Twojej wiedzy). Zastrzeżenie karty jest nieodwracalne - nikt już z niej nie skorzysta.
- zgłoś sprawę na policję lub do prokuratury, jeśli widzisz transakcje, których nie rozpoznajesz
Powiadom o sprawie policję lub prokuraturę. Możesz skorzystać z przygotowanego przez nas [wzoru](https://www.mbank.pl/pdf/inne/formularz-zgloszenia-zawiadomienia.pdf).
Możesz przesłać nam zaświadczenie, że policja/prokuratura rozpoczęły postępowanie:
- e-mailem na adres: [kontakt@mbank.pl](mailto:kontakt@mbank.pl)
- pocztą na adres: mBank S.A. Bankowość Detaliczna, Skrytka Pocztowa 2108, 90-959 Łódź
Jeśli przekażesz policji lub prokuraturze [upoważnienie](https://www.mbank.pl/pdf/inne/upowaznienie-dla-organow-scigania.pdf), które zwalnia nas z tajemnicy bankowej, będziemy mogli przekazywać materiały i wyjaśnienia, które pomogą rozwiązać Twoją sprawę.""")