import sys
print("Python path:", sys.executable)

try:
    print("\n1. Testing torch import...")
    import torch
    print("✅ torch imported successfully")
    print(f"   PyTorch version: {torch.__version__}")
    
    print("\n2. Testing model.py import...")
    from model import U2NET
    print("✅ U2NET class imported successfully")
    
    print("\n3. Creating U2NET instance...")
    model = U2NET(3, 1)
    print("✅ U2NET instance created")
    
    print("\n4. Testing model weight loading...")
    import os
    model_path = 'models/u2net_portrait.pth'
    if os.path.exists(model_path):
        print(f"✅ Model file exists: {model_path}")
        size_mb = os.path.getsize(model_path) / (1024*1024)
        print(f"   Size: {size_mb:.1f} MB")
        
        print("\n5. Loading weights...")
        model.load_state_dict(torch.load(model_path, map_location='cpu'))
        print("✅ Weights loaded successfully!")
        
        print("\n6. Setting to eval mode...")
        model.eval()
        print("✅ Model ready for inference!")
        
        print("\n" + "="*50)
        print("ALL CHECKS PASSED - U-2-Net is working!")
        print("="*50)
    else:
        print(f"❌ Model file not found: {model_path}")
        
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
