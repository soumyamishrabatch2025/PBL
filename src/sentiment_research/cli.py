import argparse
import json

from .common import ROOT, path, read_json


def main():
    parser = argparse.ArgumentParser(description="Reproducible Hinglish sentiment experiments")
    parser.add_argument("command", choices=["prepare", "train", "report", "all", "predict", "doctor", "preflight", "audit-packet"])
    parser.add_argument("--config", default=str(ROOT / "configs/research.json"))
    parser.add_argument("--models", nargs="+", choices=["naive_bayes", "svm", "svm_word_char", "mbert", "hingbert"], default=None)
    parser.add_argument("--seeds", nargs="+", type=int, default=[42])
    parser.add_argument("--model-path", help="Saved .joblib pipeline or transformer checkpoint directory for predict")
    parser.add_argument("--text", help="Text to classify with predict")
    args = parser.parse_args()
    config = read_json(args.config)
    args.models = args.models or config.get("models", ["naive_bayes", "svm", "mbert"])
    if args.command in ("preflight", "audit-packet"):
        from .development import preflight, audit_packet
        (preflight if args.command == "preflight" else audit_packet)(config)
        return
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
                if model in ("mbert", "hingbert"):
                    from .transformer import train_transformer
                    train_transformer(config, seed, model)
                else:
                    from .baselines import train_baseline
                    train_baseline(config, model, seed)
                if config.get("evaluation_splits") == ["validation"]:
                    from .development import development_report
                    development_report(config)
    if args.command in ("report", "all", "train"):
        if config.get("evaluation_splits") == ["validation"] and args.command != "report":
            return  # Development reports are already generated after each completed run.
        from .report import report
        report(config)


if __name__ == "__main__":
    main()
