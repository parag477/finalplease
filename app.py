import streamlit as st
from streamlit_webrtc import webrtc_streamer, RTCConfiguration
import cv2
import av
from makeup_app import MakeupApplication  # Your MakeupApplication class

# Define a TURN server configuration
# RTC_CONFIGURATION = RTCConfiguration({
#     "iceServers": [
#         {"urls": ["stun:stun.l.google.com:19302"]},  # STUN server
#         {
#             "urls": ["turn:turn.anyfirewall.com:443?transport=tcp"],  # Example TURN server
#             "username": "webrtc",
#             "credential": "webrtc"
#         }
#     ]
# })

rtc_config = RTCConfiguration({
            "iceServers": [
                {"urls": "stun:stun.l.google.com:19302"},  # Google's STUN server
                {"urls": "stun:stun1.l.google.com:19302"},  # Backup STUN server
                {"urls": "stun:bn-turn2.xirsys.com"},  # Backup STUN server
                {"urls": "turn:openrelay.metered.ca:80", "username": "openrelayproject", "credential": "openrelayproject"},
                {"urls": "turn:turn.mozilla.org:3478", "username": "mozilla", "credential": "webrtcdemo"},
                {"urls": [ "turn:bn-turn2.xirsys.com:80?transport=udp", 
                                "turn:bn-turn2.xirsys.com:3478?transport=udp", 
                                "turn:bn-turn2.xirsys.com:80?transport=tcp",
                                "turn:bn-turn2.xirsys.com:3478?transport=tcp", 
                                "turns:bn-turn2.xirsys.com:443?transport=tcp", 
                                "turns:bn-turn2.xirsys.com:5349?transport=tcp"], "username": "41G6nRJn3PLi5np_1pjDKAtO9fygkHx94ENGd59gP28EvVonLQ10bXjIA5sxYcLIAAAAAGcINydwYXJhZzQ3Nw==", "credential": "275e088c-8745-11ef-9116-0242ac140004"},
                ]
            })


class VideoProcessor:
    def __init__(self):
        self.makeup_app = MakeupApplication()

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img = self.makeup_app.process_frame(img)
        return av.VideoFrame.from_ndarray(img, format="bgr24")

st.title("Virtual Makeup Application with Webcam")

webrtc_streamer(key="example", video_processor_factory=VideoProcessor, rtc_configuration=rtc_config)
