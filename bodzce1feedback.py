import yaml
import os
import pandas as pd
from psychopy import visual, core
from psychopy.hardware import keyboard
import random

global_trial_number = 0

# Załadowanie ustawień z pliku .yaml: funkcja load_config
def load_config(file_name):
    with open(file_name, encoding="utf-8") as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


win = visual.Window(
    size=[1024, 768],
    fullscr=False,
    color='black',
    units='pix',
    checkTiming=False
)
kb = keyboard.Keyboard()

COLOR_BLUE = '#44EDFF'
COLOR_GREEN = '#E2FF55'

stim_bc = visual.Circle(win, radius=60, fillColor=COLOR_BLUE, lineColor=None)
stim_gc = visual.Circle(win, radius=60, fillColor=COLOR_GREEN, lineColor=None)

stim_bs = visual.Rect(win, width=120, height=120, fillColor=COLOR_BLUE, lineColor=None)
stim_gs = visual.Rect(win, width=120, height=120, fillColor=COLOR_GREEN, lineColor=None)

stim_list = [stim_bc, stim_gc, stim_bs, stim_gs]
# Poprawne odpowiedzi
#Punkt fiksacji (biały krzyżyk)
fixation = visual.TextStim(win, text='+', color='white', height=20)

#  Wskazówki
cue_bg = visual.Rect(win, width=200, height=80, fillColor='#DEDEDE', lineColor='#B0B0B0', lineWidth=6)
cue_text_color = visual.TextStim(win, text='KOLOR', color='black', height=32, bold=True)
cue_text_shape = visual.TextStim(win, text='KSZTAŁT', color='black', height=32, bold=True)

#  Feedback (nie wiem tu mam propozycje czata zeby feedback byl tekstem, ale nie wiem, mozna przerobic na jpg)
feedback_correct = visual.TextStim(win, text='✓', color='grey', height=100)
feedback_incorrect = visual.TextStim(win, text='✗', color='grey', height=100)
feedback_timeout = visual.TextStim(win, text='ZA WOLNO', color='grey', height=40)

answers_color = {stim_bc: "k", stim_gc: "d", stim_bs: "k", stim_gs: "d"}
answers_shape = {stim_bc: "d", stim_gc: "d", stim_bs: "k", stim_gs: "k"}



# Losowanie bodźców: funkcja make_stim_list
def make_stim_list(n,# n - liczba bodźców do wygenerowania
                   mixed_trial = False): # mixed_trial - wskazuje, czy mamy do czynienia z próbą mieszaną

    opts = stim_list.copy()
    stim_queue = []
    quota = {}
    m = (n - n % 4)

    for i in opts:
        quota[i] = int(m / 4)
    # zapewniamy równoliczność (tak bardzo jak to możliwe) poszczególnych bodźców

    stim_queue.append(random.choice(opts))
    quota[stim_queue[0]] = quota[stim_queue[0]] - 1

    for i in range(m - 1):
        if quota[stim_queue[i]] == 0 and stim_queue[i] in opts:
            opts.remove(stim_queue[i])
        curr_opts = opts.copy()
        if stim_queue[i] in opts:
            curr_opts.remove(stim_queue[i])
        stim_queue.append(random.choice(curr_opts))
        quota[stim_queue[i + 1]] = quota[stim_queue[i + 1]] - 1

    if m != n:
        for i in range(m - 1, n - 1):
            opts = stim_queue.copy()
            curr_opts = opts.copy()
            if stim_queue[i] in opts:
                curr_opts.remove(stim_queue[i])
            stim_queue.append(random.choice(curr_opts))

    # losujemy n bodźców tak, by nie powtarzały się jedno po drugim
    # czyli jeśli stims[i] = stim1 to stims[i+1] != stim1 i stims[i-1] != stim1
    # zdefiniowanie tego jako funkcji pozwoli nam uniknąć pisania tego samego
    # 32873529 razy: po prostu przywołujemy kod za każdym razem, gdy musimy
    # stworzyć listę bodźców

    focus_times = [random.randint(400, 700) for _ in range(n)]

    #losujemy n czasów wyświetlania się punktów fiksacji

    if mixed_trial:
        l = (n - 1) - (n-1)%2
        switch_opts = [True, False]
        switch_queue = []
        switch_quota = {}

        trial_type_queue = []

        for i in switch_opts:
            switch_quota[i] = l/2

        switch_queue.append(random.choice(switch_opts))
        switch_quota[switch_queue[0]] = switch_quota[switch_queue[0]] - 1

        for i in range(l - 1):
            if switch_quota[switch_queue[i]] == 0:
                switch_opts.remove(switch_queue[i])
            switch_queue.append(random.choice(switch_opts))
            switch_quota[switch_queue[i + 1]] = switch_quota[switch_queue[i + 1]] - 1

        if l != n-1:
            switch_opts = [True, False]
            switch_queue.append(random.choice(switch_opts))

        trial_type_queue.append(random.choice(["color", "shape"]))

        for switch in switch_queue:
            if switch:
                if trial_type_queue[-1] == "color":
                    trial_type_queue.append("shape")
                else:
                    trial_type_queue.append("color")
            else:
                if trial_type_queue[-1] == "color":
                    trial_type_queue.append("color")
                else:
                    trial_type_queue.append("shape")

        switch_queue.insert(0, None)

        return stim_queue, focus_times, switch_queue, trial_type_queue

    else:
        return stim_queue, focus_times

        # ok nie wiem czy to najlepszy sposób, ale na ten moment jest jedyny więc
        # najlepszy by default :P
        # proponuję wygenerować najpierw listę pomocniczą n-1 wartości logicznych
        # (czyli True/False)
        # a następnie:
        # 1. losujemy color/shape (typ pierwszej próby)
        # 2. jeśli switch = true, następny element będzie odmienny
        # 3. jeśli false to taki sam
        # i w taki sposób otrzymamy listę trial_types

