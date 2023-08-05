from keras.models import load_model
from matplotlib import pyplot
from numpy.random import randn
import os

path_model = 'model'

# 선택한 모델을 다운로드 받거나 로드해서 리턴해 줌
def load_generator(model_name):
    # model 폴더 있는지 확인
    # model 폴더 없으면
    if not os.path.isdir(path_model):
        # model 폴더 만들고
        os.mkdir(path_model)
        # 모델 다운로드
        print("모델 다운로드")
        model = load_model('model/test_model.h5')
    # model 폴더 있으면
    else:
        # 사용자가 원하는 모델 있는지 확인하고
        model_list_extension = os.listdir(path_model)
        model_list = []
        for m in model_list_extension:
            model_list.append(os.path.splitext(m)[0])
        # 있으면
        if model_name in model_list:
            # 모델 가져오기
            print("모델 가져오기")
            n = model_list.index(model_name)
            model = load_model(f'model/{model_list_extension[n]}')
        else:
            # 없으면

            # 모델 다운로드
            print("모델 다운로드")
            model = load_model('model/test_model.h5')
    # 가져왔거나 다운받은 모델 리턴
    return model

# 모델을 돌려서 생성된 얼굴이미지를 원하는 위치에 저장해 줌
def run_generator(generator, pieces, width, height, save_location):
    # 잠재변수 생성 ~ 모델마다 잠재변수 형태 다른 경우 어떻게 해야할지 고민해야함
    latent_points = generate_latent_points(100, pieces)
    # generator로 분산값 생성하기 (pieces)
    X = generator.predict(latent_points)
    X = (X + 1) / 2.0
    # 분산값 이미지로 변환하기
    for index, piece in enumerate(X):
        pyplot.imshow(piece)
        # 이미지 크기 조절하기 (width,height) ~ 어떻게 구현할지 고민 중

        # 이미지 저장하기 (save_location)
        # save_location 폴더 있는지 확인
        # save_location 폴더 없으면
        if not os.path.isdir(save_location):
            # save_location 폴더 만들고
            os.mkdir(save_location)
        # save_location에 이미지 저장 ~ 예외처리 해야하나??
        pyplot.savefig(save_location + str(index)+ '.png')
        # 이미지 리턴하기 ~ 하고 싶은데 어떻게 구현할지 고민 중

def generate_latent_points(latent_dim, n_samples):
    # generate points in the latent space
    x_input = randn(latent_dim * n_samples)
    # reshape into a batch of inputs for the network
    z_input = x_input.reshape(n_samples, latent_dim)
    return z_input

