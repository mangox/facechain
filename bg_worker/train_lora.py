#!/usr/bin/env python -tt
# -*- coding: utf-8 -*-
# **********************************************************************************************************
# This is the confidential unpublished intellectual property of Bybit Corporation,
# and includes without limitation exclusive copyright and trade secret rights of Bybit throughout the world.
# **********************************************************************************************************
import os
import platform
import shutil
import subprocess
from typing import Tuple

import slugify
import torch

from bg_worker.models import ModelScopeModel
from facechain.constants import base_models
from facechain.train_text_to_image_lora import prepare_dataset, data_process_fn


class Trainer:

    @staticmethod
    def train_lora_fn(base_model_path=None, revision=None, sub_path=None, output_img_dir=None, work_dir=None,
                      photo_num=0):
        torch.cuda.empty_cache()

        lora_r = 4
        lora_alpha = 32
        max_train_steps = min(photo_num * 200, 800)

        if platform.system() == 'Windows':
            command = [
                'accelerate', 'launch', 'facechain/train_text_to_image_lora.py',
                f'--pretrained_model_name_or_path={base_model_path}',
                f'--revision={revision}',
                f'--sub_path={sub_path}',
                f'--output_dataset_name={output_img_dir}',
                '--caption_column=text',
                '--resolution=512',
                '--random_flip',
                '--train_batch_size=1',
                '--num_train_epochs=200',
                '--checkpointing_steps=5000',
                '--learning_rate=1.5e-04',
                '--lr_scheduler=cosine',
                '--lr_warmup_steps=0',
                '--seed=42',
                f'--output_dir={work_dir}',
                f'--lora_r={lora_r}',
                f'--lora_alpha={lora_alpha}',
                '--lora_text_encoder_r=32',
                '--lora_text_encoder_alpha=32',
                '--resume_from_checkpoint="fromfacecommon"'
            ]

            try:
                subprocess.run(command, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error executing the command: {e}")
        else:
            os.system(
                f'PYTHONPATH=. accelerate launch facechain/train_text_to_image_lora.py '
                f'--pretrained_model_name_or_path={base_model_path} '
                f'--revision={revision} '
                f'--sub_path={sub_path} '
                f'--output_dataset_name={output_img_dir} '
                f'--caption_column="text" '
                f'--resolution=512 '
                f'--random_flip '
                f'--train_batch_size=1 '
                f'--num_train_epochs=200 '
                f'--checkpointing_steps=5000 '
                f'--learning_rate=1.5e-04 '
                f'--lr_scheduler="cosine" '
                f'--lr_warmup_steps=0 '
                f'--seed=42 '
                f'--output_dir={work_dir} '
                f'--lora_r={lora_r} '
                f'--lora_alpha={lora_alpha} '
                f'--lora_text_encoder_r=32 '
                f'--lora_text_encoder_alpha=32 '
                f'--resume_from_checkpoint="fromfacecommon"')

    @staticmethod
    def run(model_scope: ModelScopeModel,
            # uuid: str,
            # instance_images: list,
            # base_model_name: str,
            # output_model_name: str,
            ) -> Tuple[bool, str]:
        # Check Cuda
        if not torch.cuda.is_available():
            return False, "CUDA is not available"

        if not model_scope.upload_images:
            return False, "需要上传训练图片"

        instance_images = model_scope.upload_images.split(',')
        # Check Instance Valid
        if instance_images is None:
            return False, '您需要上传训练图片(Please upload photos)!'

        # Check output model name
        if not model_scope.output_model_name:
            return False, '请指定人物lora的名称(Please specify the character LoRA name)！'

        # Limit input Image
        if len(instance_images) > 20:
            return False, '请最多上传20张训练图片(20 images at most!)'

        # Check UUID & Studio
        uuid = model_scope.token
        # if not uuid:
        #     if os.getenv("MODELSCOPE_ENVIRONMENT") == 'studio':
        #         return False, "请登陆后使用(Please login first)! "
        #     else:
        #         uuid = 'qw'

        base_model = None
        base_model_name = model_scope.base_model_name
        for model in base_models:
            if model['name'] == base_model_name:
                base_model = model
                break
        else:
            return False, f"Unknown model {base_model_name}"

        base_model_path = base_model['model_id']
        revision = base_model['revision']
        sub_path = base_model['sub_path']
        output_model_name = slugify.slugify(model_scope.output_model_name)

        # mv user upload data to target dir
        instance_data_dir = os.path.join('/tmp', uuid, 'training_data', base_model_path, output_model_name)
        print("--------uuid: ", uuid)

        if not os.path.exists(f"/tmp/{uuid}"):
            os.makedirs(f"/tmp/{uuid}")
        work_dir = f"/tmp/{uuid}/{base_model_path}/{output_model_name}"

        if os.path.exists(work_dir):
            return False, "人物lora名称已存在。(This character lora name already exists.)"

        print("----------work_dir: ", work_dir)
        shutil.rmtree(work_dir, ignore_errors=True)
        shutil.rmtree(instance_data_dir, ignore_errors=True)

        prepare_dataset([img['name'] for img in instance_images], output_dataset_dir=instance_data_dir)
        data_process_fn(instance_data_dir, True)

        # train lora
        print("instance_data_dir", instance_data_dir)
        Trainer.train_lora_fn(base_model_path=base_model_path,
                              revision=revision,
                              sub_path=sub_path,
                              output_img_dir=instance_data_dir,
                              work_dir=work_dir,
                              photo_num=len(instance_images))

        # message = '''<center><font size=4>训练已经完成！请切换至 [无限风格形象写真] 标签体验模型效果。</center>
        #
        # <center><font size=4>(Training done, please switch to the Infinite Style Portrait tab to generate photos.)</center>'''
        # print(message)
        return True, "训练已经完成！请切换至 [无限风格形象写真] 标签体验模型效果。"