# Podsumowując, funkcja zwraca:
    # listę bodźców stim_queue
    # listę czasów wyświetlania punktów fiksacji focus_times
    # w próbach mieszanych:
        # listę pomocniczą switch_queue
        # listę typów prób trial_type_queue



#def check_correct(stim, #stim - rodzaj bodźca
                  trial_type, # trial_type - typ próby (shape/color)
                  focus_time,  # focus_time - czas wyświetlania punktu fiksacji
                  # (losowany),

                  #zadane, nie będziemy ich zmieniać

    # tu kod
def check_correct(stim, trial_type, focus_time, reaction_time=1500, cue_time=600):
            global answered, correct_answer, rt, response_key

            kb.clearEvents()

            fixation.draw()
            win.flip()
            core.wait(focus_time / 1000.0)


            cue_bg.draw()
            if trial_type == "color":
                cue_text_color.draw()
            else:
                cue_text_shape.draw()
            win.flip()
            core.wait(cue_time / 1000.0)

            stim.draw()
            win.flip()

            kb.clock.reset()

            keys = kb.waitKeys(maxWait=reaction_time / 1000.0, keyList=['d', 'k'], waitRelease=False)


            if keys:
                answered = True
                response_key = keys[0].name
                rt = keys[0].rt * 1000.0

                if trial_type == "color":
                    correct_key = answers_color[stim]
                else:
                    correct_key = answers_shape[stim]

                if response_key == correct_key:
                    correct_answer = True
                else:
                    correct_answer = False
            else:
                answered = False
                correct_answer = False
                response_key = None
                rt = None

    # Czekamy na odpowiedź przez zadany czas (reaction_time)

    # Funkcja zwraca zmienne:
    # answered - czy odpowiedź została udzielona (True/False)
    # correct_answer - czy udzielona odpowiedź jest poprawna (True/False)


def give_feedback():
    global answered, correct_answer

    if not answered:
        feedback_timeout.draw()
    elif correct_answer:
        feedback_correct.draw()
    else:
        feedback_incorrect.draw()

    win.flip()
    core.wait(0.5)

    win.flip()
    core.wait(0.5)

    # Funkcja wyświetla odpowiedni feedback:
    # answered = False: ZA WOLNO
    # answered = True i correct_answer = False: ŹLE
    # answered = True i correct_answer = True: DOBRZE

def save_data(result_list, block_name, stim, trial_type, is_switch):
        global answered, correct_answer, rt, response_key, global_trial_number

        global_trial_number += 1

        if stim == stim_bc:
            stim_name = "Niebieskie_Koło"
        elif stim == stim_gc:
            stim_name = "Zielone_Koło"
        elif stim == stim_bs:
            stim_name = "Niebieski_Kwadrat"
        elif stim == stim_gs:
            stim_name = "Zielony_Kwadrat"
        else:
            stim_name = "Nieznany"

        if answers_color[stim] == answers_shape[stim]:
            congruency = "Kongruentna"
        else:
            congruency = "Niekongruentna"

        if is_switch:
            transition = "SWITCH"
        else:
            transition = "REPEAT"

        individual_result = {
            "Trial_Number": global_trial_number,
            "Block_Name": block_name,
            "Transition": transition,
            "Cue_Type": trial_type,
            "Stimulus": stim_name,
            "Congruency": congruency,
            "Reaction_Time_ms": rt,
            "Correct": correct_answer,
            "Timeout": not answered,
            "Response_Key": response_key
        }

        result_list.append(individual_result)



