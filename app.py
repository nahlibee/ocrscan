import cv2
from PIL import Image
import matplotlib.pyplot as plt

def preprocess_image(image_path):
    # Read the image
    image = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to binarize the image
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Remove noise using a median filter
    denoised = cv2.medianBlur(thresh, 3)
    
    # Save the processed image
    processed_image_path = "processed_image.png"
    cv2.imwrite(processed_image_path, denoised)
    
    return processed_image_path

def display_image(image_path):
    # Open the image using PIL
    image = Image.open(image_path)
    
    # Convert image to numpy array for matplotlib
    image_np = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
    
    # Display the image using matplotlib
    plt.imshow(image_np)
    plt.axis('off')  # Hide axes
    plt.show()

# Example usage
image_path = r"C:\Users\yahya\Desktop\ocrscan\output\page_1.png"
processed_image_path = preprocess_image(image_path)

# Display the original and processed images
print("Displaying original image:")
display_image(image_path)
print("Displaying processed image:")
display_image(processed_image_path)