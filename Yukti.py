#run this
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
import csv
from facial_emotion_recognition import EmotionRecognition
import cv2
import time


st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        # background: white;
        color: smoke;
        animation: pulse 3s infinite;
        padding: 20px;
    }
    @keyframes pulse {
        0% { background-color: rgba(0, 128, 255, 0.9); color:green;}
        50% { background-color: rgba(0, 212, 255, 1); color:blue;}
        100% { background-color: rgba(0, 128, 255, 0.9); }
    }
    .emoji {
        font-size: 3.5rem;
        margin-right: 10px;
        animation: bounce 1.5s infinite;
    }
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(120deg, #1e3c72, #2a5298, #0f2027);
        background-size: 400% 400%;
        animation: gradientShift 10s ease infinite;
        height: 100vh;
        padding: 0;
        margin: 0;
    }
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @media (max-width: 768px) {
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(120deg, #6a11cb, #2575fc);
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)


#########################################################################################################################
st.sidebar.markdown('<div class="yellow-subheader">Features</div>', unsafe_allow_html=True)
st.sidebar.markdown("""
- 🏠 **Home**: Chat with Yukti.  
- 😠😮😐 **Emotion Recognition**: To Enable Emotion Recognition mode.  
""")
# Main page content
# st.title("Yukti -An AI Assistant 🤖")

# Choose language: 'en' for English, 'kn' for Kannada, 'hi' for Hindi
st.markdown(
        """
        <style>
        .marquee {
            text-align: center;
            font-size: 1.2rem;
            font-weight: bold;
            color: #ff0000;
            padding: 10px;
            border-radius: 5px;
            animation: scroll 10s linear infinite;
            # animation: glow 1.5s infinite;
        }

        @keyframes scroll {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
        </style>
        <div class="marquee">
            To Communicate with it,Choose any one language.. 
        </div>
        """,
        unsafe_allow_html=True
        )
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

st.markdown(
    """
    <style>
    .yel-col{
        color:yellow;
        font-weight: bold;
        font-size: 1.0rem;
        # animation: glow 1.5s infinite;
        align-content: center;
    }
    
    .pink-subheader {
        color: pink;
        font-weight: bold;
        font-size: 1.5rem;
        animation: glow 1.5s infinite;
        align-content: center;
    }
    .yellow-subheader {
        color: yellow;
        font-weight: bold;
        font-size: 1.5rem;
        animation: glow 1.5s infinite;
    }

    @keyframes glow {
        0% {
            text-shadow: 0 0 5px #ffd700, 0 0 10px #ffd700, 0 0 15px #ffd700;
        }
        50% {
            text-shadow: 0 0 10px #ffd700, 0 0 20px #ffd700, 0 0 30px #ffd700;
        }
        100% {
            text-shadow: 0 0 5px #ffd700, 0 0 10px #ffd700, 0 0 15px #ffd700;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)



# st.markdown(
#     """
#     <style>
#     [data-testid="stMain"]{
#         background: rgb(2,0,36);
# background: linear-gradient(90deg, rgba(2,0,36,1) 0%, rgba(9,98,121,0.8352591036414566) 35%, rgba(0,212,255,1) 100%);
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

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
    server.login('email@gmail.com', 'API-Key')
    server.sendmail('email@gmail.com', to, content)
    server.close()

timestamp = datetime.datetime.now().strftime(f"%Y-%m-%d %H:%M:%S")
st.markdown('<div class="yellow-subheader">AI Assistant</div>', unsafe_allow_html=True)
# st.title("Yukti 🤖" if lang_code == 'en' else "युक्ति 🤖" if lang_code == 'hi' else "ಯುಕ್ತಿ 🤖")
st.markdown(
    """
    <style>
    .yukti-title {
        font-size: 3rem;
        font-weight: bold;
        text-align: left;
        color: yellow;
        animation: yukti-glow 2s infinite;
    }

    @keyframes yukti-glow {
        0% {
            text-shadow: 0 0 10px yellow, 0 0 20px yellow, 0 0 30px green;
        }
        50% {
            text-shadow: 0 0 20px green, 0 0 30px yellow, 0 0 40px green;
        }
        100% {
            text-shadow: 0 0 10px green, 0 0 20px green, 0 0 30px yellow;
        }
    }
    </style>
    <div class="yukti-title">
        Yukti 🤖
    </div>
    """,
    unsafe_allow_html=True
)

st.image("bot.gif")

def main():
    if not os.path.exists('chat_log.csv'):
        with open('chat_log.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['User Input', 'Response', 'Timestamp'])


    greeting = wishMe()
    speak(f"{greeting} Hello! How can I make your day better ?" if lang_code == 'en' else 
          f"{greeting} मैं आपकी किस प्रकार सहायता कर सकती हूँ?" if lang_code == 'hi' else 
          f"{greeting} ನಾನು ನಿಮಗೆ ಸಹಾಯ ಮಾಡಬಹುದೇ?")
    
    # wishMe()
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        # greeting = wishMe()
        # speak(f"{greeting} Hello! How can I make your day better ?" if lang_code == 'en' else 
            #   f"{greeting} मैं आपकी किस प्रकार सहायता कर सकता हूँ?" if lang_code == 'hi' else 
            #   f"{greeting} ನಾನು ನಿಮಗೆ ಸಹಾಯ ಮಾಡಬಹುದೇ?")

    if 'listening' not in st.session_state:
        st.session_state.listening = False

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Start Listening" if lang_code == 'en' else "सुनना प्रारंभ करें" if lang_code == 'hi' else "ಶ್ರವಣ ಪ್ರಾರಂಭಿಸಿ"):
            if 'greeted' not in st.session_state:
                st.session_state.greeted = True
            #     greeting = wishMe()
            #     speak(f"{greeting} Hello! How can I make your day better?" if lang_code == 'en' else 
            #           f"{greeting} मैं आपकी किस प्रकार सहायता कर सकती हूँ?" if lang_code == 'hi' else 
            #           f"{greeting} ನಾನು ನಿಮಗೆ ಸಹಾಯ ಮಾಡಬಹುದೇ?")
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
                results = wikipedia.summary(query, sentences=1)
                res=("According to Wikipedia" if lang_code == 'en' else 
                      "विकिपीडिया के अनुसार" if lang_code == 'hi' else 
                      "ವಿಕಿಪೀಡಿಯ ಪ್ರಕಾರ")
                output.write(results)
                speak(results)
                with open('chat_log.csv', 'w', newline='', encoding='utf-8') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow([query, res,timestamp])

            elif 'open youtube' in query or 'यूट्यूब खोलें' in query or 'ಯುಟ್ಯೂಬ್ ತೆರೆಯಿರಿ' in query:
                webbrowser.open("https://www.youtube.com/")
                res=("Opening YouTube" if lang_code == 'en' else 
                      "यूट्यूब खोल रहा हूँ" if lang_code == 'hi' else 
                      "ಯೂಟ್ಯೂಬ್ ತೆರೆಯುತ್ತಿದೆ")
                speak(res)
                with open('chat_log.csv', 'w', newline='', encoding='utf-8') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow([query, res,timestamp])

            elif 'open google' in query or 'गूगल खोलें' in query or 'ಗೂಗಲ್ ತೆರೆಯಿರಿ' in query:
                webbrowser.open("https://google.com")
                res=("Opening Google" if lang_code == 'en' else 
                      "गूगल खोल रहा हूँ" if lang_code == 'hi' else 
                      "ಗೂಗಲ್ ತೆರೆಯುತ್ತಿದೆ")
                speak(res)
                with open('chat_log.csv', 'w', newline='', encoding='utf-8') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow([query, res,timestamp])


            elif 'time' in query or 'समय' in query or 'ಸಮಯ' in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                res=(f"The time is {strTime}" if lang_code == 'en' else 
                      f"समय है {strTime}" if lang_code == 'hi' else 
                      f"ಈಗ ಸಮಯ {strTime}")
                speak(res)
                with open('chat_log.csv', 'w', newline='', encoding='utf-8') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow([query, res,timestamp])


            elif 'search' in query or 'google' in query or 'खोजें' in query or 'गूगल' in query or 'ಹುಡುಕು' in query or 'ಗೂಗಲ್' in query:
                search_query = query.replace("search", "").replace("google", "").replace("खोजें", "").replace("गूगल", "").replace("ಹುಡುಕು", "").replace("ಗೂಗಲ್", "").strip()
                res=(f"Searching Google for {search_query}" if lang_code == 'en' else 
                      f"गूगल पर {search_query} खोज रहा हूँ" if lang_code == 'hi' else 
                      f"ಗೂಗಲ್‌ನಲ್ಲಿ {search_query} ಹುಡುಕುತ್ತಿದೆ")
                search_google(search_query)
                output.write(f"Searched Google for: {search_query}" if lang_code == 'en' else 
                             f"गूगल पर खोजा गया: {search_query}" if lang_code == 'hi' else 
                             f"ಗೂಗಲ್‌ನಲ್ಲಿ ಹುಡುಕಿದೆ: {search_query}")
                speak(res)
                with open('chat_log.csv', 'w', newline='', encoding='utf-8') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow([query, res,timestamp])


            elif 'sleep' in query or 'quit' in query or 'सो जाओ' in query or 'बंद करो' in query or 'ನಿದ್ರೆ' in query or 'ನಿಲ್ಲಿಸಿ' in query:
                speak('Thank you so much! I’ll be right here when you need me again.' if lang_code == 'en' else 
                      'धन्यवाद! फिर मिलेंगे।' if lang_code == 'hi' else 
                      'ಧನ್ಯವಾದಗಳು! ಮತ್ತೆ ಕಾಣೋಣ.')
                st.session_state.listening = False


            elif 'send' or 'Email' or 'ಇಮೇಲ್ ಕಳುಹಿಸಿ' or 'ಸಂದೇಶ' or 'ईमेल भेजें' or 'ईमेल' in query:
                try:
                    speak("What to send?" if lang_code == 'en' else 
                  "क्या भेजना है?" if lang_code == 'hi' else "ಏನು ಕಳುಹಿಸಬೇಕು?")
                    content = takeCommand()
                    to = "email@gmail.com"    
                    # speak("To whom?")
                    sendEmail(to, content)
                    speak("Email has been sent!" if lang_code == 'en' else 
                  "ईमेल भेज दिया गया है" if lang_code == 'hi' else "ಇಮೇಲ್ ಕಳುಹಿಸಲಾಗಿದೆ")
                except Exception as e:
                    speak("The api not genereted!" if lang_code == 'en' else 
                  "क्षमा। मैं यह ईमेल भेजने में सक्षम नहीं हूं" if lang_code == 'hi' else "ದೋಷವೊಂದು ಉಂಟಾಗಿದೆ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ")

            else:
                speak("I'm really sorry, I didn't catch that. Would you mind trying again, please?" if lang_code == 'en' else 
                      "मुझे समझ नहीं आया। कृपया फिर से प्रयास करें।" if lang_code == 'hi' else 
                      "ನಾನು ಸಹಾಯ ಮಾಡಲು ಸಾಧ್ಯವಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೊಮ್ಮೆ ಪ್ರಯತ್ನಿಸಿ.")

        elif query == "Timeout" or query == "समय समाप्त" or query == "ಟೈಮೌಟ್":
            speak("I didn’t catch anything, sweetie. Could you please try again?" if lang_code == 'en' else 
                  "कोई आवाज़ नहीं सुनी। कृपया फिर से प्रयास करें।" if lang_code == 'hi' else 
                  "ಏನೂ ಕೇಳಲಾಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.")
        elif query == "Unknown" or query == "अज्ञात" or query == "ಅಜ್ಞಾತ":
            speak("I couldn’t quite understand that, Can you please repeat it?" if lang_code == 'en' else 
                  "समझ नहीं पाया। कृपया फिर से प्रयास करें।" if lang_code == 'hi' else 
                  "ಗುರುತಿಸಲಾಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.")
        else:
            speak("Oh no! Something went wrong. Let me know how I can be of help." if lang_code == 'en' else 
                  "एक त्रुटि हुई। कृपया फिर से प्रयास करें।" if lang_code == 'hi' else 
                  "ದೋಷವೊಂದು ಉಂಟಾಗಿದೆ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.")

        time.sleep(2.5)
        st.rerun()

def nav():
    menu = ["Home","Emotion Recognition mode"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice=="Emotion Recognition mode":
        device = 'cuda' if cv2.cuda.getCudaEnabledDeviceCount() > 0 else 'cpu'
        er = EmotionRecognition(device=device)
        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # CAP_DSHOW to reduce latency on Windows

        if not cam.isOpened():
            print("Error: Cannot access the camera.")
            exit()

        # Set optimal frame size
        frame_width, frame_height = 640, 480
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

        frame_counter = 0
        fps = 0

        while True:
            start_time = time.time()
            success, frame = cam.read()
            if not success:
                print("Failed to capture frame.")
                break
            
            # Preprocess frame: Grayscale conversion for consistency
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)  # Convert back to 3-channel for emotion recognition

            # Process every 3rd frame to improve performance if needed
            if frame_counter % 3 == 0:
                frame = er.recognise_emotion(gray_frame, return_type='BGR')

            frame_counter += 1
            # Calculate and display FPS
            elapsed_time = time.time() - start_time
            fps = 1.0 / elapsed_time if elapsed_time > 0 else 0
            cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)


            # Display the frame
            cv2.imshow("Emotion Recognition", frame)

            # Press 'Esc' to exit
            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                break
            
        # Release resources
        cam.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    nav()
    main()
