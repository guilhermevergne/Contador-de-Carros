import yolov5
import cv2
import numpy as np
from collections import defaultdict
from IPython.display import clear_output
from PIL import Image, ImageDraw, ImageFont


def main():
  # Carregar o modelo
  path = '../../Assets/yolov5s.pt'
  path = './Assets/yolov5s.pt'
  model = yolov5.load(path)
  # Abrir o vídeo
  video_path = '../../Assets/video.mp4'  # caminho para o vídeo
  video_path = './Assets/video.mp4'
  cap = cv2.VideoCapture(video_path)

  # Dicionário para rastrear os IDs dos veículos e suas últimas posições
  vehicle_positions = {}

  # Definir a distância mínima para considerar um veículo como novo
  min_distance_new_vehicle = 200 # Tentativa e erro com valores arbitrários

  # Configurações do vídeo
  largura, altura = 640, 480
  fps = 24
  # Define o codec e cria o objeto VideoWriter
  video_saida = cv2.VideoWriter('video_saida.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (largura, altura))


  aux = 0
  overlap_limit = 0.25
  # Loop para processar o vídeo frame por frame
  while True:
    ret, frame = cap.read()  # Lê um frame do vídeo
    if not ret:
      break  # Sai do loop quando não houver mais frames

    # Fazer a inferência no frame
    results = model(frame)

    # Verificar os veículos identificados
    for detection in results.xyxy[0]:
      _, _, _, _, confidence, class_idx = detection.numpy()
      class_idx = int(class_idx)
      class_name = results.names[class_idx]
      if class_name in ['car','truck','bus','motorcycle']:
        # Calcular o centro do retângulo delimitador
        x_center = (detection[0] + detection[2]) / 2
        y_center = (detection[1] + detection[3]) / 2
        center = np.array([x_center, y_center])

        # Verificar se o veículo é novo ou se já foi detectado anteriormente
        new_vehicle = True
        box = detection[0:4].numpy()
        for vehicle_id, last_box in vehicle_positions.items():
          #distance = np.linalg.norm(center - last_position)
          print(f'{box=}\n{last_box=}\n\n')
          if overlap_limit < IoU(box,last_box):
            new_vehicle = False
            # Atualizar a posição do veículo no dicionário
            vehicle_positions[vehicle_id] = box
            break

        # Se o veículo for novo, adicioná-lo ao dicionário de posições
        if new_vehicle:
          vehicle_id = len(vehicle_positions) + 1
          vehicle_positions[vehicle_id] = box

    # Contar o número de veículos distintos
    num_vehicles = len(vehicle_positions)

    # Exibição dos frames
    if aux%5==0:
      print(f'{num_vehicles} veículos distintos atravessaram a rua!')
      #results.show()
    
    # Criação do vídeo frame a frame
    img = cv2.resize(results.render()[0], (largura, altura))
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    font_size = 72
    font_txt = ImageFont.truetype('arial.ttf',font_size)
    pos_txt = (20,40)
    txt=str(num_vehicles)
    cor_txt = (255,255,255)
    cor_bg = (0, 0, 0)
    draw = ImageDraw.Draw(img_pil)

    # Calculo de tamanho do texto
    width_txt = font_size//1.75*len(txt)
    size_txt = (width_txt,font_size)
    padding = 10

    # Posição do retangulo
    rect_pos = (pos_txt[0] - padding, pos_txt[1] - padding, pos_txt[0] + size_txt[0] + padding, pos_txt[1] + size_txt[1] + padding)

    # Desenhar o retangulo
    draw.rectangle(rect_pos, outline=cor_txt, width=2)
    # Desenhar o texto
    draw.text(pos_txt, txt, fill=cor_txt, font=font_txt)

    img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    video_saida.write(img)
    
    aux += 1


  # Liberar recursos
  cap.release()
  cv2.destroyAllWindows()

  return 0

def IoU(box1, box2):
    """
    Calculate the Intersection over Union (IoU) of two bounding boxes.
    """
    x_left = max(box1[0], box2[0])
    y_top = max(box1[1], box2[1])
    x_right = min(box1[2], box2[2])
    y_bottom = min(box1[3], box2[3])

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])

    iou = intersection_area / float(box1_area + box2_area - intersection_area)
    return iou

if __name__ == "__main__":
    SystemExit(main())
