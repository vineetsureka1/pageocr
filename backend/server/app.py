from typing import Optional

from fastapi import FastAPI, File, Form, UploadFile

from .helper import *
from .models import *

app = FastAPI(
	title='PageOCR Backend API',
	description='',
	docs_url='/',
)


@app.post('/pageocr', tags=['Page OCR'], response_model=PageOCRResponse)
async def perform_page_level_ocr(
	image: UploadFile = File(...),
	language: Optional[str] = Form('hindi')
):
	image_path = save_uploaded_image(image)
	print(f'Saved the image at {image_path}')
	regions = call_layout_parser(image_path)
	print(f'{len(regions)} word regions detected by layout-parser')
	path = crop_regions(image_path, regions)
	print(f'Saved the cropped word images at: {path}')
	ocr_output = perform_ocr(path, language)
	return format_ocr_output(ocr_output, regions)


@app.post('/load_ocr', tags=['Helper'])
async def load_ocr_model(
	language: str
):
	"""
	This is the API endpoint to load the given language ocr model to memory
	this endpoint directly calls the "/ocr/v0/load"
	"""
	print(f'Loading the {language} OCR model.')
	load_model(language)
	return {'detail': 'Model loaded'}
