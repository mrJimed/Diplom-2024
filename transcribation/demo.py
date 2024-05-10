"""
Демонстрация использования модуля SpeechRecognitionModule.
"""
import torch

from SpeechRecognitionModule import speech2text


def transcribation(path2audio: str):
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    verbose = 1  # 0 = just output, 1 = output + time stats, 2 = output + time stats + all in-between outputs
    # verbose лучше 0 ставить, 1 для тестов
    return speech2text(path2audio,
                       device,
                       verbose)
