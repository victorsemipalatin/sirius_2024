import os
import time
import tqdm
import matplotlib.pyplot as plt
from openai import OpenAI


# инициализация языковой модели
client = OpenAI(
    base_url="https://api.sambanova.ai/v1", 
    api_key="07fadff5-5caf-400a-b5bb-c6386e466bb3"
)


client_ooo = OpenAI(
    base_url="https://api.sambanova.ai/v1", 
    api_key="1ae209ec-3dfc-40bc-9ad4-e14465a87730"
)

client_vic = OpenAI(
    base_url = "https://api.sambanova.ai/v1",
    api_key='7fe27712-17db-467c-bc36-a4dfdfae19a3'
)


def get_tags(clusters):
    """
        Tags extractor
        clusters: list of clusters` dict
        return: tags
    """
    result = []
    i = 0
    for cluster in clusters:
        tags = list(cluster.keys())
        values = [cluster[el] for el in tags]
        res = []
        for i, tag in tqdm.tqdm(enumerate(tags)):
            question = "Важно: сформулируй общую проблему в следующих предложениях в трёх словах: " + tag
            try:
                completion = client.chat.completions.create(
                model="Meta-Llama-3.1-405B-Instruct",
                messages = [
                    {"role": "system", "content": question}],
                stream= True)
                answer = ""
                for chunk in completion:
                    answer += chunk.choices[0].delta.content + " "
                res.append(answer)
                if i % 4 == 0 and i != 0:
                    time.sleep(5)
            except:
                try:
                    completion = client_vic.chat.completions.create(
                        model="Meta-Llama-3.1-405B-Instruct",
                        messages=[
                            {"role": "system", "content": question}],
                        stream=True)
                    answer = ""
                    for chunk in completion:
                        answer += chunk.choices[0].delta.content + " "
                    res.append(answer)
                    time.sleep(5)
                except:
                    pass
            finally:
                pass
        final = {}
        for i, el in enumerate(res):
            final[el] = values[i]
        result.append(final)
    return result


def get_texts(clusters): # получение анализа графиков
    """
        Text extractor
        clusters: list of clusters` dict
        return: texts
    """
    texts = []
    time.sleep(10)
    i = 0
    for cluster in clusters:
        promt = ""
        promt = "По опросам уволившихся сотрудников было выявлено, что "
        for el in cluster.keys():
            promt += f"{cluster[el]} процентов человек уволилось из-за {el}, "
        promt = promt[:-2] + ". "
        promt += "Сделай вывод, что стоит сделать компании для дальнейшего развития. В своём отчёте используй числа, которые тебе даны. Напиши не более 5 тезисов без разделения на пункты. "
        try:
            question = promt
            completion_ooo = client_ooo.chat.completions.create(
            model="Meta-Llama-3.1-405B-Instruct",
            messages = [
                {"role": "system", "content": question}],
            stream= True)
            answer = ""
            for chunk in completion_ooo:
                answer += chunk.choices[0].delta.content + " "
        except Exception as err:
            answer = "gjdgjkdljgfkdlfgdkglj"
            print(err)
        texts.append(answer.replace("*", ""))

    return texts


def get_pictures(results):
    """
        Graphics creator
        results: list of processed dicts
        return: pictures
    """
    trash = "trash"
    pics = []
    for i, res in enumerate(results):
        x = [key for key in res.keys()][::-1]
        y = [res[el] for el in x]

        fig = plt.figure(figsize=(11, 5))
        plt.xlim(0, max(y) + 5)
        plt.barh(x, y, color="#416836", alpha=0.9)
        font = {'family': 'Times New Roman', 'color':  'black', 'weight': 'normal', 'size': 10} # настройки шрифта
        for index, value in enumerate(y):   
            plt.text(value, index, str(value) + "%", va='center', fontdict=font)
        plt.savefig(os.path.join(trash, f"{i}.png"), bbox_inches='tight')
        pics.append(f"{i}.png")
    return pics
