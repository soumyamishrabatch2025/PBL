from . import LABELS
from .common import read_json
from .data import normalize


def predict(model_path, text):
    run = model_path.parent
    config = read_json(run / "config.json")
    normalized = normalize(text, config.get("lowercase", False))
    if model_path.suffix == ".joblib":
        import joblib
        model = joblib.load(model_path)
        label = LABELS[int(model.predict([normalized])[0])]
        result = {"label": label, "normalized_text": normalized}
        if hasattr(model, "predict_proba"):
            result["probabilities"] = dict(zip(LABELS, map(float, model.predict_proba([normalized])[0])))
        return result
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(model_path, local_files_only=True).eval()
    encoded = tokenizer(normalized, return_tensors="pt", truncation=True, max_length=config["transformer"]["max_length"])
    with torch.inference_mode():
        probabilities = model(**encoded).logits.softmax(-1)[0].numpy()
    return {"label": LABELS[int(probabilities.argmax())], "normalized_text": normalized,
            "probabilities": dict(zip(LABELS, map(float, probabilities)))}
