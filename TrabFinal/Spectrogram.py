import numpy
import matplotlib.pyplot as plt
import pylab
from scipy.io import wavfile
from scipy.fftpack import fft

_audio = "harpsi-cs.wav"

#Lê o arquivo e pega a amostragem de frequencia e o som
amostraFreq, _sound = wavfile.read(_audio)

#Checa se o arquivo wave eh 16bit ou 32 bit.
_soundDataType = _sound.dtype

#Convertando o array som para valores de ponto flutuante variando de -1 a 1
_sound = _sound / (2.**15)

#Pega uma amostragem de pontos do arquivo de audio a partir de seu formato
_soundShape = _sound.shape
amostraPontos_audio = float(_sound.shape[0])

#Duracao do arquivo de audio
_soundDuration = _sound.shape[0] / amostraFreq

#Quero apenas um canal de som
_soundOneChannel = _sound

#  Plotando o audio
# Para representar o som farei um grafico dos valores do canal de som pelo tempo
#Criando um array de pontos em uma dimensao, que sera o tempo
arrayTempo =  numpy.arange(0, amostraPontos_audio, 1)

arrayTempo = arrayTempo / amostraFreq

#em milisegundos
arrayTempo = arrayTempo * 1000  

plt.plot(arrayTempo, _soundOneChannel, color='G')
plt.xlabel('Time (ms)')
plt.ylabel('Amplitude')
plt.show()

#  Plotando o espectrograma
# Para ter a frequencia usarei a Transformada de Fourier (FFT), 

#Comprimento do audio
_soundLenght = len(_sound)

arrayFFT = fft(_soundOneChannel)

amostraPontos_freq = int (numpy.ceil((_soundLenght + 1) / 2.0))
arrayFFT = arrayFFT[0:amostraPontos_freq]

#A FFT retorna um numero imaginario, porem quero apenas a parte real desse numero (a magnitude) 
arrayFFT = abs(arrayFFT)

#agora preciso arrumar o array de frequencia para que ele escale segundo o comprimento do audio
#dessa maneira a magnitude nao depende da amostragem de frequencia ou do comprimento do sinal

arrayFFT = arrayFFT / float(_soundLenght)

#FFT possui numeros negativos e positivos, quero apenas os positivos
arrayFFT = arrayFFT **2


if _soundLenght % 2 > 0: #NUmero impar de pontos da fft
    arrayFFT[1:len(arrayFFT)] = arrayFFT[1:len(arrayFFT)] * 2

else: #Numer par de pontos na fft
    arrayFFT[1:len(arrayFFT) -1] = arrayFFT[1:len(arrayFFT) -1] * 2  

freqArray = numpy.arange(0, amostraPontos_freq, 1.0) * (amostraFreq / _soundLenght)

plt.plot(freqArray/1000, 10 * numpy.log10 (arrayFFT), color='B')
plt.xlabel('Frequency (Khz)')
plt.ylabel('Power (dB)')
plt.show()
