import sys
sys.path.append('.')

try:
    print("Importing modules...")
    from main import app
    print("Main app imported successfully")
    
    import uvicorn
    print("Starting server with debug logging...")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug", reload=False)
    
except Exception as e:
    print(f"Error starting server: {e}")
    import traceback
    traceback.print_exc()