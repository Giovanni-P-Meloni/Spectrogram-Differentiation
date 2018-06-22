import numpy
import matplotlib.pyplot as plt
import pylab
from scipy.io import wavfile
from scipy.fftpack import fft
from scipy import signal

def getFreqArray(_sound, _soundSampleRate):
    _soundLenght = len(_sound)
    amostraPontos_freq = int (numpy.ceil((_soundLenght + 1) / 2.0))

    return numpy.arange(0, amostraPontos_freq, 1.0) * (_soundSampleRate / _soundLenght)

# Para representar o som farei um grafico dos valores do canal de som pelo tempo
#Criando um array de pontos em uma dimensao, que sera o tempo
def AmpPlot(amostraFreq, amostraPontos, _sound):

    arrayTempo =  numpy.arange(0, amostraPontos, 1)
    arrayTempo = arrayTempo / amostraFreq

    #em milisegundos
    arrayTempo = arrayTempo * 1000  

    plt.plot(arrayTempo, _soundOneChannel, color='G')
    plt.xlabel('Time (ms)')
    plt.ylabel('Amplitude')
    plt.show()
    return


# Para ter a frequencia usarei a Transformada de Fourier (FFT), 
def FreqPlot(_sound, _soundSampleRate):
    #Comprimento do audio
    _soundLenght = len(_sound)

    arrayFFT = fft(_sound)

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

    freqArray = numpy.arange(0, amostraPontos_freq, 1.0) * (_soundSampleRate / _soundLenght)

    plt.plot(freqArray/1000, 10 * numpy.log10 (arrayFFT), color='B')
    plt.xlabel('Frequency (Khz)')
    plt.ylabel('Power (dB)')
    plt.show()
    return


#Declaracoes e Entrada
filenames = ["cello.wav", "ClassicalGuitar.wav", "gtr-jaz-2.wav", "harpsi-cs.wav"]
comparisons = []
answer = 1000000000
pos = 0
for i in range(0, 4):
    _soundSampleRate, _sound = wavfile.read(filenames[i])
    comparisons.append(getFreqArray(_sound, _soundSampleRate))

print(".wav file name:")
_audio = str(input()).rstrip()

#Lê o arquivo e pega a amostragem de frequencia e o som
_soundSampleRate, _sound = wavfile.read(_audio)

#Checa se o arquivo wave eh 16bit ou 32 bit.
_soundDataType = _sound.dtype

#Convertando o array som para valores de ponto flutuante variando de -1 a 1
_sound = _sound / (2.**15)

#Pega uma amostragem de pontos do arquivo de audio a partir de seu formato
_soundShape = _sound.shape
amostraPontos_audio = float(_sound.shape[0])

#Duracao do arquivo de audio
_soundDuration = _sound.shape[0] / _soundSampleRate

#Quero apenas um canal de som
_soundOneChannel = _sound

#  Plotando o audio
AmpPlot(_soundSampleRate, amostraPontos_audio, _soundOneChannel)

#  Plotando a frequencia
FreqPlot(_soundOneChannel, _soundSampleRate)


#comparing
_soundFreqArray = getFreqArray(_sound, _soundSampleRate) 

for i in range(0,4):

    if(len(_soundFreqArray) > len(comparisons[i])):
        trying = 0
        trying = numpy.linalg.norm(_soundFreqArray-comparisons[i])
    else:
        trying = numpy.linalg.norm(comparisons[i]-_soundFreqArray)
    if (trying < answer):
        answer = trying
        pos = i

print("most similar: " + filenames[pos])
print("by a Euclidian Distance of:" + answer)