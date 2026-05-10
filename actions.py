import webbrowser
import pyautogui


def execute_action(data):

    action = data.get("action")


    # =========================
    # OPEN WEBSITE
    # =========================

    if action == "open_website":

        target = data.get("target", "")

        if "youtube" in target:

            webbrowser.open(
                "https://www.youtube.com"
            )

        elif "google" in target:

            webbrowser.open(
                "https://www.google.com"
            )


    # =========================
    # OPEN APP
    # =========================

    elif action == "open_app":

        app = data.get("target", "")

        pyautogui.press("win")

        pyautogui.write(app)

        pyautogui.press("enter")


    # =========================
    # GOOGLE SEARCH
    # =========================

    elif action == "google_search":

        query = data.get("query", "")

        webbrowser.open(
            f"https://www.google.com/search?q={query}"
        )


    # =========================
    # YOUTUBE SEARCH
    # =========================

    elif action == "youtube_search":

        query = data.get("query", "")

        webbrowser.open(
            f"https://www.youtube.com/results?search_query={query}"
        )


    # =========================
    # TYPE TEXT
    # =========================

    elif action == "type_text":

        text = data.get("text", "")

        pyautogui.write(text)