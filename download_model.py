import gdown
import os

# Create models directory if it doesn't exist
os.makedirs('models', exist_ok=True)

# Download u2net_portrait.pth from Google Drive
url = 'https://drive.google.com/uc?id=1IG3HdpcRiDoWNookbncQjeaPN28t90yW'
output = 'models/u2net_portrait.pth'

print("Downloading u2net_portrait.pth (~170MB)...")
gdown.download(url, output, quiet=False)
print("Download complete!")
