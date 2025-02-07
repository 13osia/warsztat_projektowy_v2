import streamlit as st
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import uuid
import time 



def send_email(subject, body, recipient):
    sender_email = "ankieta831@gmail.com" 
    sender_password = "elhg snux ihtn lnnx" 

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient, message.as_string())
            print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print(f"SMTP error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def go_to_summary():
    st.session_state.page = "summary"

def main():
    st.set_page_config(page_title="Ankieta", page_icon="📋", layout="centered")

    if 'responses' not in st.session_state:
        st.session_state['responses'] = {}

    if 'page' not in st.session_state:
        st.session_state.page = 'start'

    if 'button_clicked' not in st.session_state:
        st.session_state.button_clicked = False

    if 'group' not in st.session_state:
        st.session_state.group = random.choice(['experimental', 'control'])

    if 'task_number' not in st.session_state:
        st.session_state.task_number = 1

    if 'user_id' not in st.session_state:
        st.session_state.user_id = f"user_{uuid.uuid4().hex[:8]}"

    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()

    def go_to_next_page(next_page):
        st.session_state.page = next_page
        st.session_state.button_clicked = False

    def go_to_next_task():
        if 'task_number' not in st.session_state:
            st.session_state.task_number = 1

        if st.session_state.task_number < 12:
            st.session_state.task_number += 1
            st.session_state.page = 'task_page'
        else:
            st.session_state.page = 'thank_you'

    task_images = [
        "Zadanie 2.png",  
        "Zadanie 2.png",
        "Zadanie 3.png",
        "Zadanie 4.png",
        "Zadanie 5.png",
        "Zadanie 6.png",
        "Zadanie 7.png",
        "Zadanie 8.png",
        "Zadanie 9.png",
        "Zadanie 10.png",
        "Zadanie 11.png",
        "Zadanie 12.png", 
    ]

    if st.session_state.page == 'start':
        st.title("Ocena trafności decyzji w zadaniach wyboru pralek.")
        st.write("""
        Nazywam się Zuzanna Bosiacka i jestem studentką Uniwersytetu SWPS na kierunku psychologia i informatyka. Przeprowadzam badanie, które jest częścią mojej pracy dyplomowej. Celem tego badania jest zrozumienie, jak ludzie oceniają decyzje dotyczące wyboru produktów, takich jak pralki, na podstawie dostępnych informacji i rekomendacji.

        Podczas badania zostaniesz poproszona/y o wykonanie 12 zadań. W każdym z nich zobaczysz opis trzech pralek oraz wybór jednej z nich jako najlepszej. Twoim zadaniem będzie dokładne zapoznanie się z przedstawionymi danymi i na ich podstawie ocena, czy zgadzasz się z wyborem rekomendowanej pralki.

        Proszę, abyś przy ocenie wyborów kierował/a się wyłącznie przedstawionymi informacjami i analizą danych, a nie swoimi osobistymi preferencjami. Liczy się Twoja opinia o decyzji bazującej na obiektywnych kryteriach, które znajdziesz w opisie zadania.

        Twoim zadaniem będzie:

        1. Zapoznanie się z opisami pralek i rekomendacją najlepszej z nich.
        2. Odpowiedź na pytania dotyczące tego, czy zgadzasz się z wyborem oraz co o nim myślisz.

        Twoje zdanie jest dla mnie ważne. Odpowiadaj szczerze i bez obaw – każda odpowiedź ma znaczenie. Twoje odpowiedzi pomogą nam lepiej zrozumieć proces podejmowania decyzji oraz ich ocenę. Całość zajmie około 15 min.

        Udział w badaniu jest całkowicie dobrowolny. Możesz przerwać udział w dowolnym momencie, bez podawania przyczyny.

        Wszystkie zebrane dane będą traktowane poufnie i wykorzystywane wyłącznie do celów naukowych. Twoje odpowiedzi pozostaną anonimowe i nie będą w żaden sposób powiązane z Twoją tożsamością.
        """)

        st.markdown(
            "<span style='color: #77AD78; font-weight: bold;'>Przechodząc do kolejnych stron badania, wyrażasz zgodę na udział i potwierdzasz, że zapoznałaś/eś się z powyższymi informacjami.</span>",
            unsafe_allow_html=True
        )

        if st.button("Rozpocznij"):
            go_to_next_page('question_1')

    elif st.session_state.page == 'question_1':
        st.title("Kilka podstawowych informacji o Tobie")

        gender = st.radio(
            "Płeć:", ["Kobieta", "Mężczyzna", "Inna/Inny"], key="gender", index=None
        )

        age = st.text_input("Ile masz lat?:", key="age")

        education = st.radio(
            "Wykształcenie:", [
                "Podstawowe",
                "Średnie",
                "Wyższe (licencjat, inżynier)",
                "Wyższe (magister, doktor)"
            ], key="education", index=None
        )

        st.markdown("Ile lat edukacji ukończyłeś/aś do tej pory?")
        st.markdown("- np: 6 lat szkoły podstawowej, 3 lata gimnazjum, 3 lata liceum, 2 lata studiów = **14 lat**")

        education_years = st.text_input("Odpowiedź otwarta:", key="education_years")


        profession = st.radio(
            "Zawód:", [
                "Uczeń/Student",
                "Pracuję zawodowo (pełny etat)",
                "Pracuję zawodowo (część etatu)",
                "Bezrobotny/a",
                "Inny (proszę podać)"
            ], key="profession", index=None
        )

        if profession == "Inny (proszę podać)":
            other_profession = st.text_input("Podaj swój zawód:", key="other_profession")
        else:
            other_profession = None  

        location = st.radio(
            "Miejsce zamieszkania:", [
                "Wieś",
                "Miasto poniżej 50 tys. mieszkańców",
                "Miasto 50–100 tys. mieszkańców",
                "Miasto powyżej 100 tys. mieszkańców"
            ], key="location", index=None
        )

        if st.button("Dalej"):
            if not all([gender, age, education, education_years, profession, location]):
                st.error("Upewnij się, że wszystkie pola zostały wypełnione.")
            else:
                st.session_state.demographic_data = {
                    "Gender": gender,
                    "Age": age,
                    "Education": education,
                    "Education Years": education_years,
                    "Profession": profession,
                    "Location": location
                }
                go_to_next_page('instructions')

    elif st.session_state.page == 'instructions':
        if st.session_state.group == 'control':
            st.title("Instrukcja do zadań")
            st.write("""
                W ramach tego badania otrzymasz serię 12 zadań. W każdym zadaniu przedstawię Ci opisy trzech różnych pralek wraz z oceną, która z nich jest najlepszym wyborem.
                """)

            st.markdown("""
                <h4 style='color: #77AD78; font-weight: bold; text-align: center;'>
                    Wybory i rekomendacje zostały wygenerowane przez system sztucznej inteligencji (AI).
                </h4>
                """, unsafe_allow_html=True)

            st.write("""
                Twoim zadaniem jest:
                - Zapoznanie się z opisami pralek i wyborem sztucznej inteligencji.
                - Odpowiedź na pytania dotyczące tego, czy zgadzasz się z przedstawioną decyzją oraz uzasadnienia swojej opinii.
                """)


            st.subheader("Analiza kluczowych parametrów pralek")
            st.write("""
            Zgodnie z badaniami marketingowymi, przyznaliśmy plusy właściwościom pralek. Im wyższa liczba plusów, tym ważniejsza dla przeciętnego użytkownika jest dana właściwość.
            """)

            st.image("instrukcja.png", use_container_width=True)

            st.write("""
            Dla przeciętnego konsumenta najważniejszą właściwością jest klasa energetyczna wyrażona w literach B, C, D, E, gdzie B ma najwyższą klasę energetyczną, kolejne litery C, D wskazują na niższe klasy energetyczne, zaś E wskazuje najniższą klasę energetyczną. Właściwość ta jako najważniejsza ma sześć plusów.

            Kolejną ważną właściwością (pięć plusów) jest zużycie wody w litrach. Porównywane pralki będą zużywały od 70l do 30l na cykl prania. Konsumenci preferują pralki zużywające mniejszą ilość wody.

            Następną istotną właściwością (cztery plusy) jest poziom hałasu w decybelach (dB). Prezentowane pralki będą miały poziom hałasu od 70dB do 40dB, gdzie mniejsza wartość oznacza cichszą pralkę. Cicha praca jest preferowana przez większość użytkowników.

            Kolejna właściwość, oceniana przez konsumentów na trzy plusy, to obecność lub brak programu szybkiego prania. Przeciętny konsument chce mieć możliwość ustawienia szybkiego prania.

            Następna właściwość, to pojemność bębna pralki w kilogramach. Pralki, które się pojawią, mają pojemność od 4 kg do 10 kg. Im większa pojemność bębna, tym zdaniem konsumentów lepiej.

            Ostatnia właściwość (jeden plus) to maksymalna prędkość wirowania, wyrażana w liczbie obrotów na minutę. Pralki, które będą prezentowane, mają maksymalną prędkość wirowania od 800 do 1600 obrotów. Im większa prędkość wirowania, tym w ocenie konsumentów lepiej.

            Za chwilę zobaczysz tabele porównujące różne pralki oraz informację dotyczącą wyboru jednej z nich przez system sztucznej inteligencji wraz z uzasadnieniem. Przestudiuj podane informacje i odpowiedz na pytania po każdym zadaniu.
            """)


        elif st.session_state.group == 'experimental':
                st.title("Instrukcja do zadań")
                st.write("""
                    W ramach tego badania otrzymasz serię 12 zadań. W każdym zadaniu przedstawię Ci opisy trzech różnych pralek wraz z oceną, która z nich jest najlepszym wyborem.
                    """)

                st.markdown("""
                    <h4 style='color: #77AD78; font-weight: bold; text-align: center;'>
                        Wybory i ich uzasadnienia zostały przygotowane przez inną osobę badaną.
                    </h4>
                    """, unsafe_allow_html=True)

                st.write("""
                    Twoim zadaniem jest:
                    - Zapoznanie się z opisami pralek i wyborem innego uczestnika badania.
                    - Odpowiedź na pytania dotyczące tego, czy zgadzasz się z przedstawioną decyzją oraz uzasadnienia swojej opinii.
                    """)

                st.subheader("Analiza kluczowych parametrów pralek")
                st.write("""
                Zgodnie z badaniami marketingowymi, przyznaliśmy plusy właściwościom pralek. Im wyższa liczba plusów, tym ważniejsza dla przeciętnego użytkownika jest dana właściwość.
                """)

                st.image("instrukcja.png", use_container_width=True)

                st.write("""
                Dla przeciętnego konsumenta najważniejszą właściwością jest klasa energetyczna wyrażona w literach B, C, D, E, gdzie B ma najwyższą klasę energetyczną, kolejne litery C, D wskazują na niższe klasy energetyczne, zaś E wskazuje najniższą klasę energetyczną. Właściwość ta jako najważniejsza ma sześć plusów.

                Kolejną ważną właściwością (pięć plusów) jest zużycie wody w litrach. Porównywane pralki będą zużywały od 70l do 30l na cykl prania. Konsumenci preferują pralki zużywające mniejszą ilość wody.

                Następną istotną właściwością (cztery plusy) jest poziom hałasu w decybelach (dB). Prezentowane pralki będą miały poziom hałasu od 70dB do 40dB, gdzie mniejsza wartość oznacza cichszą pralkę. Cicha praca jest preferowana przez większość użytkowników.

                Kolejna właściwość, oceniana przez konsumentów na trzy plusy, to obecność lub brak programu szybkiego prania. Przeciętny konsument chce mieć możliwość ustawienia szybkiego prania.

                Następna właściwość, to pojemność bębna pralki w kilogramach. Pralki, które się pojawią, mają pojemność od 4 kg do 10 kg. Im większa pojemność bębna, tym zdaniem konsumentów lepiej.

                Ostatnia właściwość (jeden plus) to maksymalna prędkość wirowania, wyrażana w liczbie obrotów na minutę. Pralki, które będą prezentowane, mają maksymalną prędkość wirowania od 800 do 1600 obrotów. Im większa prędkość wirowania, tym w ocenie konsumentów lepiej.

                Za chwilę zobaczysz tabele porównujące różne pralki oraz informację dotyczącą wyboru jednej z nich przez inną osobę badaną wraz z uzasadnieniem. Przestudiuj podane informacje i odpowiedz na pytania po każdym zadaniu.
                """)


        if st.button("Dalej"):
            go_to_next_page('task_page')

    elif st.session_state.page == 'task_page':
        st.title(f"Zadanie {st.session_state.task_number} z 12")
        st.write(f"To jest zadanie numer {st.session_state.task_number}. Zapoznaj się z poniższymi danymi oraz dokonanym wyborem pralki, a następnie odpowiedz na znajdujące się poniżej pytania.")

        image_path = task_images[st.session_state.task_number - 1]
        st.image(image_path, caption=f"Obraz do zadania {st.session_state.task_number}", use_container_width=True)

        if st.session_state.task_number == 1:
            if st.session_state.group == "experimental":
                st.markdown(f"""
                <h3 style='color: #77AD78; font-weight: bold;'>
                    Najlepsza według innej osoby badanej jest pralka 3:
                </h3>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <h3 style='color: #77AD78; font-weight: bold;'>
                    Najlepsza według AI jest pralka 3:
                </h3>
                """, unsafe_allow_html=True)

            st.write("""
            **Zalety:**
            - Duża pojemność bębna (8 kg) (++), co sprawdza się w przypadku większych prań.
            - Najwyższa maksymalna prędkość wirowania (1400 obrotów/min) (+), co znacząco skraca czas suszenia i może poprawić efektywność prania.

            **Wady:**
            - Klasa energetyczna E (++++) – standardowa, choć nie najlepsza.
            - Wyższe zużycie wody (65 l) (++++).
            - Wysoki poziom hałasu (70 dB) (+++).
            - Brak programu szybkiego (+++).

            **Wniosek:** Pralka 3 wyróżnia się na tle konkurencji dzięki dużej pojemności bębna oraz najwyższej maksymalnej prędkości wirowania, co czyni ją bardziej wydajną i praktyczną opcją w przypadku dużych gospodarstw domowych lub częstych prań.
            """)

        if st.session_state.task_number == 2:
            if st.session_state.group == "experimental":
                st.markdown(f"""
                <h3 style='color: #77AD78; font-weight: bold;'>
                    Najlepsza według innej osoby badanej jest pralka 1:
                </h3>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <h3 style='color: #77AD78; font-weight: bold;'>
                    Najlepsza według AI jest pralka 1:
                </h3>
                """, unsafe_allow_html=True)

            st.write("""
            **Zalety:**
            - Posiada program szybki (+++), co zwiększa jej funkcjonalność, szczególnie przy szybkim praniu codziennym.
            - Parametry pralki są wyważone i dobrze dopasowane do standardowych potrzeb użytkownika.

            **Wady:**
            - Klasa energetyczna E (++++) – mogłaby być lepsza, jednak różnica kosztów eksploatacji jest akceptowalna przy umiarkowanym użytkowaniu.
            - Zużycie wody 65 l (++++) – nie jest najniższe, ale pozostaje w rozsądnych granicach.
            - Poziom hałasu 70 dB (+++) – standardowy, nie wyróżnia się, ale też nie jest gorszy od konkurencji.

            **Wniosek:**
            Pralka 1 oferuje solidny zestaw funkcji, w tym program szybki, który jest kluczowy dla wygody użytkowania. Jej parametry są wystarczające dla większości użytkowników.
            """)

        if st.session_state.task_number == 3:
            if st.session_state.group == "experimental":
                st.markdown(f"""
                <h3 style='color: #77AD78; font-weight: bold;'>
                    Najlepsza według innej osoby badanej jest pralka 1:
                </h3>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <h3 style='color: #77AD78; font-weight: bold;'>
                    Najlepsza według AI jest pralka 1:
                </h3>
                """, unsafe_allow_html=True)
            st.write("""
            **Zalety:**
            - Obecność programu szybkiego (+++), co pozwala na szybsze pranie przy mniejszym zużyciu energii i czasu, co jest szczególnie przydatne w codziennym użytkowaniu.
            - Klasa energetyczna D (++++) – wyższa efektywność energetyczna w porównaniu do pozostałych pralek, co przekłada się na oszczędności w dłuższym okresie czasu.
            - Niska maksymalna prędkość wirowania (1200 obr./min) (++), wystarczająca do codziennych zastosowań i zmniejszająca zużycie ubrań.
            - Poziom hałasu (50 dB) (+++), co sprawia, że urządzenie pracuje cicho, co jest korzystne dla domów z otwartą przestrzenią.

            **Wady:**
            - Zużycie wody na poziomie 50 l (++++) – standardowe, ale nie najniższe.
            - Pojemność bębna (8 kg) (++), odpowiednia, ale nie wyróżniająca się na tle konkurencji.

            **Wniosek:**
            Pralka 1 stanowi najlepszy wybór dzięki połączeniu wysokiej klasy energetycznej, obecności programu szybkiego oraz niskiego poziomu hałasu. Te cechy sprawiają, że jest to urządzenie energooszczędne, wygodne w użytkowaniu i idealne do codziennego użytku, szczególnie w mniejszych gospodarstwach domowych.
            """)

        if st.session_state.task_number == 4:
            if st.session_state.group == "experimental":
                st.markdown(f"""
                <h3 style='color: #77AD78; font-weight: bold;'>
                    Najlepsza według innej osoby badanej jest pralka 3:
                </h3>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <h3 style='color: #77AD78; font-weight: bold;'>
                    Najlepsza według AI jest pralka 3:
                </h3>
                """, unsafe_allow_html=True)
            st.write("""
            **Zalety:**
            - Najlepsza klasa energetyczna B (+++++), co istotnie obniża koszty eksploatacji.
            - Najniższy poziom hałasu (40 dB) (+++), co zapewnia cichszą pracę.
            - Maksymalna prędkość wirowania (1600 obrotów/min) (+) – najwyższa w zestawieniu.

            **Wady:**
            - Brak programu szybkiego (+++), co ogranicza elastyczność użytkowania.
            - Pojemność bębna (8 kg) – standardowa (++).

            **Wniosek:**
            Pralka 3 wyróżnia się najlepszą klasą energetyczną, najniższym poziomem hałasu oraz wysoką prędkością wirowania. Te cechy czynią ją najbardziej wszechstronną i odpowiednią opcją w zestawieniu.
            """)

        if st.session_state.task_number == 5:
            if st.session_state.group == "experimental":
                st.markdown(f"""
                <h3 style='color: #77AD78; font-weight: bold;'>
                    Najlepsza według innej osoby badanej jest pralka 2:
                </h3>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <h3 style='color: #77AD78; font-weight: bold;'>
                    Najlepsza według AI jest pralka 2:
                </h3>
                """, unsafe_allow_html=True)
            st.write("""
            **Zalety:**
            - Program szybki (+++), co zwiększa funkcjonalność i elastyczność użytkowania.
            - Niższy poziom hałasu 60 dB (+++), co czyni ją cichszą od Pralki 1 i 3.

            **Wady:**
            - Klasa energetyczna E (++++) – najmniej efektywna.
            - Pojemność bębna 4 kg (++), co jest ograniczeniem przy większych załadunkach.
            - Zużycie wody 65 l (++++) – najwyższe w zestawieniu.
            - Maksymalna prędkość wirowania 1000 obrotów/min (+), co jest niższe od konkurencji.

            **Wniosek:**
            Pralka 2 jest cichsza, ale jej niska pojemność bębna, wysokie zużycie wody i niższa prędkość wirowania sprawiają, że przegrywa z Pralką 3.
            """)

        if st.session_state.task_number == 6:
            if st.session_state.group == "experimental":
                st.markdown(f"""
                <h3 style='color: #77AD78; font-weight: bold;'>
                    Najlepsza według innej osoby badanej jest pralka 1:
                </h3>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <h3 style='color: #77AD78; font-weight: bold;'>
                    Najlepsza według AI jest pralka 1:
                </h3>
                """, unsafe_allow_html=True)

            st.write("""
            **Zalety:**
            - Program szybki (+++), który zapewnia elastyczność i wygodę w codziennym użytkowaniu.
            - Maksymalna prędkość wirowania 1000 obrotów/min (+) – standardowa, odpowiednia dla podstawowych potrzeb użytkowników.

            **Wady:**
            - Klasa energetyczna E (++++) – najmniej efektywna, co może zwiększać koszty eksploatacji.
            - Zużycie wody 65 l (++++) – wyższe w porównaniu z Pralką 2.
            - Poziom hałasu 65 dB (+++), co jest najgorszym wynikiem w zestawieniu.
            - Pojemność bębna 4 kg (++), co ogranicza możliwość prania większych ilości odzieży.

            **Wniosek:**
            Pralka 1 oferuje program szybki, który jest kluczowym atutem dla użytkowników ceniących wygodę i oszczędność czasu. Mimo gorszej klasy energetycznej i mniejszej pojemności, jest odpowiednia dla osób szukających funkcjonalności w codziennym użytkowaniu.
            """)

        if st.session_state.task_number == 7:
            if st.session_state.group == "experimental":
                st.markdown(f"""
                <h3 style='color: #77AD78; font-weight: bold;'>
                    Najlepsza według innej osoby badanej jest pralka 3:
                </h3>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <h3 style='color: #77AD78; font-weight: bold;'>
                    Najlepsza według AI jest pralka 3:
                </h3>
                """, unsafe_allow_html=True)
            st.write("""
            **Zalety:**
            - Maksymalna prędkość wirowania 1200 obrotów/min (+), co zapewnia skuteczne odwirowanie.
            - Poziom hałasu 65 dB (+++), co jest cichsze niż w Pralce 2.
            - Klasa energetyczna E (++++) – standardowa jak w pozostałych modelach.

            **Wady:**
            - Zużycie wody 65 l (++++) – takie samo jak w Pralce 1, wyższe niż w Pralce 2.
            - Brak programu szybkiego (+++), co ogranicza elastyczność użytkowania.
            - Pojemność bębna 4 kg (++), co jest ograniczeniem dla większych załadunków.

            **Wniosek:**
            Pralka 3 oferuje najlepszy balans między prędkością wirowania, poziomem hałasu i standardową efektywnością energetyczną. Choć brakuje programu szybkiego, jej pozostałe parametry są dobrze dopasowane do codziennych potrzeb użytkownika.
            """)

        if st.session_state.task_number == 8:
            if st.session_state.group == "experimental":
                st.markdown(f"""
                <h3 style='color: #77AD78; font-weight: bold;'>
                    Najlepsza według innej osoby badanej jest pralka 2:
                </h3>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <h3 style='color: #77AD78; font-weight: bold;'>
                    Najlepsza według AI jest pralka 2:
                </h3>
                """, unsafe_allow_html=True)
            st.write("""
            **Zalety:**
            - Klasa energetyczna E (++++), co jest lepsze od klasy D w Pralce 1.
            - Program szybki (+++), co zwiększa funkcjonalność i wygodę użytkowania.
            - Pojemność bębna 4 kg (++), co odpowiada średnim potrzebom użytkowników.

            **Wady:**
            - Zużycie wody 65 l (++++), najwyższe w zestawieniu.
            - Maksymalna prędkość wirowania 1000 obrotów/min (+), co jest podstawowym poziomem w tej kategorii.
            - Poziom hałasu 70 dB (+++), porównywalny do innych pralek, ale nie wyróżnia się.

            **Wniosek:**
            Pralka 2 wyróżnia się obecnością programu szybkiego, który jest jej głównym atutem. Jednak wysokie zużycie wody i podstawowa prędkość wirowania sprawiają, że trudno ją uznać za najbardziej efektywną opcję. Lepszym wyborem w wielu przypadkach może być Pralka 3, która posiada większą pojemność bębna.
            """)

        if st.session_state.task_number == 9:
            if st.session_state.group == "experimental":
                st.markdown(f"""
                <h3 style='color: #77AD78; font-weight: bold;'>
                    Najlepsza według innej osoby badanej jest pralka 1:
                </h3>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <h3 style='color: #77AD78; font-weight: bold;'>
                    Najlepsza według AI jest pralka 1:
                </h3>
                """, unsafe_allow_html=True)
            st.write("""
            **Zalety:**
            - Najniższe zużycie wody 45 l (++++) – najbardziej oszczędne w zestawieniu.
            - Program szybki (+++), co zapewnia elastyczność i wygodę w codziennym użytkowaniu.
            - Poziom hałasu 60 dB (+++), co czyni ją jedną z cichszych pralek w zestawieniu.
            - Standardowa maksymalna prędkość wirowania 1000 obrotów/min (+), odpowiednia dla codziennych potrzeb.

            **Wady:**
            - Klasa energetyczna E (++++) – mogłaby być lepsza, ale różnica kosztów eksploatacji jest akceptowalna.
            - Pojemność bębna 4 kg (++), co jest standardowe, ale wystarczające dla większości użytkowników.

            **Wniosek:**
            Pralka 1 oferuje najlepszy balans kluczowych parametrów. Jej oszczędne zużycie wody, niski poziom hałasu oraz program szybki czynią ją najbardziej funkcjonalnym wyborem.
            """)

        if st.session_state.task_number == 10:
            if st.session_state.group == "experimental":
                st.markdown(f"""
                <h3 style='color: #77AD78; font-weight: bold;'>
                    Najlepsza według innej osoby badanej jest pralka 2:
                </h3>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <h3 style='color: #77AD78; font-weight: bold;'>
                    Najlepsza według AI jest pralka 2:
                </h3>
                """, unsafe_allow_html=True)
            st.write("""
            **Zalety:**
            - Najniższe zużycie wody (55 l) – najbardziej oszczędne (++++).
            - Pojemność bębna 6 kg – idealna dla większych załadunków (++), co czyni ją bardziej praktyczną.
            - Cichy poziom hałasu (65 dB) – zapewnia komfort użytkowania (+++).

            **Wady:**
            - Klasa energetyczna E (++++), standardowa w tej kategorii.
            - Maksymalna prędkość wirowania 1000 obrotów/min (+), co jest podstawowym poziomem w tej kategorii.

            **Wniosek:**
            Pralka 2 jest najlepszym wyborem. Łączy oszczędność wody, większą pojemność i komfort użytkowania. To najbardziej funkcjonalna opcja w zestawieniu.
            """)

        if st.session_state.task_number == 11:
            if st.session_state.group == "experimental":
                st.markdown(f"""
                <h3 style='color: #77AD78; font-weight: bold;'>
                    Najlepsza według innej osoby badanej jest pralka 2:
                </h3>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <h3 style='color: #77AD78; font-weight: bold;'>
                    Najlepsza według AI jest pralka 2:
                </h3>
                """, unsafe_allow_html=True)
            st.write("""
            **Zalety:**
            - Klasa energetyczna D (++++) – dobra efektywność, choć nieco niższa od Pralki 1.
            - Program szybki (+++), co zapewnia elastyczność i wygodę w codziennym użytkowaniu.
            - Zużycie wody 50 l (++++) – oszczędne i standardowe w zestawieniu.
            - Pojemność bębna 8 kg (++), odpowiednia dla większych załadunków.
            - Maksymalna prędkość wirowania 1200 obrotów/min (+), co przyspiesza suszenie.

            **Wady:**
            - Poziom hałasu 50 dB (+++), co jest standardowe i nie wyróżnia się w zestawieniu.

            **Wniosek:**
            Pralka 2 oferuje najlepszy balans kluczowych parametrów, takich jak program szybki, oszczędne zużycie wody i duża pojemność bębna, co czyni ją najbardziej funkcjonalną.
            """)

        if st.session_state.task_number == 12:
            if st.session_state.group == "experimental":
                st.markdown(f"""
                <h3 style='color: #77AD78; font-weight: bold;'>
                    Najlepsza według innej osoby badanej jest pralka 3:
                </h3>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <h3 style='color: #77AD78; font-weight: bold;'>
                    Najlepsza według AI jest pralka 3:
                </h3>
                """, unsafe_allow_html=True)
            st.write("""
            **Zalety:**
            - Największa pojemność bębna 12 kg (++), co jest idealne dla dużych załadunków.
            - Maksymalna prędkość wirowania 1600 obrotów/min (+), co znacznie skraca czas suszenia i poprawia efektywność prania.
            - Najniższe zużycie wody 30 l (++++) – najbardziej ekonomiczne w zestawieniu.
            - Program szybki (+++), co zapewnia elastyczność użytkowania.

            **Wady:**
            - Klasa energetyczna D (++++) – mogłaby być lepsza.
            - Poziom hałasu 50 dB (+++), co jest głośniejsze niż w Pralce 1, ale nadal akceptowalne.

            **Wniosek:**
            Pralka 3 wyróżnia się najlepszymi parametrami użytkowymi: największą pojemnością bębna, najszybszym wirowaniem oraz oszczędnym zużyciem wody, co czyni ją najbardziej wszechstronnym wyborem.
            """)

        st.subheader("Pytania:")

        agree_choice = st.radio(
            "Czy zgadzasz się z wyborem rekomendowanej pralki?",
            ["Tak", "Nie"],
            key=f"agree_choice_{st.session_state.task_number}",
            index=None 
        )

        agree_scale = st.radio(
            "Na ile zgadzasz się z wyborem rekomendowanej pralki?",
            [
            "Zupełnie się nie zgadzam",
            "Nie zgadzam się",
            "Trochę się nie zgadzam, trochę się zgadzam",
            "Zgadzam się",
            "Całkowicie się zgadzam"
            ],
            key=f"scale_{st.session_state.task_number}",
            index=None 
        )


        justification = st.text_area(
            "Uzasadnij swoją odpowiedź:",
            key=f"justification_{st.session_state.task_number}"
        )

        clarity_scale = st.radio(
            "Na ile uzasadnienie wyboru pralki było dla Ciebie zrozumiałe?",
            [
                "Zupełnie niezrozumiałe",
                "Niezrozumiałe",
                "Trochę niezrozumiałe, trochę zrozumiałe",
                "Zrozumiałe",
                "Bardzo zrozumiałe"
            ],
            key=f"clarity_{st.session_state.task_number}",
            index=None, 
        )

        consideration_scale = st.radio(
            "Na ile uważasz, że uwzględniono wszystkie istotne parametry?",
            [
                "Zupełnie nie uwzględniono",
                "Nie uwzględniono",
                "Trochę nie uwzględniono, trochę uwzględniono",
                "Uwzględniono",
                "Całkowicie uwzględniono"
            ],
            key=f"consideration_{st.session_state.task_number}",
            index=None, 
        )

        if st.button("Dalej"):
            if any(value is None or value == "" for value in [
                agree_choice, justification
            ]):
                st.error("Upewnij się, że wszystkie pola zostały wypełnione.")
            else:
                if 'responses' not in st.session_state:
                    st.session_state['responses'] = {}

                st.session_state['responses'][st.session_state.task_number] = {
                    "Agree Choice": agree_choice,
                    "Agree Scale": agree_scale,
                    "Justification": justification,
                    "Clarity Scale": clarity_scale,
                    "Consideration Scale": consideration_scale
                }

                go_to_next_task()  

    elif st.session_state.page == 'thank_you':
        st.title("Ostatnie pytania przed zakończeniem")

        # GRUPA EKSPERYMENTALNA - podsumowanie i pytania
        if st.session_state.group == 'control':

            final_q1 = st.radio(
                "W jakim stopniu świadomość, że decyzje podejmowało AI, wpłynęła na Twoje postrzeganie i uzasadnienie tych decyzji?",
                [
                    "Wcale nie wpłynęła",
                    "Nie wpłynęła",
                    "Trochę nie wpłynęła, trochę wpłynęła",
                    "Wpłynęła",
                    "Bardzo wpłynęła"
                ],
                key="final_q1",
                index=None,
            )
            final_q2 = st.radio(
                "Jak często korzystasz z produktów lub usług opartych na AI?",
                ["Nigdy", "Rzadko", "Czasami", "Często", "Bardzo często"], key="final_q2", index=None
            )
            final_q3 = st.radio(
                "Jak często korzystasz z technologii opartych na sztucznej inteligencji (np. asystentów głosowych, rekomendacji zakupowych)?",
                ["Nigdy", "Rzadko", "Czasami", "Często", "Bardzo często"], key="final_q3", index=None
            )
            final_q4 = st.radio(
                "Jak oceniasz swoje zaufanie do technologii AI?",
                [
                    "Całkowicie nie ufam",
                    "Nie ufam",
                    "Trochę nie ufam, trochę ufam",
                    "Ufam",
                    "Całkowicie ufam"
                ],
                key="final_q4",
                index=None,  
            )
            final_q5 = st.radio(
                "Czy wolisz, aby decyzje zakupowe były podejmowane przez człowieka czy technologię AI?",
                [
                    "Zawsze przez człowieka",
                    "Najczęściej przez człowieka, rzadko przez AI",
                    "Czasami przez człowieka, czasami przez AI",
                    "Najczęściej przez AI, rzadko przez człowieka",
                    "Zawsze przez AI"
                ],
                key="final_q5",
                index=None, 
            )

        elif st.session_state.group == 'experimental':


            final_q1 = st.radio(
                "W jakim stopniu świadomość, że decyzje podejmowała inna osoba badana, wpłynęła na Twoje postrzeganie i uzasadnienie tych decyzji?",
                [
                    "Wcale nie wpłynęła",
                    "Nie wpłynęła",
                    "Trochę nie wpłynęła, trochę wpłynęła",
                    "Wpłynęła",
                    "Bardzo wpłynęła"
                ],
                key="final_q1",
                index=None, 
            )
            final_q2 = st.radio(
                "Jak często korzystasz z produktów lub usług oprartych na AI",
                ["Nigdy", "Rzadko", "Czasami", "Często", "Bardzo często"], key="final_q2", index=None
            )
            final_q3 = st.radio(
                "Jak często korzystasz z technologii opartych na sztucznej inteligencji (np. asystentów głosowych, rekomendacji zakupowych)?",
                ["Nigdy", "Rzadko", "Czasami", "Często", "Bardzo często"], key="final_q3",index=None
            )
            final_q4 = st.radio(
                "Jak oceniasz swoje zaufanie do technologii AI?",
                [
                    "Całkowicie nie ufam",
                    "Nie ufam",
                    "Trochę nie ufam, trochę ufam",
                    "Ufam",
                    "Całkowicie ufam"
                ],
                key="final_q4",
                index=None,  
            )
            final_q5 = st.radio(
                "Czy wolisz, aby decyzje zakupowe były podejmowane przez człowieka czy technologię AI?",
                ["Zawsze przez człowieka", "Najczęściej przez człowieka, rzadko przez AI", "Czasami przez człowieka", "czasami przez AI", "Najczęściej przez AI, rzadko przez człowieka", "Zawsze przez AI" ], key="final_q5", index=None
            )

        # Sprawdzenie czy użytkownik wypełnił wszystkie pytania przed wysłaniem
        if st.button("Dalej", key="send_final"):
            if not all([final_q1, final_q2, final_q3, final_q4, final_q5]):
                st.error("Proszę odpowiedzieć na wszystkie pytania przed zakończeniem badania.")
            elif 'responses' not in st.session_state or not st.session_state['responses']:
                st.error("Proszę upewnić się, że wypełniłeś wszystkie pola przed zakończeniem badania.")
            else:
       
                elapsed_time = time.time() - st.session_state.start_time
                minutes = int(elapsed_time // 60)
                seconds = int(elapsed_time % 60)

                task_responses = "\n".join([
                    f"Zadanie {task_num}: {response}"
                    for task_num, response in st.session_state['responses'].items()
                ])

                user_responses = f"""
                ID Użytkownika: {st.session_state.user_id}
                Grupa: {st.session_state.group}
                Odpowiedzi demograficzne: {st.session_state.get('demographic_data', 'Brak danych')}

                Odpowiedzi z zadań:
                {task_responses}

                Odpowiedzi na pytania końcowe:
                1. Wpływ świadomości (1-5): {final_q1}
                2. Korzystanie z AI: {final_q2}
                3. Korzystanie z technologii AI: {final_q3}
                4. Zaufanie do AI (1-5): {final_q4}
                5. Preferencje w podejmowaniu decyzji zakupowych (1-5): {final_q5}

                ⏳ Czas trwania badania: {minutes} min {seconds} sek.
                """

                send_email(
                    subject=f"Nowe odpowiedzi z badania - ID: {st.session_state.user_id}",
                    body=user_responses,
                    recipient="ankieta831@gmail.com"
                )

                go_to_summary()

    elif st.session_state.page == "summary":
        st.success("Twoje odpowiedzi zostały zapisane i wysłane.")


        if st.session_state.group == "experimental":
            st.write("""
            Chciałabym przekazać ważną informację: wszystkie decyzje dotyczące wyboru najlepszej pralki w zadaniach zostały wygenerowane przez system sztucznej inteligencji (AI), a nie przez innego uczestnika badania.
            Ujawnienie tej informacji dopiero po zakończeniu badania było celowym zabiegiem badawczym, który pozwala nam lepiej zrozumieć, jak ludzie oceniają decyzje podejmowane przez AI w porównaniu do tych podejmowanych przez człowieka.

            Dziękuję za udział w badaniu! Jeśli masz jakiekolwiek pytania dotyczące badania, możesz się ze mną skontaktować pod adresem: **zbosiacka@st.swps.edu.pl**
            """)

        elif st.session_state.group == "control":
            st.write("""
            Celem tego badania było zrozumienie, jak ludzie oceniają decyzje podejmowane przez systemy sztucznej inteligencji (AI) w porównaniu do ich własnych oczekiwań i doświadczeń.

            Dziękuję za Twój udział! Twoje odpowiedzi pomogą mi lepiej zrozumieć, jak zwiększyć przejrzystość i zaufanie do technologii AI.

            Jeśli masz jakiekolwiek pytania dotyczące badania, możesz się skontaktować pod adresem:
            **zbosiacka@st.swps.edu.pl**
            """)



if __name__ == "__main__":
    main()
