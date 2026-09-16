
import torch

from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM

# 指定模型ID
model_id="Qwen/Qwen-1.5-0.5B-Chat"

# 设置设备，优先使用GPU
device ="cuda" if torch.cuda.is_available() else "cpu"
print(f"使用设备: {device}")

# 加载分词器
tokenizer = AutoTokenizer.from_pretrained(model_id)

#加载模型，并将其移动到指定设备
model = AutoModelForCausalLM.from_pretrained(model_id).to(device)

print("模型和分词器加载完成!")

# 准备对话输入
message= [
    {"role":"system","content":"你是一个帮助用户的智能体"},
    {"role":"user","content":"你好，帮我写一个简单的排序函数"}
]

# 使用分词器的模板格式化输入
text =tokenizer.apply_chat_template(
    message,
    tokenize=False,
    add_generation_prompt=True,
    )

# 编码输入文本
model_inputs = tokenizer([text],return_tensors="pt").to(device)

print("编码后的输入文本:")
print(model_inputs)


generated_ids=model.generate(
    model_inputs.input_ids,
    max_new_tokens=512
)

generate_ids=[
    output_ids[len(input_ids):]for input_ids ,output_ids in zip(model_inputs.input_ids,generated_ids)
]

response=tokenizer.batch_decode(generate_ids,skip_special_tokens=True)[0]

print("\n模型回复:")
print(response)
