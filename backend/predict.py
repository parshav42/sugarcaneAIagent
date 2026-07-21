# from ultralytics import YOLO
#
# model = YOLO("/home/parshav/finalproject/pythonproject/backend/model/best.pt")
#
# # results1 = model.predict("/home/parshav/finalproject/pythonproject/image051.jpg")
# # print(results1)
#
# def predict(image_path):
#     results = model(image_path)
#
#
#     predictions = []
#
#     for box in results[0].boxes:
#         predictions.append({
#             "disease": model.names[int(box.cls[0])],
#             "confidence": round(float(box.conf[0]) * 100, 2)
#         })
#
#     return predictions
#
# predict("/home/parshav/finalproject/pythonproject/image051.jpg")

from ultralytics import YOLO

model = YOLO("/home/parshav/finalproject/pythonproject/backend/model/best.pt")

def predict(image_path):

    results = model.predict(
        source=image_path,
        conf=0.25,
        verbose=False
    )

    predictions = []

    # for box in results[0].boxes:
    #     predictions.append({
    #         "disease": model.names[int(box.cls[0])],
    #         "confidence": round(float(box.conf[0]) * 100, 2),
    #         "bbox": box.xyxy[0].tolist()
    #     })

    return predictions


# result = predict("/home/parshav/PycharmProjects/sugarcaneAIagent/image051.jpg")
#
# print(result)