import torch
import transformers

torch.hub.load("unitaryai/detoxify", "multilingual_toxic_xlm_r")
transformers.pipeline(model="blanchefort/rubert-base-cased-sentiment")
