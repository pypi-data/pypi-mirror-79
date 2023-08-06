from dsboard import dsboard
from time import sleep
from random import randrange, random

def main():
    project = dsboard("TestProject")
    project.addLinePlot("sensorSimulation", "time", "temperature(°C)", linet = 0)
    project.addTextPlot("console")
    project.addImagePlot("schematic", "jpg")
    project.createPlots()

    t = 0
    while True:
        fail = random()
        if fail > 0.8:
            project.append("console", f"Temperature sensor reading failed at {t}s\n")
        else:
            temp = randrange(20, 25)
            project.append("sensorSimulation", (t, temp))
        t+=2
        sleep(2)


if __name__ == "__main__":
    main()