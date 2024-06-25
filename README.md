## Project overview 

1. receive low-resolution medical images provided by the user and train them through GAN (using checkpoints) 
2. improve resolution via the GAN's Generator  
3. provide users with improved images 

<img src="./images/Before : After Brain Tumor MRI Enhancement.png" high="600px" width="600px"></img>

MRI of brain tumors improved using GANs 

## 'A Parallelism-Based, Stepwise Approach to GAN for Efficient Stability Training' 

<img src="./images/A Parallelism-Based, Stepwise Approach to GAN for Efficient Stability Training.png" width="400px"></img>

## PSTGAN

	Developing a weight transfer mechanism to utilize previous model weights.

	Implementing a model training loop with hyperparameter adjustments based on the learning rate.


## SRGAN
Implementation of _Photo-Realistic Single Image Super-Resolution Using a Generative Adversarial Network_.

[Code](srgan/srgan.py)

Paper: https://arxiv.org/abs/1609.04802

<p align="center">
    <img src="http://eriklindernoren.se/images/superresgan.png" width="640"\>
</p>


## Example
```
$ cd srgan/
<follow steps at the top of srgan.py>
$ python3 srgan.py
```

<p align="center">
    <img src="http://eriklindernoren.se/images/srgan.png" width="640"\>
</p>

## Use_Start the serve

One command

```bash
$ python manage.py runserver
```

Model will be saved to `./models/{name}` every 1000 iterations, and samples from the model saved to `./results/{name}`. `name` will be `default`, by default.
