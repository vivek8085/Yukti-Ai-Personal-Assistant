#run this but not adjested

import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
import tempfile
import datetime
import wikipedia
import webbrowser
import smtplib
import time
import base64
import webbrowser

# Choose language: 'en' for English, 'kn' for Kannada, 'hi' for Hindi
language = st.selectbox("Select Language / भाषा चुनें / ಭಾಷೆ ಆಯ್ಕೆಮಾಡಿ:", ["English", "Hindi", "Kannada"])

if language == "Kannada":
    lang_code = 'kn'
elif language == "Hindi":
    lang_code = 'hi'
else:
    lang_code = 'en'

# Function to convert text to speech
def speak(text):
    tts = gTTS(text=text, lang=lang_code)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        with open(fp.name, "rb") as audio_file:
            audio_bytes = audio_file.read()
    
    audio_base64 = base64.b64encode(audio_bytes).decode()
    audio_tag = f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_base64}">'
    st.markdown(audio_tag, unsafe_allow_html=True)
    os.unlink(fp.name)

# Sidebar text in all three languages
with st.sidebar:
    with st.echo():
        st.write("This code will print to the sidebar." if lang_code == 'en' else
                 "यह कोड साइडबार में मुद्रित होगा।" if lang_code == 'hi' else 
                 "ಈ ಕೋಡ್ ಸೈಡ್ಬಾರ್‌ನಲ್ಲಿ ಮುದ್ರಿತವಾಗುತ್ತದೆ.")
    with st.spinner("Loading..." if lang_code == 'en' else
                    "लोड हो रहा है..." if lang_code == 'hi' else 
                    "ಲೋಡ್ ಆಗುತ್ತಿದೆ..."):
        time.sleep(5)
    st.success("Done!" if lang_code == 'en' else "पूर्ण हुआ!" if lang_code == 'hi' else "ಮುಗಿದಿದೆ!")

