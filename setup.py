from setuptools import setup, find_packages

setup(
    name="ai-script-compiler",
    version="1.1.0",
    author="Brah-Timo",
    author_email="your.email@example.com",
    description="A high-performance AI-powered script compiler for image-to-video conversion.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Brah-Timo/AI-Script-Lang",
    packages=find_packages(),
    install_requires=[
        "llvmlite>=0.42.0",
        "numpy>=1.26.0",
        "torch>=2.1.0",
        "pytest>=8.0.0",
        "pycuda>=2024.1",
        "pyopencl>=2023.1",
        "numba>=0.59.0",
        "opencv-python>=4.8.0",
        "ffmpeg-python>=0.3.0",
        "onnxruntime>=1.17.0",
        "pytorch-lightning>=2.2.0",
        "scipy>=1.11.0",
        "matplotlib>=3.8.0",
        "tqdm>=4.66.0",
        "requests>=2.31.0",
        "flask>=3.0.0",
        "fastapi>=0.110.0",
        "uvicorn>=0.27.0",
    ],
    entry_points={
        "console_scripts": [
            "ai-script=src.main:main"
        ]
    },
    "console_scripts": [
        "ai-script=src.main:main",
        "ai-debugger=src.debugger:main"  # إضافة المصحح كأداة CLI
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Compilers",
        "Topic :: Multimedia :: Video",
        "Intended Audience :: Developers",
        "Natural Language :: English",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    zip_safe=False,
)
