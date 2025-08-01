import json
import csv
from nltk import word_tokenize
from nltk.translate.bleu_score import sentence_bleu


def f1_score(pred, gold):
    pred_tokens = word_tokenize(pred.lower())
    gold_tokens = word_tokenize(gold.lower())
    common = set(pred_tokens) & set(gold_tokens)

    if not common:
        return 0.0

    precision = len(common) / len(pred_tokens)
    recall = len(common) / len(gold_tokens)
    return 2 * precision * recall / (precision + recall)

def bleu_score(pred, gold):
    return sentence_bleu([word_tokenize(gold.lower())], word_tokenize(pred.lower()))

def evaluate_models(json_path="evaluacion_comparativa.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    modelos = ["ollama", "chatgpt", "notebooklm"]
    acumuladores = {m: {"f1": 0.0, "bleu": 0.0} for m in modelos}
    resultados = []

    for item in data:
        resultado_item = {
            "prompt": item["prompt"],
            "esperada": item["esperada"]
        }

        for modelo in modelos:
            respuesta = item.get(modelo, "")
            f1 = f1_score(respuesta, item["esperada"])
            bleu = bleu_score(respuesta, item["esperada"])

            resultado_item[f"{modelo}_f1"] = round(f1, 4)
            resultado_item[f"{modelo}_bleu"] = round(bleu, 4)

            acumuladores[modelo]["f1"] += f1
            acumuladores[modelo]["bleu"] += bleu

        resultados.append(resultado_item)

    total = len(data)
    print(f"📊 Evaluación sobre {total} preguntas\n")

    for modelo in modelos:
        print(f"Modelo: {modelo.upper()}")
        print(f"  🔹 F1 Promedio:   {acumuladores[modelo]['f1'] / total:.4f}")
        print(f"  🔹 BLEU Promedio: {acumuladores[modelo]['bleu'] / total:.4f}\n")

    print("-" * 40)

    for r in resultados:
        print(f"❓ {r['prompt']}")
        print(f"✅ Esperada: {r['esperada']}")
        for modelo in modelos:
            print(f"🤖 {modelo}: F1={r[f'{modelo}_f1']} | BLEU={r[f'{modelo}_bleu']}")
        print("-" * 40)
        
    with open("resultados_evaluacion.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["prompt", "esperada"] + [f"{modelo}_{m}" for modelo in modelos for m in ["f1", "bleu"]]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for r in resultados:
            writer.writerow(r)

    print("📁 Resultados exportados a 'resultados_evaluacion.csv'")

if __name__ == "__main__":
    evaluate_models()