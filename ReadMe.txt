라이브러리 버젼(서버기준, 애매하면 코랩에서 해보는거 추천)
- numpy 1.22.2
- pandas 1.4.1
- tensorflow 2.8.0
- keras 2.8.0


-----------------------------------------------------------------------------------------


ipynb 설명

parsing.ipynb : 
 - input : pnas_sd01.txt, pnas_sd02.txt 
 - output : ddi_type_description.csv, final_interaction.csv
 - 문장으로 되어있는 DDI를 drug,drug,interaction_num 형태로 바꿔줌
 - 사용하지 않는 ddi를 제거한뒤, 개수가 많은 ddi순으로 번호를 부여

model_training_full.ipynb :
 - input : final_interaction.csv, ssp_pca, psp_pca
 - output : model_parameter.h5
 - final_interaction에 있는 drug pair의 ssp와 pca가 모델 training 과정에서 input으로 사용됨
 - training 진행, training된 모델의 결과를 model_parameter.h5로 출력

drug_prediction_pipeline.ipynb : 
 - input : ddi_type_description.csv, model_parameter.h5
 - output : prediction 결과 프린트
 - drug pair를 drugbank ID로 입력받음. ddi prediction결과를 출력해줌. 
 - .py파일과 sh파일로 따로 pipeline 존재. 이건 코드 분석 필요하면 연습용!


-----------------------------------------------------------------------------------------


DDI prediction 진행 파일

drug_prediction_pipeline.py : '
 - drug_prediction_pipeline.ipynb의 .py버젼
 - work_dir, drug_a, drug_b에 대한 정보를 argv로 받음

running_ddi_predictor.sh :
 - drug_prediction_pipeline.py를 실행하는 bash_script
 - work_dir, drug_a, drug_b에 대한 정보를 script 내에서 입력해주면됨
 - work_dir : pnas_sd01.csv, pnas_sd02.csv, SSP_PCA.txt, PSP_pca.txt가 있는 디렉토리 
 - drug_a, drug_b : 예측하고자 하는 drug의 drugbank ID


-----------------------------------------------------------------------------------------


파일 진행 순서'
 - work_dir에 있어야 하는 프로그램 파일들 : .ipynb, .py, .sh 파일들
 - work_dir에 있어야 하는 데이터 파일들 : pnas_sd01.csv, pnas_sd02.csv, SSP_PCA.txt, PSP_pca.txt
 - training부터 돌리기 (모델에 대한 이해가 필요한 경우, colab이나 jupyter에서 돌려보기) : parsing.ipynb -> model_training_full.ipynb -> running_ddi_predictor.sh
 - ddi 예측 pipeline만 진행시 : running_ddi_predictor.sh


-----------------------------------------------------------------------------------------


Pipeline만 돌려보기

 - 있어야하는 파일들 : pretrained_model.h5, ddi_type_description.csv, SSP_pca.txt, PSP_pca.txt
 - 실행 명령어 : bash running_ddi_predictor.sh
 - 결과물 예시
    Result

    DDI between DB01068 and DB00951 is DDI type 0
    Description of DDI :  The risk or severity of adverse effects can be increased when Drug a is combined with Drug b.
    Confidence Level : 50.93%







