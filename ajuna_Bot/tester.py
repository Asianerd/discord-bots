# import psutil

# def ram_bar(p, length):
#     final = [' ' for _ in range(length)]
#     if p > 1:
#         p = 1
#     for i in range(int(length * p)):
#         final[i] = "#"
#     return ''.join(final)

# for i in range(10):
#     print(f'[{ram_bar(i/10, 10)}]')

# pip install:
#   torch
#   transformers
#   sentencepiece


from transformers import T5Tokenizer, T5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")


while True:
    outputs = model.generate(
        tokenizer(input(), return_tensors="pt").input_ids,
        max_length=100,
        num_beams=4,
        do_sample=True
    )
    print(tokenizer.decode(outputs[0]))

