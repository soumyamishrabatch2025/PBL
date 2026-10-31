import argparse
import json

from .common import ROOT, path, read_json


def main():
    parser = argparse.ArgumentParser(description="Reproducible Hinglish sentiment experiments")
    parser.add_argument("command", choices=["prepare", "train", "report", "all", "predict", "doctor"])
    parser.add_argument("--config", default=str(ROOT / "configs/research.json"))
    parser.add_argument("--models", nargs="+", choices=["naive_bayes", "svm", "mbert"], default=["naive_bayes", "svm", "mbert"])
    parser.add_argument("--seeds", nargs="+", type=int, default=[42])
    parser.add_argument("--model-path", help="Saved .joblib pipeline or transformer checkpoint directory for predict")
    parser.add_argument("--text", help="Text to classify with predict")
    args = parser.parse_args()
    config = read_json(args.config)
    if args.command == "doctor":
        import torch
        from .common import environment
        print(json.dumps({**environment(), "cuda_available": torch.cuda.is_available(),
                          "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None}, indent=2))
        return
    if args.command == "predict":
        if not args.model_path or not args.text:
            parser.error("predict requires --model-path and --text")
        from .inference import predict
        print(json.dumps(predict(path(args.model_path), args.text), indent=2, ensure_ascii=False))
        return
    if args.command in ("prepare", "all"):
        from .data import prepare
        prepare(config)
    if args.command in ("train", "all"):
        for model in args.models:
            for seed in args.seeds:
                if model == "mbert":
                    from .transformer import train_transformer
                    train_transformer(config, seed)
                else:
                    from .baselines import train_baseline
                    train_baseline(config, model, seed)
    if args.command in ("report", "all", "train"):
        from .report import report
        report(config)


if __name__ == "__main__":
    main()
