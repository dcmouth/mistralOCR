'''
Description:  通过mistral包调用ocr模型
Author: Puyol lee
Date: 2025-04-02 10:31:28
'''
import gradio as gr
from mistralai import Mistral
from pathlib import Path
import os
import base64
from mistralai import DocumentURLChunk, ImageURLChunk
from mistralai.models import OCRResponse
from typing import Union, Literal
from src.ocr import process_image, process_pdf 
import os 
import base64


def process_file(file_path: str, api_key="GcQX1IjolKz9o4VO7ta2VPzOvgWwbWtN") -> str:
    """
    处理PDF或图片文件
    
    Args:
        file_path: 文件路径
        api_key: Mistral API密钥
        
    Returns:
        输出目录路径
    """
    # file_path = file_path[0].name
    client = Mistral(api_key=api_key)
    
    file = Path(file_path)
    if not file.is_file():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    file_extension = file.suffix.lower()  # 获取文件后缀
    supported_extensions = {'.pdf', '.jpg', '.jpeg', '.png'}
    
    if file_extension not in supported_extensions:
        raise ValueError(f"不支持的文件类型: {file_extension}。支持的类型: {', '.join(supported_extensions)}")
    
    if file_extension == '.pdf':
        response = process_pdf(file_path, client)
        output = save_ocr_results(response, file, 'pdf')
    else:
        response = process_image(file_path, client)
        output = save_ocr_results(response, file, 'image')
    return output



def save_ocr_results(ocr_response: OCRResponse, original_file: Path, file_type: Literal['pdf', 'image']) -> str:
    """
    保存OCR结果
    Args:
        ocr_response: OCR响应结果
        original_file: 原始文件路径
        file_type: 文件类型 ('pdf' 或 'image')
    Returns:
        输出目录路径
    """
    base_dir = 'results_pdf' if file_type == 'pdf' else 'results_image'
    os.makedirs(base_dir, exist_ok=True)
    original_name = original_file.stem
    if file_type == 'pdf':
        output_dir = os.path.join(base_dir, original_name)
        os.makedirs(output_dir, exist_ok=True)
        images_dir = os.path.join(output_dir, "images")
        os.makedirs(images_dir, exist_ok=True)
        
        all_markdowns = []
        for page in ocr_response.pages:
            page_images = {}
            for img in page.images:
                img_data = base64.b64decode(img.image_base64.split(',')[1])
                img_path = os.path.join(images_dir, f"{img.id}.png")
                with open(img_path, 'wb') as f:
                    f.write(img_data)
                page_images[img.id] = f"images/{img.id}.png"
            "".join(all_markdowns.append(page.markdown))
    else:
        all_markdowns = ocr_response.pages[0].markdown
    return all_markdowns


if __name__ == "__main__":
    file_path = "./data/image7.png"
    res = process_file(file_path=file_path, api_key="GcQX1IjolKz9o4VO7ta2VPzOvgWwbWtN")
    print(res)