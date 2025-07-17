---
license: apache-2.0
language:
- id
metrics:
- wer
pipeline_tag: automatic-speech-recognition
---

# Whisper-medium-id model for CTranslate2

This repository contains the conversion of [cahya/whisper-medium-id](https://huggingface.co/cahya/whisper-medium-id) to the [CTranslate2](https://github.com/OpenNMT/CTranslate2) model format.

This model can be used in CTranslate2 or projects based on CTranslate2 such as [faster-whisper](https://github.com/systran/faster-whisper).

## Example

```python
from faster_whisper import WhisperModel

model = WhisperModel("cahya/faster-whisper-medium-id")

segments, info = model.transcribe("audio.mp3", language="en", condition_on_previous_text=False)
for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
```

## Conversion details

The original model was converted with the following command:

```
ct2-transformers-converter --model cahya/whisper-medium-id --output_dir faster-whisper-medium-id \
    --copy_files tokenizer-config.json preprocessor_config.json --quantization float16
```

Note that the model weights are saved in FP16. This type can be changed when the model is loaded using the [`compute_type` option in CTranslate2](https://opennmt.net/CTranslate2/quantization.html).

## More information

**For more information about the original model, see its [model card](https://huggingface.co/cahya/faster-whisper-medium-id).**