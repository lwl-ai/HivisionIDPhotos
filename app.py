import argparse
import os
from demo.processor import IDPhotoProcessor
from demo.ui import create_ui
from hivision.creator.choose_handler import HUMAN_MATTING_MODELS

root_dir = os.path.dirname(os.path.abspath(__file__))

HUMAN_MATTING_MODELS_EXIST = [
    os.path.splitext(file)[0]
    for file in os.listdir(os.path.join(root_dir, "hivision/creator/weights"))
    if file.endswith(".onnx") or file.endswith(".mnn")
]
# 在HUMAN_MATTING_MODELS中的模型才会被加载到Gradio中显示
HUMAN_MATTING_MODELS = [
    model for model in HUMAN_MATTING_MODELS if model in HUMAN_MATTING_MODELS_EXIST
]

FACE_DETECT_MODELS = ["face++ (联网Online API)", "mtcnn"]
FACE_DETECT_MODELS_EXPAND = (
    ["retinaface-resnet50"]
    if os.path.exists(
        os.path.join(
            root_dir, "hivision/creator/retinaface/weights/retinaface-resnet50.onnx"
        )
    )
    else []
)
FACE_DETECT_MODELS += FACE_DETECT_MODELS_EXPAND

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "--port", type=int, default=7860, help="The port number of the server"
    )
    argparser.add_argument(
        "--host", type=str, default="127.0.0.1", help="The host of the server"
    )
    argparser.add_argument(
        "--root_path",
        type=str,
        default=None,
        help="The root path of the server, default is None (='/'), e.g. '/myapp'",
    )
    args = argparser.parse_args()

    processor = IDPhotoProcessor()

    demo = create_ui(
        processor, root_dir, HUMAN_MATTING_MODELS_EXIST, FACE_DETECT_MODELS
    )
    demo.launch(
        server_name=args.host,
        server_port=args.port,
        show_api=False,
        favicon_path=os.path.join(root_dir, "assets/hivision_logo.png"),
        root_path=args.root_path,
    )
