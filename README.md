# GEM QC2

## Hole Inspection
  - 파일 안에 path_data와 path_saved에 필요한 파일을 링크해 주세요.
  - path_data는 폴더 안의 M*_B0*_* 폴더 안의 엑셀 파일을 읽어들입니다.
  - 실행: python3 hole_inspection.py
  - result: 각 포일의 섹션 별 mean/std, 전체 포일의 mean/std, 엑셀 파일

## QC2 Long - Part1

* `part1_tcv.py`
  - 시간에 따른 전압과, 전류 2가지 그래프를 가진  플랏을 그리는 코드
  - QC2 Long Part1 실험 후 자동 저장되는 txt 파일을 이용합니다. 
    - (Ex. QC2LONG_PART1_GE21-FOIL-M2-G12-KR-B05-0014_20210712_12-27_test3.txt)
  - data 파일(위에서 언급한 txt 파일)을 path_data 디렉토리로 옮겨주세요.
  - 실행 : python3 part1_tcv.py
  - result : part1 전체 tcv 플롯, 루트파일

* `part1_vc.py`
  - 처음에 전압을 올리는 구간 중에서 전류의 resolution이 좋은 순간들만 추려내서 각 전압에서의 전류 평균을 구하고 전압-전류 플랏을 그리는 코드
  - 돌리면서 600V, 100V에서의 전류 평균들과 그 차이을 print해주는데 이를 엑셀로 정리하고 저장해주시면 됩니다. (참고: Current Difference.xlsx)
  - 혹시 코드가 불안정할 수 있으니 몇가지 경우들에 대해서 직접 평균값을 액셀로 구해보시고 비교해보시면 좋을 것 같습니다. 또는 output png에서 y축 scale이 엄청 큰 경우들이 있는데 이는 spark때문에 생기는 것으로  생각됩니다. 확인해주시면 안전할 것 같습니다.
  - 실행 : python3 part1_vc.py
  - result : part1 전체 vc 플롯, 루트파일

## QC2 Long - Part2

* part2_tcv.py
  - 앞과 비슷하게 시간에 따른 전압과, 전류 2가지 그래프를 가진  플랏을 그리는 코드
  - QC2 Long Part2 실험 후 자동 저장되는 txt 파일을 이용합니다.
    - (Ex. QC2_all_channels_monitor_20210722_16-55_F18F16F05F24_2nd.txt)
  - 반드시 몇 번 foil이 몇 번 channel에 연결되어 있는 지를 알고 있어야 합니다.
  - 파일 실행 시, foil별로 png 파일들과 root 파일들이 여러개 만들어집니다.
  - 실행 : python3 part2_tcv.py -c 2 3 4 5 6 -f 13A 16A 8B 20A 6B
  - 실행 시 HV channel 순서와 foil 순서를 맞춰주셔야 합니다.
  - result : 해당 포일들의 tcv플롯, 루트파일

## For All Code

- 맥북에서 코드가 돌아가는지 테스트했습니다. Homebrew를 이용하여 root, python을 설치하셨다면 잘 돌아갈 것으로 생각됩니다. (brew install  root, python) - Python 3.9.6, ROOT 6.22/08, matplotlib 2.2.4 
- 확실하지는 않으나 일단은 python2로도 돌아가는 것 같은데 수정이 좀 필요한 코드가 있을 수 있습니다.

- 각 스크립트에 대해 다음은 직접 수정해 주셔야 합니다.
- path_data : csv 파일, txt 파일과 같은 data 파일이 저장되어 있는 디렉토리
- path_saved : png 파일, root 파일이 저장될 디렉토리

- 'GE21-FOIL-M#-G3-KR-B03-0000' 와 같은 plot title에서 M#은 M type을 의미합니다. 현재 M type  number로 수정해 주세요.
- 'GE21-FOIL-M2-G##-KR-B03-0000' 와 같은 plot title에서 G##은 Foil 종류를 의미합니다. 현재 포일 종류로 수정해 주세요. e.g. G12 or G3
- 'GE21-FOIL-M2-G3-KR-B05-0000' 와 같은 plot title에서 BXX는 batch number를 의미합니다. 현재 batch number로 수정해 주세요.

QC2 Long 같은 경우에는 같은 foil에 대해서 여러번 실험을 반복하여 결과들이 여러개 있을 수 있습니다. 시간 순서대로 Pre 혹은 1st, 2nd, 3rd 혹은 test1,2,3 식으로 txt 파일 이름에 추가해주시면 코드들이 알아서 output들을 분리하여 저장하도록 하였습니다.

## Update note
* 전원 2021.08.26
  - 파일 저장 위치 typo 수정
  - Part1_VC에서 전류의 resolution이 좋은 순간들에서도 스파크가 튀는 경우가 가끔 있어, 전류가 9nA 이상의 경우들을 배제하고 평균들을 내고, 플랏들을 그리게 수정을 하였습니다.
* 최민욱 2021.09.10
  - 파일 불러오는 방식이 좀 불편해서 원터치로 모든 파일을 프로세스하게 바꿨습니다. 환경에 맞추어 사용하시기 바랍니다.
* 최진 2022.02.23
  - hole_inspection파트에 수작업이 필요 없게 수정하였습니다. OV과정에서 규격에 맞지 않게 데이터를 정리했다면 버그가 있을 수 있습니다.
