import glob
import os

ns = glob.glob(r'statics/upload/*')
print(ns)
print(os.getcwd())
os.chdir('statics')
print(os.getcwd())
ns = glob.glob(r'upload/*.jpg')
print(ns)
os.chdir('..')
print(os.getcwd())
print(os.path.basename('statics/upload/1.jpg'))
# pip install pillow
# from PIL import image
