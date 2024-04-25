from dataclasses import dataclass
from os.path import dirname, abspath

# replace '\' on windows to '/'
PROJECT_ROOT: str = '/'.join(abspath(dirname(__file__)).split('\\')) if '\\' in abspath(dirname(__file__)) else abspath(dirname(__file__))

# ===================================================================================
# 以下为推断的配置
@dataclass
class InferConfig:
    max_seq_len: int = 320                          # 回答的最大长度
    mixed_precision: str = "bf16"                   # 混合精度 ''no','fp16','bf16' or 'fp8'

    # 全量DPO模型文件, tokenizer文件和model权重放在同一个文件夹
    model_dir: str = PROJECT_ROOT + '/model_save/sft/'

    # lora PDO 合并后的模型文件
    # model_file: str = PROJECT_ROOT + '/model_save/chat_small_t5.best.dpo.lora_merged.bin'
    
    # this confing for api demo:
    api_key: str = ""
    host: str = '127.0.0.1'
    port: int = 8812
    reload: bool = True
    workers: int = 1
    log_level: str = 'info'


# 以下为sft配置
@dataclass
class SFTconfig:
    max_seq_len: int = 384 + 8                # 8 for eos token

    finetune_from_ckp_file = PROJECT_ROOT + '/model_save/'

    tokenizer_dir: str = PROJECT_ROOT + '/model_save/'  # tokenizer一般和model权重放在同一个文件夹
    sft_train_file: str = PROJECT_ROOT + '/data/sft_train.json'

    batch_size: int = 19
    num_train_epochs: int = 600
    save_steps: int = 1000000
    gradient_accumulation_steps: int = 4
    learning_rate: float = 5e-5
    logging_first_step: bool = True
    logging_steps: int = 100                      
    output_dir: str = PROJECT_ROOT + '/model_save/sft'
    warmup_steps: int = 100
    fp16: bool = True
    seed: int = 240422



#======================================================================================
# 以下为模型的配置
@dataclass
class T5ModelConfig:

    d_ff: int = 3072                        # 全连接层维度

    d_model: int = 768                      # 词向量维度
    num_heads: int = 12                     # 注意力头数 d_model // num_heads == d_kv
    d_kv: int = 64                          # d_model // num_heads

    num_decoder_layers: int = 10            # Transformer decoder 隐藏层层数
    num_layers: int = 10                    # Transformer encoder 隐藏层层数