# do zarejestrowania:
    # numer kolejny próby w skali całego eksperymentu (od 1 do 200)
    # nazwa i typ aktualnej części badania
    # typ próby w kolejnych trialach (REPEAT/SWITCH)
    # rodzaj zaprezentowanego sygnału wskazującego aktualną regułę
    # cechy prezentowanego bodźca docelowego
    # stopień zgodności mapowania odpowiedzi (kongruentna/niekongruentna)
    # czas reakcji osoby badanej liczony od momentu pojawienia się bodźca
    # poprawność udzielonej odpowiedzi (lub przekroczenie czasu/timeout)
    # rodzaj udzielonej reakcji ("D"/"K")

def save_tofile(result_list,
              file_name,
              path = 'results'):
    os.makedirs(path, exist_ok=True)
    df = pd.DataFrame(result_list)
    df.to_csv(os.path.join(path, file_name), index=False)

    # Zapisuje wynik do pliku


def practice_run_single(n, trial_type):
    stims, focus_times = make_stim_list(n, mixed_trial=False)
    for i in range(n):
        stim = stims[i]
        focus_time = focus_times[i]
        answered = False
        correct_answer = False
        check_correct(stim=stim, trial_type=trial_type, focus_time=focus_time)
        give_feedback()

def testing_run_single(n, trial_type, results):
    stims, focus_times = make_stim_list(n, mixed_trial=False)
    for i in range(n):
        stim = stims[i]
        focus_time = focus_times[i]
        answered = False
        correct_answer = False
        check_correct(stim=stim, trial_type=trial_type, focus_time=focus_time)
        save_data(result_list=results, block_name=f"Single_{trial_type}", stim=stim, trial_type=trial_type, is_switch=False)

def practice_run_mixed(n):
    stims, focus_times, switch_queue, trial_types = make_stim_list(n, mixed_trial=True)
    for i in range(n):
        stim = stims[i]
        focus_time = focus_times[i]
        trial_type = trial_types[i]
        answered = False
        correct_answer = False
        check_correct(stim=stim, trial_type=trial_type, focus_time=focus_time)
        give_feedback()

def testing_run_mixed(n, results):
    stims, focus_times, switch_queue, trial_types = make_stim_list(n, mixed_trial=True)
    for i in range(n):
        stim = stims[i]
        focus_time = focus_times[i]
        trial_type = trial_types[i]
        is_sw = switch_queue[i]
        answered = False
        correct_answer = False
        check_correct(stim=stim, trial_type=trial_type, focus_time=focus_time)
        save_data(result_list=results, block_name="Mixed_Block", stim=stim, trial_type=trial_type, is_switch=is_sw)
    # funkcja zwraca listy stims, focus_times






# Wyświetlenie instrukcji

def trial(single_training_n = load_config(),
          # ilość bodźców wyświetlanych podczas treningu kolor i treningu kształt
          # (z load_config)
          single_trial_n = load_config(),
          # ilość bodźców wyświetlanych podczas próby kolor i próby kształt
          # (z load_config)
          mixed_training_n = load_config(),
          # ilość bodźców wyświetlanych podczas treningu mieszanego
          # (z load_config)
          mixed_trial_n = load_config()):
          # ilość bodźców wyświetlanych podczas próby mieszanej
          # (z load_config)

    # Utworzenie listy na wyniki prób

    results = []

    # TRENING KOLOR

    # Wyświetlenie informacji o rozpoczęciu treningu KOLOR

    practice_run_single(single_training_n, "color")

    # Wyświetlenie informacji o zakończeniu treningu KOLOR

# ///////////////////////////////////////////////////

    #PRÓBA KOLOR

    # Wyświetlenie informacji o rozpoczęciu badania KOLOR

    testing_run_single(single_trial_n, "color", results = results)

    # Wyświetlenie informacji o zakończeniu badania KOLOR

# ///////////////////////////////////////////////////
    # TRENING KSZTAŁT

    # Wyświetlenie informacji o rozpoczęciu treningu KSZTAŁT

    practice_run_single(single_training_n, "shape")

    # Wyświetlenie informacji o zakończeniu treningu KSZTAŁT

# ///////////////////////////////////////////////////

    #PRÓBA KSZTAŁT

    # Wyświetlenie informacji o rozpoczęciu badania KSZTAŁT

    testing_run_single(single_trial_n, "shape", results = results)

    # Wyświetlenie informacji o zakończeniu badania KSZTAŁT

# ///////////////////////////////////////////////////
    # TRENING MIESZANE

    # Wyświetlenie informacji o rozpoczęciu treningu MIESZANE

    practice_run_mixed(mixed_training_n)

    # Wyświetlenie informacji o zakończeniu treningu MIESZANE

# ///////////////////////////////////////////////////

    #PRÓBA MIESZANE

    # Wyświetlenie informacji o rozpoczęciu badania MIESZANE

    testing_run_mixed(mixed_trial_n, results = results)

    # Wyświetlenie informacji o zakończeniu badania MIESZANE

# ///////////////////////////////////////////////////

    save_tofile(results, "file_name", "results")