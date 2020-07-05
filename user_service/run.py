from src.app.app import app
import time

if __name__ == '__main__':
    time.sleep(35)
    app.run(debug=True,host="0.0.0.0", port=5000)