st.markdown(
    """
    <style>
    [data-testid="stMain"]{
        background: rgb(2,0,36);
background: linear-gradient(90deg, rgba(2,0,36,1) 0%, rgba(9,98,121,0.8352591036414566) 35%, rgba(0,212,255,1) 100%);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to recognize speech
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening..." if lang_code == 'en' else "सुन रहा हूँ..." if lang_code == 'hi' else "ಕೆಳಗಿರುವ...")
        audio = r.listen(source, timeout=10, phrase_time_limit=10)
    try:
        st.write("Recognizing..." if lang_code == 'en' else "पहचान कर रहा हूँ..." if lang_code == 'hi' else "ಗುರುತಿಸುತ್ತಿದೆ...")
        query = r.recognize_google(audio, language='en-IN' if lang_code == 'en' else 'hi-IN' if lang_code == 'hi' else 'kn-IN')
        st.write(f"User said: {query}" if lang_code == 'en' else f"यूजर ने कहा: {query}" if lang_code == 'hi' else f"ಬಳಕೆದಾರರು ಹೇಳಿದರು: {query}")
        return query.lower()
    except sr.WaitTimeoutError:
        return "Timeout" if lang_code == 'en' else "समय समाप्त" if lang_code == 'hi' else "ಟೈಮೌಟ್"
    except sr.UnknownValueError:
        return "Unknown" if lang_code == 'en' else "अज्ञात" if lang_code == 'hi' else "ಅಜ್ಞಾತ"
    except Exception as e:
        st.write(f"An error occurred: {str(e)}" if lang_code == 'en' else f"एक त्रुटि हुई: {str(e)}" if lang_code == 'hi' else f"ದೋಷವೊಂದು ಉಂಟಾಗಿದೆ: {str(e)}")
        return "Error" if lang_code == 'en' else "त्रुटि" if lang_code == 'hi' else "ದೋಷ"

def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        return "Good Morning!" if lang_code == 'en' else "सुप्रभात!" if lang_code == 'hi' else "ಶುಭೋದಯ!"
    elif 12 <= hour < 18:
        return "Good Afternoon!" if lang_code == 'en' else "नमस्कार!" if lang_code == 'hi' else "ಶುಭ ಮಧ್ಯಾಹ್ನ!"
    else:
        return "Good Evening!" if lang_code == 'en' else "शुभ संध्या!" if lang_code == 'hi' else "ಶುಭ ಸಂಜೆ!"

def search_google(query):
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('skbhagoji97@gmail.com', 'jsoq tvkh ijov iayo')
    server.sendmail('skbhagoji97@gmail.com', to, content)
    server.close()

st.title("AI Assistant - Nayra (Female Version) 🤖" if lang_code == 'en' else "एआई सहायक - नायरा 🤖" if lang_code == 'hi' else "ಎಐ ಸಹಾಯಕ - ನಾಯರಾ 🤖")
st.image("bot.gif")

def main():
    greeting = wishMe()
    speak(f"{greeting} Hello! How can I make your day better, dear?" if lang_code == 'en' else 
          f"{greeting} मैं आपकी किस प्रकार सहायता कर सकता हूँ?" if lang_code == 'hi' else 
          f"{greeting} ನಾನು ನಿಮಗೆ ಸಹಾಯ ಮಾಡಬಹುದೇ?")
    
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        greeting = wishMe()
        speak(f"{greeting} Hello! How can I make your day better, dear?" if lang_code == 'en' else 
              f"{greeting} मैं आपकी किस प्रकार सहायता कर सकता हूँ?" if lang_code == 'hi' else 
              f"{greeting} ನಾನು ನಿಮಗೆ ಸಹಾಯ ಮಾಡಬಹುದೇ?")

    if 'listening' not in st.session_state:
        st.session_state.listening = False

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Start Listening" if lang_code == 'en' else "सुनना प्रारंभ करें" if lang_code == 'hi' else "ಶ್ರವಣ ಪ್ರಾರಂಭಿಸಿ"):
            if 'greeted' not in st.session_state:
                st.session_state.greeted = True
                greeting = wishMe()
                speak(f"{greeting} Hello! How can I make your day better, dear?" if lang_code == 'en' else 
                      f"{greeting} मैं आपकी किस प्रकार सहायता कर सकती हूँ?" if lang_code == 'hi' else 
                      f"{greeting} ನಾನು ನಿಮಗೆ ಸಹಾಯ ಮಾಡಬಹುದೇ?")
            st.session_state.listening = True
            st.rerun()
    
    with col2:
        if st.button("Stop Listening" if lang_code == 'en' else "सुनना बंद करें" if lang_code == 'hi' else "ಶ್ರವಣ ನಿಲ್ಲಿಸಿ"):
            st.session_state.listening = False
            st.rerun()

    output = st.empty()

    if st.session_state.listening:
        output.write("Listening... Say something!" if lang_code == 'en' else 
                     "सुन रहा हूँ... कुछ कहें!" if lang_code == 'hi' else 
                     "ಕೆಳಗಿರುವ... ಏನಾದರೂ ಮಾತನಾಡಿ!")
        query = takeCommand()
        
        if query not in ["Timeout", "Unknown", "Error", "समय समाप्त", "अज्ञात", "त्रुटि", "ಟೈಮೌಟ್", "ಅಜ್ಞಾತ", "ದೋಷ"]:
            output.write(f"Processing: {query}" if lang_code == 'en' else 
                         f"प्रसंस्करण: {query}" if lang_code == 'hi' else 
                         f"ಸಂಸ್ಕರಿಸುತ್ತಿದೆ: {query}")
            
            if 'wikipedia' in query or 'विकिपीडिया' in query or 'ವಿಕಿಪೀಡಿಯ' in query:
                speak('Searching Wikipedia...' if lang_code == 'en' else 
                      'विकिपीडिया में खोज कर रहा हूँ...' if lang_code == 'hi' else 
                      'ವಿಕಿಪೀಡಿಯದಲ್ಲಿ ಹುಡುಕುತ್ತಿದೆ...')
                query = query.replace("wikipedia", "").replace("विकिपीडिया", "").replace("ವಿಕಿಪೀಡಿಯ", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia" if lang_code == 'en' else 
                      "विकिपीडिया के अनुसार" if lang_code == 'hi' else 
                      "ವಿಕಿಪೀಡಿಯ ಪ್ರಕಾರ")
                output.write(results)
                speak(results)

            elif 'open youtube' in query or 'यूट्यूब खोलें' in query or 'ಯುಟ್ಯೂಬ್ ತೆರೆಯಿರಿ' in query:
                webbrowser.open("https://www.youtube.com/")
                speak("Opening YouTube" if lang_code == 'en' else 
                      "यूट्यूब खोल रहा हूँ" if lang_code == 'hi' else 
                      "ಯೂಟ್ಯೂಬ್ ತೆರೆಯುತ್ತಿದೆ")

            elif 'open google' in query or 'गूगल खोलें' in query or 'ಗೂಗಲ್ ತೆರೆಯಿರಿ' in query:
                webbrowser.open("https://google.com")
                speak("Opening Google" if lang_code == 'en' else 
                      "गूगल खोल रहा हूँ" if lang_code == 'hi' else 
                      "ಗೂಗಲ್ ತೆರೆಯುತ್ತಿದೆ")

            elif 'time' in query or 'समय' in query or 'ಸಮಯ' in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"The time is {strTime}" if lang_code == 'en' else 
                      f"समय है {strTime}" if lang_code == 'hi' else 
                      f"ಈಗ ಸಮಯ {strTime}")

            elif 'search' in query or 'google' in query or 'खोजें' in query or 'गूगल' in query or 'ಹುಡುಕು' in query or 'ಗೂಗಲ್' in query:
                search_query = query.replace("search", "").replace("google", "").replace("खोजें", "").replace("गूगल", "").replace("ಹುಡುಕು", "").replace("ಗೂಗಲ್", "").strip()
                speak(f"Searching Google for {search_query}" if lang_code == 'en' else 
                      f"गूगल पर {search_query} खोज रहा हूँ" if lang_code == 'hi' else 
                      f"ಗೂಗಲ್‌ನಲ್ಲಿ {search_query} ಹುಡುಕುತ್ತಿದೆ")
                search_google(search_query)
                output.write(f"Searched Google for: {search_query}" if lang_code == 'en' else 
                             f"गूगल पर खोजा गया: {search_query}" if lang_code == 'hi' else 
                             f"ಗೂಗಲ್‌ನಲ್ಲಿ ಹುಡುಕಿದೆ: {search_query}")

            elif 'sleep' in query or 'quit' in query or 'सो जाओ' in query or 'बंद करो' in query or 'ನಿದ್ರೆ' in query or 'ನಿಲ್ಲಿಸಿ' in query:
                speak('Thank you so much! I’ll be right here when you need me again.' if lang_code == 'en' else 
                      'धन्यवाद! फिर मिलेंगे।' if lang_code == 'hi' else 
                      'ಧನ್ಯವಾದಗಳು! ಮತ್ತೆ ಕಾಣೋಣ.')
                st.session_state.listening = False

            else:
                speak("I'm really sorry, I didn't catch that. Would you mind trying again, please?" if lang_code == 'en' else 
                      "मुझे समझ नहीं आया। कृपया फिर से प्रयास करें।" if lang_code == 'hi' else 
                      "ನಾನು ಸಹಾಯ ಮಾಡಲು ಸಾಧ್ಯವಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೊಮ್ಮೆ ಪ್ರಯತ್ನಿಸಿ.")

        elif query == "Timeout" or query == "समय समाप्त" or query == "ಟೈಮೌಟ್":
            speak("I didn’t catch anything, sweetie. Could you please try again?" if lang_code == 'en' else 
                  "कोई आवाज़ नहीं सुनी। कृपया फिर से प्रयास करें।" if lang_code == 'hi' else 
                  "ಏನೂ ಕೇಳಲಾಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.")
        elif query == "Unknown" or query == "अज्ञात" or query == "ಅಜ್ಞಾತ":
            speak("I couldn’t quite understand that, dear. Can you please repeat it?" if lang_code == 'en' else 
                  "समझ नहीं पाया। कृपया फिर से प्रयास करें।" if lang_code == 'hi' else 
                  "ಗುರುತಿಸಲಾಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.")
        else:
            speak("Oh no! Something went wrong. Let me know how I can be of help, dear." if lang_code == 'en' else 
                  "एक त्रुटि हुई। कृपया फिर से प्रयास करें।" if lang_code == 'hi' else 
                  "ದೋಷವೊಂದು ಉಂಟಾಗಿದೆ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.")
        
        time.sleep(1.5)
        st.rerun()

if __name__ == "__main__":
    main()