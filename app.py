import gradio as gr
import edge_tts
import asyncio
import os
# https://speech.platform.bing.com/consumer/speech/synthesize/readaloud/voices/list?trustedclienttoken=6A5AA1D4EAFF4E9FB37E23D68491D6F4
SUPPORTED_VOICES = {
    'Xiaoxiao-晓晓': 'zh-CN-XiaoxiaoNeural',
    'Xiaoyi-晓伊': 'zh-CN-XiaoyiNeural',
    'Yunjian-云健': 'zh-CN-YunjianNeural',
    'Yunxi-云希': 'zh-CN-YunxiNeural',
    'Yunxia-云夏': 'zh-CN-YunxiaNeural',
    'Yunyang-云扬': 'zh-CN-YunyangNeural',
    'liaoning-Xiaobei-晓北辽宁': 'zh-CN-liaoning-XiaobeiNeural',
    'shaanxi-Xiaoni-陕西晓妮': 'zh-CN-shaanxi-XiaoniNeural'
}

# Changement de voix
def changeVoice(voices):
    example = SUPPORTED_VOICES[voices]
    example_file = os.path.join(os.path.dirname(__file__), "example/"+example+".wav")
    return example_file

# Texte en parole
async def textToSpeech(text, voices, rate, volume):
    output_file = "output.mp3"
    voices = SUPPORTED_VOICES[voices]
    if (rate >= 0):
        rates = rate = "+" + str(rate) + "%"
    else:
        rates = str(rate) + "%"
    if (volume >= 0):
        volumes = "+" + str(volume) + "%"
    else:
        volumes = str(volume) + "%"
    communicate = edge_tts.Communicate(text,
                                       voices,
                                       rate=rates,
                                       volume=volumes,
                                       proxy=None)
    await communicate.save(output_file)
    audio_file = os.path.join(os.path.dirname(__file__), "output.mp3")
    if (os.path.exists(audio_file)):
        return audio_file
    else:
        raise gr.Error("La conversion a échoué !")
        return FileNotFoundError


# Effacer les résultats de la conversion
def clearSpeech():
    output_file = os.path.join(os.path.dirname(__file__), "output.mp3")
    if (os.path.exists(output_file)):
        os.remove(output_file)
    return None, None


with gr.Blocks(css="style.css", title="Text to Speech") as demo:
    gr.Markdown("""
    # Texte en parole avec Microsoft Edge
    Utilisation de edge-tts pour la conversion
    """)
    with gr.Row():
        with gr.Column():
            text = gr.TextArea(label="Texte", elem_classes="text-area")
            btn = gr.Button("Générer", elem_id="submit-btn")
        with gr.Column():
            voices = gr.Dropdown(choices=[
                "Xiaoxiao-晓晓", "Xiaoyi-晓伊", "Yunjian-云健", "Yunxi-云希",
                "Yunxia-云夏", "Yunyang-云扬", "liaoning-Xiaobei-晓北辽宁",
                "shaanxi-Xiaoni-陕西晓妮"
            ],
                                 value="Xiaoxiao-晓晓",
                                 label="Voix",
                                 info="Veuillez choisir une voix",
                                 interactive=True)
            
            example = gr.Audio(label="Exemple",
                              value="example/zh-CN-XiaoxiaoNeural.wav",
                              interactive=False,
                              elem_classes="exemple")

            voices.change(fn=changeVoice,inputs=voices,outputs=example)
            rate = gr.Slider(-100,
                             100,
                             step=1,
                             value=0,
                             label="Augmentation/diminution de la vitesse",
                             info="Accélérer ou ralentir la vitesse",
                             interactive=True)
            
            volume = gr.Slider(-100,
                               100,
                               step=1,
                               value=0,
                               label="Augmentation/diminution du volume",
                               info="Augmenter ou diminuer le volume",
                               interactive=True)
            audio = gr.Audio(label="Sortie",
                             interactive=False,
                             elem_classes="audio")
            clear = gr.Button("Effacer", elem_id="clear-btn")
            btn.click(fn=textToSpeech,
                      inputs=[text, voices, rate, volume],
                      outputs=[audio])
            clear.click(fn=clearSpeech, outputs=[text, audio])

if __name__ == "__main__":
    demo.launch()
