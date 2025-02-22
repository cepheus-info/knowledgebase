To implement a GAN model using Keras in a functional style, we'll define the generator and discriminator models using the Keras functional API. This approach provides more flexibility than the Sequential model, especially for complex models.

### Step 1: Import Libraries

```python
import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Reshape, Flatten, Input, BatchNormalization, LeakyReLU
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.datasets import mnist
```

### Step 2: Define the Generator Model

```python
def build_generator(latent_dim):
    inputs = Input(shape=(latent_dim,))
    x = Dense(256, activation=LeakyReLU(alpha=0.2))(inputs)
    x = BatchNormalization(momentum=0.8)(x)
    x = Dense(512, activation=LeakyReLU(alpha=0.2))(x)
    x = BatchNormalization(momentum=0.8)(x)
    x = Dense(1024, activation=LeakyReLU(alpha=0.2))(x)
    x = BatchNormalization(momentum=0.8)(x)
    x = Dense(np.prod((28, 28, 1)), activation='tanh')(x)
    x = Reshape((28, 28, 1))(x)
    model = Model(inputs, x)
    return model
```

### Step 3: Define the Discriminator Model

```python
def build_discriminator(img_shape):
    inputs = Input(shape=img_shape)
    x = Flatten()(inputs)
    x = Dense(512, activation=LeakyReLU(alpha=0.2))(x)
    x = Dense(256, activation=LeakyReLU(alpha=0.2))(x)
    x = Dense(1, activation='sigmoid')(x)
    model = Model(inputs, x)
    return model
```

### Step 4: Compile the Discriminator

```python
def compile_discriminator(model):
    model.compile(loss='binary_crossentropy',
                  optimizer=Adam(0.0002, 0.5),
                  metrics=['accuracy'])
    return model
```

### Step 5: Build and Compile the GAN Model

```python
def build_gan(generator, discriminator):
    discriminator.trainable = False
    gan_input = Input(shape=(latent_dim,))
    x = generator(gan_input)
    gan_output = discriminator(x)
    gan = Model(gan_input, gan_output)
    gan.compile(loss='binary_crossentropy', optimizer=Adam(0.0002, 0.5))
    return gan
```

### Step 6: Training Function

```python
def train(gan, generator, discriminator, epochs, batch_size, latent_dim):
    (X_train, _), (_, _) = mnist.load_data()
    X_train = X_train / 127.5 - 1.0
    X_train = np.expand_dims(X_train, axis=-1)
    valid = np.ones((batch_size, 1))
    fake = np.zeros((batch_size, 1))

    for epoch in range(epochs):
        idx = np.random.randint(0, X_train.shape[0], batch_size)
        imgs = X_train[idx]
        noise = np.random.normal(0, 1, (batch_size, latent_dim))
        gen_imgs = generator.predict(noise)
        d_loss_real = discriminator.train_on_batch(imgs, valid)
        d_loss_fake = discriminator.train_on_batch(gen_imgs, fake)
        d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

        noise = np.random.normal(0, 1, (batch_size, latent_dim))
        g_loss = gan.train_on_batch(noise, valid)

        print(f"{epoch} [D loss: {d_loss[0]}] [G loss: {g_loss}]")
```

### Step 7: Initialize and Train the GAN

```python
latent_dim = 100
generator = build_generator(latent_dim)
discriminator = compile_discriminator(build_discriminator((28, 28, 1)))
gan = build_gan(generator, discriminator)

train(gan, generator, discriminator, epochs=30000, batch_size=32, latent_dim=latent_dim)
```
