import subprocess
import os
import time
from difflib import SequenceMatcher
import matplotlib.pyplot as plt
from PIL import Image

# Ensure the output directory exists
def ensure_output_dir(path):
    os.makedirs(path, exist_ok=True)

# Remove alpha channel if it exists
def remove_alpha_channel(image_path):
    with Image.open(image_path) as img:
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        img.save(image_path)

# Define the OCR tools commands
def run_tesseract(image_path, output_path):
    ensure_output_dir(output_path)
    output_file = os.path.join(output_path, 'output')
    subprocess.run(['tesseract', image_path, output_file, '-l', 'ara'])
    with open(f"{output_file}.txt", 'r', encoding='utf-8') as file:
        return file.read()

def run_ocrmypdf(image_path, output_path, dpi=300):
    ensure_output_dir(output_path)
    pdf_output = os.path.join(output_path, 'output.pdf')
    text_output = os.path.join(output_path, 'output.txt')
    subprocess.run(['ocrmypdf', '--image-dpi', str(dpi), '-l', 'ara', image_path, pdf_output])
    if os.path.exists(pdf_output):
        subprocess.run(['pdftotext', pdf_output, text_output])
        with open(text_output, 'r', encoding='utf-8') as file:
            return file.read()
    else:
        raise FileNotFoundError(f"Output PDF not created: {pdf_output}")


# Helper functions for benchmarking
def levenshtein_distance(s1, s2):
    matcher = SequenceMatcher(None, s1, s2)
    return 1 - matcher.ratio()

def cer(ocr_output, ground_truth):
    return levenshtein_distance(ocr_output, ground_truth)

def wer(ocr_output, ground_truth):
    ocr_words = ocr_output.split()
    gt_words = ground_truth.split()
    return levenshtein_distance(ocr_words, gt_words)

# Benchmark OCR tools
def benchmark_ocr(image_path, ground_truth_path, ocr_function, output_path):
    remove_alpha_channel(image_path)  # Remove alpha channel before processing
    start_time = time.time()
    ocr_output = ocr_function(image_path, output_path)
    duration = time.time() - start_time

    with open(ground_truth_path, 'r', encoding='utf-8') as file:
        ground_truth_text = file.read()

    cer_score = cer(ocr_output, ground_truth_text)
    wer_score = wer(ocr_output, ground_truth_text)

    return {
        'cer': cer_score,
        'wer': wer_score,
        'time': duration
    }

# Run benchmarks and visualize results
def run_benchmarks(images, ground_truths):
    ocr_functions = {
        'Tesseract': run_tesseract,
        'OCRmyPDF': lambda img, out: run_ocrmypdf(img, out, dpi=300)
        
    }

    results = {tool: [] for tool in ocr_functions}

    for image_path, ground_truth_path in zip(images, ground_truths):
        for tool, ocr_function in ocr_functions.items():
            output_path = f"output/{tool}"
            result = benchmark_ocr(image_path, ground_truth_path, ocr_function, output_path)
            results[tool].append(result)

    return results

def visualize_results(results):
    tools = list(results.keys())
    metrics = ['cer', 'wer', 'time']
    
    avg_results = {tool: {metric: sum(result[metric] for result in results[tool]) / len(results[tool]) for metric in metrics} for tool in tools}

    x = range(len(tools))
    fig, ax = plt.subplots(3, 1, figsize=(10, 15))
    
    for i, metric in enumerate(metrics):
        y = [avg_results[tool][metric] for tool in tools]
        ax[i].bar(x, y, tick_label=tools)
        ax[i].set_title(f'Average {metric.upper()}')
        ax[i].set_ylabel(metric.upper())
        ax[i].set_xlabel('OCR Tool')
    
    plt.tight_layout()
    plt.show()




# Example usage
images = [
    'C:/Users/yahya/Desktop/stag2/image.png'
]

ground_truths = [
    'C:/Users/yahya/Desktop/stag2/text_image.txt'
]

results = run_benchmarks(images, ground_truths)
visualize_results(results)
