from ModelClass import ModelClass
import time




# W DZIWNY SPOSOB WSZYSTKIE MODELE DĄŻĄ DO WIĘKSZEGO ANTYKONSERWATYZMU SPRAWDZIC CZY COS NIE ZEPSULEM W POPRZEDNIM COMMICIE
# UPEWNILEM SIE ZE STAN POCZATKOWY MA ROZKLAD NORMALNY O SREDNIEJ W 0.5 MNIEJ WIECEJ



def test_d_parameter(d_value):
    start = time.time()
    model2005 = ModelClass()
    end = time.time()
    print("inicjalizacja[s]:")
    print(end - start)

    model2005.set_D(d_value)
    print("D:"+str(d_value))
    d_tmp = []
    start = time.time()
    for iteration in range(333):
        model2005.model_timestep_synchronous()
        d_tmp.append(model2005.get_sd())
    end = time.time()
    print("333 iteracji modelu[s]:")
    print(end - start)
    file_out = open('d_'+str(d_value)+'_sdev.txt', 'w')
    print(d_tmp, file=file_out)
    opinions = model2005.get_support()
    file_out2 = open('opinions_' + str(d_value) + '.txt', 'w')
    print(opinions, file=file_out2)

for i in range(4):
    test_d_parameter(0.01+(i/100))








