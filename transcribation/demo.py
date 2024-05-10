"""
Демонстрация использования модуля SpeechRecognitionModule.
"""
import torch
from SpeechRecognitionModule import speech2text

# Setting up parameters
path2audio = "path/to/your/audio" # тут путь прям к файлу типа audio.avi или как там, ну ты понял
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
verbose = 1  # 0 = just output, 1 = output + time stats, 2 = output + time stats + all in-between outputs
#verbose лучше 0 ставить, 1 для тестов
# Getting text from audio
output_text = speech2text(path2audio,
                          device,
                          verbose)
print(output_text)
