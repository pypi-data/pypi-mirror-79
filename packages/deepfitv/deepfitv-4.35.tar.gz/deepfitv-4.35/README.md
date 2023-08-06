# DeepFit
DeepFit is an open source package for creating novel methods that help all the stake holders better manage Patient Engagement. It leverages research technology like Data Shapley, Multi-Accuracy and cPCA from Stanford Artificial Intelligence Labs (**SAIL**)

![DeepFit](/Docs/deepfitnew.jpg)

* [Getting Started](#getting-started)
* [Programming Guide](#programming-guide)
* [vLife](www.virtusa.com/vlife)
* [License](license)

### Getting Started
Please Install DeepFit package using 
```
!pip install deepfitv
```

### Programming Guide

**Incision Object Declaration**
```
deepfitv.incision.Incision(<path of image>)
```

1. To identify incision image object detection run the object detection function run 
```
deepfitv.incision.Incision(<path of image>).object_detection()
```

2. To classify the incisin image into less than 30 or post 30 days of surgery run 
```
deepfitv.incision.Incision(<path of image>).classify_image()
```

3. To use SinGAN feature, use a single image and generate random sample images from it refer :
```
deepfitv.SinGAN.help()
```

#### Prerequisites

deepfitv.incision module requires 'imageai' and 'tensorflow' libraries as dependencies
```
!pip install tensorflow
!pip install imageai
```

To run the Incision Object Image use case one would need to download the model h5 files which we have developed and copy in the
directory 
```
Incision/models
```
[https://github.com/Virtusa-vLife/DeepFit/releases/download/deepfit/Image_classification.h5]

[https://github.com/Virtusa-vLife/DeepFit/releases/download/deepfit/detection_model.h5]

[https://github.com/OlafenwaMoses/ImageAI/releases/download/essential-v4/pretrained-yolov3.h5]

 download reference json at 

```
 Incision/json
```
 [https://github.com/Virtusa-vLife/DeepFit/releases/download/deepfit/detection_config.json]


### License
Coming Soon
