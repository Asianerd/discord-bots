from transformers import T5Tokenizer, T5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small")


def generate(prompt):
    outputs = model.generate(
        tokenizer(prompt, return_tensors="pt").input_ids,
        max_length=100,
        num_beams=4,
        do_sample=True
    )
    final = str(tokenizer.decode(outputs[0])).strip("<pad>").strip("</s>")
    return final