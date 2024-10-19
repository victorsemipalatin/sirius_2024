import ml_prev
import os
import grig_module
import matplotlib.pyplot as plt


static = "static"


def get_pictures(results, questions): # получение графиков
    pics = []
    for i, res in enumerate(results):
        x = [key for key in res.keys()][::-1]
        y = [res[el] for el in x]

        fig = plt.figure(figsize=(11, 5))
        plt.xlim(0, max(y) + 5)
        plt.barh(x, y, color="#416836", alpha=0.9)
        font = {'family': 'serif', 'color':  'black', 'weight': 'normal', 'size': 10} # настройки шрифта
        for index, value in enumerate(y):   
            plt.text(value, index, str(value) + "%", va='center', fontdict=font)
        plt.title(questions[i])
        plt.savefig(os.path.join(static, f"histogram{i + 1}.jpg"), bbox_inches='tight')
        pics.append(f"histogram{i + 1}.jpg")
    return pics


def get_report(file):
    questions, clusters = ml_prev.process(file)
    tags = grig_module.get_tags(clusters)
    texts = grig_module.get_texts(clusters)
    for i, text in enumerate(texts):
        with open(os.path.join(static, f"text{i + 1}.txt"), 'w') as f:
            f.write(text)
    pics = get_pictures(tags, questions)
