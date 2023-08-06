import __init__

retSamples = []
for i in range(5):
    __init__.recordAsyn("test"+str(i)+".wav",RECORD_SECONDS=10,TH=0.01,retSamples=retSamples)
print(retSamples)