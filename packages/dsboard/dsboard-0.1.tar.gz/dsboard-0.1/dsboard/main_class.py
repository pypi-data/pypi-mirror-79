import os

class dsboard:
    def __init__(self, name):
        self.path = os.path.join(os.getcwd() , name)
        if not os.path.exists(self.path):
            try:
                os.mkdir(self.path)
            except OSError:
                print ("Creation of the directory %s failed" % self.path)
        self.name = name
        self.__configFile = '[\n{\n"project_name": "' + name + '",\n'
        self.__configFile += '"project_folder": "' + self.path + '"\n},\n'
        self.__plots = []

    def __createDataFileHead(self, name, ptype):
        assert self.__findIndex(name) == -1, f"plot with name '{name}' already exists"
        path = os.path.join(self.path, name+'.data')
        if os.path.exists(path):
            os.remove(path)
        self.__plots.append({
            "type" : ptype,
            "path" : path,
            "name" : name
        })
        self.__configFile+='{\n'
        self.__configFile+=f'"plot_name": "{name}",\n'
        self.__configFile+=f'"data_file": "{name}.data",\n'
        self.__configFile+=f'"plot_type" : "{ptype}",\n'

    def addLinePlot(self, name, xLabel = "", yLabel = "", bgColor = (0, 99, 132, 0.2), boColor = (0, 99, 132, 1), linet = 0.4):
        self.__createDataFileHead(name, 'line')
        self.__configFile+=f'"x_axis_label": "{xLabel}", \n'
        self.__configFile+=f'"y_axis_label": "{yLabel}", \n'
        bgColor = 'rgba' + str(bgColor)
        self.__configFile+=f'"background_color": "{bgColor}",\n'
        boColor = 'rgba' + str(boColor)
        self.__configFile+=f'"border_color": "{boColor}",\n'
        self.__configFile+=f'"line_tension": "{linet}"\n'
        self.__configFile+='},\n'

    def addTextPlot(self, name):
        self.__createDataFileHead(name, 'text')
        self.__configFile = self.__configFile[:-2] + '\n'
        self.__configFile+='},\n'

    def addImagePlot(self, name, img_format):
        assert self.__findIndex(name) == -1, f"plot with name '{name}' already exists"
        self.__plots.append({
            "type" : "image",
            "path" : name+'.'+img_format,
            "name" : name
        })
        self.__configFile+='{\n'
        self.__configFile+=f'"plot_name": "{name}",\n'
        self.__configFile+=f'"data_file": "{self.__plots[-1]["path"]}",\n'
        self.__configFile+='"plot_type" : "image"\n'
        self.__configFile+='},\n'



    def createPlots(self):
        self.__configFile = self.__configFile[:-2]
        self.__configFile+='\n]'

        config_path = os.path.join(self.path, "config.json")
        with open(config_path, "w") as f:
            f.write(self.__configFile)

    def __findIndex(self, name):
        for i in range(len(self.__plots)):
            if self.__plots[i]['name'] == name:
                return i
        return -1

    def append(self, name, data):
        ind = self.__findIndex(name)
        assert ind != -1, f"plot with name '{name}' not found"

        plot = self.__plots[ind]
        if plot['type'] == 'line':
            if isinstance(data, list):
                with open(plot['path'], "a") as f:
                    for point in data:
                        f.write(str(point[0]) + ' ' + str(point[1]) + '\n')

            else:
                with open(plot['path'], "a") as f:
                    f.write(str(data[0]) + ' ' + str(data[1]) + '\n')
        
        elif plot['type'] == 'text':
            with open(plot['path'], "a") as f:
                    f.write(data)

    def getPath(self, name):
        ind = self.__findIndex(name)
        assert ind != -1, f"plot with name '{name}' not found"

        return self.__plots[ind]['path']