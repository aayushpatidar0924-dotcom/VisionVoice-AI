import speech_recognition as sr
import webbrowser
import pyautogui


class VoiceController:

    def __init__(self):

        self.running = True

        # recognizer object
        self.recognizer = sr.Recognizer()

        # mic sensitivity
        self.recognizer.energy_threshold = 300

        # noise adjustment
        self.recognizer.dynamic_energy_threshold = True


    
    # START LISTENING
    

    def start(self):

        print("🎤 AI Listening...")

        with sr.Microphone() as source:

            # noise calibration
            self.recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            while self.running:

                try:

                    print("Listening...")

                    audio = self.recognizer.listen(
                        source,
                        timeout=5,
                        phrase_time_limit=5
                    )

                    text = self.recognizer.recognize_google(
                        audio
                    ).lower()

                    print(
                        "You said:",
                        text
                    )

                    self.execute_command(text)

                except sr.UnknownValueError:

                    print(
                        "Could not understand"
                    )

                except sr.WaitTimeoutError:

                    pass

                except Exception as e:

                    print(
                        "Error:",
                        e
                    )



    # COMMANDS


    def execute_command(self, text):

        # wake word
        if not text.startswith("vision"):
            return

        # remove wake word
        text = text.replace(
            "vision",
            ""
        ).strip()


    
        # OPEN YOUTUBE
        

        if "youtube" in text:

            print("Opening YouTube")

            webbrowser.open(
                "https://www.youtube.com"
            )



        # OPEN CHATGPT
    

        elif "chatgpt" in text:

            print("Opening ChatGPT")

            webbrowser.open(
                "https://chat.openai.com"
            )


        
        # OPEN GOOGLE


        elif "google" in text:

            print("Opening Google")

            webbrowser.open(
                "https://www.google.com"
            )


        
        # OPEN CHROME


        elif "chrome" in text:

            print("Opening Chrome")

            pyautogui.press("win")

            pyautogui.write(
                "chrome"
            )

            pyautogui.press("enter")


        # OPEN VS CODE


        elif (
            "vs code" in text or
            "vscode" in text
        ):

            print("Opening VS Code")

            pyautogui.press("win")

            pyautogui.write(
                "Visual Studio Code"
            )

            pyautogui.press("enter")



        # GOOGLE SEARCH
        

        elif "search" in text:

            query = text.replace(
                "search",
                ""
            )

            print(
                "Searching:",
                query
            )

            webbrowser.open(
                f"https://www.google.com/search?q={query}"
            )


        
        # TYPE TEXT
        

        elif "type" in text:

            msg = text.replace(
                "type",
                ""
            )

            print(
                "Typing:",
                msg
            )

            pyautogui.write(msg)


        
        # SCROLL DOWN
        

        elif "scroll down" in text:

            pyautogui.scroll(-500)


        
        # SCROLL UP
    

        elif "scroll up" in text:

            pyautogui.scroll(500)


    
        # CLOSE TAB


        elif "close tab" in text:

            pyautogui.hotkey(
                "ctrl",
                "w"
            )


        
        # NEW TAB
    

        elif "new tab" in text:

            pyautogui.hotkey(
                "ctrl",
                "t"
            )


    
    # STOP


    def stop(self):

        self.running = False